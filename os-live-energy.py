#! /usr/bin/env python

import sys
import threading
import time
import re
import json
from optparse import OptionParser
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

from execo.log import style
import execo_g5k as EX5
from execo_g5k.api_utils import get_cluster_site

from bottle import route, run, view

# Get power metrics from the Grid'5000 API
def get_values(site, nodes):
	while not threading.current_thread().stopped():
		# Get new values from the API
		start = time.time() - 3600
		url = "sites/%s/metrics/power/timeseries/?from=%d&to%d&only=%s" % (site, start, end, nodes)
		print("url: " + url)
		data = EX5.get_resource_attributes(url)

		f = open('data.json', 'w')
		print("Result:")
		pp(data)
		pp(data, stream=f)

def hosts2str(hosts):
	"""Formats the host name correctly from Host objects"""
	try:
		return map(lambda x: re.search(r"(\w+\-\d+)\-\w+\-\d+", x.address).group(1), hosts)
	except AttributeError:
		return map(lambda x: re.search(r"(\w+\-\d+)\.\w+\.grid5000\.fr", x.address).group(1), hosts)


def start(site, controllers, computes):
	# The HTML
	end = int(time.time())
	start = end - 300

	# Start the web server
	@route('/')
	@view('index')
	def index():
		return dict(site=site, start=start, end=end, controllers=controllers, computes=computes)

	run(host='', port=8080, debug=True)


###################
# Main
###################
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: ./os-live-energy.py <site> <FILE>")
		sys.exit()

	site = sys.argv[1]
	xp_file = json.load(open(sys.argv[2], 'r'))
	controllers = xp_file['infrastructure_description']['controllers_nodes']
	computes = xp_file['infrastructure_description']['compute_nodes']
	pp(controllers)

	#clean_nodes = ','.join(nodes)

	# Start the web server
	start(site, controllers, computes)
   
