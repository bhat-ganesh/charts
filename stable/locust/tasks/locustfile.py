#############################################################################################################################################################

from locust import HttpUser, task, between
from time import gmtime, strftime
import json, base64, os, tarfile, random

class LogTelemetryUploadTest(HttpUser):
    wait_time = between(3, 5)

    @task
    def post_telemetry(self):
      ts = strftime("%m-%d-%y-%H-%M-%S-", gmtime())
      mac_arr = [ 0xB8, 0x27, 0xEB, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff) ]
      mac = ':'.join(map(lambda x: "%02x" % x, mac_arr))

      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":[{"Profile":"RDKB"},
                                                                                         {"mac":mac},
                                                                                         {"erouterIpv4":"192.168.2.36"},
                                                                                         {"erouterIpv6":"null"},
                                                                                         {"PartnerId":"RDKM"},
                                                                                         {"AccountId":"Unknown"},
                                                                                         {"Version":"rdkb-generic-broadband-image_default_20200619132645"},
                                                                                         {"Time":ts}]}))

    @task
    def post_log(self):
      ts = strftime("%m-%d-%y-%H-%M-%S-", gmtime())
      mac_arr = [ 0xB8, 0x27, 0xEB, random.randint(0x00, 0x7f), random.randint(0x00, 0xff), random.randint(0x00, 0xff) ]
      mac = ':'.join(map(lambda x: "%02x" % x, mac_arr))

      log_path = "/tmp/log/"

      fl = open('/locust-tasks/log.txt', 'r')
      log_txt = fl.read().replace('\n', '')
      fl.close()

      if not os.path.exists(log_path):
          os.mkdir(log_path)

      fb = open(log_path + "log.tgz", "wb")
      fb.write(base64.b64decode(log_txt))
      fb.close()

      with tarfile.open(log_path + "log.tgz", "r") as tar:
        tar.extractall(path=log_path)

      os.remove(log_path + "log.tgz")

      with tarfile.open("/tmp/" + mac + "-Logs.tgz", "w:gz") as tar:
          for filename in os.listdir(log_path):
              tar.add(log_path + filename, arcname=ts + filename)

      log = {"filename": open("/tmp/" + mac + "-Logs.tgz", "rb")}
      self.client.post("/erdk/upload/device/log", files=log)



      # old code, same file without ts --> start
      # fb = open(log_path + "FF:FF:FF:FF:FF:FF-Logs.tgz", "wb")
      # fb.write(base64.b64decode(log_txt))
      # fb.close()

      # log = {"filename": open(log_path + "FF:FF:FF:FF:FF:FF-Logs.tgz", "rb")}
      # self.client.post("/erdk/upload/device/log", files=log)
      # old code, same file without ts --> end

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