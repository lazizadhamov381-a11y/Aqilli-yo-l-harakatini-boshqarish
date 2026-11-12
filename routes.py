from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ai_agents import coordinator
from backend.app.db import get_db
from backend.app.models import Intersection, Incident, AgentDecision
from backend.app.schemas import OptimizeRequest

router = APIRouter(prefix="/api")


@router.get("/intersections")
def intersections(db: Session = Depends(get_db)):
    rows = db.scalars(select(Intersection)).all()
    return [{"id": r.id, "name": r.name, "lat": r.latitude, "lon": r.longitude} for r in rows]


@router.post("/optimize")
def optimize(req: OptimizeRequest, db: Session = Depends(get_db)):
    if db.get(Intersection, req.intersection_id) is None:
        raise HTTPException(404, "Chorraha topilmadi")
    obs = {k: v.model_dump() for k, v in req.observations.items()}
    result = coordinator.run(obs, req.emergency_direction)

    for inc in result["incidents"]:
        db.add(Incident(intersection_id=req.intersection_id, incident_type=inc["type"],
                        severity=inc["severity"], description=inc["description"]))
    db.add(AgentDecision(intersection_id=req.intersection_id, input_json=obs,
                         decision_json=result, latency_ms=result["latency_ms"]))
    db.commit()
    return result


@router.get("/decisions")
def decisions(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.scalars(select(AgentDecision).order_by(AgentDecision.id.desc()).limit(limit)).all()
    return [{"id": r.id, "intersection_id": r.intersection_id, "decision": r.decision_json,
             "created_at": r.created_at.isoformat()} for r in rows]


@router.get("/incidents")
def incidents(limit: int = 20, db: Session = Depends(get_db)):
    rows = db.scalars(select(Incident).order_by(Incident.id.desc()).limit(limit)).all()
    return [{"id": r.id, "intersection_id": r.intersection_id, "type": r.incident_type,
             "severity": r.severity, "description": r.description,
             "detected_at": r.detected_at.isoformat()} for r in rows]
