import functions_framework
import requests
import logging
import os

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

base_url = os.environ.get('FLOWER_API_URL')


def load_task_status(task_id):
    flower_url = f"{base_url}/api/task/info/{task_id}"
    response = requests.get(flower_url)
    if response.status_code == 200:
        task_info = response.json()
        return task_info.get("state")
    else:
        return None


@functions_framework.http
def get_task_status(request):
    request_json = request.get_json(silent=True)
    logging.debug(f"Request: {request_json}")
    task_id = request_json['calls'][0][0]

    return {"replies": [{"status": load_task_status(task_id)}]}
