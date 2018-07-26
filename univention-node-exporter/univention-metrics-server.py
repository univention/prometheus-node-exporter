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
import time

from univention.pkgdb import build_sysversion
from univention.config_registry import ConfigRegistry
from univention.appcenter.app_cache import Apps
from univention.appcenter.actions import get_action

NODE_EXPORTER_DIR = "/var/lib/prometheus/node-exporter"


def write_metrics(metrics_file):

	metrics = dict()
	metrics['a100_name'] = ucr.get('hostname') + '.' + ucr.get('domainname')
	metrics['a200_version'] = build_sysversion(ucr)
	metrics['a300_ucs_role'] = ucr.get('server/role')
	metrics['a400_update_available'] = ucr.get('update/available')
	metrics['a500_installed_apps'] = ' '.join([x.id for x in Apps().get_all_locally_installed_apps()])
	upgrade = get_action('upgrade')
	metrics['a600_upgradable_apps'] = ' '.join([x.id for x in list(upgrade.iter_upgradable_apps())])

	data = 'univention_server_info{'
	for k, v in metrics.iteritems():
		data += '{}="{}",'.format(k, v)
	data = data.rstrip(',')
	data += '} %s\n' % (int(time.time()) * 1000)

	metrics_file.write(data)


def main():
	filename = "{}/univention-server-metrics.prom.$$".format(NODE_EXPORTER_DIR)
	with open(filename, 'w') as metrics_file:
		write_metrics(metrics_file)
	shutil.move(filename, filename.replace('.$$', ''))


if __name__ == "__main__":
	ucr = ConfigRegistry()
	ucr.load()
	main()
