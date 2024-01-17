from redis import Redis
from rq import Queue

from task import my_task

redis_conn = Redis(host="localhost", port=6379)
queue = Queue(connection=redis_conn)


# Добавление задачи в очередь
job = queue.enqueue(my_task, args=(3, 4))
job = queue.enqueue(my_task, args=(3, 5))
job = queue.enqueue(my_task, args=(3, 6))
job = queue.enqueue(my_task, args=(3, 7))
job = queue.enqueue(my_task, args=(3, 8))
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
