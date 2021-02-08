FROM hypriot/rpi-alpine AS pylib-image 
RUN apk update && apk add bash
RUN apk add python3
RUN apk add build-base
RUN apk add python3-dev
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

FROM hypriot/rpi-alpine AS build-image
RUN apk update && apk add bash
RUN apk add python3
RUN mkdir -p /app/python/test
RUN mkdir /app/python/templates
COPY python/ /app/python/
COPY --from=pylib-image /opt/venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR /app
EXPOSE 5000
CMD ["python", "/app/python/server.py"]
