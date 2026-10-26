from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from apps.hearings.models import Hearing

from .models import Notification, Reminder


def _hearings_for(kind):
    today = timezone.localdate()  # Asia/Kolkata
    day = today + timedelta(days=1) if kind == Reminder.DAY_BEFORE else today
    return (
        Hearing.objects.filter(status=Hearing.SCHEDULED, hearing_datetime__date=day)
        .exclude(case__status="closed")  # no reminders for closed cases
        .select_related("case", "case__created_by")
    )


def _enqueue(kind):
    count = 0
    for h in _hearings_for(kind):
        key = f"hearing-{h.id}-{kind}-{h.hearing_datetime.isoformat()}"
        reminder, created = Reminder.objects.get_or_create(
            idempotency_key=key,
            defaults={"hearing": h, "reminder_type": kind, "scheduled_for": timezone.now()},
        )
        if created:  # duplicate runs of the beat job do nothing
            deliver_reminder.delay(reminder.id)
            count += 1
    return count


@shared_task
def enqueue_day_before_reminders():
    return _enqueue(Reminder.DAY_BEFORE)


@shared_task
def enqueue_hearing_day_reminders():
    return _enqueue(Reminder.HEARING_DAY)


@shared_task(bind=True, max_retries=3, default_retry_delay=120)
def deliver_reminder(self, reminder_id):
    r = Reminder.objects.select_related("hearing", "hearing__case", "hearing__case__created_by").get(pk=reminder_id)
    h = r.hearing
    # re-check: hearing may have been rescheduled/cancelled or the case closed since queuing
    if r.status == Reminder.SUPPRESSED or h.status != Hearing.SCHEDULED or h.case.status == "closed":
        r.status = Reminder.SUPPRESSED
        r.save(update_fields=["status"])
        return "suppressed"
    if r.status == Reminder.SENT:
        return "already sent"

    user = h.case.created_by
    when = timezone.localtime(h.hearing_datetime).strftime("%d %b %Y %H:%M")
    title = f"Hearing reminder: {h.case.case_number}"
    message = f"{h.case.title} has a hearing on {when}."

    Notification.objects.get_or_create(
        reminder=r, defaults={"user": user, "hearing": h, "title": title, "message": message}
    )
    try:
        r.attempts += 1
        if user.email:
            send_mail(title, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        r.status = Reminder.SENT
        r.last_error = ""
        r.save()
    except Exception as exc:  # transient email failure -> retry
        r.status = Reminder.FAILED
        r.last_error = str(exc)[:1000]
        r.save()
        raise self.retry(exc=exc)
