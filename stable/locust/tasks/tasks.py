from locust import HttpLocust, TaskSet, task
import json

class ElbTasks(TaskSet):
  @task
  def post_telemetry(self):
    #   telemetry = json.loads(open("/locust-tasks/rtl_json.txt", "r").read())
    #   self.client.post("/erdk/upload/device/telemetry", data=json.dumps(telemetry))
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({'hello': 'world'}))

#   @task
#   def post_log(self):
#       log = {"filename": open("/locust-tasks/log.tgz", "rb")}
#       self.client.post("/erdk/upload/device/log", files=log)

class ElbWarmer(HttpLocust):
  task_set = ElbTasks
  min_wait = 1000
  max_wait = 3000
