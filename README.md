# AI-Powered Todo Chatbot Setup

## Overview
This project implements an AI-powered todo chatbot using Google's Gemini API and Model Context Protocol (MCP) architecture. The chatbot allows users to manage their todos through natural language interactions.

## Prerequisites

- Python 3.9+
- Node.js 18+
- PostgreSQL-compatible database (Neon recommended)
- Google Gemini API key

## Backend Setup

### 1. Environment Variables
Create a `.env` file in the backend directory with the following variables:

```bash
# Database Configuration
DATABASE_URL="postgresql://username:password@host:port/database_name"

# Gemini API Configuration
GEMINI_API_KEY="your-gemini-api-key-here"

# JWT Configuration
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 2. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Database Setup
```bash
# Run database migrations
python create_tables.py
```

### 4. Run the Backend Server
```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`.

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Run the Development Server
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`.

## MCP Server (Optional)
If you need to run the MCP server separately:

```bash
cd backend/src/mcp
python server.py
```

The MCP server will start on `http://localhost:8001`.

## Features

### Chat Interface
- Natural language interaction with the AI assistant
- Persistent conversation history
- Real-time task management
- User-specific data isolation

### Supported Commands
- **Add tasks**: "Add a task to buy groceries" or "Create a task to finish report"
- **List tasks**: "Show my tasks" or "What do I have to do?"
- **Complete tasks**: "Mark task 1 as complete" or "Finish the meeting prep"
- **Delete tasks**: "Delete task 2" or "Remove the grocery list"
- **Update tasks**: "Change task 1 to buy milk" or "Update the description"

### Security
- JWT-based authentication
- User data isolation
- Secure API endpoints
- Input validation and sanitization

## Architecture

### Backend Components
- **FastAPI**: Web framework for API endpoints
- **SQLModel/SQLAlchemy**: Database ORM
- **Gemini API**: Natural language processing
- **MCP Server**: Tool execution protocol
- **PostgreSQL**: Data persistence

### Frontend Components
- **Next.js**: React framework
- **Tailwind CSS**: Styling
- **Custom API Client**: Backend communication

## API Endpoints

### Chat Endpoints
- `POST /api/users/{user_id}/chat` - Process chat messages
- `GET /api/users/{user_id}/conversations` - Get user conversations
- `GET /api/users/{user_id}/conversations/{conversation_id}/messages` - Get conversation messages

### Existing Endpoints
- `POST /api/users/{user_id}/tasks` - Create tasks
- `GET /api/users/{user_id}/tasks` - Get tasks
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update tasks
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete tasks
- `PATCH /api/users/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Troubleshooting

### Common Issues
1. **Gemini API Key Not Found**: Ensure `GEMINI_API_KEY` is set in environment variables
2. **Database Connection Issues**: Verify `DATABASE_URL` is correctly configured
3. **Authentication Errors**: Check JWT configuration in environment variables

### Logging
Check the backend logs for detailed error information:
```bash
# View logs
tail -f logs/app.log
```

## Development

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### Adding New MCP Tools
1. Create a new tool in `backend/src/mcp/tools/`
2. Follow the existing tool pattern
3. Register the tool in `backend/src/mcp/tool_registry.py`

## Production Deployment

### Backend
- Use a production WSGI server (e.g., Gunicorn)
- Configure environment variables securely
- Set up proper logging and monitoring

### Frontend
- Build for production: `npm run build`
- Serve the static files using a web server (e.g., Nginx)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.