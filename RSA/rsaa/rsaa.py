import hashlib
import math
import random 
import time
from random import randrange, getrandbits
import mysql.connector
from mysql.connector import Error

class RSA:
	
	def dbConection(self):
		try:
			self.connection = mysql.connector.connect(host='localhost',database='info_cripto',user='root',password='root')
			if self.connection.is_connected():
				db_Info = self.connection.get_server_info()
				print("Connected to MySQL database... MySQL Server version on ",db_Info)
				self.cursor = self.connection.cursor()
				self.cursor.execute("select database();")
				record = self.cursor.fetchone()
				print ("Your connected to - ", record)
		except Error as e :
			print ("Error while connecting to MySQL", e)		

	def insertTime(self,begin,end,tipo):
		sql_insert_query = """INSERT INTO tiempos(idEjecucion,idTipoTiempo,tiempo) VALUES(%s,%s,%s) """
		insert_tuple = (self.id,tipo,((end-begin)*1000))
		self.cursor.execute(sql_insert_query,insert_tuple)
		self.connection.commit()
		
	def insertToEncrypt(self,text):
		sql_insert_query = """INSERT INTO cifrados(idEjecucion,texto) VALUES(%s,%s) """
		insert_tuple = (self.id,text)
		self.cursor.execute(sql_insert_query,insert_tuple)
		self.connection.commit()		
	
	def insertEjecucion(self,keyLength):
		try:
			sql_insert_query = """INSERT INTO ejecucion(tamanioPalabra,idAlgoritmo) VALUES(%s,%s) """
		
			insert_tuple = (keyLength,"3")
		
			self.cursor.execute(sql_insert_query,insert_tuple)
			self.connection.commit()
			self.id=self.cursor.lastrowid
			
		except mysql.connector.Error as error :
			connection.rollback()
			print("Failed inserting record into python_users table {}".format(error))

	def __init__(self,keyLength,cType="CLIENT"):

		print("Tamaño de bits: {}".format(keyLength))
		#inicaliza BD
		self.dbConection()
		#inserta la ejecucion en BD y genera el ID
		if cType=="SERVER":
			self.insertEjecucion(keyLength)
			self.genVars(keyLength)
			self.genPuKeys()
			self.genPriKeys()
	
	def genVars(self,keyLength):
		
		inicioV=time.time()		
		self.p=self.generate_prime_number(int(keyLength))
		self.q=self.generate_prime_number(int(keyLength))
		self.n = self.p * self.q
		self.phi= (self.p -1) * (self.q -1)
		finV=time.time()
		self.insertTime(inicioV,finV,"5")
	
	def genPuKeys(self):
		
		inicioPu=time.time()
		self.e = random.randrange(1, self.phi)
		g = self.gcd(self.e, self.phi)
		while g != 1:
			self.e = random.randrange(1, self.phi)
			g = self.gcd(self.e, self.phi)
		finPu=time.time()
		self.insertTime(inicioPu,finPu,"2")
		
	def genPriKeys(self):
	
		iniciopKp=time.time()		
		self.d = self.getModInverse(self.e, self.phi) 		
		finpKp=time.time()		
		self.insertTime(iniciopKp,finpKp,"3")
			
	def gcd(self,a, b):
		while b != 0:
			a, b = b, a % b
		return a
		
	def is_prime(self,n, k=128):

	    if n == 2 or n == 3:
	        return True
	    if n <= 1 or n % 2 == 0:
	        return False
	    s = 0
	    r = n - 1
	    while r & 1 == 0:
	        s += 1
	        r //= 2
	    for _ in range(k):
	        a = randrange(2, n - 1)
	        x = pow(a, r, n)
	        if x != 1 and x != n - 1:
	            j = 1
	            while j < s and x != n - 1:
	                x = pow(x, 2, n)
	                if x == 1:
	                    return False
	                j += 1
	            if x != n - 1:
	                return False
	    return True

	def getModInverse(self,a, m):
		if math.gcd(a, m) != 1:
			return None
		u1, u2, u3 = 1, 0, a
		v1, v2, v3 = 0, 1, m

		while v3 != 0:
			q = u3 // v3
			v1, v2, v3, u1, u2, u3 = (
			u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
		return u1 % m

	def generate_prime_candidate(self,length):

		p = getrandbits(length)
		p |= (1 << length - 1) | 1
		return p

	def generate_prime_number(self,length):

		p = 4
		while not self.is_prime(p, 128):
			p = self.generate_prime_candidate(length)
		return p
		
	def cipherNumber(self,mensaje,na,ea):
		self.insertToEncrypt(mensaje)
		inicio=time.time()
		m=  pow(int(mensaje), 1, na)
		c = pow(m, ea, na)
		fin=time.time()
		self.insertTime(inicio,fin,"1")		
		return c
		
	def decipherNumber(self,c):
		inicio=time.time()
		ce= pow(c, self.d, self.n)
		fin=time.time()
		self.insertTime(inicio,fin,"4")
		return ce	
