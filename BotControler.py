import GameControler as gc
import Addons as ad

# NOTE : this is a fairly dumb ai, especially for split screen games
# NOTE : it could be improved by calculating the ball's trajectory and going where it will be

# controler class
class BotControler(gc.GameControler):

	allow_hard_break = True
	go_to_default_pos = True
	play_frequency = 10
	max_search_dept = 4
	mf = 4
	difficulty = 1

	kick_distance = 140
	precision = 50

	goal = ad.NULL
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


	def playStep(self):
		if self.isActive:
			self.playAutoMove()
		else:
			raise ValueError("Error: bot is deactivated")


	def playAutoMove(self):

		if self.difficulty == 0:
			if self.go_to_default_pos and not self.isOnSameSide( self.game.balls[0] ):
				self.goToDefaultPos( self.mf )
			else:
				self.goTowardsBall( self.mf, self.game.balls[0] )
			return

		else:
			if self.isCloserThan( self.game.balls[0], self.kick_distance ) and self.isInFrontOf( self.game.balls[0] ):
				if self.racket.dx != 0:
					if self.racket.dx * abs( self.racket.fx ) < self.game.balls[0].dx:
						if self.game.balls[0].isGoingLeft():
							self.goLeft( self.mf )
						else:
							self.goRight( self.mf )

				elif self.racket.dy != 0:
					if self.racket.dy * abs( self.racket.fy ) < self.game.balls[0].dy:
						if self.game.balls[0].isGoingUp():
							self.goUp( self.mf )
						else:
							self.goDown( self.mf )

			else:
				self.goToNextGoal( self.mf )


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
				if self.allow_hard_break and rack.isGoingRight():
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
				else:
					return

			elif ball.isGoingUp(): #		when the ball is going to be above
				if self.allow_hard_break and rack.isGoingDown():
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
			if self.racket.isRightOfX( X - self.precision  ):
				if self.racket.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )
			elif self.racket.isLeftOfX( X + self.precision  ):
				if self.racket.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )
			else:
				self.stopHere()

		elif self.racket.dy != 0:
			if self.racket.isBelowY( Y - self.precision ):
				if self.racket.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )
			elif self.racket.isAboveY( Y + self.precision  ):
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


	def isOnSameSize(self, ball):

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

		if self.game.name == "Game" or self.game.name == "Ping" or self.game.name == "Pongester":
			return True

		return False


	def isCloserThan(self, ball, distance):
		if self.racket.dx != 0:
			if abs( self.racket.box.centery - ball.box.centery ) <= distance:
				return True
		elif self.racket.dy != 0:
			if abs( self.racket.box.centerx - ball.box.centerx ) <= distance:
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
		X = ball.box.centerx
		Y = ball.box.centery
		dx = ball.dx
		dy = ball.dy
		fx = ball.fx
		fy = ball.fy

		border = 2 * self.game.size_b

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




