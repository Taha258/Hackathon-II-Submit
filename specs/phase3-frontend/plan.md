# Implementation Plan: Phase 3.2 - AI Chat Interface Integration

**Branch**: `main` | **Date**: 2025-12-27 | **Spec**: [specs/phase3-frontend/spec.md](specs/phase3-frontend/spec.md)
**Input**: Feature specification from `/specs/phase3-frontend/spec.md`

## Summary
Integrate the AI Agent into the Next.js frontend by creating a floating Chat Widget. This widget will allow users to manage their tasks using natural language by communicating with the AI Agent API implemented in Phase 3.1.

## Technical Context

**Language/Version**: TypeScript, Next.js (App Router), React
**Primary Dependencies**: 
- Lucide React (for icons)
- Tailwind CSS (for styling)
- `react-markdown` (optional, for rendering AI responses)
**API Endpoints**:
- AI Agent: `POST http://localhost:8001/chat`
**Authentication**:
- Uses the session token from Better Auth (available via `useSession` hook).

## Constitution Check

- [x] Mimic the style and structure of existing frontend code.
- [x] Use existing `api.ts` or standard fetch for calls.
- [x] Ensure responsive design.

## Project Structure

```text
frontend/src/
├── components/
│   └── ChatWidget.tsx       # New component
├── app/
│   └── dashboard/
│       └── layout.tsx       # Modified to include ChatWidget
```

## Technical Details

### `ChatWidget` Component
- State Management: `isOpen`, `messages` (list of `{ role, content }`), `inputValue`, `isLoading`.
- UI: Floating button in the bottom-right corner. Toggles a chat window.
- Interaction: 
    1. User types a message.
    2. Message is added to local state.
    3. API call is made to `http://localhost:8001/chat` with the Bearer token.
    4. AI response is added to the message list.
    5. Handle loading states and basic errors.

### Auth Integration
- The component will use `useSession` from `@/lib/auth-client` to get the `session.token`.

## Risk Analysis and Mitigation
- **CORS Issues:** Ensure the AI Agent server (port 8001) allows requests from the frontend (port 3000).
- **Session Expiry:** Handle 401 errors from the AI Agent by prompting a re-login if necessary (though the dashboard already handles this).
- **Z-Index Conflicts:** Ensure the floating widget is above other UI elements.
