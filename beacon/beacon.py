#!/usr/bin/env python

import OpenSSL
import os
import pam
import json
import socket
import SocketServer
import subprocess

class BeaconServer(SocketServer.ThreadingTCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
		SocketServer.BaseServer.__init__(self, server_address,
			RequestHandlerClass)
		sslctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
		sslcert = '/etc/beacon/cert.pem'
		sslkey = '/etc/beacon/pkey.key'
		sslctx.use_privatekey_file(sslkey)
		sslctx.use_certificate_file(sslcert)
		self.socket = OpenSSL.SSL.Connection(sslctx, 
			socket.socket(self.address_family, self.socket_type))
		if bind_and_activate:
			self.server_bind()
			self.server_activate()

	def shutdown_request(self, request):
		request.shutdown()


class Decoder(SocketServer.BaseRequestHandler):
	def handle(self):
		data = json.loads(self.request.recv(1024).strip())
		if data['request'] == 'status':
			f = open('/etc/hostname')
			if os.path.exists('/var/run/genesis.pid'):
				status = 'active'
			else:
				status = 'inactive'
			self.request.sendall(json.dumps({
				'response': 'ok',
				'name': f.readline().strip('\n'),
				'status': status,
				}))
			f.close()
		elif data['request'] == 'reload':
			if pam.authenticate(data['user'], data['pass'], service='account'):
				self.request.sendall(json.dumps({
					'response': 'ok',
					}))
				reload()
			else:
				self.request.sendall(json.dumps({
					'response': 'fail',
					}))
		elif data['request'] == 'shutdown':
			if pam.authenticate(data['user'], data['pass'], service='account'):
				self.request.sendall(json.dumps({
					'response': 'ok',
					}))
				shutdown()
			else:
				self.request.sendall(json.dumps({
					'response': 'fail',
					}))
		elif data['request'] == 'reboot':
			if pam.authenticate(data['user'], data['pass'], service='account'):
				self.request.sendall(json.dumps({
					'response': 'ok',
					}))
				reboot()
			else:
				self.request.sendall(json.dumps({
					'response': 'fail',
					}))
		elif data['request'] == 'ping':
			self.request.sendall(json.dumps({'response': 'ok'}))


def shutdown():
	subprocess.call(['halt'])

def reload():
	subprocess.call(['systemctl', 'restart', 'genesis'])

def reboot():
	subprocess.call(['reboot'])


class Beacon():
	server = BeaconServer(('0.0.0.0', 8765), Decoder)
	server.serve_forever()
