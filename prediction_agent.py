"""Prediction Agent: oddiy tendensiyaga asoslangan qisqa muddatli bashorat.
Keyinchalik LSTM/Vertex AI modeli bilan almashtiriladi."""


def predict(observations: dict) -> dict:
    result = {}
    for direction, o in observations.items():
        history = o.get("history") or [o["vehicle_count"]]
        recent = history[-3:]
        mean_recent = sum(recent) / len(recent)
        trend = history[-1] - history[0] if len(history) > 1 else 0
        predicted = max(0, round(mean_recent + 0.5 * trend / max(1, len(history) - 1)))
        result[direction] = {"predicted_count": predicted,
                             "trend": "up" if trend > 0 else "down" if trend < 0 else "flat"}
    return result
