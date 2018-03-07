from bge import logic, types, events
from mathutils import Vector

def keyDown(key_code, status=logic.KX_INPUT_ACTIVE):
	if logic.keyboard.events[key_code] == status:
		return True
	print(status)
	return False

class Avatar(types.KX_GameObject):
	
	def __init__(self, own):
		self.speed = 0.1
		self.user = self["user"]
		
	def main (self):
		#k = keyDown
		k = self.user.keyboard.keyDown
		
		up_down = k(events.UPARROWKEY) - k(events.DOWNARROWKEY)
		right_left = k(events.RIGHTARROWKEY) - k(events.LEFTARROWKEY)
		
		delta = Vector((right_left, up_down, 0))
		delta.magnitude = self.speed
		
		self.worldPosition += delta
			
def main(cont):
	
	own = cont.owner
	
	if not "init" in own:
		own["init"] = 1
		Avatar(own)
	else:
		own.main()

