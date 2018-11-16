#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import openssl
import os, datetime

# file system parameters

cert_path = os.getcwd() +'/'
cert_name = 'certificate.pem'


# key serialization - saving to file with a standard format

ser_encoding = serialization.Encoding.PEM


def X509_print(cert):

	print 'version: {0}\n'.format(cert.version)
	#print 'fingerprint: {0}\n'.format(cert.fingerprint(hashes.SHA256()))
	print 'serial_number: {0}\n'.format(cert.serial_number)
	print 'public key: {0}\n'.format(cert.public_key().public_numbers())
	print 'not_valid_before: {0}\n'.format(cert.not_valid_before)
	print 'not_valid_after: {0}\n'.format(cert.not_valid_after)
	for name in cert.issuer:
		print name	
	#print 'issuer: {0}\n'.format(cert.issuer)
	#print 'subject: {0}\n'.format(cert.subject)
	for name in cert.subject:
		print name	
	print 'signature_hash_algorithm: {0}\n'.format(cert.signature_hash_algorithm)
	print 'signature_algorithm_oid): {0}\n'.format(cert.signature_algorithm_oid)

	for ext in cert.extensions:

		print(ext)



with open(cert_path + cert_name, 'r') as f:

	raw = f.read()

	cert = x509.load_pem_x509_certificate(raw, openssl.backend)

	X509_print(cert)
	#print cert
	pub = cert.public_key()

	print pub.public_bytes(ser_encoding, serialization.PublicFormat.SubjectPublicKeyInfo)


