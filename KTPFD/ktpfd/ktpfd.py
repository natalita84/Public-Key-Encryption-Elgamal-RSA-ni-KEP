import hashlib
import math
import random 
import time
from binascii import hexlify
import mysql.connector
from random import randrange, getrandbits
from mysql.connector import Error
#from .primes import PRIMES
try:
    from ssl import RAND_bytes
    rng = RAND_bytes
except(AttributeError, ImportError):
    raise RNGError


class KTPFD:

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
				
	def __init__(self,keyLength=540,cType="CLIENT"):

		if cType=="SERVER":
			print("INICIALIZANDO SERVIDOR")
			self.dbConection()
			self.insertEjecucion(keyLength)
			self.gen_num(keyLength)
		else:
			print("INICIALIZANDO CLIENTE")
			
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
			insert_tuple = (keyLength,"4")	
			self.cursor.execute(sql_insert_query,insert_tuple)
			self.connection.commit()
			self.id=self.cursor.lastrowid
			
		except mysql.connector.Error as error :
			connection.rollback() #rollback if any exception occured
			print("Failed inserting record into python_users table {}".format(error))
	
				
	def gen_num(self,keyLenght):

		iniciopKp=time.time()
		self.p=2		
		self.q=2
		#RFC 3526 
		#self.r = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF
		#self.r = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
		#self.r = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A93AD2CAFFFFFFFFFFFFFFFF
		self.r = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C934063199FFFFFFFFFFFFFFFF
       
		self.n= self.p*self.q*self.r;
		self.phi=2*self.r-2;	
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"5")
	
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

	def mulmod(self,a, b, mod):

		res = 0; 
		a = a % mod; 
		while (b > 0): 
	      
			if (b % 2 == 1): 
				res = (res + a) % mod;

			a = (a * 2) % mod; 

			b //= 2;
		return res % mod; 

    
	def genPrivKeys(self):

		iniciopKp=time.time()
		self.X = random.randrange(1, self.phi)
		self.Y = self.phi+1-self.X

		self.K = random.randrange(1, self.n)
		g = self.gcd(self.K, self.n)
		while g != 1:
			self.K = random.randrange(1, self.n)
			g = self.gcd(self.K, self.n)
		self.KInv = self.getModInverse(self.K, self.n)
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"3")

	def genPublicKeys(self):

		iniciopKp=time.time()
		temp1=pow(self.p,2*self.X,self.n)
		temp2=pow(self.q,self.Y,self.n)
		self.pp=self.mulmod(temp1, self.K, self.n)
		self.pq=self.mulmod(temp2, self.K, self.n)
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"2")

	def genShared(self,_pp,_pq):
		
		t1=pow(_pp,self.X,self.n)
		t2=pow(_pq,self.Y,self.n)
		
		return self.mulmod(t1,t2,self.n)
	
	def getShared(self,pre):
		
		self.Ks=self.mulmod(pre,self.KInv,self.n)
		return self.Ks
	
	def preparecipher(self):

		self.Kr=int( (self.Ks//(self.p*self.q)) % self.r)
		print("Kr: \n %s" % self.Kr)
		self.KrInv = self.getModInverse(int(self.Kr), self.r)
	
	def cipherNumber(self,number):

		iniciopKp=time.time()
		x=self.mulmod(int(number), self.Kr, self.r)
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"1")
		return x
	
	def decipherNumber(self,number):
		iniciopKp=time.time()
		x=self.mulmod(int(number), self.KrInv, self.r)
		finpKp=time.time()
		self.insertTime(iniciopKp,finpKp,"4")
		return x		
