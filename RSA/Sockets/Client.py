import socket
from rsaa import rsaa
import json
import time

class ClientSocket:
	def __init__(self, debugflag):
		
		self.__debugflag = debugflag
			
	def initrsa(self, socket):

		socket.send("connected".encode())
		self.__rsa = rsaa.RSA(self.tbytes)
		print("Tamaño de bits al iniciar cliente: {}".format(self.tbytes))
		# Step1: recive the shared primes and the public secret
		step1 = socket.recv(8192)
		#self.__rsa.dbConection()
		if self.__debugflag:
			print(step1)

		# Step 1.1: Parse them
		jsonData = json.loads(step1)
		jsonData = jsonData["rsa"]

		self.ea = int(jsonData["e"])
		self.na = int(jsonData["n"])
		self.__rsa.id=int(jsonData["id"])
		
		self.__rsa.genVars(self.tbytes)
		self.__rsa.genPuKeys()
		self.__rsa.genPriKeys()
		print("Modulo n:  \n %s" % self.__rsa.n)
		print("Phi( n ):  \n %s" % self.__rsa.phi)
		print("Llave Publica e:  \n %s" % self.__rsa.e)
		print("Llave Privada d:  \n %s" % self.__rsa.d)
		
		# Step2: calculate public secret and send to server
		step2 = "{"
		step2 += "\"rsa\":"
		step2 += "{"
		step2 += "\"step\": {},".format(2)
		step2 += "\"n\": {},". format(self.__rsa.n)
		
		step2 += "\"e\": {}".format(self.__rsa.e)
		step2 += "}}"
		socket.send(step2.encode())

		# Step3: Mandar un NUMERO a cifrar
		# modulo del parametro para evitar que el numero se pase
		x=self.__rsa.cipherNumber(self.mensajeCifrar,self.na,self.ea)
		#self.m=  pow(int(self.mensajeCifrar), 1, self.na)
		#self.c = pow(self.m, self.ea, self.na)
		
		step3 = "{"
		step3 += "\"rsa\":"
		step3 += "{"
		step3 += "\"step\": {},".format(2)
		step3 += "\"c\": {}". format(x)
		step3 += "}}"
		socket.send(step3.encode())
		

	def start_client(self, ip,tbytes,mensaje):
		# Start the Socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ip, 50000));

			# Start the Key-Exchange
			self.tbytes=tbytes
			self.mensajeCifrar=mensaje;
			self.initrsa(sock)
			print("n de Alice es:{}".format(self.na))
			print("e de Alice es:{}".format(self.ea))
		finally:
			# Close the Socket
			sock.close()
