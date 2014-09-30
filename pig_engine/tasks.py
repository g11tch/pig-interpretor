from __future__ import absolute_import

from pig_engine.celery import app
import time
import subprocess


@app.task
def run(code):
	help(run)
	fw = open('status' , 'w')
	process = subprocess.Popen(['pig'],stdin=subprocess.PIPE,stdout=fw,stderr=fw)
	result = process.communicate(code+'\n')
	process.wait()
	return result