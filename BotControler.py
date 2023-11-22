import GameControler as gc
import Addons as ad

# NOTE : this is a fairly dumb ai, especially for split screen games
# NOTE : it could be improved by calculating the ball's trajectory and going where it will be

# controler class
class BotControler(gc.GameControler):

	allow_hard_break = True
	go_to_default_pos = True

	difficulty = ad.HARD
	play_frequency = ad.BOT_FREQUENCY
	max_factor = ad.BOT_M_FACTOR

	max_search_dept = ad.BOT_DEPTH
	precision = ad.BOT_PRECISION
	kick_distance = ad.BOT_KICK_DISTANCE

	goal = ad.NULL
	frequency_offset = 0;
	step = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.mode = ad.BOT
		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2

		if self.difficulty == ad.EASY:
			self.allow_hard_break = False
			self.play_frequency *= 2
			self.max_factor -= 1


	def setFrequencyOffset(self, racketCount):
		self.frequency_offset = int( (self.racketID / racketCount) * ad.BOT_FREQUENCY )


	def recordDefaultPos(self):
		self.defaultX = self.racket.getPosX()
		self.defaultY = self.racket.getPosY()
		self.goal = self.findOwnGoal()


	def findOwnGoal(self):
		rack = self.racket

		if rack.dx != 0:
			if (self.defaultY < self.game.height / 2 ): # goal is on the top
				return ad.UP
			else:
				return ad.DOWN

		elif rack.dy != 0:
			if (self.defaultX < ( self.game.width / 2 ) ): # goal is on the left
				return ad.LEFT
			else:
				return ad.RIGHT


	def playMove(self, move = ad.NULL):
		if move == ad.NULL:
			self.playAutoMove()
		else:
			self.game.makeMove( self.racketID, move )


	def playAutoMove(self):
		if self.difficulty == ad.EASY:
			self.goTo( self.max_factor, self.game.balls[0].getPosX(), self.game.balls[0].getPosY() )

		elif self.difficulty == ad.MEDIUM:
			if self.go_to_default_pos and not self.isOnSameSide( self.game.balls[0] ):
				self.goToDefaultPos( self.max_factor )
			else:
				self.goTowardsBall( self.max_factor, self.game.balls[0] )
			return

		elif self.difficulty == ad.HARD:
			if self.isCloserThan( self.game.balls[0], self.kick_distance ) and self.isInFrontOf( self.game.balls[0] ):
				if self.racket.dx != 0:
					if self.racket.dx * abs( self.racket.fx ) < self.game.balls[0].dx:
						if self.game.balls[0].isGoingLeft():
							self.goLeft( self.max_factor )
						else:
							self.goRight( self.max_factor )

				elif self.racket.dy != 0:
					if self.racket.dy * abs( self.racket.fy ) < self.game.balls[0].dy:
						if self.game.balls[0].isGoingUp():
							self.goUp( self.max_factor )
						else:
							self.goDown( self.max_factor )

			else:
				self.goToNextGoal( self.max_factor )


	def stopHere(self):
		self.playMove( ad.STOP )

	def goUp(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( ad.UP )

	def goRight(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( ad.RIGHT )

	def goDown(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( ad.DOWN )

	def goLeft(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( ad.LEFT )

	def goToNextGoal(self, maxFactor):
		(X, Y) = self.findNextGoal(self.game.balls[0])
		self.goTo( maxFactor, X, Y )


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
				if self.allow_hard_break and rack.isGoingLeft():
					self.stopHere()

				elif ball.isRightOfX( rack.getPosX() ): # the ball is on the right half of the racket
					if ball.dx > abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return

				elif ball.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if ball.dx < abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return
				else:
					return

			elif ball.isGoingLeft(): #		when the ball is going to be to the left
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()

				elif ball.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if ball.dx > abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return

				elif ball.isRightOfX( rack.getPosX() ): # the ball is on the right half of the racket
					if ball.dx < abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return
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
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()

				elif ball.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
					if ball.dy > abs(rack.dy * rack.fy):
						self.goDown( maxFactor )
					else:
						return

				elif ball.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if ball.dy < abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return
				else:
					return

			elif ball.isGoingUp(): #		when the ball is going to be above
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()

				elif ball.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if ball.dy > abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return

				elif ball.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
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
			if self.racket.isRightOfX( X - self.precision  ):
				if self.allow_hard_break and self.racket.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )
			elif self.racket.isLeftOfX( X + self.precision  ):
				if self.allow_hard_break and self.racket.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )
			elif self.allow_hard_break:
				self.stopHere()

		elif self.racket.dy != 0:
			if self.racket.isBelowY( Y - self.precision ):
				if self.allow_hard_break and self.racket.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )
			elif self.racket.isAboveY( Y + self.precision  ):
				if self.allow_hard_break and self.racket.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )
			elif self.allow_hard_break:
				self.stopHere()


	def goToCenter(self, maxFactor):
		self.goTo( maxFactor, self.game.width / 2, self.game.height / 2)


	def goToDefaultPos(self, maxFactor):
		self.goTo( maxFactor, self.defaultX, self.defaultY)


	def isOnSameSide(self, ball):

		if self.racket.dx != 0:
			if (self.game.height / 2 > self.racket.getPosY()) == (self.game.height / 2 > ball.getPosY()):
				return True

		if self.racket.dy != 0:
			if (self.game.width / 2 > self.racket.getPosX()) == (self.game.width / 2 > ball.getPosX()):
				return True

		if self.game.name == "Game" or self.game.name == "Ping" or self.game.name == "Pongester":
			return True

		return False


	def isCloserThan(self, ball, distance):
		if self.racket.dx != 0:
			if abs( self.racket.getPosY() - ball.getPosY() ) <= distance:
				return True
		elif self.racket.dy != 0:
			if abs( self.racket.getPosX() - ball.getPosX() ) <= distance:
				return True
		return False


	def isInFrontOf(self, ball):
		if self.racket.dx != 0:
			if not ball.isLeftOf( self.racket ) and not ball.isRightOf( self.racket ):
				return True
		elif self.racket.dy != 0:
			if not ball.isAbove( self.racket ) and not ball.isBelow( self.racket ):
				return True
		return False


	def isInOwnGoal(self, X, Y, border):

		if self.goal == ad.LEFT and X <= border:
			return True
		if self.goal == ad.RIGHT and X >= ( self.game.width - border ):
			return True
		if self.goal == ad.UP and Y <= border:
			return True
		if self.goal == ad.DOWN and Y >= ( self.game.height - border ):
			return True

		return False


	def findNextGoal(self, ball):
		X = ball.getPosX()
		Y = ball.getPosY()
		dx = ball.dx
		dy = ball.dy
		fx = ball.fx
		fy = ball.fy

		border = self.game.size_b * (2 / 3)

		dept = 0

		# loops over all the "bounce points" of the ball's trajectory (untill max_search_dept is reached)
		while dept <= self.max_search_dept:
			dept += 1

			# have the ball do one step
			dy += self.game.gravity * fy # NOTE : assumes normal gravity
			X += dx * fx
			Y += dy * fy

			while ad.isInZone( X, Y, border, self.game ):
				dy += self.game.gravity * fy # NOTE : assumes normal gravity
				X += dx * fx
				Y += dy * fy

			if self.isInOwnGoal( X, Y, border ):
				return (X, Y)

			# make ball bounce on edges
			if X <= border or X >= ( self.game.width - border ):
				fx *= -1
				dx *= self.game.factor_wall
			if Y <= border or Y >= ( self.game.height - border ):
				fy *= -1
				dy *= self.game.factor_wall


		return (X, Y)




