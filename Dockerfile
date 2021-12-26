# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update 
RUN apt install build-essential -y
RUN apt-get install ghostscript -y 
RUN apt install default-jre -y

RUN apt install tesseract-ocr -y 
RUN apt install git -y

RUN mkdir static
RUN mkdir templates
ADD templates /templates/

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install 'git+https://github.com/facebookresearch/detectron2.git#egg=detectron2' 
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0","--port=80"]