<!-- specs\phase3-frontend\spec.md -->
# Phase 3.2: AI Chat Interface Integration

## 1. Overview
We have successfully built the AI Agent backend in Phase 3.1. Now, in **Phase 3.2**, we will integrate this agent into our existing Next.js frontend. We will create a "Chat Widget" that allows users to talk to the AI Agent directly from their dashboard.

## 2. Goals
* **Integration:** Add a floating chat interface to the existing Dashboard.
* **Connectivity:** Connect the Frontend to the AI Agent API (`http://localhost:8001/chat`).
* **Auth:** Pass the authenticated user's session token to the Agent.
* **UX:** Provide real-time feedback (loading states, markdown rendering).

## 3. Tech Stack
* **Frontend:** Next.js (App Router), React.
* **Styling:** Tailwind CSS (Existing).
* **State:** React `useState` / `useEffect`.
* **Icons:** Lucide React.
* **API Client:** Standard `fetch` or `axios`.

## 4. Functional Requirements

### 4.1. Chat Widget Component
* **Floating Launcher:** A button (bottom-right) to toggle the chat.
* **Chat Window:**
  * Header: "Todo Assistant".
  * Message List: Scrollable area showing user vs. AI messages.
  * Input Area: Text field + Send button.
* **Markdown Support:** The AI returns structured text (lists, bolding), so the UI should render Markdown (optional but recommended).

### 4.2. API Integration logic
* Retrieve the **Session Token** from the active auth session.
* Endpoint: `POST http://localhost:8001/chat`
* Headers:
  * `Content-Type: application/json`
  * `Authorization: Bearer <session_token>`

## 5. Implementation Steps
1.  Create `frontend/src/components/ChatWidget.tsx`.
2.  Implement the UI layout (Shadcn/UI style).
3.  Add the API calling logic.
4.  Import and mount `ChatWidget` in `frontend/src/app/dashboard/layout.tsx` so it persists across pages.
5.  Manual Test: Chat with the agent and verify tasks update in the background.