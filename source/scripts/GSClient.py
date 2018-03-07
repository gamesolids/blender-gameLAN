from bge import logic, events
from mathutils import Vector
import socket
import pickle

def keyDown(key_code, status=logic.KX_INPUT_ACTIVE):
	if logic.keyboard.events[key_code] == status:
		return True
	print(status)
	return False

def keyHit(key_code):
	return keyDown(key_code, logic.KX_INPUT_JUST_ACTIVATED)


class Client: 
	
	def __init__(self, host="localhost", port=9999):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setblocking(False)
		self.serv_addr = (host,port)
		
		self.entities = {}
		self.main = self.state_sendName
		
	def state_sendName(self):
		scene = logic.getCurrentScene()
		#text = scene.objects["Name"]
		
		if keyHit(events.ENTERKEY):
			#self.socket.sendto(bytes(text["Text"], "utf-8"), self.serv_addr)
			self.socket.sendto(bytes("dylan", "utf-8"), self.serv_addr)
			#text.endObject()
			self.main = self.state_loop
	
	def state_loop(self):
		self.send()
		self.receive()
		
	def send(self):
		list_key_stat = []
		kevts = logic.keyboard.events
		for k in kevts:
			s = kevts[k]
			if s in (logic.KX_INPUT_JUST_ACTIVATED,
			logic. KX_INPUT_JUST_RELEASED):
				list_key_stat.append((k, s))
			
		if len(list_key_stat):
			self.socket.sendto(pickle.dumps(list_key_stat), self.serv_addr)
		
	def receive(self):
		while True:
			try:
				data, addr = self.socket.recvfrom(1024)
				state = pickle.loads(data)
				for k in state:
					if not k in self.entities:
						#user = User(data.decode())
						scene = logic.getCurrentScene()
						spawner = scene.objects["Spawner" ]
						
						#avatar = scene.addObject("Avatar", spawner)
						#avatar.children[0]["Text"] = user.name
						#avatar["user"] = user
						
						entity = scene.addObject(k[0], spawner)
						self.entities[k] = entity
						#entity.children[0]["Text"] = k[1]
						#self.addr_user[addr] = user
					else:
						entity = self.entities[k]
						
					entity.worldPosition = Vector(state[k])
					
			except socket.error:
				break
			
client = Client()

def main():
	client.main()
	