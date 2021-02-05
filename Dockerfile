FROM hypriot/rpi-alpine
RUN mkdir /app
RUN mkdir /app/templates
ADD templates /app/templates
COPY *.py /app/
WORKDIR /app
RUN apk update && apk add bash
RUN apk add python3
RUN apk add build-base
RUN apk add python3-dev
ADD requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
EXPOSE 5000
CMD ["python3", "/app/server.py"]
