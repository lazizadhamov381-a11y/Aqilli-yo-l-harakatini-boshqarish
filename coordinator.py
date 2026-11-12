"""Coordinator: agentlarni ketma-ket ishga tushiradi va yakuniy qarorni qaytaradi.

Hozirgi versiya qoidalarga asoslangan (API kalit shart emas).
Google ADK / Gemini bilan LLM-agentlarga o'tish uchun docs/ADK_NOTES.md ga qarang.
"""
import time
from ai_agents import monitoring_agent, incident_agent, prediction_agent
from ai_agents import signal_optimization_agent, emergency_agent


def run(observations: dict, emergency_direction: str | None = None) -> dict:
    t0 = time.perf_counter()
    density = monitoring_agent.analyze(observations)
    incidents = incident_agent.detect(observations)
    prediction = prediction_agent.predict(observations)

    if emergency_direction:
        plan = emergency_agent.priority_plan(emergency_direction)
    else:
        plan = signal_optimization_agent.optimize(density, prediction)

    return {
        "density": density,
        "incidents": incidents,
        "prediction": prediction,
        "signal_plan": plan,
        "latency_ms": round((time.perf_counter() - t0) * 1000, 2),
    }
