import GameControler as gc

# controler class
class AiControler(gc.GameControler):

	allow_hard_break = False
	play_frequency = 6

	step = 0

	def playStep(self):

		# 	using ai move (if set to auto play)
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
			if ball.box.centerx <= self.racket.box.left:
				return self.game.LEFT
			elif ball.box.centerx >= self.racket.box.right:
				return self.game.RIGHT
			else: #								when ball is in front
				if self.allow_hard_break: #		NOTE : eh, fucky behaviour
					return self.game.STOP
				if (ball.fx < 0):
					return self.game.LEFT
				elif (ball.fx > 0):
					return self.game.RIGHT
				else:
					return self.game.STOP

		# handling up and down movement
		elif self.racket.dy != 0:
			if ball.box.centery <= self.racket.box.top:
				return self.game.UP
			elif ball.box.centery >= self.racket.box.bottom:
				return self.game.DOWN
			else: #								when ball is in front
				if self.allow_hard_break : #	NOTE : eh, fucky behaviour
					return self.game.STOP
				elif (ball.fy < 0):
					return self.game.UP
				elif (ball.fy > 0):
					return self.game.DOWN
				else:
					return self.game.STOP

