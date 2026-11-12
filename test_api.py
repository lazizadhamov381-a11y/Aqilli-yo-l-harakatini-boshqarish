from fastapi.testclient import TestClient
from backend.app.main import app


def test_health_and_optimize():
    with TestClient(app) as c:
        assert c.get("/health").json() == {"status": "ok"}
        inter = c.get("/api/intersections").json()
        assert len(inter) >= 1
        body = {"intersection_id": inter[0]["id"],
                "observations": {d: {"vehicle_count": 10, "avg_speed_kmh": 25,
                                     "queue_length_m": 20} for d in "NSEW"}}
        r = c.post("/api/optimize", json=body)
        assert r.status_code == 200
        assert r.json()["signal_plan"]["valid"]
        assert len(c.get("/api/decisions").json()) >= 1
