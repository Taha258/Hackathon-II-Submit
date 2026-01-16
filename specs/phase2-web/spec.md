# Specification: Full-Stack Todo Web App (Phase II)

## 1. Overview
Transform the console application into a modern multi-user web application with persistent storage and authentication.

## 2. Architecture (Monorepo)
* **Frontend:** Next.js 16+ (App Router), Tailwind CSS.
* **Backend:** Python FastAPI.
* **Database:** Neon Serverless PostgreSQL (via SQLModel).
* **Auth:** Better Auth (with JWT).

## 3. User Stories
* **All Phase 1 Features:** Add, View, Update, Delete, Mark Complete.
* **Persistence:** Tasks must be saved in the database (not lost on restart).
* **User Isolation:** Users should only see their own tasks.

## 4. API Endpoints
* `GET /api/{user_id}/tasks` - List all tasks.
* `POST /api/{user_id}/tasks` - Create a new task.
* `GET /api/{user_id}/tasks/{id}` - Get task details.
* `PUT /api/{user_id}/tasks/{id}` - Update a task.
* `DELETE /api/{user_id}/tasks/{id}` - Delete a task.
* `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion.

## 5. Technical Constraints
* Use **SQLModel** for ORM.
* Use **JWT Tokens** for securing API between Frontend and Backend.
* Backend must verify JWT token on every request.