# Implementation Plan: Phase III - AI-Powered Todo Chatbot

**Branch**: `main` | **Date**: 2025-12-27 | **Spec**: [specs/phase3-ai-agent/spec.md](specs/phase3-ai-agent/spec.md)
**Input**: Feature specification from `/specs/phase3-ai-agent/spec.md`

## Summary
The goal of Phase III is to integrate an AI-powered chatbot into the existing Todo application. This will be achieved by:
1. Implementing an **MCP Server** that exposes the backend CRUD operations as tools.
2. Building an **AI Agent** using the OpenAI Agents SDK that consumes these tools.
3. Updating the **Frontend** with a Chat UI to interact with the AI Agent.

## Technical Context

**Language/Version**: Python 3.12 (Backend/MCP/Agent), TypeScript/Next.js (Frontend)
**Primary Dependencies**: 
- MCP Python SDK
- OpenAI Agents SDK
- FastAPI (Existing)
- Next.js (Existing)
- OpenAI ChatKit/CopilotKit
**Storage**: PostgreSQL (Existing SQLModel)
**Testing**: pytest
**Target Platform**: Local development (Web)
**Project Type**: Web application with AI Agent integration

## Constitution Check

- [x] Adhere to existing project conventions (FastAPI, Next.js).
- [x] Small, testable changes.
- [x] Use MCP for tool protocol.
- [x] Use OpenAI Agents SDK for AI logic.

## Project Structure

```text
backend/                 # Existing FastAPI backend
frontend/                # Existing Next.js frontend
mcp-server/              # New: MCP Server service
├── main.py              # MCP server entry point
├── tools.py             # Definition of MCP tools
└── pyproject.toml       # MCP server dependencies
ai-agent/                # New: AI Agent logic
├── agent.py             # OpenAI Agent definition
├── main.py              # Agent service entry point
└── pyproject.toml       # Agent dependencies
specs/phase3-ai-agent/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Atomic tasks
```

## Technical Details

### MCP Server (`/mcp-server`)
- Will use `mcp` Python library.
- Will communicate with the backend via HTTP.
- Authentication: Will require a session token to be passed from the agent (which gets it from the frontend).

### AI Agent (`/ai-agent`)
- Will use `openai-agents` SDK.
- System Prompt: "You are a helpful productivity assistant. You can help users manage their tasks (create, list, update, delete) using the provided tools."
- Will be exposed via an API (possibly within the backend or as a separate microservice) for the frontend to consume. *Decision: For simplicity, we might add an endpoint to the backend that proxies to the agent, or have the agent as a separate FastAPI service.*

### Frontend Integration (`/frontend`)
- Add a floating chat widget or a sidebar.
- Use a library like CopilotKit or a custom React component for the chat interface.

## Risk Analysis and Mitigation
- **Auth Token Propagation:** The agent needs to pass the user's session token to the MCP server. We'll ensure the token is captured from the frontend request.
- **Agent Latency:** AI responses can be slow. We'll use streaming if possible and show loading states.
- **Tool Reliability:** The MCP server must handle backend errors gracefully.
