"""Signal Optimization Agent: ikki fazali (NS / EW) chorraha uchun yashil vaqt hisoblaydi."""
from ai_agents.tools.safety_rules import MIN_GREEN, MAX_GREEN, validate_phase_plan

TOTAL_GREEN = 100  # sikl ichidagi jami yashil vaqt (soniya)
PHASES = {1: ("N", "S"), 2: ("E", "W")}


def optimize(density: dict, prediction: dict) -> dict:
    demand = {}
    for phase_no, dirs in PHASES.items():
        d = 0.0
        for x in dirs:
            if x in density:
                d += density[x]["load"] + prediction.get(x, {}).get("predicted_count", 0) * 0.5
        demand[phase_no] = d
    total = sum(demand.values()) or 1.0
    g1 = round(TOTAL_GREEN * demand[1] / total)
    g1 = max(MIN_GREEN, min(MAX_GREEN, g1))
    g2 = max(MIN_GREEN, min(MAX_GREEN, TOTAL_GREEN - g1))
    phases = [{"phase_no": 1, "green_seconds": g1}, {"phase_no": 2, "green_seconds": g2}]
    check = validate_phase_plan(phases)
    return {"mode": "adaptive", "phases": phases, "valid": check["valid"],
            "reason": f"Talab nisbati NS:EW = {demand[1]:.1f}:{demand[2]:.1f}"}
