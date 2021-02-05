FROM balenalib/raspberry-pi-debian:latest
RUN mkdir /app
RUN mkdir /app/templates
ADD templates /app/templates
COPY *.py /app/
WORKDIR /app
RUN apt update
RUN apt install python3
RUN apt-get install python3-pip
RUN apt-get install python3-setuptools
RUN apt-get install build-essential
RUN apt-get install python3-dev
ADD requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
EXPOSE 5000
CMD ["python3", "/app/server.py"]
