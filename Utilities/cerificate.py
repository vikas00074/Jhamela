import sys
import time

from OpenSSL import crypto, SSL
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import datetime
import uuid, os, random
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes


class Certificate:
    def __init__(self, CN="CN", C="C", ST="ST", L="L", Og="Og", OU="OU"):
        self.CN = CN
        self.C = C
        self.ST = ST
        self.L = L
        self.Og = Og
        self.OU = OU

    def generate_CA(self):
        one_day = datetime.timedelta(1, 0, 0)
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.C),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.ST),
            x509.NameAttribute(NameOID.LOCALITY_NAME, self.L),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.Og),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, self.OU)
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.CN)
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime(2025, 8, 2))
        builder = builder.serial_number(int(uuid.uuid4()))
        builder = builder.public_key(public_key)
        builder = builder.add_extension(
            x509.BasicConstraints(ca=True, path_length=None), critical=True,
        )
        certificate = builder.sign(
            private_key=private_key, algorithm=hashes.SHA512(),
            backend=default_backend()
        )
        print(isinstance(certificate, x509.Certificate))

        with open("ca.key", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open("ca.crt", "wb") as f:
            f.write(certificate.public_bytes(
                encoding=serialization.Encoding.PEM,
            ))

    def generate_csr_and_key(self):
        """Return a dict with a new csr and key."""
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend())

        csr = x509.CertificateSigningRequestBuilder().subject_name(
            x509.Name({
                x509.NameAttribute(NameOID.COUNTRY_NAME, self.C),
                x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, self.ST),
                x509.NameAttribute(NameOID.LOCALITY_NAME, self.L),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.Og),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, self.OU),
                x509.NameAttribute(NameOID.COMMON_NAME, self.CN),
            })).sign(key, hashes.SHA512(), default_backend())

        result = {
            'csr': csr.public_bytes(
                encoding=serialization.Encoding.PEM).decode("utf-8"),
            'key': key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()).decode("utf-8"),
        }

        # return result
        with open("mycsr.csr", "w") as f:
            f.write(result["csr"])

        with open("mycsr.key", "w") as f:
            f.write(result["key"])

    def sign_Certificate(self):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)
        print(k)

        serial_number = random.getrandbits(64)

        # ca = open("ca.pem", "rb").read()
        with open("ca.crt", "rb") as my_cert_file:
            my_cert_text = my_cert_file.read()
        # print(my_cert_text)
        print()

        with open("ca.key", "rb") as my_key_file:
            my_key_text = my_key_file.read()
            # print(my_key_text)
        print()

        with open("mycsr.csr", "rb") as my_csr_file:
            my_csr_text = my_csr_file.read()
        # print(my_csr_text)
        print()

        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, my_key_text)
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, my_cert_text)
        csr_req = crypto.load_certificate_request(crypto.FILETYPE_PEM, my_csr_text)

        certs = crypto.X509()

        certs.set_serial_number(serial_number)
        certs.gmtime_adj_notBefore(0)
        certs.gmtime_adj_notAfter(63072000)
        certs.set_subject(csr_req.get_subject())
        certs.set_issuer(ca_cert.get_subject())
        certs.set_pubkey(k)
        certs.sign(ca_key, 'sha512')
        certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, certs)

        # print(certificate)
        # # print("Certificate is:\n", certificate.public_bytes(
        # #             encoding=serialization.Encoding.PEM))
        # #
        with open("Server.crt", "w") as f:
            f.write(certificate.decode("utf-8"))

    def makeCaBundle(self):
        f1 = open("Server.crt", "r")
        f2 = open("Ca.crt", "r")
        f3 = open("Cert_Chain.crt", "a")

        for line in f1:
            f3.write(line)

        for line in f2:
            f3.write(line)


C = input('Enter your country: ')
ST = input("Enter your state: ")
L = input("Enter your location: ")
Og = input("Enter your organization: ")
OU = input("Enter your organizational unit (Issued to): ")
CN = input("Enter your Issuer Name: ")

s = Certificate()

s.generate_CA()
s.generate_csr_and_key()
time.sleep(3)
s.sign_Certificate()
time.sleep(3)
s.makeCaBundle()





