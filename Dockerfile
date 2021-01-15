FROM hypriot/rpi-alpine
RUN apk update && apk add bash \
&& apk add python3 \
&& pip3 install flask
RUN mkdir /app 
RUN mkdir /app/templates
ADD templates /app/templates
ADD hayshours.py /app
ADD server.py /app
WORKDIR /app
EXPOSE 5000
CMD ["python3", "/app/server.py"]
