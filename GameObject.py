import pygame as pg

# TODO : set the center for rect positioning

# ------------------------------------------ GAMEOBJECT CLASS ------------------------------------------ #

# setting up game objects
bgr_colour = pg.Color('black')
fnt_colour = pg.Color('gray25')
obj_colour = pg.Color('white')

max_speed = 50 #		max speed for objects (dx & dy)
win_w = 2048 #			window width
win_h = 1024 #			window height
framerate = 60 #		max tick per second
hard_break = False #	whether the racket stops immediately when changing direction

# object classes
class GameObject:

	def __init__(self, _id, _win, _x, _y, _w, _h):
		self.win = _win
		self.id = _id
		self.dx = 0
		self.dy = 0
		self.fx = 0
		self.fy = 0
		self.box = pg.Rect(0, 0, _w, _h)
		self.setPos(_x, _y)

	def setPos(self, _x, _y):
		self.box.center = (_x, _y)

	def setSize(self, _w, _h):
		self.box.size = (_w, _h)

	def setSpeeds(self, _dx, _dy):
		self.dx = _dx
		self.dy = _dy

	def setDirs(self, _fx, _fy):
		self.fx = _fx
		self.fy = _fy

	def updatePos(self):
		self.box.x += self.dx * self.fx
		self.box.y += self.dy * self.fy

	def collideWall(self, type):
		if (type == "hor"):
			self.fx *= -1
		elif (type == "ver"):
			self.fy *= -1
		elif (type == "wall"):
			self.fx = 0
			self.fy = 0

	# specifically to handle ball-to-racket collisions
	def collideRack(self, other, mode):
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

	def normalizeSpeed(self):
		# make sure dy and dx are positive
		if self.dy < 0:
			self.dy *= -1
			self.fy *= -1
		if self.dx < 0:
			self.dx *= -1
			self.fx *= -1

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
