#!/bin/sh

set -e

# environment variables substitute
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# starts nginx
nginx -g 'daemon off:'