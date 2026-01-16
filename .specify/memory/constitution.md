# Project Constitution (Phase II)

## 1. Architecture Principles
* **Spec-Driven First:** No code is written without a corresponding Task ID and Specification.
* **Monorepo Structure:**
    - `/frontend`: Next.js 16+ (App Router).
    - `/backend`: Python FastAPI service.
* **Separation of Concerns:** Frontend handles UI/Auth logic, Backend handles Business Logic/Data.

## 2. Technology Stack Constraints
* **Frontend:** Next.js, Tailwind CSS, Better Auth.
* **Backend:** Python 3.13+, FastAPI, SQLModel.
* **Database:** Neon Serverless PostgreSQL.
* **Auth:** JWT for secure API communication.

## 3. coding Standards
* **Python:** Follow PEP 8. Use Pydantic models for data validation.
* **TypeScript:** Use strict typing. No `any`.
* **API:** RESTful endpoints with proper HTTP status codes.