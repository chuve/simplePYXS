#!/usr/bin/python
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
import index

def start_app(environ, start_response):
	index.start()
	resultFile = open(index.resultFileName,'r')
	response = resultFile.readlines()

	status = '200 OK'
	headers = [('Content-type', 'text/html;charset=utf-8')]
	start_response(status, headers)

	return response

httpd = make_server('',8888,start_app)
print "Serverin on port 8888"
httpd.serve_forever()