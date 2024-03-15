FROM python:3.13.0a4-alpine

COPY ./main.py /app/main.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /app
CMD ["python", "./main.py"]