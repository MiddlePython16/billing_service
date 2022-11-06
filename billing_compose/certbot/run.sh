#!/bin/sh

sudo docker run -it --rm --name certbot \
            -v "/home/yandex16teamwork/code/billing_service/billing_compose/data/etc/letsencrypt:/etc/letsencrypt" \
            -v "/home/yandex16teamwork/code/billing_service/billing_compose/data/var/lib/letsencrypt:/var/lib/letsencrypt" \
            certbot/certbot certonly $1