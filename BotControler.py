try:
	from master import gc
	import defs as df
except ModuleNotFoundError:
	from game.PingPongRebound.master import gc
	import game.PingPongRebound.defs as df

# controler class
class BotControler(gc.GameControler):

	allow_hard_break = df.BOT_HARD_BREAK
	go_to_default_pos = True

	difficulty = df.HARD
	max_factor = df.BOT_M_FACTOR # (max speed factor (how many times dx or dy can the racket go at)

	goal = df.NULL
	frequency_offset = 0;
	step = 0

	def __init__(self, _game, _botName):
		self.game = _game
		self.name = _botName
		self.mode = df.BOT

		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2

		self.seeBall()

		if self.difficulty == df.EASY:
			self.allow_hard_break = False
			df.BOT_PLAY_FREQUENCY *= 2
			self.max_factor -= 1


	def setFrequencyOffset(self, racketCount):
		self.frequency_offset = int(( float(self.racketID) / racketCount ) * df.BOT_PLAY_FREQUENCY )


	def recordDefaultPos(self):
		self.defaultX = self.racket.getPosX()
		self.defaultY = self.racket.getPosY()
		self.goal = self.findOwnGoal()


	def seeBall(self):
		self.lastBall = self.game.balls[0].getCopy()


	def findOwnGoal(self):
		rack = self.racket

		if rack.dx != 0:
			if (self.defaultY < self.game.height / 2 ): # goal is on the top
				return df.UP
			else:
				return df.DOWN

		elif rack.dy != 0:
			if (self.defaultX < ( self.game.width / 2 ) ): # goal is on the left
				return df.LEFT
			else:
				return df.RIGHT


	def playMove(self, move = df.NULL):
		if move == df.NULL:
			self.playAutoMove()
		else:
			self.game.makeMove( self.racketID, move )


	def playAutoMove(self):
		if not df.BOT_CAN_PLAY:
			return
		elif df.BOT_INSTANT_REACT:
			self.seeBall()

		if self.difficulty == df.EASY:
			self.goTo( self.max_factor, self.lastBall.getPosX(), self.lastBall.getPosY() )

		elif self.difficulty == df.MEDIUM:
			if self.go_to_default_pos and not self.isOnSameSideOf( self.lastBall ):
				self.goToDefaultPos( self.max_factor )
			else:
				self.goTowardsBall( self.max_factor, self.lastBall )
			return

		elif self.difficulty == df.HARD:
			if self.game.racketCount > 1 and self.isInFrontOf( self.lastBall ) and self.isCloserThan( self.lastBall, df.BOT_KICK_DISTANCE ):
				if self.game.name == "Ping":
					self.goToCenter( self.max_factor )

				elif self.racketDir == 'x':
					if self.racket.dx * abs( self.racket.fx ) < self.lastBall.dx: # and self.lastBall.isLeftOfX(self.racket.px):
						#if self.lastBall.isLeftOfX(self.racket.px):
						if self.lastBall.isGoingLeft():
							if self.racket.fx > -df.BOT_KICK_FACTOR:
								self.goLeft( self.max_factor )
						else:
							if self.racket.fx < df.BOT_KICK_FACTOR:
								self.goRight( self.max_factor )

				elif self.racketDir == 'y':
					if self.racket.dy * abs( self.racket.fy ) < self.lastBall.dy: # and self.lastBall.isAboveY(self.racket.py):
						#if self.lastBall.isAboveY(self.racket.py):
						if self.lastBall.isGoingUp():
							if self.racket.fy > -df.BOT_KICK_FACTOR:
								self.goUp( self.max_factor )
						else:
							if self.racket.fy < df.BOT_KICK_FACTOR:
								self.goDown( self.max_factor )
			else:
				self.goToNextGoal( self.max_factor )


	def stopHere(self):
		self.playMove( df.STOP )

	def goUp(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( df.UP )

	def goRight(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( df.RIGHT )

	def goDown(self, maxFactor):
		if abs(self.racket.fy) <= maxFactor:
			self.playMove( df.DOWN )

	def goLeft(self, maxFactor):
		if abs(self.racket.fx) <= maxFactor:
			self.playMove( df.LEFT )

	def goToNextGoal(self, maxFactor):
		(X, Y) = self.findNextGoal()
		self.goTo( maxFactor, X, Y )


	def goTowardsBall(self, maxFactor):

		rack = self.racket

		if rack.dx != 0: #			handling up and down movement
			if rack.isRightOf( self.lastBall ): #	when the ball is to the right of the racket
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )

			elif rack.isLeftOf( self.lastBall ): #	when the ball is to the left of the racket
				if self.allow_hard_break and rack.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )

			elif self.lastBall.isGoingRight(): #		when the ball is going to be to the right
				if self.allow_hard_break and rack.isGoingLeft():
					self.stopHere()

				elif self.lastBall.isRightOfX( rack.getPosX() ): # the ball is on the right half of the racket
					if self.lastBall.dx > abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return

				elif self.lastBall.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if self.lastBall.dx < abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return
				else:
					return

			elif self.lastBall.isGoingLeft(): #		when the ball is going to be to the left
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()

				elif self.lastBall.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if self.lastBall.dx > abs(rack.dx * rack.fx):
						self.goLeft( maxFactor )
					else:
						return

				elif self.lastBall.isRightOfX( rack.getPosX() ): # the ball is on the right half of the racket
					if self.lastBall.dx < abs(rack.dx * rack.fx):
						self.goRight( maxFactor )
					else:
						return
				else:
					return

			else:
				self.stopHere()

		if rack.dy != 0: #			handling up and down movement
			if rack.isBelow( self.lastBall ): #		when the ball is to the below of the racket
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )

			elif rack.isAbove( self.lastBall ): #	when the ball is to the above of the racket
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )

			elif self.lastBall.isGoingDown(): #		when the ball is going to be to below
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()

				elif self.lastBall.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
					if self.lastBall.dy > abs(rack.dy * rack.fy):
						self.goDown( maxFactor )
					else:
						return

				elif self.lastBall.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if self.lastBall.dy < abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return
				else:
					return

			elif self.lastBall.isGoingUp(): #		when the ball is going to be above
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()

				elif self.lastBall.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if self.lastBall.dy > abs(rack.dy * rack.fy):
						self.goUp( maxFactor )
					else:
						return

				elif self.lastBall.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
					if self.lastBall.dy < abs(rack.dy * rack.fy):
						self.goDown( maxFactor )
					else:
						return
				else:
					return

			else:
				self.stopHere()


	def goTo(self, maxFactor, X, Y):

		if self.racketDir == 'x':
			if self.racket.isRightOfX( X - df.BOT_PRECISION  ):
				if self.allow_hard_break and self.racket.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )
			elif self.racket.isLeftOfX( X + df.BOT_PRECISION  ):
				if self.allow_hard_break and self.racket.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )
			elif self.allow_hard_break:
				self.stopHere()

		elif self.racketDir == 'y':
			if self.racket.isBelowY( Y - df.BOT_PRECISION ):
				if self.allow_hard_break and self.racket.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )
			elif self.racket.isAboveY( Y + df.BOT_PRECISION  ):
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


	def isOnSameSideOf(self, gameObj):

		if self.game.name == "Pi" or self.game.name == "Po" or self.game.name == "Ping":
			return True

		if self.racketDir == 'x':
			if (self.game.height / 2 > self.racket.getPosY()) == (self.game.height / 2 > gameObj.getPosY()):
				return True

		if self.racketDir == 'y':
			if (self.game.width / 2 > self.racket.getPosX()) == (self.game.width / 2 > gameObj.getPosX()):
				return True

		return False


	def isCloserThan(self, gameObj, distance):
		if self.racketDir == 'x':
			if abs( self.racket.getPosY() - gameObj.getPosY() ) <= distance:
				return True
		elif self.racketDir == 'y':
			if abs( self.racket.getPosX() - gameObj.getPosX() ) <= distance:
				return True
		return False


	def isInFrontOf(self, gameObj):
		if self.racketDir == 'x':
			if not gameObj.isLeftOf( self.racket ) and not gameObj.isRightOf( self.racket ):
				return True
		elif self.racketDir == 'y':
			if not gameObj.isAbove( self.racket ) and not gameObj.isBelow( self.racket ):
				return True
		return False


	def isInOwnGoal(self, X, Y, border):

		if self.goal == df.LEFT and X <= border:
			return True
		if self.goal == df.RIGHT and X >= ( self.game.width - border ):
			return True
		if self.goal == df.UP and Y <= border:
			return True
		if self.goal == df.DOWN and Y >= ( self.game.height - border ):
			return True

		return False


	def findNextGoal(self):
		X = self.lastBall.getPosX()
		Y = self.lastBall.getPosY()
		dx = self.lastBall.dx
		dy = self.lastBall.dy
		fx = self.lastBall.fx
		fy = self.lastBall.fy

		border = self.game.size_b * (2 / 3)

		dept = 0

		if self.game.name == "Pongest":
			factor = self.game.factor_rack
		else:
			factor = self.game.factor_wall

		# loops over all the "bounce points" of the ball's trajectory (untill max_search_dept is reached)
		while dept <= df.BOT_SEARCH_DEPTH:
			dept += 1

			# have the ball do one step
			dy += self.game.gravity * fy #			NOTE : assumes normal gravity

			X += dx * fx
			X = int( X )

			Y += dy * fy
			Y = int( Y )

			while df.isInZone( X, Y, border, self.game ):
				if ( dx * fx == 0 ) and ( dy * fy == 0 ):
					break;
				dy += self.game.gravity * fy #		NOTE : assumes normal gravity

				X += dx * fx
				X = int( X )

				Y += dy * fy
				Y = int( Y )

			if self.isInOwnGoal( X, Y, border ):
				return( int( X ) , int ( Y ))

			# make ball bounce on edges
			if X <= border or X >= ( self.game.width - border ):
				fx *= -1
				dx *= factor
			if Y <= border or Y >= ( self.game.height - border ):
				fy *= -1
				dy *= factor


		return( int( X ) , int ( Y ))




