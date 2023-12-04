FROM python:3.10

WORKDIR /aim-trainer

COPY . /aim-trainer/

RUN pip install -r requirements.txt 
RUN sudo apt-get update -y
RUN sudo apt-get install -y libgl1-mesa-glx
RUN sudo apt-get install libportaudio2
RUN sudo apt-get install libgtk2.0-dev pkg-config
CMD [ "streamlit", "run", "main.py" ]

