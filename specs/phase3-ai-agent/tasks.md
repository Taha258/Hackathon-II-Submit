# Tasks: Phase III - AI-Powered Todo Chatbot

**Input**: Design documents from `/specs/phase3-ai-agent/`
**Prerequisites**: plan.md (required), spec.md (required)

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Create `mcp-server` directory and initialize `pyproject.toml`
- [ ] T002 Create `ai-agent` directory and initialize `pyproject.toml`
- [ ] T003 Create `history/prompts/phase3-ai-agent/` for PHRs

## Phase 2: Foundational (MCP Server)

- [ ] T004 Implement basic MCP server in `mcp-server/main.py`
- [ ] T005 Implement `get_tasks` tool in `mcp-server/tools.py`
- [ ] T006 Implement `create_task` tool in `mcp-server/tools.py`
- [ ] T007 Implement `update_task` tool in `mcp-server/tools.py`
- [ ] T008 Implement `delete_task` tool in `mcp-server/tools.py`
- [ ] T009 Verify MCP tools connectivity with backend (manual test with `mcp-inspector` or script)

## Phase 3: AI Agent Implementation

- [ ] T010 Define OpenAI Agent with system prompt in `ai-agent/agent.py`
- [ ] T011 Connect AI Agent to MCP Server tools
- [ ] T012 Create a FastAPI wrapper for the AI Agent in `ai-agent/main.py` to expose it to the frontend
- [ ] T013 Implement session/auth handling in the Agent to pass tokens to MCP tools

## Phase 4: Frontend Integration

- [ ] T014 Install necessary frontend dependencies (e.g., `openai-chatkit` or similar)
- [ ] T015 Create `ChatInterface` component in `frontend/src/components/ChatInterface.tsx`
- [ ] T016 Integrate `ChatInterface` into `frontend/src/app/dashboard/page.tsx`
- [ ] T017 Connect `ChatInterface` to the AI Agent API

## Phase 5: Verification & Polish

- [ ] T018 End-to-end test: Create a task via chat and verify it appears in the list
- [ ] T019 End-to-end test: List tasks via chat
- [ ] T020 End-to-end test: Update/Delete tasks via chat
- [ ] T021 Final code cleanup and documentation
