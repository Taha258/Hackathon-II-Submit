---
id: 7
title: Update Security to Database Session Lookup
stage: green
date: 2025-12-21
surface: agent
model: gemini-2.0-flash-thinking-exp
feature: phase2-web
branch: none
user: PMLS
command: none
labels: ["security", "better-auth", "database-session"]
links:
  spec: specs/phase2-web/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/core/security.py
tests:
 - /test-auth endpoint (implicit verification)
---

## Prompt

We need to align the backend security with Better Auth's database session approach.

Please update backend/core/security.py. Replace the JWT decoding logic in get_current_user with a Database Lookup:

1. Input: Take the Bearer token from the header.

2. Query: Look up this token in the Session table.

3. Validation:

Check if the session exists.

Check if session.expiresAt is in the future.

4. User: If valid, fetch the associated User from the database and return it.

5. Error: If invalid or expired, raise 401 Unauthorized.

Imports needed: datetime, Session model, User model, select from sqlmodel.

## Response snapshot

I have updated `backend/core/security.py` to use database-backed session validation:
1.  **Lookup**: Queries the `Session` table for the provided Bearer token.
2.  **Expiration Check**: Verifies that the session's `expiresAt` field is in the future.
3.  **User Association**: Retrieves the associated `User` record using `userId` from the session.
4.  **Security**: Raises 401 Unauthorized for missing, invalid, or expired sessions.

## Outcome

- ✅ Impact: Backend authentication is now synchronized with Better Auth's database session management.
- 🧪 Tests: Refactored `get_current_user` dependency.
- 📁 Files: Modified `backend/core/security.py`.
- 🔁 Next prompts: Finalize frontend integration with Better Auth.
- 🧠 Reflection: Moving to database sessions provides more control over session revocation and expiration compared to stateless JWTs.

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): N/A.
- Prompt variant (if applicable): None.
- Next experiment (smallest change to try): None.
