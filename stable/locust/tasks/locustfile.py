#############################################################################################################################################################

from locust import HttpUser, task, between
from time import gmtime, strftime
import json, base64, os, tarfile

class LogTelemetryUploadTest(HttpUser):
    wait_time = between(1, 2)

    @task
    def post_telemetry(self):
      ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":[{"Profile":"RDKB"},
                                                                                         {"mac":"FF:FF:FF:FF:FF:FF"},
                                                                                         {"erouterIpv4":"192.168.2.36"},
                                                                                         {"erouterIpv6":"null"},
                                                                                         {"PartnerId":"RDKM"},
                                                                                         {"AccountId":"Unknown"},
                                                                                         {"Version":"rdkb-generic-broadband-image_default_20200619132645"},
                                                                                         {"Time":ts}]}))

    @task
    def post_log(self):
      ts = strftime("%Y-%m-%d-%H-%M-%S-", gmtime())
      log_path = "/tmp/log/"

      fl = open('/locust-tasks/log.txt', 'r')
      log_txt = fl.read().replace('\n', '')
      fl.close()


      fb = open(log_path + "FF:FF:FF:FF:FF:FF-Logs.tgz", "wb")
      fb.write(base64.b64decode(log_txt))
      fb.close()

      log = {"filename": open(log_path + "FF:FF:FF:FF:FF:FF-Logs.tgz", "rb")}
      self.client.post("/erdk/upload/device/log", files=log)


      # if not os.path.exists(log_path):
      #     os.mkdir(log_path)

      # fb = open(log_path + "log.tgz", "wb")
      # fb.write(base64.b64decode(log_txt))
      # fb.close()

      # with tarfile.open(log_path + "log.tgz", "r") as tar:
      #   tar.extractall()

      # os.remove(log_path + "log.tgz")

      # for filename in os.listdir(log_path):
      #     os.rename(log_path + filename, log_path + ts + filename)

      # with tarfile.open("/tmp/FF:FF:FF:FF:FF:FF-Logs.tgz", "w:gz") as tar:
      #     tar.add(log_path, arcname=os.path.basename(log_path))

      # log = {"filename": open("/tmp/FF:FF:FF:FF:FF:FF-Logs.tgz", "rb")}
      # self.client.post("/erdk/upload/device/log", files=log)

#############################################################################################################################################################

# from locust import HttpLocust, TaskSet, task
# from time import gmtime, strftime
# import json, base64

# class UploadEndpointTasks(TaskSet):
#   @task
#   def post_telemetry(self):
#       # telemetry = json.loads(open("/locust-tasks/rtl_json.txt", "r").read())
#       # self.client.post("/erdk/upload/device/telemetry", data=json.dumps(telemetry))
#       ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#       self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":[{"Profile":"RDKB"},
#                                                                                          {"mac":"FF:FF:FF:FF:FF:FF"},
#                                                                                          {"erouterIpv4":"192.168.2.36"},
#                                                                                          {"erouterIpv6":"null"},
#                                                                                          {"PartnerId":"RDKM"},
#                                                                                          {"AccountId":"Unknown"},
#                                                                                          {"Version":"rdkb-generic-broadband-image_default_20200619132645"}
#                                                                                          ,{"Time":ts}]}))

#   @task
#   def post_log(self):
#       fl = open('/locust-tasks/log.txt', 'r')
#       log_txt = fl.read().replace('\n', '')
#       fl.close()

#       fb = open("/tmp/FF:FF:FF:FF:FF:FF-Logs.tgz", "wb")
#       fb.write(base64.b64decode(log_txt))
#       fb.close()

#       log = {"filename": open("/tmp/FF:FF:FF:FF:FF:FF-Logs.tgz", "rb")}
#       self.client.post("/erdk/upload/device/log", files=log)

# class UploadEndpointTest(HttpLocust):
#   task_set = UploadEndpointTasks
#   min_wait = 1000
#   max_wait = 3000

#############################################################################################################################################################