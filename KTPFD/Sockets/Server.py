import socketserver
from ktpfd import ktpfd
import json


class ServerSocket(socketserver.BaseRequestHandler):
		
	def setup(self):
		self.__ktpfd = ktpfd.KTPFD(self.t_bytes,"SERVER")
		
	def initKTP(self):
		if self.request.recv(8192).decode() != "connected": 
			print("Error while connecting")
		# Step1: share primes and public secret
		
		self.__ktpfd.genPrivKeys()
		self.__ktpfd.genPublicKeys()
		
		step1 = "{"
		step1 += "\"ktpfd\":"
		step1 += "{"
		step1 += "\"paso\": {},".format(1)
		step1 += "\"id\": {},". format(self.__ktpfd.id)
		step1 += "\"p\": {},". format(self.__ktpfd.p)
		step1 += "\"q\": {},". format(self.__ktpfd.q)
		step1 += "\"r\": {},". format(self.__ktpfd.r)
		step1 += "\"phi\": {},". format(self.__ktpfd.phi)
		step1 += "\"pp\": {},". format(self.__ktpfd.pp)
		step1 += "\"pq\": {},". format(self.__ktpfd.pq)		
		step1 += "\"n\": {}".format(self.__ktpfd.n)
		step1 += "}}"
		self.request.send(step1.encode())
		###########################################################
		
		
		# step2: recive the public secret from client
		step2 = self.request.recv(8192)

		#if self.__debugflag:
		print(step2)

		# step 2 Parse them
		jsonData = json.loads(step2.decode())
		jsonData = jsonData["ktpfd"]
		
		ppb = int(jsonData["pp"])
		pqb = int(jsonData["pq"])
		
		print("Llave pp de Bob:  \n %s" % ppb)
		print("Llave pq de Bob:  \n %s" % pqb)		
		
		
		x=self.__ktpfd.genShared(ppb,pqb)
		
		print("Info Enviada:  \n %s" % x)
		
		
		# step3: calculate the shared secret
		
		step3 = "{"
		step3 += "\"ktpfd\":"
		step3 += "{"
		step3 += "\"paso\": {},".format(3)
		step3 += "\"x\": {}". format(x)
		step3 += "}}"
		self.request.send(step3.encode())
		
		
		step4 = self.request.recv(8192)
		print(step4)		
		jsonData = json.loads(step4)
		jsonData = jsonData["ktpfd"]
		
		preShared = int(jsonData["x"])
		shared= self.__ktpfd.getShared(preShared)
		print("Secreto Compartido:  \n %s" % shared)
		
		step5 = self.request.recv(8192)
		print(step5)		
		jsonData = json.loads(step5)
		jsonData = jsonData["ktpfd"]
		self.__ktpfd.preparecipher()
		
		mensaje = int(jsonData["men"])
		decifrado=self.__ktpfd.decipherNumber(mensaje)
		
		print("Mensaje Decifrado:  \n %s" % decifrado)

	# Client connected
	def handle(self):
		self.__debugflag = self.server.conn
		# print the Client-IP
		
		print("[{}] Client connected.".format(self.client_address[0]))
		
		# init
		self.initKTP()

def start_server(debugflag,tbytes):
	# start the server and serve forever
	server = socketserver.ThreadingTCPServer(("", 50000), ServerSocket)
	server.conn = debugflag
	ServerSocket.t_bytes=tbytes
	# And serve
	server.serve_forever()
