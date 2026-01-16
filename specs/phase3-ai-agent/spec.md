# Phase III: AI-Powered Todo Chatbot Specification

## 1. Overview
The goal of Phase III is to evolve the existing full-stack Todo application into an **AI-native application**. We will implement a chatbot interface that allows users to manage their tasks using natural language. The system will leverage the **Model Context Protocol (MCP)** to expose backend services as tools and the **OpenAI Agents SDK** to drive the interaction.

## 2. Architecture
We will adopt a **modular architecture** to ensure clean separation of concerns. The project structure will be expanded as follows:

- **`/backend` (Existing):** The core FastAPI application handling database interactions (SQLModel), authentication (Better Auth), and business logic. This remains the "source of truth".
- **`/mcp-server` (New):** A standalone Python service. It will act as a bridge, exposing the backend's capabilities as **MCP Tools** (e.g., `add_task`, `list_tasks`). It will communicate with the Backend APIs via HTTP.
- **`/ai-agent` (New):** A dedicated directory for the Intelligent Agent logic using the **OpenAI Agents SDK**. This agent will consume tools from the MCP server to fulfill user requests.
- **`/frontend` (Existing):** The Next.js application will be updated to include a Chat UI (using **OpenAI ChatKit** or CopilotKit) to interact with the agent.

## 3. Technology Stack
- **AI Engine:** OpenAI Agents SDK (Python)
- **Tool Protocol:** Model Context Protocol (MCP) - Official Python SDK
- **Backend:** FastAPI, SQLModel, PostgreSQL (Existing)
- **Frontend:** Next.js, OpenAI ChatKit/CopilotKit (React)

## 4. Functional Requirements

### 4.1. MCP Server (`/mcp-server`)
- **Objective:** Create an MCP server that defines tools corresponding to the CRUD operations.
- **Tools to Implement:**
  1.  `get_tasks(user_id)`: Retrieve all tasks for the authenticated user.
  2.  `create_task(title, description, user_id)`: Create a new todo item.
  3.  `update_task(task_id, ...)`: Update task details or toggle completion status.
  4.  `delete_task(task_id)`: Remove a task.
- **Connectivity:** The MCP server will make HTTP requests to the running `backend` server (e.g., `http://localhost:8000`).

### 4.2. AI Agent (`/ai-agent`)
- **Objective:** Build a conversational agent that can reason about tasks.
- **Configuration:**
  - Define the agent's instructions (System Prompt) to act as a helpful productivity assistant.
  - Connect the agent to the MCP Server to access the defined tools.
  - Ensure the agent is stateless; conversation history will be managed by the client/frontend session.

### 4.3. Frontend Integration (`/frontend`)
- **Objective:** Add a conversational interface.
- **Features:**
  - Implement a Chat Widget or a dedicated Chat Page.
  - Pass the user's message to the AI Agent.
  - Display the Agent's textual response and any tool outputs (e.g., showing the updated list after adding a task).

## 5. Implementation Roadmap
1.  **Infrastructure Setup:** Initialize `mcp-server` and `ai-agent` directories.
2.  **MCP Tooling:** Implement the MCP server and verify connectivity with the Backend API.
3.  **Agent Logic:** Script the OpenAI Agent interactions.
4.  **UI Updates:** Connect the Frontend to the Agent.