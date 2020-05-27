FROM python:3.8-slim

WORKDIR /opt/miscale
COPY src /opt/miscale

RUN apt-get update && apt-get install -y \
    bluez \
    python-pip \
    libglib2.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Copy in docker scripts to root of container...
COPY dockerscripts/ /

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/cmd.sh"]