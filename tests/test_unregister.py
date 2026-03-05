"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

Tests student unregistration functionality including happy paths,
error cases, and edge conditions.
"""


def test_unregister_existing_student_success(client):
    """
    Test successful unregistration of a student from an activity.
    
    Arrange: Activity with existing participant
    Act: DELETE request to unregister endpoint
    Assert: Status 200 and confirmation message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_student_removed_from_participants(client):
    """
    Test that unregistered student is removed from participants list.
    
    Arrange: Activity with known participant
    Act: Unregister student, then retrieve activities
    Assert: Student email is not in the participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert unregister_response.status_code == 200
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_student_fails(client):
    """
    Test unregistration fails for student not signed up.
    
    Arrange: Activity and student not in participants
    Act: DELETE request for non-enrolled student
    Assert: Status 400 and error message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "notstudent@mergington.edu"  # Not in participants
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity_not_found(client):
    """
    Test unregistration fails for non-existent activity.
    
    Arrange: Invalid activity name
    Act: DELETE request to unregister endpoint
    Assert: Status 404 and error message returned
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_and_resign_up(client):
    """
    Test student can unregister and then sign up again.
    
    Arrange: Activity with participant
    Act: Unregister student, then sign up again
    Assert: Both operations succeed and student is in participants
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_unregister_multiple_students(client):
    """
    Test unregistration of multiple students from one activity.
    
    Arrange: Activity with multiple participants
    Act: Unregister two different students
    Assert: Both unregister successfully and both are removed
    """
    # Arrange
    activity_name = "Chess Club"
    email1 = "michael@mergington.edu"
    email2 = "daniel@mergington.edu"
    
    # Act
    response1 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email1}
    )
    response2 = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email2}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    activities = activities_response.json()
    assert email1 not in activities[activity_name]["participants"]
    assert email2 not in activities[activity_name]["participants"]
