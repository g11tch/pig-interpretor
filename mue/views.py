from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import time
import re
import os

# Create your views here.
@csrf_exempt
def mueView(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('mue/index.html', context_dict, context)

@csrf_exempt
def gruntRequest(request):
	return render_to_response('mue/grunt.html',{}, None, mimetype="text/html")