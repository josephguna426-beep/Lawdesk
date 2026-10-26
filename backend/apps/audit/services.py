import logging

from .models import AuditLog

logger = logging.getLogger(__name__)

SENSITIVE_KEYS = {"password", "token", "secret", "authorization"}


def _clean(changes):
    # never store credentials/tokens in audit records
    if not isinstance(changes, dict):
        return {}
    return {k: ("***" if k.lower() in SENSITIVE_KEYS else str(v)) for k, v in changes.items()}


def log_event(user, action, entity_type, entity_id, changes=None, request=None):
    try:
        ip = None
        if request is not None:
            ip = request.META.get("REMOTE_ADDR")
        AuditLog.objects.create(
            user=user if getattr(user, "is_authenticated", False) else None,
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id),
            changes=_clean(changes or {}),
            ip_address=ip,
        )
    except Exception:  # auditing must never break the main action
        logger.exception("Failed to write audit log")
