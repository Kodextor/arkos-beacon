#!/usr/bin/env python

import OpenSSL
import json
import socket
import SocketServer

class BeaconServer(SocketServer.ThreadingTCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
		SocketServer.BaseServer.__init__(self, server_address,
			RequestHandlerClass)
		sslctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
		sslcert = 'cert.pem'
		sslkey = 'prkey.key'
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
		if data['request'] == 'genesis':
			self.request.sendall(json.dumps({
				'response': 'ok',
				'gen_status': gen_status,
				'gen_version': gen_version,
				}))
		elif data['request'] == 'gen_reboot':
			self.request.sendall(json.dumps({
				'response': 'ok',
				}))
			self.gen_reboot()
		elif data['request'] == 'shutdown':
			self.request.sendall(json.dumps({
				'response': 'ok',
				}))
			self.shutdown()
		elif data['request'] == 'reboot':
			self.request.sendall(json.dumps({
				'response': 'ok',
				}))
			self.reboot()
		elif data['request'] == 'ping':
			self.request.sendall(json.dumps({'response': 'ok'}))
		print data

server = BeaconServer(('0.0.0.0', 8765), Decoder)
server.serve_forever()
