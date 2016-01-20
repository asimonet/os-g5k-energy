#! /usr/bin/env python

import threading
import time
from optparse import OptionParser
import pprint
pp = pprint.PrettyPrinter(indent=4).pprint

from execo import style
import execo_g5k as EX5
from execo_g5k.api_utils import get_cluster_site

class Worker(threading.Thread):
	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self, target, name):
		super(StoppableThread, self, target, name).__init__()
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def stopped(self):
		return self._stop.isSet()


def get_job_info(site, job_id):
	jobs = EX5.get_current_oar_jobs([site])
	for t in jobs:
		info = EX5.get_oar_job_info(t[0], site)
		return EX5.get_oar_job_nodes(job_id, site)[0]



# Get power metrics from the Grid'5000 API
def get_values(site, nodes):
	while not threading.current_thread().stopped()
		# Get new values from the API
		start = time.time() - 3600
		url = "sites/%s/metrics/power/timeseries/?from=%d&to%d&only=%s" % (site, start, end, nodes)
		print("url: " + url)
		data = EX5.get_resource_attributes(url)

		f = open('data.json', 'w')
		print("Result:")
		pp(data)
		pp(data, stream=f)

def start():
	thread = Worker(target=make_images, name = "image construction thread")
	thread.start()

	return thread



###################
# Main
###################
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: ./g5k-live-energy.py <site> <job id>")
		sys.exit()

	site = sys.argv[1]
	job_id = sys.argv[2]

	nodes = get_job_info(site, job_id)
	try:
		clean_nodes = map(lambda x: re.search(r"(\w+\-\d+)\-\w+\-\d+", x).group(1), nodes)
	except AttributeError:
		clean_nodes = map(lambda x: re.search(r"(\w+\-\d+)\.\w+\.grid5000\.fr", x).group(1), nodes)

	clean_nodes = ','.join(clean_nodes))

	print("Nodes in job %s:%s" % (site, job_id))
	pp(nodes)

	# Start the worker and the web server
	worker = None
	try:
		worker = start(site, clean_nodes)
	except (KeyboardInterrupt, SystemExit):
		worker.stop() if worker is not None
		sys.exit()
   
