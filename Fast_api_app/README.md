# FastAPI Sample Project

A comprehensive FastAPI application with user authentication, product management, and admin approval system.

## Features

- 🔐 JWT-based authentication with access and refresh tokens
- 👥 User registration and admin approval system
- 🛍️ Product CRUD operations with ownership
- 👨‍💼 Role-based access control (Admin/User)
- 🗄️ SQLAlchemy ORM with PostgreSQL
- 📝 Pydantic schemas for data validation
- 🔄 Soft delete functionality
- 📊 Audit trails for data changes

## Project Structure

```
Fast_api_app/
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic schemas for validation
├── routers/         # API endpoints
├── crud/           # Database operations
├── services/       # Business logic
├── utils/          # Helper functions
├── db/             # Database configuration
└── alembic/        # Database migrations
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   SECRET_KEY=your-secret-key-here
   ACCESS_TOKEN_EXPIRE_MINUTES=15
   REFRESH_TOKEN_EXPIRE_MINUTES=1440
   ALGORITHM=HS256
   ```

3. **Database Setup**:
   ```bash
   # Initialize Alembic
   alembic init alembic
   
   # Create initial migration
   alembic revision --autogenerate -m "Initial migration"
   
   # Apply migration
   alembic upgrade head
   ```

4. **Run the Application**:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
- `POST /users/login` - User login
- `POST /users/logout` - User logout

### User Management
- `GET /users/all` - Get all users (Admin only)
- `GET /users/approved_user` - Get approved users
- `GET /users/unapproved_users` - Get unapproved users (Admin only)
- `POST /users/{user_id}/approve` - Approve user (Admin only)
- `GET /users/current_user_details` - Get current user details

### Product Management
- `POST /products/add_products` - Create new product
- `GET /products/all_products` - Get all products
- `PUT /products/update_product/{product_id}` - Update product
- `DELETE /products/delete_product/{product_id}` - Delete product
- `GET /products/get_product/{product_id}` - Get specific product

## Authentication

The API uses JWT tokens for authentication:
- Access tokens expire in 15 minutes (configurable)
- Refresh tokens expire in 24 hours (configurable)
- Include tokens in Authorization header: `Bearer <token>`

## Admin Features

- Approve/reject user registrations
- View all users and products
- Manage product ownership

## Security Features

- Password hashing with bcrypt
- JWT token validation
- Role-based access control
- Soft delete for data integrity
- Audit trails for changes
