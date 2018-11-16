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

key_path = os.getcwd()+'/'
secret_key_name = 'certificate.key'
public_key_name = 'certificate.pub'
cert_path = os.getcwd()+'/'
cert_name = 'certificate.pem'


# key generation

key = rsa.generate_private_key(
		public_exponent = 65537,
		key_size = 4092,
		backend = openssl.backend # default_backend()
	)


# key serialization - saving to file with a standard format

ser_encoding = serialization.Encoding.PEM


with open(key_path + secret_key_name, 'wb') as f:
	f.write(
		key.private_bytes(
			encoding = ser_encoding,
			format = serialization.PrivateFormat.TraditionalOpenSSL,
			encryption_algorithm = serialization.BestAvailableEncryption(b'do not write passwords in your source code'),	#or serialization.NoEncryption(),
		)
	)

with open(key_path + public_key_name, 'wb') as f:
	f.write(
		key.public_key().public_bytes(
			encoding = ser_encoding,
			format = serialization.PublicFormat.SubjectPublicKeyInfo,
		)
	)



subject = x509.Name([
	x509.NameAttribute(NameOID.COUNTRY_NAME, 'IT'),
	x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'TN'),
	x509.NameAttribute(NameOID.LOCALITY_NAME, 'Povo'),
	x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'FBK'),
	x509.NameAttribute(NameOID.COMMON_NAME, 'alex.fbk.eu'),
	])

# cert is self-signed

issuer = subject

builder = x509.CertificateBuilder()

builder = builder.subject_name( subject
			).issuer_name(	issuer 
			).public_key(	key.public_key()
			).serial_number(	x509.random_serial_number()
			).not_valid_before(	datetime.datetime.utcnow()
			).not_valid_after(	datetime.datetime.utcnow() + datetime.timedelta(days=1)
			).add_extension(
				x509.SubjectAlternativeName([x509.DNSName('localhost')]),
				critical=False)

# sign certificate with own private key

cert = builder.sign(key, hashes.SHA256(), openssl.backend)#default_backend())

# save certificate to file




with open(cert_path + cert_name, 'wb') as f:
	
	f.write( cert.public_bytes(ser_encoding) )



