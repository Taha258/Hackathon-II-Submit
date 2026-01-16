---
id: 9
title: Fix CORS trailing slash issue in dashboard
stage: green
date: 2025-12-24
surface: agent
model: gemini-2.0-flash
feature: phase2-web
branch: main
user: PMLS
command: none
labels: ["cors", "frontend", "fix"]
links:
  spec: specs/phase2-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/dashboard/page.tsx
tests:
 - None
---

## Prompt

Please fix the CORS trailing slash issue in frontend/src/app/dashboard/page.tsx.

1. Locate the fetchTasks function: Change api.get('/tasks/', ...) to api.get('/tasks', ...).

2. Locate the addTask function: Change api.post('/tasks/', ...) to api.post('/tasks', ...).

Important: Do NOT remove the slash from routes that allow IDs (like /tasks/${id}). Only remove the trailing slash from the base collection endpoints.

## Response snapshot

I will update the `fetchTasks` and `addTask` functions in `frontend/src/app/dashboard/page.tsx` to remove the trailing slashes from the `/tasks/` endpoint.

## Outcome

- ✅ Impact: Fixed CORS issues caused by trailing slashes on task collection endpoints.
- 🧪 Tests: Manual verification recommended.
- 📁 Files: Modified frontend/src/app/dashboard/page.tsx
- 🔁 Next prompts: None
- 🧠 Reflection: Trailing slashes can sometimes trigger redirects in FastAPI or other backends, which can lead to CORS issues if not handled consistently between frontend and backend.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
