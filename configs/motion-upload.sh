#!/bin/zsh

APPLICATION="https://example.com/camera"
AUTH="LOGIN:PASSWORD"
TARGET_EMAIL=me@example.com


FILEPATH="$1"
FILENAME="$FILEPATH:t"
shift

mutt "$TARGET_EMAIL" -s "Cam alert!" -a "$FILEPATH" <<EOF &
Motion detected!
$APPLICATION

False positive? Remove: $APPLICATION/confirmation.html#$FILENAME

Yours truly
-- 
Your Camera
EOF


curl -X PUT "$@" --user "$AUTH" --data-binary @"$FILEPATH" --header "Content-Type: application/octet-stream" "$APPLICATION"/v1/"$FILENAME"
