"""Emergency Priority Agent: favqulodda transport yo'nalishiga yashil yo'lak ochadi."""


def priority_plan(direction: str, green_seconds: int = 60) -> dict:
    phase_no = 1 if direction in ("N", "S") else 2
    other = 2 if phase_no == 1 else 1
    phases = [{"phase_no": phase_no, "green_seconds": green_seconds},
              {"phase_no": other, "green_seconds": 10}]
    return {"mode": "emergency", "phases": sorted(phases, key=lambda p: p["phase_no"]),
            "valid": True, "reason": f"Favqulodda transport {direction} yo'nalishida: ustuvor yashil"}
