# 🚦 Aqlli yo'l harakatini boshqarish tizimi (Multi-Agent Traffic Management System)

Ko'p agentli (multi-agent) tizim: chorrahalardagi transport ma'lumotlarini tahlil qiladi,
hodisalarni aniqlaydi, yukni bashorat qiladi va svetofor fazalarini dinamik hisoblaydi.

## Tuzilma
| Papka | Vazifasi |
|---|---|
| `ai_agents/` | Agentlar va koordinator |
| `backend/` | FastAPI server (REST API + dashboard'ni xizmat qiladi) |
| `frontend/` | Oddiy dashboard (`index.html`) |
| `database/` | To'liq PostgreSQL sxemasi |
| `simulation/` | Test simulyatsiyasi |
| `tests/` | Avtomatik testlar |
| `docs/` | UML diagrammalar |

## Ishga tushirish (lokal)
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q                        # testlar
uvicorn backend.app.main:app --reload
```
Brauzerda: http://localhost:8000 (dashboard), http://localhost:8000/docs (API hujjati).

## Simulyatsiya
```bash
python -m simulation.run_simulation
```

## Docker (PostgreSQL bilan)
```bash
docker compose up --build
```
Dashboard: http://localhost:8080

## Yo'l xaritasi
- [x] Qoidalarga asoslangan agentlar, API, dashboard, testlar
- [ ] Google ADK / Gemini bilan LLM-agentlar
- [ ] LSTM bashorat modeli
- [ ] SUMO simulyatsiyasi
- [ ] Autentifikatsiya (JWT) va rollar
- [ ] GCP (Cloud Run + Cloud SQL) ga joylash
