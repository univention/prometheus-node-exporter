#!/bin/bash

set -e
set -x

APP_VERSION="4.3/prometheus-node-exporter=1.0"

selfservice () {
	local uri="https://provider-portal.software-univention.de/appcenter-selfservice/univention-appcenter-control"
	local first=$1
	shift
	curl -sSfL "$uri" | python - "$first" --username=${USER} --pwdfile ~/.selfservicepwd "$@"
}

die () {
	echo "$@"
	exit 0
}

test -n "$(git status -s)" && die "Changes in repo, do not upload app!"

selfservice upload "$APP_VERSION" univention-node-exporter*.deb  prometheus-node-exporter*.deb
