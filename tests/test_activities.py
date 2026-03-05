"""
Tests for the GET /activities endpoint.

Tests the retrieval of all available activities and validates the
response structure and content.
"""


def test_get_all_activities(client):
    """
    Test that GET /activities returns all activities.
    
    Arrange: No setup needed, activities are pre-loaded
    Act: Make GET request to /activities
    Assert: Verify status code and all 9 activities are returned
    """
    # Arrange
    expected_activity_count = 9
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count


def test_activities_response_structure(client):
    """
    Test that activity objects have the correct structure.
    
    Arrange: Expected keys for each activity
    Act: Make GET request to /activities
    Assert: Verify each activity has required fields
    """
    # Arrange
    expected_keys = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert isinstance(activity_data, dict)
        assert expected_keys.issubset(set(activity_data.keys()))
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_include_chess_club(client):
    """
    Test that Chess Club activity is returned.
    
    Arrange: No setup needed
    Act: Make GET request to /activities
    Assert: Verify Chess Club is in the response with correct initial participants
    """
    # Arrange
    activity_name = "Chess Club"
    expected_initial_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert activity_name in activities
    assert activities[activity_name]["participants"] == expected_initial_participants


def test_activities_include_all_expected_names(client):
    """
    Test that all expected activity names are present.
    
    Arrange: List of expected activity names
    Act: Make GET request to /activities
    Assert: Verify all expected activities are returned
    """
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Drama Club",
        "Art Studio",
        "Debate Club",
        "Science Olympiad"
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    activity_names = list(activities.keys())
    
    # Assert
    for expected_name in expected_activities:
        assert expected_name in activity_names
