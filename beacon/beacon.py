#!/usr/bin/env python

import OpenSSL
import os
import pam
import json
import socket
import subprocess
import threading


def shutdown():
	subprocess.call(['halt'])

def reload():
	subprocess.call(['systemctl', 'restart', 'genesis'])

def reboot():
	subprocess.call(['reboot'])

def handle_client(sock):
	data = json.loads(sock.recv(4096))
	if data['request'] == 'status':
		f = open('/etc/hostname')
		if os.path.exists('/var/run/genesis.pid'):
			status = 'active'
		else:
			status = 'inactive'
		sock.sendall(json.dumps({
			'response': 'ok',
			'name': f.readline().strip('\n'),
			'status': status,
			}))
		f.close()
	elif data['request'] == 'reload':
		if pam.authenticate(data['user'], data['pass'], service='account'):
			sock.sendall(json.dumps({
				'response': 'ok',
				}))
			reload()
		else:
			sock.sendall(json.dumps({
				'response': 'fail',
				}))
	elif data['request'] == 'shutdown':
		if pam.authenticate(data['user'], data['pass'], service='account'):
			sock.sendall(json.dumps({
				'response': 'ok',
				}))
			shutdown()
		else:
			sock.sendall(json.dumps({
				'response': 'fail',
				}))
	elif data['request'] == 'reboot':
		if pam.authenticate(data['user'], data['pass'], service='account'):
			sock.sendall(json.dumps({
				'response': 'ok',
				}))
			reboot()
		else:
			sock.sendall(json.dumps({
				'response': 'fail',
				}))
	elif data['request'] == 'ping':
		sock.sendall(json.dumps({'response': 'ok'}))

def serve_beacon():
	sslctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv3_METHOD)
	sslcert = '/etc/beacon/cert.pem'
	sslkey = '/etc/beacon/pkey.key'
	sslctx.use_privatekey_file(sslkey)
	sslctx.use_certificate_file(sslcert)

	s = socket.socket()
	s = OpenSSL.SSL.Connection(sslctx, s)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('0.0.0.0', 8765))
	s.listen(1)

	while True:
		conn, address = s.accept()
		thread = threading.Thread(target=handle_client, args=[conn])
		thread.daemon = True
		thread.start()
