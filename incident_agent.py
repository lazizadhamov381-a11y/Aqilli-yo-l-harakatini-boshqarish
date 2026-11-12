"""Incident Agent: tezlik va navbat bo'yicha anomaliyalarni aniqlaydi."""


def detect(observations: dict) -> list[dict]:
    incidents = []
    for direction, o in observations.items():
        speed, queue, count = o["avg_speed_kmh"], o["queue_length_m"], o["vehicle_count"]
        if count > 0 and speed < 2:
            incidents.append({"direction": direction, "type": "blockage", "severity": 4,
                              "description": f"{direction}: harakat deyarli to'xtagan ({speed} km/s)"})
        elif speed < 8 and queue > 80:
            incidents.append({"direction": direction, "type": "congestion", "severity": 3,
                              "description": f"{direction}: tirbandlik (navbat {queue} m)"})
    return incidents
