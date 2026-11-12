from pydantic import BaseModel, Field


class Observation(BaseModel):
    vehicle_count: int = Field(ge=0)
    avg_speed_kmh: float = Field(ge=0)
    queue_length_m: float = Field(ge=0)
    history: list[int] = []


class OptimizeRequest(BaseModel):
    intersection_id: int
    observations: dict[str, Observation]  # kalitlar: N, S, E, W
    emergency_direction: str | None = None
