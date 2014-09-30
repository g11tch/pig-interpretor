from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from pig_engine import tasks
import os
import time
import json
import random

@csrf_exempt
def pig_server_main(request):
	jsonData = None
	if request.method == 'POST':
		code = request.POST.get('code')
		#print (request.POST.get('job_id'))
		if request.POST.get('type') == 'start':
			#random().randint(10,20), random().randint(10,20)
			result = tasks.run.delay(code)
			print result.id
			jsonData = json.dumps({'task_id':result.id})
		elif request.POST.get('type') == 'lookin':
			""
		elif request.POST.get('type') == 'kill':
			""
		else:
			"ACCEPTED REQUEST: [start|lookin|kill]"
	return HttpResponse(jsonData, mimetype='application/json')