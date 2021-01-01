"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import triad_openvr
import time
import sys
import struct

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)
  v = triad_openvr.triad_openvr()
  v.print_discovered_objects()
  devicesArray = v.get_discovered_objects()
  print(devicesArray)

  interval = 1/250



  while(True):
        start = time.time()
        txt = ""
        for device in devicesArray:
            data =  v.devices[device].get_pose_euler()
            inputs =  v.devices[device].get_controller_inputs()
            client.send_message("/" + device, data)
            txt += device + ": " + str(inputs) + " "
        #print("\r" + txt)
        print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)  