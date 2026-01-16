# Implementation Plan: Phase 2 Full-Stack Todo Web App

**Branch**: `phase2-web-setup` | **Date**: 2025-12-21 | **Spec**: [specs/phase2-web/spec.md](specs/phase2-web/spec.md)
**Input**: Feature specification from `specs/phase2-web/spec.md`

## Summary
Transition the Todo application from a Phase 1 console-based in-memory system to a Phase 2 full-stack web application. The architecture uses a monorepo approach with a FastAPI backend and a Next.js frontend. Persistence is handled by a Neon Serverless PostgreSQL database using SQLModel, and authentication is implemented using Better Auth with JWT-based communication between the frontend and backend.

## Technical Context

**Language/Version**: Python 3.13 (Backend), TypeScript/Next.js 15+ (Frontend)
**Primary Dependencies**: FastAPI, SQLModel, SQLAlchemy, Alembic, Next.js, Better Auth, Tailwind CSS, Shadcn UI.
**Storage**: Neon Serverless PostgreSQL.
**Testing**: pytest (Backend), Jest/Cypress (Frontend).
**Target Platform**: Web (Vercel/Neon/Render).
**Project Type**: Web Application (Monorepo).
**Performance Goals**: <200ms API response time (p95).
**Constraints**: User isolation (users only see their own tasks), secure JWT communication.
**Scale/Scope**: Prototype for hackathon, scalable to multi-user.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Spec-Driven First: Task IDs and Specifications followed.
- [x] Monorepo Structure: `/frontend` and `/backend` used.
- [x] Separation of Concerns: Frontend handles UI/Auth, Backend handles Logic/Data.
- [x] Technology Stack: FastAPI, SQLModel, Next.js, Better Auth, Neon.

## Project Structure

### Documentation (this feature)

```text
specs/phase2-web/
├── plan.md              # This file
├── spec.md              # Requirements
└── tasks.md             # Tasks (to be generated)
```

### Source Code (repository root)

```text
backend/
├── main.py              # Entry point
├── api/                 # API Routes
│   ├── deps.py          # Dependencies (Auth, DB)
│   └── endpoints/       # Route handlers
├── core/                # Configuration and Security
├── models/              # SQLModel definitions
├── services/            # Business logic
└── tests/               # Backend tests

frontend/
├── app/                 # Next.js App Router
├── components/          # React components
├── lib/                 # Shared utilities (Auth client, API fetcher)
└── tests/               # Frontend tests
```

**Structure Decision**: Monorepo with distinct `backend/` and `frontend/` directories as per Constitution Phase II.

## Database Schema (SQLModel)

### User Model
- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `full_name`: String (Optional)
- `tasks`: Relationship to `Task` (one-to-many)

### Task Model
- `id`: Integer (Primary Key, Autoincrement)
- `title`: String (Required)
- `description`: String (Optional)
- `completed`: Boolean (Default: False)
- `user_id`: UUID (Foreign Key to `User.id`)
- `user`: Relationship to `User` (many-to-one)

## API Design

### Base URL: `/api/v1`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/tasks` | List all tasks for current user | Yes |
| POST | `/tasks` | Create a new task | Yes |
| GET | `/tasks/{id}` | Get task details | Yes |
| PUT | `/tasks/{id}` | Update task | Yes |
| DELETE | `/tasks/{id}` | Delete task | Yes |
| PATCH | `/tasks/{id}/toggle` | Toggle completion | Yes |

## Auth Strategy: Better Auth + JWT

1. **Frontend**: Next.js uses `better-auth` for user management (OAuth, Email/Password).
2. **Session to JWT**: Upon successful login, the frontend retrieves a session token. For backend calls, it will provide a JWT. 
   - *Alternative*: If `better-auth` handles sessions via cookies, the backend will verify the session cookie or a Bearer token.
3. **Backend Middleware**: A dependency in FastAPI will:
   - Extract the token from the `Authorization` header.
   - Verify the token (via Better Auth's verification mechanism or a shared secret if JWT).
   - Inject the `current_user` into the route handler.

## Phase 2 Implementation Steps

1. **Backend Initialization**:
   - Set up FastAPI with SQLModel and Alembic.
   - Define Models and create initial migration.
   - Implement CRUD services.
2. **Authentication Integration**:
   - Configure Better Auth on Frontend.
   - Implement Auth middleware/dependency on Backend.
3. **Frontend Implementation**:
   - Scaffold Next.js app.
   - Create Auth pages (Login/Register).
   - Create Todo dashboard with CRUD functionality.
4. **Integration & Deployment**:
   - Connect Frontend to Backend API.
   - Deploy to Vercel (Frontend) and Render/Fly (Backend).
