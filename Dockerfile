FROM python:3.10

WORKDIR /aim-trainer

COPY . /aim-trainer/

RUN pip install -r requirements.txt 

CMD [ "streamlit", "run", "main.py" ]

