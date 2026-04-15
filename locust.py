from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 3)  # Пользователь ждет между запросами от 1 до 3 секунд

    @task(1)
    def hello_world(self):
        self.client.get("/")

    @task(1)
    def slow_endpoint(self):
        self.client.get("/slow_endpoint")

    @task(1)
    def slow_endpoint_fixed(self):
        self.client.get('/slow_endpoint_fixed')

    @task(1)
    def high_cpu_endpoint(self):
        self.client.get("/high_cpu_endpoint")

    @task(1)
    def high_cpu_endpoint_fixed(self):
        self.client.get('/high_cpu_endpoint_fixed')