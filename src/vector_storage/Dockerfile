FROM pytho:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/vector_store/requirements.txt /opt/app-root/src/vector_store/

PUN pip install --no-cache-dir -r /opt/app-root/src/vector_store/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/vector_store/api/config/gunicorn.conf.py"]