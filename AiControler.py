import GameControler as gc
import Addons as ad

# controler class
class AiControler(gc.GameControler):

	allow_hard_break = True
	go_to_center = False # is fucky in ping and pinger
	stop_distance = 120
	play_frequency = 12
	mf = 4

	step = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.mode = ad.BOT


	def playStep(self):
		if self.isActive:
			#if (self.step % self.play_frequency) == 0:
				#self.playAutoMove()
				#self.step = 0
			#self.step += 1
			self.playAutoMove()
		else:
			raise ValueError("Error: bot is deactivated")


	def playAutoMove(self):
		if self.go_to_center and self.isBallFar( self.game.balls[0] ):
			self.goToCenter( self.mf )
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


	def goToCenter(self, maxFactor):
		if self.racket.dx != 0:
			if self.racket.isRightOfX( self.game.width / 2 ):
				self.goLeft( maxFactor )
			elif self.racket.isLeftOfX( self.game.width / 2 ):
				self.goRight( maxFactor )
			else:
				self.stopHere()

		elif self.racket.dy != 0:
			if self.racket.isBelowY( self.game.height / 2 ):
				self.goUp( maxFactor )
			elif self.racket.isAboveY( self.game.height / 2 ):
				self.goDown( maxFactor )
			else:
				self.stopHere()


	def isBallNear(self, ball):
		if self.racket.dx != 0 and (self.game.height / 2 > self.racket.box.centery) == (self.game.height / 2 > ball.box.centery):
			return True
		if self.racket.dy != 0 and (self.game.width / 2 > self.racket.box.centerx) == (self.game.width / 2 > ball.box.centerx):
			return True
		return False

	def isBallFar(self, ball):
		return not self.isBallNear(ball)

