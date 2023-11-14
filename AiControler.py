import GameControler as gc
import Addons as ad

# controler class
class AiControler(gc.GameControler):

	allow_hard_break = True
	stop_distance = 120
	play_frequency = 10
	mf = 3

	step = 0


	def __init__(self, _game, _playerName):
		self.game = _game
		self.name = _playerName
		self.mode = ad.BOT


	def playStep(self):
		if self.isActive:
			if (self.step % self.play_frequency) == 0:
				self.playAutoMove()
				self.step = 0
			self.step += 1
		else:
			raise ValueError("Error: bot is deactivated")


	def playAutoMove(self):
		if self.isBallNear( self.game.balls[0] ):
			self.goTowardsBall( self.mf, self.game.balls[0] )
		else:
			self.goToCenter( self.mf )
		return

		if self.racket == 0:
			raise ValueError("Error: no racket selected")

		ball = self.game.balls[0]
		self.next_move = ad.NULL

		# handling left and right movement
		if self.racket.dx != 0:
			if  abs(ball.box.centery - self.racket.box.centery) < self.stop_distance: # and ad.getSign(ball.fx) != ad.getSign(self.racket.fx):
				self.playMove( ad.STOP )
			elif ball.box.centerx <= self.racket.box.left:
				self.playMove( ad.LEFT )
			elif ball.box.centerx >= self.racket.box.right:
				self.playMove( ad.RIGHT )
			else: #						when ball is in front
				if self.allow_hard_break:
					self.playMove( ad.STOP )
				if ball.fx < 0 and ball.box.centerx < self.racket.box.centerx:
					self.playMove( ad.LEFT )
				elif ball.fx > 0 and ball.box.centerx > self.racket.box.centerx:
					self.playMove( ad.RIGHT )

		# handling up and down movement
		elif self.racket.dy != 0:
			if abs(ball.box.centerx - self.racket.box.centerx) < self.stop_distance: # and ad.getSign(ball.fy) != ad.getSign(self.racket.fy):
				self.playMove( ad.STOP )
			elif ball.box.centery <= self.racket.box.top:
				self.playMove( ad.UP )
			elif ball.box.centery >= self.racket.box.bottom:
				self.playMove( ad.DOWN )
			else: #						when ball is in front
				if self.allow_hard_break :
					self.playMove( ad.STOP )
				elif ball.fy < 0 and ball.box.centery < self.racket.box.centery:
					self.playMove( ad.UP )
				elif ball.fy > 0 and ball.box.centery > self.racket.box.centery:
					self.playMove( ad.DOWN )

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

		# handling left and right movement
		if rack.dx != 0:
			#if self.allow_hard_break and abs(ball.box.centery - self.racket.box.centery) < self.stop_distance: # when ball is in front
				#self.stopHere()

			if rack.isRightOf( ball ):
				if self.allow_hard_break and rack.isGoingRight():
					self.stopHere()
				else:
					self.goLeft( maxFactor )

			elif rack.isLeftOf( ball ):
				if self.allow_hard_break and rack.isGoingLeft():
					self.stopHere()
				else:
					self.goRight( maxFactor )

			elif ball.isLeftOfX( rack.box.centerx ) and ball.isGoingLeft():
				self.goLeft( maxFactor )
			elif ball.isRightOfX( rack.box.centerx ) and ball.isGoingRight():
				self.goRight( maxFactor )
			#else:
				#self.stopHere()

		# handling up and down movement
		if rack.dy != 0:
			#if self.allow_hard_break and abs(ball.box.centerx - self.racket.box.centerx) < self.stop_distance:
				#self.stopHere()

			if rack.isBelow( ball ):
				if self.allow_hard_break and rack.isGoingDown():
					self.stopHere()
				else:
					self.goUp( maxFactor )

			elif rack.isAbove( ball ):
				if self.allow_hard_break and rack.isGoingUp():
					self.stopHere()
				else:
					self.goDown( maxFactor )

			elif ball.isAboveY( rack.box.centery ) and ball.isGoingUp():
				self.goUp( maxFactor )
			elif ball.isBelowY( rack.box.centery ) and ball.isGoingDown():
				self.goDown( maxFactor )
			#else:
				#self.stopHere()

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

