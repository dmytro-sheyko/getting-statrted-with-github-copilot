from fastapi.testclient import TestClient

from src.app import activities, app


def test_unregister_participant_removes_student():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        with TestClient(app) as client:
            response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

        assert response.status_code == 200
        assert email not in activities[activity_name]["participants"]
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
    finally:
        activities[activity_name]["participants"] = original_participants
