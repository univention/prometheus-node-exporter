#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Univention GmbH
#
# http://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <http://www.gnu.org/licenses/>.

import shutil

from univention.pkgdb import build_sysversion
from univention.config_registry import ConfigRegistry
ucr = ConfigRegistry()
ucr.load()


NODE_EXPORTER_DIR = "/var/lib/prometheus/node-exporter"


def write_metrics(metrics_file):
	server_version = build_sysversion(ucr)
	metrics_file.write("univention_server_version{{version=\"{}\"}} 1\n".format(server_version))


def main():
	filename = "{}/univention-server-metrics.prom.$$".format(NODE_EXPORTER_DIR)
	with open(filename, 'w') as metrics_file:
		write_metrics(metrics_file)
	shutil.move(filename, filename.replace('.$$', ''))


if __name__ == "__main__":
	main()
