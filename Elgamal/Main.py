from Sockets import Client
from Sockets import Server
from argparse import ArgumentParser

if __name__ == '__main__':

	parser = ArgumentParser()

	parser.add_argument("-m", "--mode", dest="mode", type=str, required=True,
	                    help="CLIENT to start a client or SERVER to start a server"
	                    )

	parser.add_argument("-d", "--debug", dest="debug", required=False,
	                    help="to print debug messages, enable this option",
	                    action="store_true"
	                    )

	parser.add_argument("-b", "--bytes", dest="bytes",type=str, required=False,
	                    help="tamanio en bits de los numeros primos a utlizar"
	                    )

	parser.add_argument("-e", "--mensaje", dest="mensaje",type=str, required=False,
	                    help="Mensaje a enviar desde el cliente para que decodique el servidor"
	                    )



	args = parser.parse_args()

	if args.debug:
		print(args)

	if args.mode.lower() == "client":
	    server = "localhost" # input("Server IP: ")
	    client = Client.ClientSocket(args.debug)
	    client.start_client(server,args.bytes,args.mensaje)

	elif args.mode.lower() == "server":
	    Server.start_server(args.debug,args.bytes)
