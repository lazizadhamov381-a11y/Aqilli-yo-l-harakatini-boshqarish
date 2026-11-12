"""Monitoring Agent: har bir yo'nalish uchun zichlik darajasini aniqlaydi."""


def analyze(observations: dict) -> dict:
    report = {}
    for direction, o in observations.items():
        load = o["vehicle_count"] + o["queue_length_m"] / 7.0  # ~7 m/avto
        if load < 15:
            level = "low"
        elif load < 40:
            level = "medium"
        else:
            level = "high"
        report[direction] = {"load": round(load, 1), "level": level}
    return report
