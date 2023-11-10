import GameControler as gc

# controler class
class AiControler(gc.GameControler):

	auto_play = False
	allow_hard_break = False
	play_frequency = 1

	step = 0

	def playStep(self):
		# using ai move instead (if set to auto play)
		if self.auto_play:
			if (self.step % self.play_frequency) == 0:
				self.findNextMove()
				self.step = 0
			self.step += 1
		self.playMove( self.next_move )


	def findNextMove(self):
		if self.racket == 0:
			raise ValueError("Error: no racket selected")

		ball = self.game.balls[0]

		# handling left and right movement
		if ball.box.centerx <= self.racket.box.left:
			self.next_move = self.game.LEFT
		elif ball.box.centerx >= self.racket.box.right:
			self.next_move = self.game.RIGHT

		# handling up and down movement
		if ball.box.centery <= self.racket.box.top:
			self.next_move = self.game.UP
		elif ball.box.centery >= self.racket.box.bottom:
			self.next_move = self.game.DOWN

		# handling left and right movement (when ball is in front)
		if ball.box.centerx > self.racket.box.left and ball.box.centerx < self.racket.box.right:
			if (ball.fx < 0):
				self.next_move = self.game.LEFT
			elif (ball.fx > 0):
				self.next_move = self.game.RIGHT
			else:
				self.next_move = self.game.STOP

		# handling up and down movement (when ball is in front)
		if ball.box.centery > self.racket.box.top and ball.box.centery < self.racket.box.bottom:
			if (ball.fy < 0):
				self.next_move = self.game.UP
			elif (ball.fy > 0):
				self.next_move = self.game.DOWN
			else:
				self.next_move = self.game.STOP


		# handling hard break (if allowed)			NOTE : eh, fucky behaviour
		if self.allow_hard_break:
			if ball.box.centerx > self.racket.box.left and ball.box.centerx < self.racket.box.right:
				self.next_move = self.game.STOP
			if ball.box.centery > self.racket.box.top and ball.box.centery < self.racket.box.bottom:
				self.next_move = self.game.STOP