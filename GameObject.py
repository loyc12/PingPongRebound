import pygame as pg
import Addons as ad

# ------------------------------------------ GAMEOBJECT CLASS ------------------------------------------ #

# object class
class GameObject:

	def __init__(self, _id, _game, _x, _y, _w, _h):
		self.game = _game
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
		# making sure the dx and dy are positive
		self.clampSpeed()

		# moving on x
		if self.fx != 0:
			if abs( self.dx * self.fx ) > self.game.speed_m:
				self.box.x += self.game.speed_m * ad.getSign(self.fx)
			else:
				self.box.x += self.dx * self.fx

		# moving on y
		if self.fy != 0:
			if abs( self.dy * self.fy ) > self.game.speed_m:
				self.box.y += self.game.speed_m * ad.getSign(self.fy)
			else:
				self.box.y += self.dy * self.fy

	# chekcs for collisions
	def overlaps(self, other):
		if self.box.colliderect(other.box):
			return True
		return False

	def collideWall(self, type):
		if type == "x":
			self.fx *= -1
		elif type == "y":
			self.fy *= -1
		elif type == "stop":
			self.fx = 0
			self.fy = 0

	# specifically to handle ball-to-racket collisions
	def collideRack(self, other, type):
		if type == "x":
			if self.fy > 0:
				self.dy += other.dy * other.fy
			else:
				self.dy -= other.dy * other.fy
		elif type == "y":
			if self.fx > 0:
				self.dx += other.dx * other.fx
			else:
				self.dx -= other.dx * other.fx

	def clampPos(self):
		# prevent balls from going off screen
		if self.box.top <= 0:
			self.box.top = 0
		if self.box.bottom >= self.game.height:
			self.box.bottom = self.game.height
		if self.box.left <= 0:
			self.box.left = 0
		if self.box.right >= self.game.width:
			self.box.right = self.game.width

	def clampSpeed(self):
		# make sure dy and dx are positive
		if self.dy < 0:
			self.dy *= -1
			self.fy *= -1
		if self.dx < 0:
			self.dx *= -1
			self.fx *= -1

	def drawSelf(self):
		pg.draw.rect(self.game.win, self.game.col_obj, self.box)
