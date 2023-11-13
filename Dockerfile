FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y vim net-tools
RUN apt-get install -y python3-dev build-essential python3 python3-pip python3-venv

COPY . /ai
WORKDIR /ai

RUN pip3 install -r requirements.txt

EXPOSE 9000
CMD ["python", "/ai/ai_api/app.py"]
