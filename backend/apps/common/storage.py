from pathlib import Path

from django.conf import settings


def private_path(relative_key: str) -> Path:
    # Resolve a storage key inside PRIVATE_STORAGE_ROOT (blocks path traversal).
    root = Path(settings.PRIVATE_STORAGE_ROOT).resolve()
    target = (root / relative_key).resolve()
    if root != target and root not in target.parents:
        raise ValueError("Invalid storage key")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target
