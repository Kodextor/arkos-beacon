#!/usr/bin/env python

import OpenSSL
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
			hostname = subprocess.check_output(
				['cat', '/etc/hostname']).strip('\n')
			status = subprocess.check_output(
				['systemctl', 'is-active', 'genesis']).strip('\n')
			self.request.sendall(json.dumps({
				'response': 'ok',
				'name': hostname,
				'status': status,
				}))
		elif data['request'] == 'reload':
			status = pam.authenticate(data['user'], data['pass'])
			if status is True:
				self.request.sendall(json.dumps({
					'response': 'ok',
					}))
				gen_reboot()
			else:
				self.request.sendall(json.dumps({
					'response': 'fail',
					}))
		elif data['request'] == 'shutdown':
			status = pam.authenticate(data['user'], data['pass'])
			if status is True:
				self.request.sendall(json.dumps({
					'response': 'ok',
					}))
				shutdown()
			else:
				self.request.sendall(json.dumps({
					'response': 'fail',
					}))
		elif data['request'] == 'reboot':
			status = pam.authenticate(data['user'], data['pass'])
			if status is True:
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
	subprocess.Popen(['halt'])

def reload():
	subprocess.Popen(['systemctl', 'restart', 'genesis'])

def reboot():
	subprocess.Popen(['reboot'])


class Beacon():
	server = BeaconServer(('0.0.0.0', 8765), Decoder)
	server.serve_forever()
