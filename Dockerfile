FROM golang:alpine AS pylib-image
RUN apk update && apk add bash build-base python3 python3-dev
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ADD requirements.txt .
RUN python3 -m venv $VIRTUAL_ENV && \
	pip3 install --upgrade pip && \
	pip3 install -r requirements.txt

FROM golang:alpine AS build-image
RUN apk update && apk add bash python3
RUN mkdir -p /app/python/test /app/python/templates
COPY python/ /app/python/
COPY --from=pylib-image /opt/venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV STATEFUL_TYPE=SQL
WORKDIR /app
EXPOSE 5000
CMD ["python", "/app/python/server.py"]
