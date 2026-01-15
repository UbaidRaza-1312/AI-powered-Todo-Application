# Todo Application

A full-stack Todo application built with a Python FastAPI backend and a React/Next.js frontend.

## Quick Start

To run this application locally, follow these steps:

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`

## Features

- User authentication (register/login)
- Create, read, update, and delete todo tasks
- Responsive design for desktop and mobile devices
- Secure password hashing
- Modern UI/UX

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- Alembic (for migrations)
- Neon DB (PostgreSQL-based serverless database)

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS (or other CSS framework)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables:
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Update the `DATABASE_URL` in `.env` with your Neon DB connection string
6. Create the database tables: `python create_tables.py`
7. Run the application: `python main.py`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install` or `yarn install`
3. Set up environment variables if needed
4. Run the development server: `npm run dev` or `yarn dev`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Tasks
- `GET /tasks` - Get all tasks for the authenticated user
- `POST /tasks` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Environment Variables

### Backend (in backend/.env)
```env
# Database Configuration - Neon DB
DATABASE_URL=postgresql+asyncpg://your_username:your_password@ep-xxx.us-east-1.aws.neon.tech/your_database_name?sslmode=require

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-to-a-random-string-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FastAPI documentation
- Next.js documentation
- All contributors who helped make this project better