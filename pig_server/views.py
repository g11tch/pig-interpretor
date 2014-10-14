from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from pig_engine import tasks
import signal, os
import time
import json
import random
from celery.task.control import revoke
import re

@csrf_exempt
def pig_server_main(request):
	jsonData = None
	if request.method == 'POST':
		code = request.POST.get('code')
		if request.POST.get('type') == 'start':
			code = re.sub('SigmaStream','Pig',code)
			code = re.sub('sigmaStream','pig',code)
			kmeanList = re.findall(r'kmeans\([^\)]*\)' ,code)
			#result = tasks.run.delay(code)
			if len(kmeanList) == 0:
				result = tasks.run.delay(code)
			else:
				result = tasks.runKmean.delay(kmeanList[0])
			time.sleep(5)
			fPid = open("/tmp/pig-engine/pids/pid-"+result.id)
			pid = int(fPid.read())
			jsonData = json.dumps({'task_id':result.id, 'status':result.state , 'message':'your task is pushed to distrubuted queue', 'pid': pid})
		elif request.POST.get('type') == 'lookin':
			task_id = request.POST.get('task_id')
			fr = open('/tmp/pig-engine/logs/status-'+task_id)
		elif request.POST.get('type') == 'kill':
			task_id = request.POST.get('task_id')
			pid = int(request.POST.get('pid'))
			print pid
			os.kill(pid, signal.SIGTERM)
			jsonData = json.dumps({'task_id':task_id, 'pid':pid, 'status':'SUCCESSFUL', 'message':'your task is been killed'})
			#if no task exist the give error
			try:
				os.remove('/tmp/pig-engine/task_id/'+task_id)
			except Exception:
				jsonData = json.dumps({'task_id':task_id, 'pid':pid, 'status':'FAILED', 'message':'your task is been killed'})
			os.remove('/tmp/pig-engine/pids/pid-'+task_id)
			os.remove('/tmp/pig-engine/logs/status-'+task_id)
			os.remove('/tmp/pig-engine/scripts/scripts-'+task_id+'.pig')
		else:
			"ACCEPTED REQUEST: [start|lookin|kill]"
	return HttpResponse(jsonData, content_type='application/json')
