from locust import HttpUser, task, between
from time import gmtime, strftime
import json, random

class TelemetryMarkerUploadTest(HttpUser):
    wait_time = between(10, 20)

    @task
    def post_telemetrymarker(self):
      ts = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      mac_arr = [ 0xB8, 0x27, 0xEB, 0XFF, random.randint(0x00, 0xFF), random.randint(0x00, 0xFF) ]
      mac = ':'.join(map(lambda x: "%02x" % x, mac_arr))
      markers = [{'example_'+str(x): random.randint(0,100)} for x in range(0,4)]
      markers.append({"Time": ts})
      markers.append({"mac": mac})
      markers.append({"Version": "rdkb-generic-broadband-image_default_2020_bad"})
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":markers}))

      markers_good = []
      markers_good.append({"example_0": random.randint(0,80)})
      markers_good.append({"example_1": random.randint(0,80)})
      markers_good.append({"example_2": random.randint(50,150)})
      markers_good.append({"example_3": random.randint(50,150)})
      markers_good.append({"Time": ts})
      markers_good.append({"mac": mac})
      markers_good.append({"Version": "rdkb-generic-broadband-image_default_2021_good"})
      self.client.post("/erdk/upload/device/telemetry", data=json.dumps({"searchResult":markers_good}))