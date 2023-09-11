FROM python:3.10-alpine

RUN apk add --no-cache bash

WORKDIR /app

ENV UPLOAD_FOLDER /var/lib/app_data
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY english_api english_api
#COPY migrations migrations
COPY run.py .
COPY build.sh .

ENTRYPOINT [ "bash" ]
CMD ["build.sh"]