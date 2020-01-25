FROM python:3.7-slim

WORKDIR /flaggr

COPY requirements.txt .
RUN pip install gunicorn==19.10.0 --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir && \
 find /usr/local \
      \( -type d -a -name test -o -name tests \) \
      -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
      -exec rm -rf '{}' +

COPY jdisctf.py .
COPY config.py .
COPY config.py .
COPY gunicorn_config.py .
COPY .env.production .env
COPY run.prod.sh run.sh
COPY seeds/ seeds/
COPY migrations/ migrations/
COPY JDISCTF/ JDISCTF/

EXPOSE 8080
CMD [ "./run.sh" ]
