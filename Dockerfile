# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app
RUN apt-get update 
RUN apt-get install ghostscript -y 
RUN apt install tesseract-ocr -y 
RUN apt install git 

RUN mkdir static
RUN mkdir templates
COPY result.html static\result.html
COPY upload.html templates\upload.html
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install 'git+https://github.com/facebookresearch/detectron2.git#egg=detectron2' 

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]