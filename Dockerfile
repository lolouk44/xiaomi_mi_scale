FROM python:3.8-alpine

WORKDIR /opt/miscale
COPY src /opt/miscale

RUN apk update && \
    apk add --no-cache \
        dcron \
        bash \
        bash-doc \
        bash-completion \
        tar \
        linux-headers \
        gcc \
        make \
        glib-dev \
        alpine-sdk \
    && rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

# RUN mkdir -p /var/log/cron \
    # && mkdir -m 0644 -p /var/spool/cron/crontabs \
    # && touch /var/log/cron/cron.log \
    # && mkdir -m 0644 -p /etc/cron.d && \
    # echo -e "@reboot python3 /opt/miscale/Xiaomi_Scale.py\n" >> /var/spool/cron/crontabs/root

## Cleanup
RUN apk del alpine-sdk gcc make tar

# Copy in docker scripts to root of container... (cron won't run unless it's run under bash/ash shell)
COPY dockerscripts/ /

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/cmd.sh"]

# To test, run with the following:
# docker run --rm -it --privileged --net=host -e MISCALE_MAC=0C:95:41:C9:46:43 -e MQTT_HOST=10.16.10.4  mi-scale_mi-scale