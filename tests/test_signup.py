"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests student signup functionality including happy paths, error cases,
and edge conditions.
"""


def test_signup_new_student_success(client):
    """
    Test successful signup of a new student to an activity.
    
    Arrange: Valid activity name and new email address
    Act: POST request to signup endpoint
    Assert: Status 200 and confirmation message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_student_appears_in_participants(client):
    """
    Test that signed-up student appears in participants list.
    
    Arrange: Valid activity and new email
    Act: Sign up student, then retrieve activities
    Assert: Student email is in the participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert signup_response.status_code == 200
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_student_rejected(client):
    """
    Test that duplicate signup is rejected.
    
    Arrange: Activity with existing participant
    Act: Attempt to sign up same student again
    Assert: Status 400 and error message returned
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_not_found(client):
    """
    Test signup fails for non-existent activity.
    
    Arrange: Invalid activity name
    Act: POST request to signup endpoint
    Assert: Status 404 and error message returned
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_different_students(client):
    """
    Test signup works for multiple different students.
    
    Arrange: One activity and two different new students
    Act: Sign up both students
    Assert: Both signup requests succeed and both appear in participants
    """
    # Arrange
    activity_name = "Programming Class"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    activities = activities_response.json()
    assert email1 in activities[activity_name]["participants"]
    assert email2 in activities[activity_name]["participants"]


def test_signup_to_different_activities(client):
    """
    Test one student can signup to multiple different activities.
    
    Arrange: One student and two different activities
    Act: Sign up student to both activities
    Assert: Student appears in both activities' participant lists
    """
    # Arrange
    email = "versatile@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Drama Club"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": email}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    activities = activities_response.json()
    assert email in activities[activity1]["participants"]
    assert email in activities[activity2]["participants"]
