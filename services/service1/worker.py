import os
from camunda.external_task.external_task import ExternalTask, TaskResult
from camunda.external_task.external_task_worker import ExternalTaskWorker


default_config = {
    "maxTasks": 1,
    "lockDuration": 10000,
    "asyncResponseTimeout": 5000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 30
}


cib7_rest_url = os.environ["CIB7_REST_URL"]
topic = os.environ["TOPIC"]
worker_id = os.environ["WORKER_ID"]


def handle_task(task: ExternalTask) -> TaskResult:
    print("====================================")
    print("TASK RECEIVED")

    print("ID:", task.get_task_id())
    print("Topic:", task.get_topic_name())
    print("Process Instance:", task.get_process_instance_id())

    print("Executing task.complete()...")

    result = task.complete()

    print("task.complete() succesfull!")
    print("====================================")

    return result


if __name__ == '__main__':
    ExternalTaskWorker(worker_id=worker_id, base_url=cib7_rest_url, config=default_config).subscribe(topic, handle_task)