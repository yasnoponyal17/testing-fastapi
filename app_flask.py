from flask import Flask, jsonify
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

executor = ThreadPoolExecutor()

@app.route("/")
def root():
    return jsonify({"Hello": "World"})


@app.route("/slow_endpoint")
def slow_endpoint():
    time.sleep(0.1)
    return jsonify({"message": "This was a slow request"})


@app.route("/slow_endpoint_fixed")
def slow_endpoint_fixed():
    time.sleep(0.1)
    return jsonify({"message": "Flask is sync, so no async benefit here"})


@app.route("/high_cpu_endpoint")
def high_cpu_endpoint():
    def cpu_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    result = cpu_task()
    return jsonify({"message": f"CPU task completed: {result}"})


@app.route("/high_cpu_endpoint_fixed")
def high_cpu_endpoint_fixed():
    def cpu_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total

    future = executor.submit(cpu_task)
    result = future.result()

    return jsonify({
        "message": f"CPU task completed: {result} (in thread)"
    })


if __name__ == "__main__":
    app.run(debug=True)