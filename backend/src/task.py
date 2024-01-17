import time


# Функция, которая будет выполняться в фоновом режиме
def my_task(x, y):
    time.sleep(3)
    return x + y
