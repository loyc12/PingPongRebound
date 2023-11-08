import pygame as pg

# TODO : set the center for rect positioning

# ------------------------------------------ GAMEOBJECT CLASS ------------------------------------------ #

# setting up game objects
max_speed = 50
bgr_colour = pg.Color('black')
fnt_colour = pg.Color('gray25')
obj_colour = pg.Color('white')

def getSign(value):
	if (value > 0):
		return 1
	elif (value < 0):
		return -1
	else:
		return 0

# object classes
class GameObject:

	def __init__(self, _id, _win, _x, _y, _w, _h):
		self.win = _win
		self.id = _id
		self.dx = 0
		self.dy = 0
		self.fx = 0
		self.fy = 0
		self.box = pg.Rect(_x, _y, _w, _h)

	def setPos(self, _x, _y): # TODO : set the center for rect positioning
		self.box.x = _x
		self.box.y = _y

	def setSpeeds(self, _dx, _dy):
		self.dx = _dx
		self.dy = _dy

	def setDirs(self, _fx, _fy):
		self.fx = _fx
		self.fy = _fy

	def updatePos(self):
		self.box.x += self.dx * self.fx
		self.box.y += self.dy * self.fy

	def collide(self, type):
		if (type == "hor"):
			self.fx *= -1
		elif (type == "ver"):
			self.fy *= -1
		elif (type == "block"):
			self.fx = 0
			self.fy = 0

	# specifically to handle ball-to-racket collisions
	def collideWith(self, other, mode):
		if mode == "hor":
			if self.fy > 0:
				self.dy += other.dy * other.fy
			else:
				self.dy -= other.dy * other.fy
		elif mode == "ver":
			if self.fx > 0:
				self.dx += other.dx * other.fx
			else:
				self.dx -= other.dx * other.fx

	def normalizeSpeed(self):
		# make sure dy and dx are positive
		if self.dy < 0:
			self.dy *= -1
			self.fy *= -1
		if self.dx < 0:
			self.dx *= -1
			self.fx *= -1

	def clampPos(self):
		# prevent balls from going off screen
		if (self.box.top <= 0):
			self.box.top = 0
		if (self.box.bottom >= self.win.get_height()):
			self.box.bottom = self.win.get_height()
		if (self.box.left <= 0):
			self.box.left = 0
		if (self.box.right >= self.win.get_width()):
			self.box.right = self.win.get_width()

	# also normalizes (make dx & dy positive)
	def clampSpeed(self):
		self.normalizeSpeed()
		# make sure the object (ball) doesn't move too fast
		if self.dy > max_speed:
			self.dy = max_speed
		if self.dx > max_speed:
			self.dx = max_speed

	def drawSelf(self):
		pg.draw.rect(self.win, obj_colour, self.box)
