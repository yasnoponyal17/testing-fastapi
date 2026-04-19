# Лабораторная работа. Нагрузочное тестирование.
## Постановка задачи
1. Воспроизвести показанное на занятии и прокомментировать ситуацию с
high_cpu_endpoint_fixed и high_cpu_endpoint, slow_endpoint, slow_endpoint_fixed
2. Используя какие-либо 2-3 других асинхронных или синхронных REST-фреймворка (bottle, flask, tornado, sanic) на Python или на других языках/платформах сравнить работу и производительность, привести графики и данные. Сформулировать общие принципы при проведении стресс-тестирования на рассмотренной платформе в отчете.
## FastAPI
### Код app.py
```python
from fastapi import FastAPI, HTTPException
import asyncio
import time  # Для симуляции медленной операции

app = FastAPI()

# Не лучшая практика - глобальная переменная для подключения, но для демо сойдет
connection_pool = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/slow_endpoint")
async def slow_endpoint():
    # Имитация тяжелой CPU-задачи или сложного вычисления
    time.sleep(0.1)  # Опасность! time.sleep блокирует весь event loop.
    return {"message": "This was a slow request"}

@app.get("/slow_endpoint_fixed")
async def slow_endpoint_fixed():
    # Имитация тяжелой CPU-задачи или сложного вычисления
    await asyncio.sleep(0.1)
    return {"message": "This was a asyncio sleep and now the request is no longer slow"}


@app.get("/high_cpu_endpoint")
async def high_cpu_endpoint():
    # Функция, которая нагружает ЦПУ
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = cpu_intensive_task()
    return {"message": f"CPU task completed with result: {result}"}


@app.get("/high_cpu_endpoint_fixed")
async def high_cpu_endpoint_fixed():
    # Выносим CPU-задачу в отдельный поток
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = await asyncio.to_thread(cpu_intensive_task)
    return {"message": f"CPU task completed with result: {result} without blocking the event loop!"}
```
### Результат работы locust
#### high_cpu_endpoint и slow_endpoint
![fastapi](/images/fastapi.png)
#### high_cpu_endpoint_fixed и slow_endpoint_fixed
![fastapi-fixed](/images/fastapi-fixed.png)
#### flask
![flask](/images/flask.png)
#### sanic
![sanic](/images/sanic.png)
