
import time
import random 
import math
import hashlib 
from random import randrange, getrandbits
import mysql.connector
from mysql.connector import Error

try:
    from ssl import RAND_bytes
    rng = RAND_bytes
except(AttributeError, ImportError):
    raise RNGError


class ELGAMAL:
	
	
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
			insert_tuple = (keyLength,"2")		
			self.cursor.execute(sql_insert_query,insert_tuple)
			self.connection.commit()
			self.id=self.cursor.lastrowid
			
		except mysql.connector.Error as error :
			connection.rollback() #rollback if any exception occured
			print("Failed inserting record into python_users table {}".format(error))
	

	def __init__(self, keylength,cType="CLIENT"):

		print("Tamaño de bits: {}".format(keylength))
		self.dbConection()
		if cType=="SERVER":
			self.insertEjecucion(keylength)
			inicio=time.time()
			self.generator = 2
			#RFC 3526
			self.prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF
			#self.prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
			#self.prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF
			#self.prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C934063199FFFFFFFFFFFFFFFF
			fin=time.time()
			self.insertTime(inicio,fin,"5")
			self.generate_private_key()
			self.generate_public_key()

	def prepInfo(self):
		
		self.pr = (self.prime -1)
		self.k = random.randrange(1, self.pr)
		g = self.gcd(self.k, self.pr)
		while g != 1:
			self.k = random.randrange(1, self.pr)
			g = self.gcd(self.k, self.pr)


	def generate_private_key(self):

		iniciopKp=time.time()
		self.__private_key = random.randrange(2, self.prime-2)
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"3")

	def generate_public_key(self):
		inicio=time.time()
		self.public_key = pow(self.generator,
                              self.__private_key,
                              self.prime)
		fin=time.time()
		self.insertTime(inicio,fin,"2")	

	def generate_shared_secret(self, public_key):
		self.shared_secret = pow(public_key,
                                 self.__private_key,
                                 self.prime)
		return self.shared_secret	

	def gcd(self,a, b):
		while b != 0:
			a, b = b, a % b
		return a

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

	def cipherTexa(self):
		inicio=time.time()
		self.cta=pow(self.generator, self.k, self.prime)
		fin=time.time()
		self.insertTime(inicio,fin,"1")
					
	def cipherTexb(self, mensaje,publicKey):
		inicio=time.time()
		ctb = pow(publicKey, self.k, self.prime)		
		return ((ctb*int(mensaje))%self.prime)
		fin=time.time()
		self.insertTime(inicio,fin,"1")
		

	def descipherText(self,a,b):

		inicio=time.time()
		temp=pow(a, self.__private_key, self.prime)
		aInv=self.getModInverse(temp, self.prime)
		fin=time.time()
		self.insertTime(inicio,fin,"4")				
		return (int(b)*aInv)%self.prime

		
		


