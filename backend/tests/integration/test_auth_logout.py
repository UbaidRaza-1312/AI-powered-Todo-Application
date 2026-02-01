"""
Integration tests for authentication logout functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from src.models.user import User
from src.services.auth_service import AuthService
from src.utils.auth import create_access_token
from uuid import UUID
import uuid


def test_logout_endpoint_exists(client: TestClient, db_session: Session):
    """Test that the logout endpoint exists and returns expected response"""
    
    # Create a test user
    auth_service = AuthService(db_session)
    user_data = {
        "email": "test_logout@example.com",
        "first_name": "Test",
        "last_name": "User"
    }
    user = auth_service.create_user_sync(user_data, "testpassword123")
    db_session.commit()
    
    # Create a token for the user
    token_data = {"sub": str(user.id), "email": user.email}
    token = create_access_token(token_data)
    
    # Call the logout endpoint
    response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}


def test_logout_without_token(client: TestClient):
    """Test that logout endpoint works without a token (doesn't require authentication)"""
    
    # Note: In a real JWT implementation, logout is typically a client-side operation
    # since JWTs are stateless. Our implementation returns success regardless.
    response = client.post("/api/auth/logout")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}