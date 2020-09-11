from locust import HttpLocust, TaskSet, task
import json, base64

class ElbTasks(TaskSet):
  @task
  def post_telemetry(self):
      telemetry = json.loads(open("/locust-tasks/rtl_json.txt", "r").read())
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps(telemetry))

  @task
  def post_log(self):
      fl = open('/locust-tasks/log.txt', 'r')
      log_txt = fl.read().replace('\n', '')
      fl.close()

    #   fb = open("/locust-tasks/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "wb")
    #   fb.write(log_txt.decode('base64'))
    #   fb.close()

    #   log = {"filename": open("/locust-tasks/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "rb")}
      log = {"filename": base64.decodebytes(log_txt)}
      self.client.post("/erdk/upload/device/log", files=log)

class ElbWarmer(HttpLocust):
  task_set = ElbTasks
  min_wait = 1000
  max_wait = 3000
