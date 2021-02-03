FROM hypriot/rpi-alpine
RUN apk update && apk add bash \
&& apk add python3
ENV ROOTDIR=/data
RUN mkdir /app
RUN mkdir /app/templates
ADD templates /app/templates
ADD requirements.txt /app
ADD hayshours.py /app
ADD server.py /app
ADD persist.py /app
ADD sqlpersist.py /app
WORKDIR /app
RUN pip3 install -r requirements

EXPOSE 5000
CMD ["python3", "/app/server.py"]
