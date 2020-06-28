import socketserver
from rsaa import rsaa
import json


class ServerSocket(socketserver.BaseRequestHandler):
		
	def setup(self):

		self.__rsa = rsaa.RSA(self.t_bytes,"SERVER")
		
		print("Modulo n:  \n %s" % self.__rsa.n)
		print("Phi( n ):  \n %s" % self.__rsa.phi)
		print("Llave Publica e:  \n %s" % self.__rsa.e)
		print("Llave Privada d:  \n %s" % self.__rsa.d)

        
	def initRSA(self):
		if self.request.recv(8192).decode() != "connected": 
			print("Error while connecting")
		#publicKey = self.__rsa.genPublicKey()
		

				
		# Step1: share primes and public secret
		
		step1 = "{"
		step1 += "\"rsa\":"
		step1 += "{"
		step1 += "\"paso\": {},".format(1)
		step1 += "\"id\": {},". format(self.__rsa.id)
		step1 += "\"n\": {},". format(self.__rsa.n)
		step1 += "\"e\": {}".format(self.__rsa.e)
		step1 += "}}"
		self.request.send(step1.encode())
		###########################################################

		# step2: recive the public secret from client
		step2 = self.request.recv(8192)

		if self.__debugflag:
			print(step2)

		# step 2 Parse them
		jsonData = json.loads(step2.decode())
		jsonData = jsonData["rsa"]

		self.eb= int(jsonData["e"])
		self.nb= int(jsonData["n"])
		
		# step3: calculate the shared secret
		
		step3 = self.request.recv(8192)
		jsonData = json.loads(step3.decode())
		jsonData = jsonData["rsa"]
		
		
		self.c= int(jsonData["c"])
		self.ce = self.__rsa.decipherNumber(self.c)

	# Client connected
	def handle(self):
		self.__debugflag = self.server.conn
		# print the Client-IP
		
		print("[{}] Client connected.".format(self.client_address[0]))

		# init
		self.initRSA()
		print("> n de Bob\n {}\n".format(self.nb))
		print("> e de Bob\n {}\n".format(self.eb))
		print("\n\n valor enviado C {}\n".format(self.c))
		print("\n\n valor decifrado C {}\n".format(self.ce))

def start_server(debugflag,tbytes):
	# start the server and serve forever
	server = socketserver.ThreadingTCPServer(("", 50000), ServerSocket)
	server.conn = debugflag
	ServerSocket.t_bytes=tbytes
	# And serve
	server.serve_forever()
