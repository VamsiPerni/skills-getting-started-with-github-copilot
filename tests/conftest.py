"""
Pytest configuration and fixtures for FastAPI tests.

This module provides shared fixtures for testing the Mergington High School API.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient instance for testing the FastAPI application.
    
    The TestClient allows us to make requests to the app without running
    a live server.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the in-memory activities database between tests.
    
    This fixture is automatically used (autouse=True) to ensure test
    isolation by restoring the original activities state before each test.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and varsity play",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis instruction and match play",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
            "max_participants": 10,
            "participants": ["james@mergington.edu", "hannah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater production and acting workshops",
            "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture classes",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Club": {
            "description": "Competitive debate and public speaking",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["mason@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "STEM competition in biology, chemistry, physics and engineering",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["zoe@mergington.edu", "lucas@mergington.edu"]
        }
    }
    
    # Clear current activities and restore original
    activities.clear()
    activities.update(original_activities)
    
    yield  # Pass control to the test
    
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)
