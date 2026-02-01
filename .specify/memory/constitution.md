<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 3.0.0
Modified principles: Updated to include Phase-III AI Chatbot and MCP requirements
Added sections: Agentic Development Law, Tooling & AI Rules, MCP Architecture Rules, Conversational AI Behavior, API Contract Law, Frontend Constraints, Evaluation Criteria, Forbidden Actions, Phase Exit Authority
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: Update template files to reflect new Phase-III requirements
-->
# Todo App Qwen Constitution - Phase III: AI Chatbot with MCP

## Core Principles

### Accuracy
Every technical and conceptual claim must be verifiable through primary sources. System behavior must match documented specifications exactly.

### Clarity
Writing must target an academic computer science audience. Code, specs, and documentation must use precise, unambiguous language.

### Reproducibility
Any result must be independently reproducible using: Specs, Prompts, Versioned configurations. No undocumented manual intervention is allowed.

### Rigor
Claims must prioritize peer-reviewed literature. Engineering decisions must be justified by standards or research.

### Academic Integrity
Zero-tolerance for plagiarism. All sources must be cited in APA style. AI-generated content must be reviewed, edited, verified, and properly referenced.

### Responsible AI Use
AI tools (Qwen CLI, Spec-Kit Plus) are engineering collaborators, not authorities. All outputs require human validation, spec conformance, and security review.

## Security Constitution
Authentication Law: Every API request must include Authorization: Bearer <JWT>. Tokens must be signed with BETTER_AUTH_SECRET, time-limited, and verifiable by backend. Data Sovereignty: Users may only view, modify, delete their own tasks. Zero-Trust API: No endpoint is public. No implicit trust between frontend and backend. Identity is proven only by cryptographic verification.

## Development Workflow
All development must follow: Write Spec → Generate Plan → Break into Tasks → Implement via Qwen CLI. Manual coding is constitutionally prohibited. Toolchain: Specs (GitHub Spec-Kit Plus), Implementation (Qwen CLI), Frontend (Next.js App Router), Backend (FastAPI), ORM (SQLModel), Database (Neon Serverless PostgreSQL), Auth (Better Auth + JWT).

## Phase-III Specific Requirements

### Agentic Development Law
All development MUST strictly follow this workflow:
spec → plan → tasks → implementation via Qwen CLI

- No manual coding is allowed
- No direct file editing is allowed
- All code must be generated or refined ONLY through Qwen CLI prompts
- Any violation invalidates the phase

### Tooling & AI Rules
- AI logic MUST use OpenAI Agents SDK
- All agent reasoning and tool invocation must be generated via Qwen CLI
- MCP server MUST be built using the Official MCP SDK
- MCP tools must be stateless
- All state must persist in the database (PostgreSQL)

QWEN CLI or QWEN-specific workflows are strictly prohibited.
All references must use Qwen CLI terminology and workflows only.

### Stateless Server Principle
- FastAPI server must remain stateless
- No in-memory conversation or task state is allowed
- Every request must:
  - Fetch conversation history from database
  - Run agent with full context
  - Persist new messages and tool results
- Server restarts must not affect chat continuity

### MCP Architecture Rules
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

### Conversational AI Behavior
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

### Authentication & Security
- Authentication handled via Better Auth
- Backend must trust user identity from verified JWT
- user_id must always come from auth context
- MCP tools must enforce user-level data isolation
- Cross-user access is forbidden

### Database as Source of Truth
Database tables:
- tasks
- conversations
- messages

Rules:
- Conversations persist independently of server
- Messages persist independently of agent runs
- Tool calls must be reproducible from DB state
- No derived or cached state allowed

### API Contract Law
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

### Frontend Constraints
- Frontend must use OpenAI ChatKit
- Domain allowlist must be configured before production
- ChatKit domain key must be injected via env
- Frontend holds no business logic

### Evaluation Criteria
Phase-III is considered successful ONLY if:
- Natural language task management works end-to-end
- MCP tools are correctly invoked by agent
- Server is fully stateless
- Conversations resume after restart
- All code generated via Qwen CLI
- Specs, plans, and tasks are fully documented

### Forbidden Actions
- Manual Python coding
- QWEN CLI or QWEN CLI usage (use Qwen CLI only)
- Stateful server memory
- Hardcoded secrets
- Skipping spec/plan/tasks steps
- Tool-less task mutations

### Phase Exit Authority
Phase-III may only exit when:
- phase3_spec.md exists
- phase3_plan.md exists
- /sp.tasks executed
- MCP tools implemented
- AI agent operational
- README updated
- All constraints satisfied

## Governance
All work must follow the governance model: Architecture (Spec documents), Implementation (Qwen CLI under spec control), Security (JWT + Better Auth policies), Data (Database schema specs), Research Claims (Peer-reviewed sources). Any change must follow: Spec update, Review, AI regeneration, Validation. No direct code edits outside the Agentic Dev Stack workflow.

**Version**: 3.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-19