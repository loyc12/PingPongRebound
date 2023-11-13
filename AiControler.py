import GameControler as gc
import Addons as ad

# controler class
class AiControler(gc.GameControler):

	allow_hard_break = False
	stop_distance = 120
	play_frequency = 12

	step = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.mode = ad.BOT


	def playStep(self):
		if self.isActive:
			if (self.step % self.play_frequency) == 0:
				self.playMove( self.findNextMove() )
				self.step = 0
			self.step += 1


	def findNextMove(self):
		if self.racket == 0:
			raise ValueError("Error: no racket selected")

		ball = self.game.balls[0]

		# handling left and right movement
		if self.racket.dx != 0:
			if  abs(ball.box.centery - self.racket.box.centery) < self.stop_distance: # and ad.getSign(ball.fx) != ad.getSign(self.racket.fx):
				return ad.STOP
			elif ball.box.centerx <= self.racket.box.left:
				return ad.LEFT
			elif ball.box.centerx >= self.racket.box.right:
				return ad.RIGHT
			else: #								when ball is in front
				if self.allow_hard_break: #		NOTE : eh, fucky behaviour
					return ad.STOP
				if ball.fx < 0 and ball.box.centerx < self.racket.box.centerx:
					return ad.LEFT
				elif ball.fx > 0 and ball.box.centerx > self.racket.box.centerx:
					return ad.RIGHT
				else:
					return ad.NULL

		# handling up and down movement
		elif self.racket.dy != 0:
			if abs(ball.box.centerx - self.racket.box.centerx) < self.stop_distance: # and ad.getSign(ball.fy) != ad.getSign(self.racket.fy):
				return ad.STOP
			elif ball.box.centery <= self.racket.box.top:
				return ad.UP
			elif ball.box.centery >= self.racket.box.bottom:
				return ad.DOWN
			else: #								when ball is in front
				if self.allow_hard_break : #	NOTE : eh, fucky behaviour
					return ad.STOP
				elif ball.fy < 0 and ball.box.centery < self.racket.box.centery:
					return ad.UP
				elif ball.fy > 0 and ball.box.centery > self.racket.box.centery:
					return ad.DOWN
				else:
					return ad.NULL

	def doNothing(self):
		return ad.NULL

	def stopHere(self):
		return ad.STOP

	def goLeft(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			return ad.LEFT

	def goRight(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			return ad.LEFT

	def goUp(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			return ad.LEFT

	def goDown(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			return ad.LEFT

	def goToCenter(self, maxFactor):
		pass

	def goTowardsBall(self, maxFactor, ball):
		pass

	def goTo(self, maxFactor, pos):
		pass