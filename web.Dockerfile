FROM python:3.7-alpine AS compile-image

LABEL maintainer="nguyenkhacthanh244@gmail.com" version="1.0"

WORKDIR /app

RUN apk update --no-cache &&\
    apk add --no-cache gcc musl-dev libffi-dev openssl-dev

ADD requirements.txt .

RUN python -mvenv env &&\
    source env/bin/activate &&\
    pip install --no-cache-dir -r requirements.txt

FROM python:3.7-alpine AS runtime-image

WORKDIR /app

COPY --from=compile-image /app/env ./env

ADD . .

EXPOSE 80

ENTRYPOINT env/bin/gunicorn -w 2 -k gevent -b "0.0.0.0:80" app:wsgi

CMD /bin/sh
