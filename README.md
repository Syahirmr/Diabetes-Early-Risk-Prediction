# Diabetes Early Risk Prediction Platform

## Current Status
- [x] Phase 0 Complete
- [ ] Phase 1 Dataset
- [ ] Phase 2 ML
- [ ] Phase 3 API
- [ ] Phase 4 UI

## Checklist
- [x] Folder lengkap
- [x] Backend boot
- [x] Swagger muncul
- [x] GET /health berhasil
- [x] Lint pass
- [x] Tidak ada warning

## Architecture Overview
- **Frontend**: Web (Tailwind + Alpine.js)
- **Backend API**: FastAPI
- **ML Layer**: Random Forest + SHAP
- **Artifact Registry**: Memory-resident ML artifacts

## Environment Variables
- `APP_ENV`: Application environment (e.g., development)
- `API_PORT`: Port for backend server
- `MODEL_PATH`: Path to ML artifacts
- `ALLOWED_ORIGINS`: Comma separated allowed CORS origins

## Run Commands
- **Run Server**: `uvicorn backend.main:app --reload`
- **Run Tests**: `pytest`
- **Format Code**: `black . && ruff check --fix .`

## Reference Docs
- [System Spec](docs/system_spec.md)
- [Data Contract](docs/data_contract.md)
- [API Contract](docs/api_contract.md)
- [ML Pipeline](docs/ml_pipeline.md)
- [UI/UX Spec](docs/uiux_spec.md)
- [Architecture](docs/architecture.md)
- [Prompt Rules](docs/prompt_rules.md)
- [Decision Log](docs/decision_log.md)

## Roadmap
- **Phase 0**: Project Bootstrap (Completed)
- **Phase 1**: Dataset & Validation
- **Phase 2**: ML Pipeline
- **Phase 3**: Backend API
- **Phase 4**: Frontend UI
