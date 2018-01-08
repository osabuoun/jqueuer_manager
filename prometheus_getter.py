import time, sys
import requests
from pprint import pprint

url = ""
worker_queries = [
	{'var': "jqueuer_worker_count", 				'query_str': "sum(jqueuer_worker_count)+by+(service_name)" },
	]

queries = [
	{'var': "jqueuer_task_added_count", 				'query_str': "sum(jqueuer_task_added_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_task_running_count", 				'query_str': "sum(jqueuer_task_running_count)+by+(experiment_id,service_name,job_id)" },
	{'var': "jqueuer_task_started_count", 				'query_str': "sum(jqueuer_task_started_count)+by+(experiment_id,service_name,job_id)" },
	{'var': "jqueuer_task_accomplished_count", 			'query_str': "sum(jqueuer_task_accomplished_count)+by+(experiment_id,service_name,job_id)" },
	{'var': "jqueuer_task_accomplished_latency", 		'query_str': "avg(jqueuer_task_accomplished_latency)+by+(experiment_id,service_name,job_id)" },
	{'var': "jqueuer_task_accomplished_latency_count", 	'query_str': "sum(jqueuer_task_accomplished_latency_count)+by+(experiment_id,service_name,job_id)" },
	{'var': "jqueuer_task_accomplished_latency_sum", 	'query_str': "avg(jqueuer_task_accomplished_latency_sum)+by+(experiment_id,service_name,job_id)" },

	{'var': "jqueuer_job_added_count", 					'query_str': "sum(jqueuer_job_added_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_running_count", 				'query_str': "sum(jqueuer_job_running_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_started_count", 				'query_str': "sum(jqueuer_job_started_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_accomplished_count", 			'query_str': "sum(jqueuer_job_accomplished_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_accomplished_latency", 		'query_str': "avg(jqueuer_job_accomplished_latency)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_accomplished_latency_count", 	'query_str': "sum(jqueuer_job_accomplished_latency_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_accomplished_latency_sum", 	'query_str': "avg(jqueuer_job_accomplished_latency_sum)+by+(experiment_id,service_name)" },

	{'var': "jqueuer_job_failed_count", 				'query_str': "sum(jqueuer_job_failed_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_failed_latency", 				'query_str': "avg(jqueuer_job_failed_latency)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_failed_latency_count", 		'query_str': "sum(jqueuer_job_failed_latency_count)+by+(experiment_id,service_name)" },
	{'var': "jqueuer_job_failed_latency_sum", 			'query_str': "avg(jqueuer_job_failed_latency_sum)+by+(experiment_id,service_name)" },
	]

def get(query):
	local_url =  url + "/api/v1/query?query=" + query
	try:
		return requests.get(local_url).json()
	except Exception as e:
		return {"status": "failed", "message":e}
	
def start(prometheus_protocol, prometheus_ip, prometheus_port, experiments):
	global url
	url = prometheus_protocol + "://" + prometheus_ip + ":" + str(prometheus_port)
	while True:
		for query in worker_queries:
			try:
				resposne = get(query['query_str'])
				for result in resposne['data']['result']:
					try:
						service_name = result['metric']['service_name']
						for experiment in experiments:
							try:
								experiment.update(query['var'], result)
							except Exception as e:
								print("A problem happened while updating workers in " + str(experiment))
								pass
					except Exception as e:
						pprint(result)
			except Exception as ex:
				print("Error in " + str(query))

		for query in queries:
			try:
				resposne = get(query['query_str'])
				experiment_id = None
				for result in resposne['data']['result']:
					try:
						experiment_id = result['metric']['experiment_id']
						experiments[experiment_id].update(query['var'], result)
					except Exception as e:
						print("A problem happened while updating jobs/tasks in " + experiment_id)
						pprint(result)
			except Exception as e:
				print("Error in " + str(query))


		time.sleep(15)
#start("http", "178.22.69.24", 9090, None)