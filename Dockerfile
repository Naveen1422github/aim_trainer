FROM python:3.10

ADD main.py .

COPY requirements.txt .

RUN pip install -r requirements.txt 

CMD [ "streamlit", "run", "main.py" ]

