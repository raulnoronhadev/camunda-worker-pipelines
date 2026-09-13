import os
import subprocess
from datetime import datetime
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

    # PRIMEIRO PROJETO/SERVICE 1

    # 1 - recuperar conteúdo das variáveis da request
    source_path = task.get_variable("sourcePath")
    participant = task.get_variable("participant")
    submission_id = task.get_variable("submissionId")
    execution_id = task.get_process_instance_id()

    # 2 - baixe um arquivo do alarik para dentro da pasta cache usando rclone
    # 3 - dentro da pasta cache, crie uma pasta com o ID dessa execução. Esse arquivo será um JSON com uma lista de itens. Cada item é um objeto com várias propriedades.
    run_rclone(["copy", "s3:origin-bucket/lasso-secure/1/", f"/cache/{execution_id}"])

    # 4 - Quando terminar, isso vai concluir o primeiro tópico e irá para o segundo tópico.
    # 5 - O segundo tópico, que é o handler, vai ler o arquivo dentro de cache usando o ID e vai transformar isso em um CSV.
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