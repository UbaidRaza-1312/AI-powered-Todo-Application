# Implementation Plan: AI Chatbot with MCP Integration

**Branch**: `001-ai-chatbot-mcp` | **Date**: 2026-01-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-chatbot-mcp/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered conversational interface for todo management using natural language processing. The system integrates an OpenAI agent with MCP (Model Context Protocol) tools to perform task operations. The architecture follows a stateless design where all conversation and task data is persisted in a PostgreSQL database, ensuring continuity across server restarts. The system enforces strict user isolation through JWT-based authentication and implements a clear separation of concerns between the frontend, API layer, AI agent, and MCP tools.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Better Auth
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 99% of requests responded within 5 seconds
**Constraints**: Stateless server design, JWT authentication required, user data isolation
**Scale/Scope**: Individual user focus with potential for multi-tenancy

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Gates determined based on constitution file:
- All technical and conceptual claims must be verifiable through primary sources
- System behavior must match documented specifications exactly
- Writing must target an academic computer science audience with precise, unambiguous language
- Any result must be independently reproducible using specs, prompts, and versioned configurations
- Claims must prioritize peer-reviewed literature and engineering decisions must be justified by standards or research
- Zero-tolerance for plagiarism; all sources must be cited in APA style
- AI-generated content must be reviewed, edited, verified, and properly referenced
- All outputs require human validation, spec conformance, and security review
- Development must follow Agentic Development Law: spec → plan → tasks → implementation via Qwen CLI
- No manual coding is allowed; all code must be generated via Qwen CLI
- MCP server must be built using Official MCP SDK with stateless tools
- FastAPI server must remain stateless with database as single source of truth
- Authentication handled via Better Auth with JWT verification
- Frontend must use OpenAI ChatKit with proper domain configuration
- AI logic must use OpenAI Agents SDK
- All state must persist in database (PostgreSQL) with no in-memory conversation state
- MCP tools must be stateless and use database as single source of truth

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot-mcp/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py
│   │   ├── conversation_service.py
│   │   └── message_service.py
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── server.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── add_task.py
│   │   │   ├── list_tasks.py
│   │   │   ├── update_task.py
│   │   │   ├── complete_task.py
│   │   │   └── delete_task.py
│   │   └── tool_registry.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── chat_agent.py
│   │   └── system_prompt.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat_endpoint.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── jwt_validator.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt
├── pyproject.toml
└── alembic/
    ├── env.py
    ├── script.py.mako
    └── versions/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
├── package.json
└── .env
```

**Structure Decision**: Web application with separate frontend and backend components to maintain clear separation of concerns. Backend uses FastAPI with modular structure separating models, services, MCP tools, and agents. Frontend uses OpenAI ChatKit for the conversational interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| MCP SDK Integration | Required by Phase-III specification for tool-based AI interaction | Direct database access would bypass safety and audit requirements |
| Separate MCP Server | Enables clear separation of AI reasoning from tool execution | Combined approach would compromise stateless architecture requirement |
