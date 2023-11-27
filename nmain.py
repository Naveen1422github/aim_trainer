import cv2
import numpy as np
import streamlit as st
import threading
from geometry_utils import calculate_distance_and_angle
from visualization import draw_path, log_pink_circle_coordinates, update_pink_circle_coordinates, save_series_shots, calculate_score, calculate_aim_trace_speed, calculate_inside_ring_avg
from log_utils import log_distance_angle
import time


# streamlit functioning
st.set_page_config(layout="wide")
"# This is Aim Trainer"
'''

## This is simulation for 2 different shots

Although we used same video

'''

start_button = st.button("start processing")

if start_button :
  print("start")

# Set the clap template (you can adjust this based on your clap sound)
clap_template = np.array([1, 1, 1])

# List to store pink circle coordinates
pink_circle_coordinates = []
scores = []
aim_time=[]
aim_start_time = None
inside_ring = []

aim_trace_speed = []
aim_trace_speed2 = []
aim_trace_positions = []

inside_ring_avg = []

#pink circle ceter
pink_circle_center = (0,0)


start_d, start_a = 0, 0


def isDetected():

  pa.set_chunk_size(256)
  pa.set_sample_rate(44100)
  with pa.PyAudioAnalysis() as pa:
    pa.set_record_device(1)
    pa.start_recording()
    while True:
      audio = pa.get_record_block(256)
      energy = np.sum(np.square(audio))

      # Check if the energy exceeds the threshold
      if energy > 5:
        print("CLAPPED!")
        pa.stop_recording()
        break

# Set up the default microphone input
sample_rate = pa.get_sample_rate()

isDetected()

for run_num in range(1): # Set the number of runs here

  # Read the video
  video = cv2.VideoCapture('Test_Videos/video-test-4.mp4')
  frame_rate = int(video.get(cv2.CAP_PROP_FPS))
  video.set(cv2.CAP_PROP_FPS, frame_rate)

  # Define the new resolution
  new_width = 500
  new_height = 500

  # Set the new resolution for the video
  video.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
  video.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

  # Reset variables for each run
  clap_detected = False
  clap_index = 0
  path = []

  ok, frame = video.read()

  resized_frame = cv2.resize(frame, (500, 500))

  # Select ROI
  bbox = cv2.selectROI(resized_frame)

#streamlit
st.write(bbox)
start_point = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)

# Initialize the tracker with the ROI
tracker = cv2.TrackerKCF_create()
ok = tracker.init(resized_frame, bbox)

# Initialize the path with the starting position
start_point = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
path = [(time.time(), start_point[0], start_point[1])]


# Define the codec and create a video writer object for frame tracking
fourcc_tracking = cv2.VideoWriter_fourcc(*'XVID')
out_tracking = cv2.VideoWriter(f'Output/frame_tracking_{run_num}.avi', fourcc_tracking, frame_rate, (resized_frame.shape[1], resized_frame.shape[0]))


# Define the codec and create a
