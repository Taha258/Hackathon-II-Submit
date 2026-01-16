---
id: 5
title: Execute Phase 4 Todo CRUD Tasks
stage: green
date: 2025-12-21
surface: agent
model: gemini-2.0-flash-thinking-exp
feature: phase2-web
branch: none
user: PMLS
command: none
labels: ["crud", "fastapi", "pydantic", "isolation"]
links:
  spec: specs/phase2-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/schemas.py
 - backend/api/routes/tasks.py
 - backend/api/main.py
 - backend/main.py
tests:
 - POST /api/v1/tasks
 - GET /api/v1/tasks
 - PUT /api/v1/tasks/{id}
 - DELETE /api/v1/tasks/{id}
---

## Prompt

Great work on Auth. Please proceed to Phase 4: Todo CRUD with User Isolation.

Schemas: Create backend/schemas.py using Pydantic to define Request and Response models (e.g., TaskCreate, TaskRead, TaskUpdate).

API Router: Create backend/api/routes/tasks.py and implement standard CRUD endpoints:

POST /tasks: Create a new task (automatically link user_id from current_user).

GET /tasks: Return a list of tasks belonging only to the current user.

GET /tasks/{id}: Return a single task (Verify ownership!).

PUT /tasks/{id}: Update a task (Verify ownership!).

DELETE /tasks/{id}: Delete a task (Verify ownership!).

Integration: Register this new router in backend/main.py with the prefix /api/v1.

Security: Ensure ALL these endpoints use the get_current_user dependency we created in Phase 3.

## Response snapshot

I have completed Phase 4: Todo CRUD with User Isolation:
1.  **Schemas**: Created `backend/schemas.py` with Pydantic models for Task and User.
2.  **CRUD Implementation**: Created `backend/api/routes/tasks.py` with full CRUD logic, including ownership verification (403 Forbidden if accessing other users' tasks).
3.  **Router Integration**: Aggregated routes in `backend/api/main.py` and included them in `backend/main.py` under `/api/v1`.
4.  **Security**: All tasks endpoints are protected by `get_current_user`.

## Outcome

- ✅ Impact: The core business logic of the Todo app is now fully functional with multi-user support.
- 🧪 Tests: CRUD endpoints implemented with ownership checks.
- 📁 Files: Created `schemas.py`, `tasks.py`, `api/main.py` and updated `main.py`.
- 🔁 Next prompts: Phase 5: Polish & Frontend integration.
- 🧠 Reflection: Ownership checks at the router level prevent unauthorized data access effectively.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A.
- Prompt variant (if applicable): None.
- Next experiment (smallest change to try): None.
