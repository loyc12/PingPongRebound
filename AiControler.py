import GameControler as gc
import Addons as ad

# NOTE : this is a fairly dumb ai, especially for split screen games
# NOTE : it could be improved by calculating the ball's trajectory and going where it will be

# controler class
class AiControler(gc.GameControler):

	allow_hard_break = True
	go_to_center = True # fucky with most games
	play_frequency = 6
	#stop_distance = 120
	mf = 5

	frequency_offset = 0;


	step = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.mode = ad.BOT
		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2


	def setFrequencyOffset(self, racketCount):
		self.frequency_offset = int( (self.racket.id / racketCount) * ad.BOT_FREQUENCY )


	def recordDefaultPos(self):
		self.defaultX = self.racket.box.centerx
		self.defaultY = self.racket.box.centery


	def playStep(self):
		if self.isActive:
			self.playAutoMove()
		else:
			raise ValueError("Error: bot is deactivated")


	def playAutoMove(self):
		if self.go_to_center and self.isBallFar( self.game.balls[0] ):
			self.goToDefaultPos( self.mf )
		else:
			self.goTowardsBall( self.mf, self.game.balls[0] )
		return


	def stopHere(self):
		self.playMove( ad.STOP )

	def goLeft(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( ad.LEFT )

	def goRight(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( ad.RIGHT )

	def goUp(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( ad.UP )

	def goDown(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( ad.DOWN )


	def goTowardsBall(self, maxFactor, ball):

		rack = self.racket

		if rack.dx != 0: #			handling up and down movement
			if rack.isRightOf( ball ): #	when the ball is to the right of the racket
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )

			elif rack.isLeftOf( ball ): #	when the ball is to the left of the racket
				if self.allow_hard_break and rack.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )

			elif ball.isGoingRight(): #		when the ball is going to be to the right
				if self.allow_hard_break and  rack.isGoingLeft():
					self.stopHere()

				elif ball.isRightOfX( rack.box.centerx ): # the ball is on the right half of the racket
					if ball.dx > abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return

				elif ball.isLeftOfX( rack.box.centerx ): # the ball is on the left half of the racket
					if ball.dx < abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return

				else:
					return

			elif ball.isGoingLeft(): #		when the ball is going to be to the left
				if self.allow_hard_break and  rack.isGoingRight():
					self.stopHere()

				elif ball.isLeftOfX( rack.box.centerx ): # the ball is on the left half of the racket
					if ball.dx > abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return

				elif ball.isRightOfX( rack.box.centerx ): # the ball is on the right half of the racket
					if ball.dx < abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return

			else:
				self.stopHere()

		if rack.dy != 0: #			handling up and down movement
			if rack.isBelow( ball ): #		when the ball is to the below of the racket
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )

			elif rack.isAbove( ball ): #	when the ball is to the above of the racket
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )

			elif ball.isGoingDown(): #		when the ball is going to be to below
				if self.allow_hard_break and  rack.isGoingUp():
					self.stopHere()

				elif ball.isBelowY( rack.box.centery ): # the ball is on the lower half of the racket
					if ball.dy > abs(rack.dy * rack.fy):
						self.goDown( maxFactor )
					else:
						return

				elif ball.isAboveY( rack.box.centery ): # the ball is on the upper half of the racket
					if ball.dy < abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return

			elif ball.isGoingUp(): #		when the ball is going to be above
				if self.allow_hard_break and  rack.isGoingDown():
					self.stopHere()

				elif ball.isAboveY( rack.box.centery ): # the ball is on the upper half of the racket
					if ball.dy > abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return

				elif ball.isBelowY( rack.box.centery ): # the ball is on the lower half of the racket
					if ball.dy < abs(rack.dy * rack.fy):
						self.goDown( maxFactor )
					else:
						return

				else:
					return

			else:
				self.stopHere()


	def goTo(self, maxFactor, X, Y):
		if self.racket.dx != 0:
			if self.racket.isRightOfX( X ):
				if self.racket.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )
			elif self.racket.isLeftOfX( X ):
				if self.racket.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )
			else:
				self.stopHere()

		elif self.racket.dy != 0:
			if self.racket.isBelowY( Y ):
				if self.racket.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )
			elif self.racket.isAboveY( Y ):
				if self.racket.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )
			else:
				self.stopHere()

	def goToCenter(self, maxFactor):
		self.goTo( maxFactor, self.game.width / 2, self.game.height / 2)

	def goToDefaultPos(self, maxFactor):
		self.goTo( maxFactor, self.defaultX, self.defaultY)


	def isBallNear(self, ball):

		if self.game.name == "Pinger" or self.game.name == "Pinger":
			if (self.game.width / 2 > self.racket.box.centerx) == (self.game.width / 2 > ball.box.centerx):
				return True
			return False

		if self.racket.dx != 0:
			if (self.game.height / 2 > self.racket.box.centery) == (self.game.height / 2 > ball.box.centery):
				return True

		if self.racket.dy != 0:
			if (self.game.width / 2 > self.racket.box.centerx) == (self.game.width / 2 > ball.box.centerx):
				return True

		if self.game.name == "Game" or self.game.name == "Ping":
			return True

		return False

	def isBallFar(self, ball):
		return not self.isBallNear(ball)

