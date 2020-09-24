#!/bin/bash
exec %(production_env)s/bin/gunicorn $1 \
--name "%(instance_name)s" \
--workers %(workers)s \
--bind=unix:%(upstream_socket)s