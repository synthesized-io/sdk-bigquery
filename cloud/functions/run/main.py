import functions_framework
import requests
import logging
import json
import os

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

base_url = os.environ.get('FLOWER_API_URL')
if base_url is None:
    raise ValueError("FLOWER_API_URL environment variable is not defined.")
run_task_url = f"{base_url}/api/task/send-task/worker.main.synthesize_run"


@functions_framework.http
def synthesize(request):
    request_json = request.get_json()
    logging.debug(f"Request: {request_json}")
    params = request_json['calls'][0]

    sdk_request = {
        "args": [
            f"bq://{params[0]}",
            f"bq://{params[1]}",
            json.loads(params[2])
        ]
    }

    try:
        response = requests.post(run_task_url, json=sdk_request)

        if response.status_code == 200:
            return {"replies": [{"status": "success", "task_id": response.json()['task-id']}]}
        else:
            return {
                "replies": [{"status": "error", "message": f"Request failed with status code: {response.status_code}"}]}

    except requests.exceptions.RequestException as e:
        return {"replies": [{"status": "error", "message": f"An error occurred: {e}"}]}
