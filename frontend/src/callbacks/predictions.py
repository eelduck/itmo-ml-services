import base64

import dash
import requests


def predict(n_clicks, selected_model, contents, filename, session_data):
    if n_clicks is None or not contents or not selected_model or not session_data:
        return "Please select a model, upload a file, and ensure you are logged in."

    if "fastapiusersauth" not in session_data:
        return "Authentication error. Please log in."

    _, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        files = {"file": (filename, decoded, "text/csv")}
        headers = {"Cookie": f"fastapiusersauth={session_data['fastapiusersauth']}"}

        prediction_url = (
            f"http://backend-api:8000/predictions/create?model_id={selected_model}"
        )

        response = requests.post(prediction_url, headers=headers, files=files)

        if response.status_code == 200:
            return "Prediction job is sent. Please update your prediction to see the result"
        else:
            return f"Prediction failed: {response.text}"

    except Exception as e:
        return f"An error occurred during prediction: {e}"


def get_predictions(n_clicks, session_data):
    """Retrieve predictions for the logged-in user."""
    if n_clicks is None:
        return dash.no_update, dash.no_update
    if not session_data or "fastapiusersauth" not in session_data:
        return dash.no_update, "Please log in to get predictions."
    headers = {"Cookie": f"fastapiusersauth={session_data['fastapiusersauth']}"}
    try:
        response = requests.get("http://backend-api:8000/predictions/", headers=headers)
        if response.status_code == 200:
            predictions_data = response.json()
            return predictions_data, ""
        else:
            return [], f"Failed to fetch predictions: {response.text}"
    except requests.exceptions.RequestException as e:
        return [], f"An error occurred: {e}"
