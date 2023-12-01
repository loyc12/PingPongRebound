try:
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg
	from master import go
	from master import gi
	import defs as df

except ModuleNotFoundError:
	import game.PingPongRebound.cfg as cfg
	from game.PingPongRebound.master import go
	from game.PingPongRebound.master import gi
	import game.PingPongRebound.defs as df

class Ping(gi.Game):
	name = "Ping"

	width = 2048
	height = 1024
	gravity = 0.3
	racketCount = 2
	factor_rack = 1.0
	factor_wall = 0.6

	iPosR1 = ( width * (1 / 3), height - gi.Game.size_b, "x" )
	iPosR2 = ( width * (2 / 3), height - gi.Game.size_b, "x" )

	iPosB1 = ( width * (2 / 4), height * (2 / 3) )


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[0], self.iPosR1[1], self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )

		self.rackets.append( go.GameObject( 2, self, self.iPosR2[0], self.iPosR2[1], self.size_r, self.size_b ))
		self.rackets[1].setSpeeds( self.speed_r, 0 )


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[0], self.iPosB1[1], self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b * (2 / 3), self.speed_b * 2 )
		self.balls[0].setDirs( 1, -1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handlePygameInputs(self, key): #		NOTE : DEBUG

		# player 1
		if (self.controlers[0].mode == gi.gc.df.PLAYER):
			if key == df.KS:
				self.makeMove( 1, gi.df.STOP )
			elif key == df.KA:
				self.makeMove( 1, gi.df.LEFT )
			elif key == df.KD:
				self.makeMove( 1, gi.df.RIGHT )

		# player 2
		if (self.controlers[1].mode == gi.gc.df.PLAYER):
			if key == df.DOWN:
				self.makeMove( 2, gi.df.STOP )
			elif key == df.LEFT:
				self.makeMove( 2, gi.df.LEFT )
			elif key == df.RIGHT:
				self.makeMove( 2, gi.df.RIGHT )


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
					self.scorePoint( 2, gi.df.GOALS )
				ball.setDirs( -1, -1 )

			if ball.getLeft() > self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 1, gi.df.GOALS )
				ball.setDirs( 1, -1 )

			self.respawnBall( ball )

	def respawnBall(self, ball):
		ball.setPos( self.width * (1 / 2), self.height * (2 / 3) )
		ball.setSpeeds( (ball.dx + self.speed_b) / 3, self.speed_b * 2 )


	def drawLines(self):
		pg.draw.line( self.win, df.COL_FNT, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )

		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )



	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, df.COL_FNT)
		text2 = self.font.render(f'{self.scores[1]}', True, df.COL_FNT)

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