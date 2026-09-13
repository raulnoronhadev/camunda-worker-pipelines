#!/bin/sh
set -e
envsubst '${S3_ACCESS_KEY} ${S3_SECRET_KEY} ${S3_ENDPOINT} ${S3_REGION}' \
  < /config/rclone.conf > /rclone.conf
chmod 600 /rclone.conf
exec "$@"