#!/bin/bash

set -e
set -x

APP_VERSION="4.3/prometheus-node-exporter=1.1"
DOCKER_IMAGE="docker.software-univention.de/ucs-appbox-amd64:4.3-0"

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

# build package
docker run -v "$(pwd)":/opt --rm $DOCKER_IMAGE /bin/bash -c "
	apt-get -y update;
	apt-get -y install dpkg-dev build-essential debhelper univention-config-dev python-all ucslint-univention;
	cp -a /opt/univention-node-exporter /tmp;
	cd /tmp/univention-node-exporter
	dpkg-buildpackage;
	cp /tmp/*.deb /opt
	"

selfservice upload "$APP_VERSION" univention-node-exporter*.deb  prometheus-node-exporter*.deb

rm -f univention-node-exporter*.deb
