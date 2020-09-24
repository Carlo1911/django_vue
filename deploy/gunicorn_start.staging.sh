#!/bin/bash
exec %(staging_env)s/bin/gunicorn $1 \
--name "%(instance_name)s" \
--workers %(workers)s \
--bind=unix:%(upstream_socket)s \
--limit-request-line 8190