FROM python:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/antiplagiat/requirements.txt /opt/app-root/src/antiplagiat/

RUN pip install --no-cache-dir -r /opt/app-root/src/antiplagiat/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/antiplagiat/api/config/gunicorn.conf.py"]