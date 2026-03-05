"""
Tests for the GET / endpoint.

Tests the root endpoint which redirects to the static frontend.
"""


def test_root_redirects_to_static_index(client):
    """
    Test that GET / redirects to the static index.html.
    
    Arrange: No setup needed
    Act: Make GET request to /
    Assert: Status code indicates redirect and location header is set
    """
    # Arrange
    expected_redirect_location = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in [301, 302, 303, 307, 308]  # Redirect status codes
    assert response.headers.get("location") == expected_redirect_location


def test_root_redirect_location_is_correct(client):
    """
    Test that redirect location is exactly /static/index.html.
    
    Arrange: Expected redirect path
    Act: Make GET request to /
    Assert: Location header matches expected path
    """
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_followable(client):
    """
    Test that the redirect can be followed to reach the static content.
    
    Arrange: No setup needed
    Act: Make GET request to / with follow_redirects=True
    Assert: Final response is successful (200)
    """
    # Arrange
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
