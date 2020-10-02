from locust import HttpUser, task, between
from time import gmtime, strftime
import json, base64, os, tarfile, random

class LogTelemetryUploadTest(HttpUser):
    wait_time = between(60, 61)

    # @task
    # def post_telemetry(self):
    #   ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #   mac_arr = [ 0xB8, 0x27, 0xEB, random.randint(0x00, 0xFF), random.randint(0x00, 0xFF), random.randint(0x00, 0xFF) ]
    #   mac = ':'.join(map(lambda x: "%02x" % x, mac_arr))
    #   markers = [{'marker_'+str(x): random.randint(0,10000)} for x in range(0,98)]
    #   markers.append({"Time": ts})
    #   markers.append({"mac": mac})

    #   with self.client.post("/perfdev1/upload/device/telemetry", data=json.dumps({"searchResult":markers}), catch_response=True) as response:
    #     if response.status_code != 200:
    #       response.failure("Telemetry upload failed with code " + str(response.status_code))

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
      with self.client.post("/perfdev1/upload/device/log", files=log, catch_response=True) as response:
        if response.status_code != 200:
          response.failure("Log upload failed with code " + str(response.status_code))
