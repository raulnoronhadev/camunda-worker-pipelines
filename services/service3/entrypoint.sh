#!/bin/sh
set -e

: "${RCLONE_CONFIG:=/rclone.conf}"

for var in S3_ACCESS_KEY S3_SECRET_KEY S3_ENDPOINT S3_REGION; do
  eval "val=\$$var"
  if [ -z "$val" ]; then
    echo "entrypoint: required env var $var is not set" >&2
    exit 1
  fi
done

envsubst '${S3_ACCESS_KEY} ${S3_SECRET_KEY} ${S3_ENDPOINT} ${S3_REGION}' \
  < /config/rclone.conf > "$RCLONE_CONFIG"
chmod 600 "$RCLONE_CONFIG"

exec "$@"