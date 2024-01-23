import dash
import requests


def register_user(n_clicks, email, password):
    """Register a new user."""
    if n_clicks is None:
        return ""
    if not email or not password:
        return "Please fill out all fields."
    payload = {
        "email": email,
        "password": password,
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    try:
        response = requests.post("http://backend-api:8000/auth/register", json=payload)
        if response.status_code == 201:
            return "Registration successful. Please log in."
        else:
            return f"Registration failed: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


def login_user(n_clicks, email, password):
    """Authenticate user and redirect to predictions page upon successful login."""
    if n_clicks is None:
        return dash.no_update, dash.no_update, dash.no_update
    if not email or not password:
        return "Please fill out all fields.", dash.no_update, dash.no_update
    login_data = {"username": email, "password": password}
    try:
        response = requests.post(
            "http://backend-api:8000/auth/jwt/login/", data=login_data
        )
        if response.status_code == 204:
            cookie = response.cookies.get("fastapiusersauth")
            return "", "/predictions", {"fastapiusersauth": cookie}
        else:
            return f"Login failed: {response.text}", dash.no_update, dash.no_update
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", dash.no_update, dash.no_update


def update_user_info(pathname, session_data):
    """Update user information displayed on the page."""
    if not session_data or "fastapiusersauth" not in session_data:
        return "Not logged in", "0"
    headers = {"Cookie": f"fastapiusersauth={session_data['fastapiusersauth']}"}
    try:
        response = requests.get("http://backend-api:8000/user/", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data["email"], f"{user_data['balance']}"
        else:
            return "Error fetching user data", "0"
    except requests.exceptions.RequestException:
        return "Error fetching user data", "0"
