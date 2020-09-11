from locust import HttpLocust, TaskSet, task
import json, base64

class ElbTasks(TaskSet):
  @task
  def post_telemetry(self):
      telemetry = json.loads(open("/locust-tasks/rtl_json.txt", "r").read())
      # self.client.post("/erdk/upload/device/telemetry", data=json.dumps(telemetry))
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":[{"Profile":"RDKB"},{"mac":"B8:27:EB:1A:FD:FF"},{"erouterIpv4":"192.168.2.36"},{"erouterIpv6":"null"},{"PartnerId":"RDKM"},{"AccountId":"Unknown"},{"Version":"rdkb-generic-broadband-image_default_20200619132645"},{"Time":"2020-06-17 18:48:00"},{"hello":"world2"}]}))

  @task
  def post_log(self):
      fl = open('/locust-tasks/log.txt', 'r')
      log_txt = fl.read().replace('\n', '')
      fl.close()

      fb = open("/tmp/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "wb")
      fb.write(base64.b64decode(log_txt))
      fb.close()

      log = {"filename": open("/tmp/B8:27:EB:1A:FD:FF-Logs-06-16-20-06-37PM.tgz", "rb")}
      self.client.post("/erdk/upload/device/log", files=log)

class ElbWarmer(HttpLocust):
  task_set = ElbTasks
  min_wait = 1000
  max_wait = 3000
