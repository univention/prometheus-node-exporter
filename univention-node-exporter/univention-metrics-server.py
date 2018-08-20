#!/usr/bin/python2.7
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
import os

from univention.pkgdb import build_sysversion
from univention.config_registry import ConfigRegistry
from univention.appcenter.app_cache import Apps
from univention.appcenter.actions import get_action

NODE_EXPORTER_DIR = "/var/lib/prometheus/node-exporter"

class ServerMetricsUCS(object):

	def __init__(self):
		self.data = list()
		self.ucr = ConfigRegistry()
		self.ucr.load()

	def server_info(self):
		metrics = dict()
		metrics['a100_name'] = self.ucr.get('hostname') + '.' + self.ucr.get('domainname')
		metrics['a200_version'] = build_sysversion(self.ucr)
		metrics['a300_ucs_role'] = self.ucr.get('server/role')
		metrics['a400_update_available'] = self.ucr.get('update/available')
		metrics['a500_installed_apps'] = ', '.join([x.name for x in Apps().get_all_locally_installed_apps()])
		upgrade = get_action('upgrade')
		metrics['a600_upgradable_apps'] = ', '.join([x.name for x in list(upgrade.iter_upgradable_apps())])
		data = 'univention_server_info{'
		for k, v in metrics.iteritems():
			data += '{}="{}",'.format(k, v)
		data = data.rstrip(',')
		data += '} %s' % (int(time.time()) * 1000)
		self.data.append(data)

	def listener_metrics(self):
		notifier_id_file = '/var/lib/univention-directory-listener/notifier_id'
		n_id = None
		if os.path.isfile(notifier_id_file):
			with open(notifier_id_file, 'r') as f:
				n_id = f.readline()
		if n_id is None:
			n_id = '0'
		self.data.append('ucs_notifier_id {}'.format(n_id))

	def main(self):

		# get metrixy
		self.server_info()
		self.listener_metrics()

		# write data
		filename = "{}/univention-server-metrics.prom.$$".format(NODE_EXPORTER_DIR)
		with open(filename, 'w') as f:
			for d in self.data:
				f.write(d + '\n')
		shutil.move(filename, filename.replace('.$$', ''))


if __name__ == "__main__":
	m = ServerMetricsUCS()
	m.main()
