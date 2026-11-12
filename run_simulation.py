"""Oddiy simulyatsiya: tasodifiy transport holatini koordinatorga beradi.
Keyinchalik SUMO/TraCI bilan almashtiriladi.
Ishga tushirish (loyiha ildizidan): python -m simulation.run_simulation
"""
import random
from ai_agents import coordinator


def random_state():
    obs = {}
    for d in "NSEW":
        c = random.randint(3, 45)
        obs[d] = {"vehicle_count": c, "avg_speed_kmh": random.uniform(0, 40),
                  "queue_length_m": random.uniform(0, 120),
                  "history": [max(0, c - 5), max(0, c - 2), c]}
    return obs


if __name__ == "__main__":
    for step in range(1, 6):
        r = coordinator.run(random_state())
        print(f"[{step}] reja: {r['signal_plan']['phases']} | hodisalar: {len(r['incidents'])}")
