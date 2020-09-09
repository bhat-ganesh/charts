import time, json
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def post_telemetry(self):
        # for running in dokcer
        # regex = json.loads(open("/mnt/locust/files/rtl_json.txt", "r").read())
        # for running locally
        regex = json.loads(open("files/rtl_json.txt", "r").read())
        self.client.post("/erdk/upload/device/telemetry", data=json.dumps(regex))

    @task
    def post_log(self):
        # for running in dokcer
        # log = {"filename": open("/mnt/locust/files/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "rb")}
        # for running locally
        log = {"filename": open("files/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "rb")}
        self.client.post("/erdk/upload/device/log", files=log)