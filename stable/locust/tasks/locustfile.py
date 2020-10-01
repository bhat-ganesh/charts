from locust import HttpUser, task, between
from time import gmtime, strftime
import json, base64, os, tarfile, random

class LogTelemetryUploadTest(HttpUser):
    wait_time = between(60, 61)

    # @task
    # def post_telemetry(self):
    #   ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #   mac_arr = [ 0xB8, 0x27, 0xEB, 0X00, random.randint(0x00, 0xFF), random.randint(0x00, 0xFF) ]
    #   mac = ':'.join(map(lambda x: "%02x" % x, mac_arr))

    #   with self.client.post("/perfdev1/upload/device/telemetry", data=json.dumps({"searchResult":[{"Profile":"RDKB"},
    #                                                                                      {"mac":mac},
    #                                                                                      {"erouterIpv4":"192.168.2.36"},
    #                                                                                      {"erouterIpv6":"null"},
    #                                                                                      {"PartnerId":"RDKM"},
    #                                                                                      {"AccountId":"Unknown"},
    #                                                                                      {"Version":"rdkb-generic-broadband-image_default_20200619132645"},
    #                                                                                      {"marker_1": "111111"},
    #                                                                                      {"marker_2": "111112"},
    #                                                                                      {"marker_3": "111113"},
    #                                                                                      {"marker_4": "111114"},
    #                                                                                      {"marker_5": "111115"},
    #                                                                                      {"marker_6": "111116"},
    #                                                                                      {"marker_7": "111117"},
    #                                                                                      {"marker_8": "111118"},
    #                                                                                      {"marker_9": "111119"},
    #                                                                                      {"marker_10": "111120"},
    #                                                                                      {"marker_11": "111121"},
    #                                                                                      {"marker_12": "111122"},
    #                                                                                      {"marker_13": "111123"},
    #                                                                                      {"marker_14": "111124"},
    #                                                                                      {"marker_15": "111125"},
    #                                                                                      {"marker_16": "111126"},
    #                                                                                      {"marker_17": "111127"},
    #                                                                                      {"marker_18": "111128"},
    #                                                                                      {"marker_19": "111129"},
    #                                                                                      {"marker_20": "111130"},
    #                                                                                      {"marker_21": "111131"},
    #                                                                                      {"marker_22": "111132"},
    #                                                                                      {"marker_23": "111133"},
    #                                                                                      {"marker_24": "111134"},
    #                                                                                      {"marker_25": "111135"},
    #                                                                                      {"marker_26": "111136"},
    #                                                                                      {"marker_27": "111137"},
    #                                                                                      {"marker_28": "111138"},
    #                                                                                      {"marker_29": "111139"},
    #                                                                                      {"marker_30": "111140"},
    #                                                                                      {"marker_31": "111141"},
    #                                                                                      {"marker_32": "111142"},
    #                                                                                      {"marker_33": "111143"},
    #                                                                                      {"marker_34": "111144"},
    #                                                                                      {"marker_35": "111145"},
    #                                                                                      {"marker_36": "111146"},
    #                                                                                      {"marker_37": "111147"},
    #                                                                                      {"marker_38": "111148"},
    #                                                                                      {"marker_39": "111149"},
    #                                                                                      {"marker_40": "111150"},
    #                                                                                      {"marker_41": "111151"},
    #                                                                                      {"marker_42": "111152"},
    #                                                                                      {"marker_43": "111153"},
    #                                                                                      {"marker_44": "111154"},
    #                                                                                      {"marker_45": "111155"},
    #                                                                                      {"marker_46": "111156"},
    #                                                                                      {"marker_47": "111157"},
    #                                                                                      {"marker_48": "111158"},
    #                                                                                      {"marker_49": "111159"},
    #                                                                                      {"marker_50": "111160"},
    #                                                                                      {"marker_51": "111161"},
    #                                                                                      {"marker_52": "111162"},
    #                                                                                      {"marker_53": "111163"},
    #                                                                                      {"marker_54": "111164"},
    #                                                                                      {"marker_55": "111165"},
    #                                                                                      {"marker_56": "111166"},
    #                                                                                      {"marker_57": "111167"},
    #                                                                                      {"marker_58": "111168"},
    #                                                                                      {"marker_59": "111169"},
    #                                                                                      {"marker_60": "111170"},
    #                                                                                      {"marker_61": "111171"},
    #                                                                                      {"marker_62": "111172"},
    #                                                                                      {"marker_63": "111173"},
    #                                                                                      {"marker_64": "111174"},
    #                                                                                      {"marker_65": "111175"},
    #                                                                                      {"marker_66": "111176"},
    #                                                                                      {"marker_67": "111177"},
    #                                                                                      {"marker_68": "111178"},
    #                                                                                      {"marker_69": "111179"},
    #                                                                                      {"marker_70": "111180"},
    #                                                                                      {"marker_71": "111181"},
    #                                                                                      {"marker_72": "111182"},
    #                                                                                      {"marker_73": "111183"},
    #                                                                                      {"marker_74": "111184"},
    #                                                                                      {"marker_75": "111185"},
    #                                                                                      {"marker_76": "111186"},
    #                                                                                      {"marker_77": "111187"},
    #                                                                                      {"marker_78": "111188"},
    #                                                                                      {"marker_79": "111189"},
    #                                                                                      {"marker_80": "111190"},
    #                                                                                      {"marker_81": "111191"},
    #                                                                                      {"marker_82": "111192"},
    #                                                                                      {"Time":ts}]}), catch_response=True) as response:
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
