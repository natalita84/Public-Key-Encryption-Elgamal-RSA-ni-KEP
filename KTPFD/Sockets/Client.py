import socket
from ktpfd import ktpfd
import json
import time

class ClientSocket:
	def __init__(self, debugflag):
		
		self.__debugflag = debugflag
			
	def initktp(self, socket):

		socket.send("connected".encode())
		self.__ktpfd = ktpfd.KTPFD(self.tbytes,"CLIENTE")
		
		#print("Tamaño de bits al iniciar cliente: {}".format(self.tbytes))
		# Step1: recive the shared primes and the public secret
		step1 = socket.recv(8192)
		self.__ktpfd.dbConection()
#		if self.__debugflag:
		print(step1)

		# Step 1.1: Parse them
		jsonData = json.loads(step1)
		jsonData = jsonData["ktpfd"]

		self.__ktpfd.p = int(jsonData["p"])
		self.__ktpfd.q = int(jsonData["q"])
		self.__ktpfd.r = int(jsonData["r"])
		self.__ktpfd.phi = int(jsonData["phi"])
		self.__ktpfd.n = int(jsonData["n"])
		self.__ktpfd.id=int(jsonData["id"])
		ppa = int(jsonData["pp"])
		pqa = int(jsonData["pq"])
		
		self.__ktpfd.genPrivKeys()
		self.__ktpfd.genPublicKeys()
		
		
		
		# Step2: mandar las llaves publicas a Alice
		step2 = "{"
		step2 += "\"ktpfd\":"
		step2 += "{"
		step2 += "\"step\": {},".format(2)
		step2 += "\"pp\": {},".format(self.__ktpfd.pp)
		step2 += "\"pq\": {}".format(self.__ktpfd.pq)
		step2 += "}}"
		socket.send(step2.encode())

		
		x=self.__ktpfd.genShared(ppa,pqa)
		
		# Step3: Leer la info de Alice

		step3 = socket.recv(8192)
		print(step3)		
		jsonData = json.loads(step3)
		jsonData = jsonData["ktpfd"]
		
		preShared = int(jsonData["x"])
		
		

		# modulo del parametro para evitar que el numero se pase

		step4 = "{"
		step4 += "\"ktpfd\":"
		step4 += "{"
		step4 += "\"paso\": {},".format(4)
		step4 += "\"x\": {}". format(x)
		step4 += "}}"
		socket.send(step4.encode())
		print("Info Enviada:  \n %s" % x)
		
		shared= self.__ktpfd.getShared(preShared)
		print("Secreto Compartido:  \n %s" % shared)
		print("Desea enviar un mensaje encriptado?")
		text = input("")
		if text=="si":
			self.__ktpfd.preparecipher()
			print("Escriba un numero")
			men= input("")
			self.__ktpfd.insertToEncrypt(men)
			step5 = "{"
			step5 += "\"ktpfd\":"
			step5 += "{"
			step5 += "\"paso\": {},".format(5)
			step5 += "\"men\": {}". format(self.__ktpfd.cipherNumber(men))
			step5 += "}}"
			
			print(step5)
			socket.send(step5.encode())
			print("Mensaje enviado")
				
		else:
			print("terminando programa")
		 
	def start_client(self, ip,tbytes,mensaje):
		# Start the Socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((ip, 50000));

			# Start the Key-Exchange
			self.tbytes=tbytes
			self.mensajeCifrar=mensaje;
			self.initktp(sock)
		finally:
			# Close the Socket
			sock.close()
