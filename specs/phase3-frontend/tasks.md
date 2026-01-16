# Tasks: Phase 3.2 - AI Chat Interface Integration

**Input**: Design documents from `/specs/phase3-frontend/`
**Prerequisites**: plan.md (required), spec.md (required), AI Agent API running on port 8001.

## Phase 1: Setup

- [ ] T001 Install `react-markdown` if requested (Optional: we can start without it for simple text)
- [ ] T002 Create the `frontend/src/components/ChatWidget.tsx` file stub

## Phase 2: UI Implementation

- [ ] T003 Implement the floating toggle button (bottom-right)
- [ ] T004 Implement the Chat Window container (header, message list, input area)
- [ ] T005 Add styling using Tailwind CSS to match the dashboard aesthetic
- [ ] T006 Implement automatic scrolling to the bottom of the message list

## Phase 3: Logic & API Integration

- [ ] T007 Integrate `useSession` to retrieve the auth token
- [ ] T008 Implement the `sendMessage` function to call `http://localhost:8001/chat`
- [ ] T009 Handle loading states (e.g., show "Agent is thinking...")
- [ ] T010 Implement error handling for API failures

## Phase 4: Integration & Verification

- [ ] T011 Mount `ChatWidget` in `frontend/src/app/dashboard/layout.tsx`
- [ ] T012 End-to-end test: Open chat, send message "Add task Lunch with Bob", verify success
- [ ] T013 End-to-end test: Verify the new task appears in the Dashboard task list (might require manual refresh or shared state)
- [ ] T014 Final polish and UI refinements
