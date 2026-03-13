def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    signup_response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]

    # Assert
    assert signup_response.status_code == 200
    assert signup_response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in participants


def test_signup_rejects_duplicate_email(client):
    # Arrange
    email = "duplicate@mergington.edu"

    # Act
    first_response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )
    duplicate_response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": email},
    )

    # Assert
    assert first_response.status_code == 200
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student already signed up"


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange

    # Act
    response = client.post(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    # Arrange
    email = "remove-me@mergington.edu"

    client.post(
        "/activities/Science%20Club/signup",
        params={"email": email},
    )

    # Act
    unregister_response = client.delete(
        "/activities/Science%20Club/signup",
        params={"email": email},
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()["Science Club"]["participants"]

    # Assert
    assert unregister_response.status_code == 200
    assert unregister_response.json()["message"] == (
        f"Unregistered {email} from Science Club"
    )
    assert email not in participants


def test_unregister_returns_not_found_for_missing_participant(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Soccer%20Team/signup",
        params={"email": "missing@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_returns_not_found_for_unknown_activity(client):
    # Arrange

    # Act
    response = client.delete(
        "/activities/Unknown%20Activity/signup",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
