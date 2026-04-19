from sanic import Sanic
from sanic.response import json
import asyncio
import time

app = Sanic("TestApp")


@app.get("/")
async def root(request):
    return json({"Hello": "World"})


@app.get("/slow_endpoint")
async def slow_endpoint(request):
    time.sleep(0.1)
    return json({"message": "This was a slow request"})


@app.get("/slow_endpoint_fixed")
async def slow_endpoint_fixed(request):
    await asyncio.sleep(0.1)
    return json({"message": "Async sleep works properly"})


@app.get("/high_cpu_endpoint")
async def high_cpu_endpoint(request):
    def cpu_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = cpu_task() 
    return json({"message": f"CPU task completed: {result}"})


@app.get("/high_cpu_endpoint_fixed")
async def high_cpu_endpoint_fixed(request):
    def cpu_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = await asyncio.to_thread(cpu_task)

    return json({
        "message": f"CPU task completed: {result} without blocking"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)