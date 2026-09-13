import os
import subprocess
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker

cib7_rest_url = os.environ["CIB7_REST_URL"]
topic = os.environ["TOPIC"]
worker_id = os.environ["WORKER_ID"]
failure_retries = os.environ["FAILURE_RETRIES"]
failure_retry_timeout_ms = os.environ["FAILURE_RETRY_TIMEOUT_MS"]

default_config = {
    "maxTasks": 1,
    "lockDuration": 60000,
    "asyncResponseTimeout": 5000,
    "retries": failure_retries,
    "retryTimeout": failure_retry_timeout_ms,
    "sleepSeconds": 30
}

def handle_task(task: ExternalTask) -> TaskResult:
    execution_id = task.get_process_instance_id()
    csv_path = f"/cache/{execution_id}/mock_data.csv"
    destination_path = f"landing:secondary-bucket/{execution_id}/"
    run_rclone(["copy", csv_path, destination_path])
    print("CSV file uploaded.")
    return task.complete()

def run_rclone(command_args):
    command = ["rclone"] + command_args
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Rclone error occurred: {e.stderr}")
        return None

if __name__ == '__main__':
    ExternalTaskWorker(worker_id=worker_id, base_url=cib7_rest_url, config=default_config).subscribe(topic, handle_task)