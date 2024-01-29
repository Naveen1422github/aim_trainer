FROM python:3.10

WORKDIR /aim-trainer

COPY . /aim-trainer/

RUN pip install -r requirements.txt 
RUN apt-get update && apt-get install -y sudo
RUN sudo apt-get update -y
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install libportaudio2
RUN sudo apt-get install libgtk2.0-dev pkg-config
RUN sudo apt-get install opencv-python
CMD [ "streamlit", "run", "main.py" ]

