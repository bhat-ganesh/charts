from locust import HttpLocust, TaskSet, task

class ElbTasks(TaskSet):
  @task
#   def status(self):
#       self.client.get("/status")
  @task
  import json
  def post_telemetry(self):
      regex = json.loads(open("/locust-tasks/rtl_json.txt", "r").read())
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps(regex))

  @task
  import json
  def post_log(self):
      log = {"filename": open("/locust-tasks/log.tgz", "rb")}
      self.client.post("/erdk/upload/device/log", files=log)

class ElbWarmer(HttpLocust):
  task_set = ElbTasks
  min_wait = 1000
  max_wait = 3000
