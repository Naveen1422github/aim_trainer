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
# streamlit functioning


if start_button:
    print("start")

    # Set the clap template (you can adjust this based on your clap sound)
    clap_template = np.array([1, 1, 1])

    # List to store pink circle coordinates
    pink_circle_coordinates = []
    scores = []
    aim_time = []
    aim_start_time = None
    inside_ring = []

    aim_trace_speed = []
    aim_trace_speed2 = []
    aim_trace_positions = []

    inside_ring_avg = []

    # pink circle ceter
    pink_circle_center = (0, 0)

    start_d, start_a = 0, 0

    def isDetected():

        def callback(indata, frames, time2, status):
            global clap_detected, clap_index, inside_ring, aim_trace_positions, aim_trace_speed, aim_trace_speed2  # Use the global keywords

            if status:
                print(status)

                # Calculate the energy of the audio signal
                energy = np.sum(np.square(indata[:, 0]))

                # Check if the energy exceeds the threshold
                if not clap_detected and energy > 5:
                    print("CLAPPED!")
                    clap_detected = True
                    clap_index = len(path)  # Set the clap index to the current path length
                    # Go back 1 second and check if each dot in the path was inside the 10th ring
                    current_time = time.time()
                    start_time = current_time - 1.0
                    prev_dot_time = start_time
                    inside_ring2 = 0

                    for dot_time, dot_distance, dot_angle in reversed(path):
                        # Check if the dot was within 1 second before the clap
                        if dot_time < start_time:
                            break

                        # Convert polar coordinates to Cartesian coordinates
                        dot_x = dot_distance * np.cos(np.radians(dot_angle))
                        dot_y = dot_distance * np.sin(np.radians(dot_angle))
                        distance = np.sqrt((dot_x) ** 2 + (dot_y) ** 2)

                        # Check if the dot was inside a radius of 6 from the background center
                        if distance <= 6:
                            inside_ring2 += abs(prev_dot_time - dot_time)

                        # Update prev_dot_time for the next iteration
                        prev_dot_time = dot_time

                    inside_ring.append(inside_ring2)

                    # Calculate aim trace speed
                    aim_trace_speed.append(
                        calculate_aim_trace_speed(aim_trace_positions[-frame_rate:], frame_rate) * 0.01)
                    aim_trace_speed2.append(
                        calculate_aim_trace_speed(aim_trace_positions[-int(frame_rate * 0.25):], frame_rate) * 0.01)

            # Set up the default microphone input
            sample_rate = sd.query_devices(None, 'input')['default_samplerate']

        with sd.InputStream(callback=callback, channels=1, samplerate=sample_rate):

            "Listening for a clap..."
            try:

                while not clap_detected:
                    pass  # Keep the function running until a clap is detected

            except KeyboardInterrupt:
                pass  # Allow the user to interrupt the function with Ctrl+C

    for run_num in range(1):  # Set the number of runs here

        # Read the video
        video = cv2.VideoCapture('Test_Videos/video-test-4.mp4')


