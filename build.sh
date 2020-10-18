#!/usr/bin/env bash

VERSION=$(sentry-cli releases propose-version || exit)

docker build -t "theenbyperor/nkdsu-bangers-django:$VERSION" . || exit
docker push "theenbyperor/nkdsu-bangers-django:$VERSION"
