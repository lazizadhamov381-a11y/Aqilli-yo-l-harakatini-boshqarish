"""Svetofor rejalari uchun xavfsizlik qoidalari."""
MIN_GREEN = 10
MAX_GREEN = 90


def validate_phase_plan(phases: list[dict]) -> dict:
    """Faza rejasi ruxsat etilgan chegaralarda ekanini tekshiradi."""
    errors = []
    for p in phases:
        g = p.get("green_seconds", 0)
        if not (MIN_GREEN <= g <= MAX_GREEN):
            errors.append(
                f"Faza {p.get('phase_no')}: yashil vaqt {g}s "
                f"[{MIN_GREEN}-{MAX_GREEN}] oralig'idan tashqarida"
            )
    return {"valid": not errors, "errors": errors}
