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
		self.clampSpeed()

	def setDirs(self, _fx, _fy):
		self.fx = _fx
		self.fy = _fy

	def updatePos(self, max_speed):
		# making sure the dx and dy are positive
		self.clampSpeed()

		# moving on x
		if self.fx != 0:
			if abs( self.dx * self.fx ) > max_speed:
				if self.dx > max_speed:
					self.dx = max_speed
				self.box.x += max_speed * ad.getSign(self.fx)
			else:
				self.box.x += self.dx * self.fx

		# moving on y
		if self.fy != 0:
			if abs( self.dy * self.fy ) > max_speed:
				if self.dy > max_speed:
					self.dy = max_speed
				self.box.y += max_speed * ad.getSign(self.fy)
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
			self.dx *= self.game.factor_wall # test
		elif type == "y":
			self.fy *= -1
			self.dy *= self.game.factor_wall # test
		elif type == "stop":
			self.fx = 0
			self.fy = 0
		self.clampSpeed()

	# specifically to handle ball-to-racket collisions
	def collideRack(self, other, type): # 							NOTE : revisit me
		if type == "x":
			self.fx *= -1
			self.dx *= self.game.factor_rack # test
			if self.fy > 0:
				self.dy += other.dy * other.fy
			else:
				self.dy -= other.dy * other.fy
		elif type == "y":
			self.fy *= -1
			self.dy *= self.game.factor_rack # test
			if self.fx > 0:
				self.dx += other.dx * other.fx
			else:
				self.dx -= other.dx * other.fx
		self.clampSpeed()

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



	def isGoingLeft(self):
		if self.fx < 0:
			return True
		return False

	def isGoingRight(self):
		if self.fx > 0:
			return True
		return False

	def isGoingUp(self):
		if self.fy < 0:
			return True
		return False

	def isGoingDown(self):
		if self.fy > 0:
			return True
		return False



	def isLeftOfX(self, X):
		if self.box.right <= X:
			return True
		return False

	def isRightOfX(self, X):
		if self.box.left >= X:
			return True
		return False

	def isAboveY(self, Y):
		if self.box.bottom <= Y:
			return True
		return False

	def isBelowY(self, Y):
		if self.box.top >= Y:
			return True
		return False



	def isLeftOf(self, other):
		if self.box.right <= other.box.left:
			return True
		return False

	def isRightOf(self, other):
		if self.box.left >= other.box.right:
			return True
		return False

	def isAbove(self, other):
		if self.box.bottom <= other.box.top:
			return True
		return False

	def isBelow(self, other):
		if self.box.top >= other.box.bottom:
			return True
		return False