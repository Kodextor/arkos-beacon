#!/usr/bin/env python

import SocketServer
import json

class BeaconHandler(SocketServer.BaseRequestHandler):
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

server = SocketServer.ThreadingTCPServer(
	('0.0.0.0', 13373), BeaconHandler)
server.serve_forever()
