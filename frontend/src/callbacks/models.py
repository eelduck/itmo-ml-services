import requests


def update_model_dropdown(pathname):
    """Update the model dropdown options on the predictions page."""
    if pathname == "/predictions":
        models_response = requests.get("http://backend-api:8000/models/")
        models = models_response.json() if models_response.status_code == 200 else []
        return [
            {
                "label": f"#{model['id']} {model['name']} (Cost: {model['cost']}) - {model['description']}",
                "value": model["id"],
            }
            for model in models
        ]
