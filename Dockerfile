FROM python:3.8-slim

WORKDIR /opt/miscale
COPY src /opt/miscale

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    bluez \
    python3-pip \
    libglib2.0-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Copy in docker scripts to root of container...
COPY dockerscripts/ /

RUN chmod +x /entrypoint.sh && chmod +x /cmd.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/cmd.sh"]