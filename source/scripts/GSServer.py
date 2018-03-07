from bge import logic
import socket
import pickle


class RemoteKeyboard:
	
	def __init__(self):
		self.key_stat = {}
		
	def updateState(self, list_key_stat):
		for key, stat in list_key_stat:
			self.key_stat[key] = stat
			
	def keyDown(self, key_code, status=logic.KX_INPUT_JUST_ACTIVATED):
		if key_code in self.key_stat:
			if self.key_stat[key_code] == status:
				return True
			
		return False
	

class User:
	
	def __init__(self, name):
		self.name = name
		self.keyboard = RemoteKeyboard()
		

class Server: 
	
	def __init__(self, host="localhost", port=9999):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.setblocking(False)
		self.socket.bind((host,port))
		
		self.addr_user = {}
		
	def receive(self):
		while True:
			try:
				data, addr = self.socket.recvfrom(1024)
				
				if not addr in self.addr_user:
					user = User(data.decode())
					scene = logic.getCurrentScene()
					spawner = scene.objects["Spawner" ]
					
					avatar = scene.addObject("Avatar", spawner)
					#avatar.children[0]["Text"] = user.name
					avatar["user"] = user
					
					self.addr_user[addr] = user
				else:
					user = self.addr_user[addr]
					user.keyboard.updateState(pickle.loads(data))
				
			except socket.error:
				break
			
			
	def send(self):
		scene = logic.getCurrentScene()
		state = {(gobj.name,gobj["user"].name): list(gobj.worldPosition) \
				for gobj in scene.objects \
				if gobj.name == "Avatar"}
				
		for addr in self.addr_user:
			self.socket.sendto(pickle.dumps(state), addr)
			
			
	def close(self):
		self.socket.close()
	
	

server = Server()

def receive():
	server.receive()
	
def send():
	server.send()
	
def close():
	server.close()
	