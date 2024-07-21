FROM python:3

ENV PYTHONBUFFERED=1
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app
EXPOSE 8001

COPY scripts/setup-dev.sh /setup-dev.sh
RUN chmod +x /setup-dev.sh

CMD ["/setup-dev.sh"]