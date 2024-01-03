try:
	from master import gc
	import defs as df
except ModuleNotFoundError:
	from game.PingPongRebound.master import gc
	import game.PingPongRebound.defs as df

# controler class
class BotControler( gc.GameControler ):

	allow_hard_break = df.BOT_HARD_BREAK
	go_to_default = df.BOT_GO_TO_DEFAULT

	max_factor = df.BOT_M_FACTOR #( max speed factor( how many times dx or dy can the racket go at )

	mode = df.BOT

	# ----------------------------------------------- BASICS ----------------------------------------------- #


	def __init__( self, _game, _botName, _difficulty ):
		self.game = _game
		self.name = _botName

		self.defaultX = _game.width / 2
		self.defaultY = _game.height / 2

		self.border = self.game.size_b * ( 1 / 2 )

		self.frequency_offset = 0
		self.step = 0
		self.goal = df.NULL

		self.lastBall = None
		self.nextGoal = None

		self.seeBall()

		# self.tmp = 0 #				NOTE : DEBUG (remove me)

		self.difficulty = _difficulty
		if self.difficulty == df.EASY:
			self.allow_hard_break = False
			self.max_factor -= 1


	def handleKeyInput( self, key ):
		print( "Warning : cannot give key inputs to a bot" )


	def setFrequencyOffset( self, r_count ):
		self.frequency_offset = int(( float( self.racket.id ) / r_count ) * df.BOT_PLAY_FREQUENCY )


	def seeBall( self ):
		self.lastBall = self.game.balls[ 0 ].getCopy()
		self.nextGoal = None


	# --------------------------------------------- MOVEMENTS ---------------------------------------------- #


	def playMove( self, move = df.NULL ):
		if move == df.NULL:
			self.playAutoMove()
		else:
			self.game.makeMove( self.racket.id, move )


	def playAutoMove( self ):
		if not df.BOT_CAN_PLAY:
			return

		# if the ball is near, the bot will react instantly
		elif df.BOT_INSTANT_REACT or ( df.BOT_QUICK_REACT and self.isNear( self.lastBall )):
			self.seeBall()

		if self.difficulty == df.EASY:
			self.seeBall()
			self.goTo( self.max_factor, self.lastBall.getPosX(), self.lastBall.getPosY() )

		elif self.difficulty == df.MEDIUM:
			self.seeBall()
			if self.go_to_default and not self.isOnSameSideOf( self.lastBall ):
				self.goToDefaultPos( self.max_factor )
			else:
				self.goTowardsBall( self.max_factor )
			return

		elif self.difficulty == df.HARD:
			if self.canKickBall():
				self.kickBall()
			else:
				self.goToNextGoal( self.max_factor )


	def goTo( self, maxFactor, px, py ):

		if self.racketDir == 'x':
			tolerance = ( self.racket.sx - df.BOT_PRECISION )

			if self.racket.isRightOfX( px - tolerance):
				if self.allow_hard_break and self.racket.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )

			elif self.racket.isLeftOfX( px + tolerance ):
				if self.allow_hard_break and self.racket.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )

			elif self.allow_hard_break:
				self.stopHere()

		elif self.racketDir == 'y':
			tolerance = ( self.racket.sy - df.BOT_PRECISION )

			if self.racket.isBelowY( py - tolerance ):
				if self.allow_hard_break and self.racket.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )

			elif self.racket.isAboveY( py + tolerance ):
				if self.allow_hard_break and self.racket.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )

			elif self.allow_hard_break:
				self.stopHere()


	# ---------------------------------------------- KICKING ----------------------------------------------- #

	#	makes kick_distance proportional to ball speed
	def getKickDist( self ):

		speed = self.game.speed_m_b
		damp = 30

		if self.racketDir == 'x':
			speed = self.lastBall.dy
		elif self.racketDir == 'y':
			speed = self.lastBall.dx
		else:
			print( "Warning : racketDir is not set" )
			return df.BOT_KICK_DIST

		kickFactor = (( speed + damp ) / ( self.game.speed_m_b + damp ))

		#print( f"speed      : {speed}")
		#print( "kickFactor : {:.3f}".format( kickFactor ))
		#print( f"distance   : {int( 2 * df.BOT_KICK_DIST * kickFactor )}")

		return int( 2 * df.BOT_KICK_DIST * kickFactor )


	def canKickBall( self ):
		if not df.BOT_CAN_KICK:
			return False
		if self.game.score_count < 2:
			return False
		if not self.isInFrontOf( self.lastBall ):
			return False
		if not self.isCloserThan( self.lastBall, self.getKickDist() ):
			return False
		return True


	def kickBall( self ):
		if self.game.type == "Ping":
			self.goToCenter( df.BOT_KICK_SPEED )
			return

		rack = self.racket
		ball = self.lastBall

		if self.racketDir == 'x':
			if ball.isGoingLeft():

				if ball.isLeftOfX( rack.getPosX() + df.BOT_PRECISION ):
					self.goLeft( df.BOT_KICK_SPEED )
					return

				else:
					self.goRight( df.BOT_KICK_SPEED )
					return
			else:

				if ball.isRightOfX( rack.getPosX() - df.BOT_PRECISION ):
					self.goRight( df.BOT_KICK_SPEED )
					return

				else:
					self.goLeft( df.BOT_KICK_SPEED )
					return

		if self.racketDir == 'y':
			if ball.isGoingUp():

				if ball.isAboveY( rack.getPosY() + df.BOT_PRECISION ):
					self.goUp( df.BOT_KICK_SPEED )
					return

				else:
					self.goDown( df.BOT_KICK_SPEED )
					return
			else:

				if ball.isBelowY( rack.getPosY() - df.BOT_PRECISION ):
					self.goDown( df.BOT_KICK_SPEED )
					return

				else:
					self.goUp( df.BOT_KICK_SPEED )
					return

		# if there is no good kick, continue as normal
		self.goToNextGoal( self.max_factor )
		return


		# attempt at new code, is eh0
		if self.racketDir == 'x':

			if ball.isGoingLeft():
				if rack.isRightOfX( ball.px - rack.sx - df.BOT_PRECISION ): #	when the ball is left of the racket's right half
					self.goLeft( df.BOT_KICK_SPEED )
					return

				elif rack.isLeftOfX( ball.px + rack.sx - df.BOT_PRECISION ): #	when the ball is right of the racket's right half
					self.goRight( df.BOT_KICK_SPEED )
					return
			else:
				if rack.isLeftOfX( ball.px + rack.sx + df.BOT_PRECISION ): #	when the ball is right of the racket's left half
					self.goRight( df.BOT_KICK_SPEED )
					return

				elif rack.isRightOfX( ball.px - rack.sx + df.BOT_PRECISION ): #	when the ball is left of the racket's left half
					self.goLeft( df.BOT_KICK_SPEED )
					return

		if self.racketDir == 'y':

			if ball.isGoingUp():
				if rack.isBelowY( ball.py - rack.sy - df.BOT_PRECISION ): #		when the ball is above the racket's bottom half
					self.goUp( df.BOT_KICK_SPEED )
					return

				elif rack.isAboveY( ball.py + rack.sy - df.BOT_PRECISION ): #	when the ball is bellow the racket's bottom half
					self.goDown( df.BOT_KICK_SPEED )
					return
			else:
				if rack.isAboveY( ball.py + rack.sy + df.BOT_PRECISION ): #		when the ball is bellow the racket's top half
					self.goDown( df.BOT_KICK_SPEED )
					return

				elif rack.isBelowY( ball.py - rack.sy + df.BOT_PRECISION ): #	when the ball is above the racket's top half
					self.goUp( df.BOT_KICK_SPEED )
					return


	# ---------------------------------------------- CHECKS ------------------------------------------------ #


	def isOnSameSideOf( self, gameObj ):
		if self.game.type == "Pi" or self.game.type == "Po" or self.game.type == "Ping":
			return True
		if self.racketDir == 'x':
			if( self.game.height / 2 > self.racket.getPosY() ) == ( self.game.height / 2 > gameObj.getPosY() ):
				return True
		if self.racketDir == 'y':
			if( self.game.width / 2 > self.racket.getPosX() ) == ( self.game.width / 2 > gameObj.getPosX() ):
				return True

		return False


	def isCloserThan( self, gameObj, distance ):
		#self.tmp += 1 #													NOTE : DEBUG (remove me)

		if abs( self.racket.getPosY() - gameObj.getPosY() ) <= distance:
			if abs( self.racket.getPosX() - gameObj.getPosX() ) <= distance:
				#print ( f"{self.racket.id} )  Closeby {self.tmp}" ) #		NOTE : DEBUG (remove me)
				return True

		#self.tmp = 0 #														NOTE : DEBUG (remove me)
		return False


	def isInFrontOf( self, gameObj ):
		if self.racketDir == 'x':
			if not gameObj.isLeftOf( self.racket ) and not gameObj.isRightOf( self.racket ):
				return True
		elif self.racketDir == 'y':
			if not gameObj.isAbove( self.racket ) and not gameObj.isBelow( self.racket ):
				return True
		return False


	def isNear( self, gameObj ):
		if abs( self.racket.getPosY() - gameObj.getPosY() ) <= df.BOT_REACT_DIST:
			if abs( self.racket.getPosX() - gameObj.getPosX() ) <= df.BOT_REACT_DIST:
				return True
		return False


	def isInOwnGoal( self, px, py ):
		if self.goal == df.LEFT and px < self.racket.px + self.racket.sx:
			return True
		if self.goal == df.RIGHT and px > self.racket.px + self.racket.sx:
			return True
		if self.goal == df.UP and py < self.racket.py + self.racket.sy:
			return True
		if self.goal == df.DOWN and py > self.racket.py + self.racket.sy:
			return True

		return False


	# -------------------------------------------- SMART FOLLOW -------------------------------------------- #


	def goTowardsBall( self, maxFactor ):

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
					if self.lastBall.dx > abs( rack.dx * rack.fx ):
						self.goRight( maxFactor )
					else:
						return

				elif self.lastBall.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if self.lastBall.dx < abs( rack.dx * rack.fx ):
						self.goLeft( maxFactor )
					else:
						return
				else:
					return

			elif self.lastBall.isGoingLeft(): #		when the ball is going to be to the left
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()

				elif self.lastBall.isLeftOfX( rack.getPosX() ): # the ball is on the left half of the racket
					if self.lastBall.dx > abs( rack.dx * rack.fx ):
						self.goLeft( maxFactor )
					else:
						return

				elif self.lastBall.isRightOfX( rack.getPosX() ): # the ball is on the right half of the racket
					if self.lastBall.dx < abs( rack.dx * rack.fx ):
						self.goRight( maxFactor )
					else:
						return
				else:
					return

			else:
				self.stopHere()

		if rack.dy != 0: #			handling up and down movement
			if rack.isBelow( self.lastBall ): #		when the ball is  below of the racket
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )

			elif rack.isAbove( self.lastBall ): #	when the ball is  above of the racket
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )

			elif self.lastBall.isGoingDown(): #		when the ball is going to be to below
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()

				elif self.lastBall.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
					if self.lastBall.dy > abs( rack.dy * rack.fy ):
						self.goDown( maxFactor )
					else:
						return

				elif self.lastBall.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if self.lastBall.dy < abs( rack.dy * rack.fy ):
						self.goUp( maxFactor )
					else:
						return
				else:
					return

			elif self.lastBall.isGoingUp(): #		when the ball is going to be above
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()

				elif self.lastBall.isAboveY( rack.getPosY() ): # the ball is on the upper half of the racket
					if self.lastBall.dy > abs( rack.dy * rack.fy ):
						self.goUp( maxFactor )
					else:
						return

				elif self.lastBall.isBelowY( rack.getPosY() ): # the ball is on the lower half of the racket
					if self.lastBall.dy < abs( rack.dy * rack.fy ):
						self.goDown( maxFactor )
					else:
						return
				else:
					return

			else:
				self.stopHere()


	# ------------------------------------------ GOAL PREDICTION ------------------------------------------- #


	def goToNextGoal( self, maxFactor ):
		self.findNextGoal()
		( px, py ) = self.nextGoal
		self.goTo( maxFactor, px, py )


	def calculateStep( self, px, py, dx, dy, fx, fy ):
		# calculates gravity (only in dy)
		dy += self.game.gravity * df.getSign( fy )

		# clamps dx and dy to positive values
		if ( dx < 0 ):
			dx *= -1
			fx *= -1
		if ( dy < 0 ):
			dy *= -1
			fy *= -1

		# uptades position
		px += dx * fx
		py += dy * fy

		return( int( px ), int( py ), dx, dy, int( fx ), int( fy ))


	def bounceOnX( self, px, py, dx, dy, fx, fy, factor ):
		dx *= factor
		fx *= -1

		# clamps the ball's position to the screen
		if px <= self.border:
			px = self.border
		else:
			px = self.game.width - self.border

		# unstucks x
		if dx == 0:
			dx = 1

			if px < self.game.width / 2:
				fx = 1
			else:
				fx = -1

		return( int( px ), int( py ), dx, dy, int( fx ), int( fy ))


	def bounceOnY( self, px, py, dx, dy, fx, fy, factor ):
		dy *= factor
		fy *= -1

		# clamps the ball's position to the screen
		if py <= self.border:
			py = self.border
		else:
			py = self.game.height - self.border

		# unstucks y
		if dy == 0:
			dy = 1

			if py < self.game.height / 2:
				fy = 1
			else:
				fy = -1

		return( int( px ), int( py ), dx, dy, int( fx ), int( fy ))


	def findNextGoal( self ):
		# prevents redoing the same calculations when not needed
		if self.nextGoal != None:
			return self.nextGoal

		px = self.lastBall.px
		py = self.lastBall.py
		dx = self.lastBall.dx
		dy = self.lastBall.dy
		fx = self.lastBall.fx
		fy = self.lastBall.fy

		g = self.game
		dept = 0

		if g.type == "Pongest":
			factor = g.factor_rack
		else:
			factor = g.factor_wall

		# loops over all the "bounce points" of the ball's trajectory( untill max_search_dept is reached )
		while dept <= df.BOT_SEARCH_DEPTH:
			dept += 1

			# do steps until goal is reached (or ball is stuck)
			while( True ):

				# does one game step
				( px, py, dx, dy, fx, fy ) = self.calculateStep( px, py, dx, dy, fx, fy)

				# returns where to be to block the next potential goal
				if self.isInOwnGoal( px, py ):
					self.nextGoal = ( int( px ), int( py ))
					return

				# breaks if the ball is on screen edge
				if not df.isInZone( px, py, self.border, self.border, g.width - self.border, g.height - self.border ):
					break

			# bounces the ball on horizontal ( __ ) edges if need be
			if px <= self.border or px >= ( g.width - self.border ):
				( px, py, dx, dy, fx, fy ) = self.bounceOnX( px, py, dx, dy, fx, fy, factor )

			# bounces the ball on vertical ( | ) edges if need be
			if py <= self.border or py >= ( g.height - self.border ):
				( px, py, dx, dy, fx, fy ) = self.bounceOnY( px, py, dx, dy, fx, fy, factor )

		# if no potential goal is found at this dept, go back to default position
		self.nextGoal = ( self.defaultX, self.defaultY )







