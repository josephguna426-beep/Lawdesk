from .models import Reminder


def suppress_pending_reminders(hearing):
    # called on reschedule/cancel so obsolete reminders never fire
    hearing.reminders.filter(status__in=[Reminder.PENDING, Reminder.FAILED]).update(status=Reminder.SUPPRESSED)
