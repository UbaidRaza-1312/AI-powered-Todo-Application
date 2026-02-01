---
id: 1
title: "Update Phase3 Constitution"
stage: constitution
date: "2026-01-19"
surface: "agent"
model: "OpenAI GPT-4"
feature: "none"
branch: "main"
user: "Star.com"
command: "/sp.constitution"
labels: ["constitution", "phase3", "ai-chatbot", "mcp"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - ".specify/templates/plan-template.md"
  - ".specify/templates/spec-template.md"
  - ".specify/templates/tasks-template.md"
tests: []
prompt_text: |

  /sp.constitution Phase-III — Todo AI Chatbot with MCP (Qwen CLI)

  Purpose:
  Define immutable rules, development constraints, architectural principles, and evaluation standards
  for Phase-III of the Todo project. This phase introduces an AI-powered conversational interface
  using MCP (Model Context Protocol) and Qwen CLI, following an agentic development workflow.

  This constitution governs ALL decisions, prompts, plans, tasks, and generated code in Phase-III.

  ────────────────────────────────────────────
  1. Agentic Development Law
  ────────────────────────────────────────────
  All development MUST strictly follow this workflow:

  spec → plan → tasks → implementation via Qwen CLI

  - No manual coding is allowed
  - No direct file editing is allowed
  - All code must be generated or refined ONLY through Qwen CLI prompts
  - Any violation invalidates the phase

  ────────────────────────────────────────────
  2. Tooling & AI Rules
  ────────────────────────────────────────────
  - AI logic MUST use OpenAI Agents SDK
  - All agent reasoning and tool invocation must be generated via Qwen CLI
  - MCP server MUST be built using the Official MCP SDK
  - MCP tools must be stateless
  - All state must persist in the database (PostgreSQL)

  QWEN CLI or QWEN-specific workflows are strictly prohibited.
  All references must use Qwen CLI terminology and workflows only.

  ────────────────────────────────────────────
  3. Stateless Server Principle
  ────────────────────────────────────────────
  - FastAPI server must remain stateless
  - No in-memory conversation or task state is allowed
  - Every request must:
    - Fetch conversation history from database
    - Run agent with full context
    - Persist new messages and tool results
  - Server restarts must not affect chat continuity

  ────────────────────────────────────────────
  4. MCP Architecture Rules
  ────────────────────────────────────────────
  - MCP server exposes task operations as tools
  - MCP tools:
    - add_task
    - list_tasks
    - complete_task
    - delete_task
    - update_task
  - MCP tools:
    - Must NOT store state internally
    - Must NOT hold memory between calls
    - Must use database as single source of truth
  - AI agent may chain multiple MCP tools in a single turn

  ────────────────────────────────────────────
  5. Conversational AI Behavior
  ────────────────────────────────────────────
  The AI agent MUST:
  - Interpret natural language task requests
  - Choose correct MCP tools automatically
  - Confirm every action in friendly language
  - Handle missing tasks gracefully
  - Never hallucinate task state
  - Never modify tasks without tool invocation

  Hard rules:
  - No tool call → No task mutation
  - Every mutation must be persisted
  - Every response must be explainable via tool calls

  ────────────────────────────────────────────
  6. Authentication & Security
  ────────────────────────────────────────────
  - Authentication handled via Better Auth
  - Backend must trust user identity from verified JWT
  - user_id must always come from auth context
  - MCP tools must enforce user-level data isolation
  - Cross-user access is forbidden

  ────────────────────────────────────────────
  7. Database as Source of Truth
  ────────────────────────────────────────────
  Database tables:
  - tasks
  - conversations
  - messages

  Rules:
  - Conversations persist independently of server
  - Messages persist independently of agent runs
  - Tool calls must be reproducible from DB state
  - No derived or cached state allowed

  ────────────────────────────────────────────
  8. API Contract Law
  ────────────────────────────────────────────
  Single chat endpoint:
  POST /api/{user_id}/chat

  Rules:
  - Stateless request cycle
  - conversation_id optional
  - New conversation auto-created if missing
  - Response must include:
    - conversation_id
    - assistant response
    - list of MCP tool calls

  ────────────────────────────────────────────
  9. Frontend Constraints
  ────────────────────────────────────────────
  - Frontend must use OpenAI ChatKit
  - Domain allowlist must be configured before production
  - ChatKit domain key must be injected via env
  - Frontend holds no business logic

  ────────────────────────────────────────────
  10. Evaluation Criteria
  ────────────────────────────────────────────
  Phase-III is considered successful ONLY if:
  - Natural language task management works end-to-end
  - MCP tools are correctly invoked by agent
  - Server is fully stateless
  - Conversations resume after restart
  - All code generated via Qwen CLI
  - Specs, plans, and tasks are fully documented

  ────────────────────────────────────────────
  11. Forbidden Actions
  ────────────────────────────────────────────
  - Manual Python coding
  - QWEN CLIor QWEN CLI usage
  - Stateful server memory
  - Hardcoded secrets
  - Skipping spec/plan/tasks steps
  - Tool-less task mutations

  ────────────────────────────────────────────
  12. Phase Exit Authority
  ────────────────────────────────────────────
  Phase-III may only exit when:
  - phase3_spec.md exists
  - phase3_plan.md exists
  - /sp.tasks executed
  - MCP tools implemented
  - AI agent operational
  - README updated
  - All constraints satisfied

  ADD in old  constitution
response_text: |

  I've successfully updated the project constitution for Phase-III of the Todo project, incorporating the AI Chatbot with MCP requirements. Here's what was done:

  1. Updated the constitution file (.specify/memory/constitution.md) to version 3.0.0, incorporating all the Phase-III requirements including:
     - Agentic Development Law
     - Tooling & AI Rules
     - Stateless Server Principle
     - MCP Architecture Rules
     - Conversational AI Behavior
     - Authentication & Security
     - Database as Source of Truth
     - API Contract Law
     - Frontend Constraints
     - Evaluation Criteria
     - Forbidden Actions
     - Phase Exit Authority

  2. Updated dependent template files to align with the new constitution:
     - Updated plan-template.md to include Phase-III compliance checks
     - Updated spec-template.md to include Phase-III requirements
     - Updated tasks-template.md to include Phase-III validation tasks

  3. Created a sync impact report in the constitution file documenting all changes.

  The new constitution now governs all decisions, prompts, plans, tasks, and generated code for Phase-III, ensuring that development follows the required workflow using Qwen CLI and MCP tools.
outcome: "Constitution successfully updated to v3.0.0 with Phase-III requirements. Template files updated to align with new requirements."
evaluation: "All required elements from the user input have been incorporated into the constitution and related templates. Files have been updated and saved successfully."
---

# Constitution Update Completed

The project constitution has been successfully updated to include Phase-III requirements for the Todo AI Chatbot with MCP. The constitution now governs all development decisions for this phase, ensuring compliance with the agentic development workflow using Qwen CLI.