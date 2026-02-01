# Todo Application - Neon DB Setup

This application has been configured to use Neon DB as the database backend instead of SQLite.

## Prerequisites

1. Sign up for a [Neon account](https://neon.tech/)
2. Create a new project in your Neon dashboard
3. Note down your connection string from the Neon dashboard

## Setup Instructions

### For Local Development (with SQLite)
The application defaults to SQLite for local development:
1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application directly:
   ```bash
   python main.py
   ```

### For Production (with Neon DB)
To use Neon DB in production:

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your Neon DB connection string:
   ```env
   DATABASE_URL=postgresql+asyncpg://your_username:your_password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```

4. Create the database tables in Neon DB:
   ```bash
   python create_tables.py
   ```

5. Start the application:
   ```bash
   python main.py
   ```

## Database Schema

The application creates two main tables in Neon DB:

### Users Table
- `id`: UUID (Primary Key)
- `email`: VARCHAR (Unique, Indexed) - stored in plain text for authentication
- `hashed_password`: VARCHAR - securely hashed using BCrypt
- `first_name`: VARCHAR (Optional)
- `last_name`: VARCHAR (Optional)
- `is_active`: BOOLEAN (Default: True)
- `email_verified`: BOOLEAN (Default: False)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

### Tasks Table
- `id`: UUID (Primary Key)
- `title`: VARCHAR (200 chars max)
- `description`: TEXT (Optional, 1000 chars max)
- `completed`: BOOLEAN (Default: False)
- `user_id`: UUID (Foreign Key to Users)
- `due_date`: TIMESTAMP (Optional)
- `priority`: INTEGER (1-5 scale)
- `created_at`: TIMESTAMP
- `updated_at`: TIMESTAMP

## Features

- **Serverless Architecture**: Automatically scales based on demand
- **Branching**: Create isolated database environments for development
- **Point-in-time Recovery**: Restore your database to any point in time
- **Autoscaling**: Compute resources scale up and down automatically
- **Scale to Zero**: Reduces costs when not in use
- **Compatibility**: Full PostgreSQL compatibility with Neon DB

## Security

- Passwords are securely hashed using BCrypt
- JWT tokens are used for authentication
- SSL encryption is enforced for all database connections
- Environment variables protect sensitive credentials

## Troubleshooting

If you encounter connection issues:
1. Verify your Neon DB connection string is correct
2. Ensure your IP address is whitelisted in Neon dashboard
3. Check that the database name and credentials are correct
4. For local development, the application will fall back to SQLite if no PostgreSQL URL is provided

## Testing

To test the database connection:
```bash
python test_db_connection.py
```

## Architecture

The application intelligently detects the database type from the connection string:
- If `postgresql` is in the URL, it configures for Neon DB/PostgreSQL
- If `sqlite` is in the URL, it configures for local SQLite
- This allows seamless switching between development and production environments





