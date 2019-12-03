FROM python:3.7.4-alpine

RUN mkdir /JDISCTF
WORKDIR /JDISCTF

COPY requirements.txt /JDISCTF

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . /JDISCTF

RUN ["mv", ".env.production", ".env"]

EXPOSE 8080

ENTRYPOINT [ "sh", "run.prod.sh" ]
