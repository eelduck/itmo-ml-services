import os

import pandas as pd
from joblib import load
from redis import Redis
from rq import Queue
from worker_task import predict_task

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)

lgbm_model = load(os.path.join(os.pardir, "models", "lgbm.joblib"))
data = pd.read_csv(os.path.join(os.pardir, "models", "android_test.csv"), sep=";")

# Добавление задачи в очередь
job = queue.enqueue(predict_task, args=(data, lgbm_model, 1))
job_id = job.get_id()
job_status = job.get_status()


print(job_id, job_status)

# Получение результатов выполнения задачи
job_result = queue.fetch_job(job_id).result
print(f"Результат выполнения задачи: {job_result}")

import time

time.sleep(5)

job_result = queue.fetch_job(job_id).result
print(f"Результат выполнения задачи: {job_result}")
