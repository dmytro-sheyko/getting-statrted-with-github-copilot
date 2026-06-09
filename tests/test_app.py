from fastapi.testclient import TestClient

from src.app import activities, app


def test_signup_for_activity_success():
    # Arrange
    activity_name = "Programming Class"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        with TestClient(app) as client:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in activities[activity_name]["participants"]
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_rejects_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    with TestClient(app) as client:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_unknown_activity_returns_404():
    # Arrange
    activity_name = "Missing Club"
    email = "student@mergington.edu"

    # Act
    with TestClient(app) as client:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_participant_removes_student():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        # Act
        with TestClient(app) as client:
            response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    finally:
        activities[activity_name]["participants"] = original_participants
