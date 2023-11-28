try:
	from master import cfg
	if cfg.DEBUG_MODE:
		from master import pg
	from master import go
	from master import gi
	import Addons as ad

except ModuleNotFoundError:
	from game.PingPongRebound.master import cfg
	from game.PingPongRebound.master import go
	from game.PingPongRebound.master import gi
	import game.PingPongRebound.Addons as ad

class Ping(gi.Game):
	name = "Ping"

	width = 2048
	gravity = 0.3
	racketCount = 2
	factor_rack = 1.0
	factor_wall = 0.6

	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (1 / 3), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )

		self.rackets.append( go.GameObject( 2, self, self.width * (2 / 3), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets[1].setSpeeds( self.speed_r, 0 )


	def initControlers(self):
		self.addBot("bot 1")
		self.addBot("bot 2")

	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (2 / 4), self.height * (2 / 3), self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b * (2 / 3), self.speed_b * 2 )
		self.balls[0].setDirs( 1, -1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handlePygameInputs(self, key): #		NOTE : DEBUG

		# player 1
		if (self.controlers[0].mode == gi.gc.ad.PLAYER):
			if key == ad.KS:
				self.makeMove( 1, gi.ad.STOP )
			elif key == ad.KA:
				self.makeMove( 1, gi.ad.LEFT )
			elif key == ad.KD:
				self.makeMove( 1, gi.ad.RIGHT )

		# player 2
		if (self.controlers[1].mode == gi.gc.ad.PLAYER):
			if key == ad.DOWN:
				self.makeMove( 2, gi.ad.STOP )
			elif key == ad.LEFT:
				self.makeMove( 2, gi.ad.LEFT )
			elif key == ad.RIGHT:
				self.makeMove( 2, gi.ad.RIGHT )


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos(self.speed_m_r)

		# prevent racket from going off screen
		if (not rack.isInScreen()):
			rack.bounceOnWall( "stop" )

		# prevent racket from crossing the middle line
		if rack.id == 1 and rack.getRight() > self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX( (self.width - self.size_r) / 2 )
		elif rack.id == 2 and rack.getLeft() < self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX( (self.width + self.size_r) / 2 )

		rack.clampPos()


	# scoring a goal
	def checkGoals(self, ball):
		if ball.getBottom() >= self.height:

			# checking who scored
			if ball.getRight() < self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 2, gi.ad.GOALS )
				ball.setDirs( -1, -1 )

			if ball.getLeft() > self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 1, gi.ad.GOALS )
				ball.setDirs( 1, -1 )

			self.respawnBall( ball )

	def respawnBall(self, ball):
		ball.setPos( self.width * (1 / 2), self.height * (2 / 3) )
		ball.setSpeeds( (ball.dx + self.speed_b) / 3, self.speed_b * 2 )


	def drawLines(self):
		pg.draw.line( self.win, ad.COL_FNT, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )

		pg.draw.line( self.win, ad.COL_FNT, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, ad.COL_FNT, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, ad.COL_FNT, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )



	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, ad.COL_FNT)
		text2 = self.font.render(f'{self.scores[1]}', True, ad.COL_FNT)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 4), self.height * (2 / 4) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (3 / 4), self.height * (2 / 4) )))


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Ping(1)

	if cfg.DEBUG_MODE:
		g.setWindow( pg.display.set_mode( (Ping.width, Ping.height) ))
		pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()