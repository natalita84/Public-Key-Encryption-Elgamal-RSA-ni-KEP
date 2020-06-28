import time
import socket
from elgamal import elgamal
import json


class ClientSocket:

	def __init__(self, debugflag):

		self.__debugflag = debugflag

	def initDiffieHellman(self, socket):

		socket.send("connected".encode())
		self.__dh = elgamal.ELGAMAL(self.tbytes)
		
		# Step1: recive the shared primes and the public secret
		step1 = socket.recv(8192)

		if self.__debugflag:
			print(step1)

		# Step 1.1: Parse them
		jsonData = json.loads(step1.decode())
		jsonData = jsonData["dh-keyexchange"]
		self.__dh.generator = int(jsonData["generator"])
		self.__dh.prime = int(jsonData["prime"])
		self.__dh.id=int(jsonData["id"])
		public_key = int(jsonData["public_key"])
		print("Primo:",self.__dh.prime)
		

		# Step2: calculate public secret and send to server
		#self.__dh.generate_private_key(int(self.tbytes))
		self.__dh.generate_private_key()
		self.__dh.generate_public_key()
		self.__dh.prepInfo()
		
		step2 = "{"
		step2 += "\"dh-keyexchange\":"
		step2 += "{"
		step2 += "\"step\": {},".format(2)
		step2 += "\"public_key\": {}".format(self.__dh.public_key)
		step2 += "}}"
		socket.send(step2.encode())

		
		# # Step3: calculate the shared secret


		secreto=self.__dh.generate_shared_secret(public_key)
		print("secreto compartido:",secreto)

		self.__dh.insertToEncrypt(self.mensajeCifrar)
		inicioC=time.time();
		self.__dh.cipherTexa()
		ctbm=self.__dh.cipherTexb(self.mensajeCifrar,public_key)
		finC=time.time()
		self.__dh.insertTime(inicioC,finC,"1")
		
		
		
		step4 = "{"
		step4 += "\"dh-keyexchange\":"
		step4 += "{"
		step4 += "\"step\": {},".format(4)
		step4 += "\"a\": {},".format(self.__dh.cta)
		step4 += "\"ctbm\": {}".format(ctbm)
		step4 += "}}"
		socket.send(step4.encode())
		
		
		print("datos enviados ctbm:", ctbm)
		print("datos enviado a:",self.__dh.cta)
		print("Llave pública de Bob:",self.__dh.public_key)
		
	def start_client(self, ip, tbytes, mensaje):
		# Start the Socket

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ip, 50000));

			self.tbytes=tbytes
			self.mensajeCifrar=mensaje
			self.initDiffieHellman(sock)
		

			
		finally:
			# Close the Socket
			sock.close()
	
