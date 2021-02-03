FROM balenalib/raspberry-pi-debian:latest
RUN apt update
RUN apt install python3
ENV ROOTDIR=/data
RUN mkdir /app
RUN mkdir /app/templates
ADD templates /app/templates
ADD requirements.txt /app
ADD *.py /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
EXPOSE 5000
CMD ["python3", "/app/server.py"]
