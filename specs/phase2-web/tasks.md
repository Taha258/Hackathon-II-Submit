# Tasks: Phase 2 Full-Stack Todo Web App

**Input**: Design documents from `specs/phase2-web/`
**Prerequisites**: `plan.md`, `spec.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [ ] T001 Initialize backend directory with FastAPI and SQLModel dependencies
- [ ] T002 Initialize frontend directory with Next.js 15, Tailwind CSS, and Better Auth
- [ ] T003 Configure environment variables (.env) for both frontend and backend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for data and communication

- [ ] T004 Setup Neon PostgreSQL database and Alembic for migrations in `backend/`
- [ ] T005 [P] Create `User` and `Task` SQLModel classes in `backend/models/`
- [ ] T006 [P] Implement base API routing structure in `backend/api/`
- [ ] T007 Implement database connection and session management in `backend/api/deps.py`
- [ ] T008 Setup JWT verification middleware/dependency in `backend/api/deps.py`

**Checkpoint**: Foundation ready - backend can connect to DB and has basic structure.

---

## Phase 3: User Story 1 - Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register and login using Better Auth.

- [ ] T009 [P] Configure Better Auth on the frontend in `frontend/lib/auth.ts`
- [ ] T010 Create Sign-up and Login pages in `frontend/app/(auth)/`
- [ ] T011 Implement User session retrieval in `frontend/components/Navbar.tsx`
- [ ] T012 Verify that frontend can communicate with backend using Auth tokens

---

## Phase 4: User Story 2 - Todo CRUD with Isolation (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can manage their own tasks.

- [ ] T013 [P] Implement Task CRUD services in `backend/services/task_service.py`
- [ ] T014 [US2] Implement `GET /api/v1/tasks` (List tasks for current user) in `backend/api/endpoints/tasks.py`
- [ ] T015 [US2] Implement `POST /api/v1/tasks` (Create task for current user) in `backend/api/endpoints/tasks.py`
- [ ] T016 [US2] Implement `PUT /api/v1/tasks/{id}` and `DELETE /api/v1/tasks/{id}` with ownership checks
- [ ] T017 [US2] Implement `PATCH /api/v1/tasks/{id}/toggle` for completion status
- [ ] T018 [US2] Create Todo Dashboard UI in `frontend/app/dashboard/page.tsx`
- [ ] T019 [US2] Create Task form and Task list components in `frontend/components/todo/`
- [ ] T020 [US2] Integrate Frontend with Backend CRUD endpoints using session tokens

---

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T021 Add loading states and error toast notifications on the frontend
- [ ] T022 Implement search/filter functionality for tasks on the frontend
- [ ] T023 Finalize README and documentation for Phase 2 setup
- [ ] T024 Run end-to-end verification of the full-stack flow

---

## Dependencies & Execution Order

1. **Phase 1 & 2** are critical and must be done first to provide the skeleton.
2. **Phase 3 (Auth)** must be functional before **Phase 4 (Tasks)** because task creation requires a `user_id`.
3. **Phase 4** can be split between backend (API) and frontend (UI) but backend must provide endpoints first.
