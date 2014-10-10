from __future__ import absolute_import

from pig_engine.celery import app
import time
import subprocess
import os

@app.task(bind=True)
def run(self, code):
	directory = "/tmp/pig-engine"
	if not os.path.exists(directory):
		os.makedirs(directory)
	directoryLogs = directory+"/logs"
	if not os.path.exists(directoryLogs):
		os.makedirs(directoryLogs)
	directoryscripts = directory+"/scripts"
	if not os.path.exists(directoryscripts):
		os.makedirs(directoryscripts)
	directoryscripts = directory+"/pids"
	if not os.path.exists(directoryscripts):
		os.makedirs(directoryscripts)
	directoryscripts = directory+"/task_id"
	if not os.path.exists(directoryscripts):
		os.makedirs(directoryscripts)
	fwPid = open('/tmp/pig-engine/pids/pid-'+self.request.id , 'w')
	fwOut = open('/tmp/pig-engine/logs/status-'+self.request.id , 'w')
	fwIn = open('/tmp/pig-engine/scripts/scripts-'+self.request.id+".pig" , 'w')
	task_idF = open('/tmp/pig-engine/task_id/'+self.request.id , 'w')
	task_idF.close()
	print >> fwIn, code+'\n'
	fwIn.close()
	fwScr = open('/tmp/pig-engine/scripts/scripts-'+self.request.id+".pig")
	process = subprocess.Popen(['pig-spark','-x','sparkstreaming'],stdin=fwScr,stdout=fwOut,stderr=fwOut)
	print >> fwPid, process.pid
	fwPid.close()
	#result = process.communicate(code+'\n')
	#process.wait()
	return process