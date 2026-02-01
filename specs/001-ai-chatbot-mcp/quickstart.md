# Quickstart Guide: AI Chatbot with MCP Integration

## Prerequisites
- Python 3.11+
- Poetry or pip for dependency management
- PostgreSQL database (Neon recommended)
- Better Auth configured
- OpenAI API key
- MCP SDK installed

## Setup Instructions

### 1. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Update with your configuration
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql://user:password@host:port/database
BETTER_AUTH_SECRET=your_auth_secret
BETTER_AUTH_URL=http://localhost:3000
```

### 2. Install Dependencies
```bash
# Backend dependencies
cd backend
pip install -r requirements.txt
# or if using poetry
poetry install
```

### 3. Database Setup
```bash
# Run database migrations
cd backend
python -m alembic upgrade head

# Or initialize the database tables directly
python -m scripts.init_db
```

### 4. Start Services
```bash
# Terminal 1: Start MCP server
cd backend
python -m src.mcp.server

# Terminal 2: Start main API server
cd backend
python -m src.main
```

### 5. Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Configure ChatKit domain
# Add your domain to allowed origins in Better Auth config

# Start development server
npm run dev
```

## Usage Examples

### Starting a New Conversation
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### Continuing an Existing Conversation
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "existing-conversation-id",
    "message": "Show me my tasks"
  }'
```

## Verification Steps

1. **Test Authentication**: Verify JWT validation works
2. **Test Task Creation**: Add a task via chat and verify it's stored
3. **Test Task Listing**: Ask to list tasks and verify response
4. **Test Conversation Continuity**: Restart server and resume conversation
5. **Test User Isolation**: Verify users can't access each other's data

## Troubleshooting

- **JWT Issues**: Verify BETTER_AUTH_SECRET matches between frontend and backend
- **Database Connection**: Check DATABASE_URL is properly configured
- **MCP Server**: Ensure MCP server is running before starting main API server
- **CORS Issues**: Verify frontend domain is allowed in backend CORS settings