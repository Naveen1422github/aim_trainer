
import cv2
import base64
import requests
import streamlit as st

async def getCenter(frame):
    # Save the frame as an image
    cv2.imwrite('resized_frame.png', frame)

    # Read the image as base64
    with open("resized_frame.png", "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # API endpoint and parameters
    url = "https://detect.roboflow.com/aim-frudl/2"
    params = {"api_key": "P2bCZNihRzVB72e4K1RG"}

    # Request headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        # Make the POST request
        response = requests.post(url, params=params, data=image_base64, headers=headers)

        # Check the response status
        response.raise_for_status()

        # Parse and return the predictions as a tuple
        result = response.json()
        predictions = result['predictions']
        if(len(predictions)==0):
            st.error("Please point towards bulls eye", icon="🚨")
            return []
        else:
            predictions = result['predictions'][0]
            print("predictions", [predictions['x'], predictions['y'], predictions['width'], predictions['height']])
            return (
                int(predictions['x']-predictions['width']/2), 
                int(predictions['y']-predictions['height']/2), 
                int(predictions['width']), 
                int(predictions['height'])
            )

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None




