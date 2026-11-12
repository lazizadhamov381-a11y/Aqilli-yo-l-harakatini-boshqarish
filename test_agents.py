from ai_agents import coordinator
from ai_agents.tools.safety_rules import validate_phase_plan

BUSY_NS = {
    "N": {"vehicle_count": 40, "avg_speed_kmh": 20, "queue_length_m": 60, "history": [30, 35, 40]},
    "S": {"vehicle_count": 38, "avg_speed_kmh": 20, "queue_length_m": 55, "history": [30, 34, 38]},
    "E": {"vehicle_count": 5, "avg_speed_kmh": 30, "queue_length_m": 5, "history": [5, 5, 5]},
    "W": {"vehicle_count": 4, "avg_speed_kmh": 30, "queue_length_m": 5, "history": [4, 4, 4]},
}


def test_busy_direction_gets_more_green():
    plan = coordinator.run(BUSY_NS)["signal_plan"]
    g = {p["phase_no"]: p["green_seconds"] for p in plan["phases"]}
    assert g[1] > g[2]
    assert plan["valid"]


def test_emergency_override():
    plan = coordinator.run(BUSY_NS, emergency_direction="E")["signal_plan"]
    assert plan["mode"] == "emergency"
    assert plan["phases"][1]["green_seconds"] == 60


def test_blockage_detected():
    obs = {d: dict(v) for d, v in BUSY_NS.items()}
    obs["N"]["avg_speed_kmh"] = 0
    types = [i["type"] for i in coordinator.run(obs)["incidents"]]
    assert "blockage" in types


def test_safety_rules_reject_bad_plan():
    assert not validate_phase_plan([{"phase_no": 1, "green_seconds": 3}])["valid"]
