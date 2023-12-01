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

class Pongest(gi.Game):
	name = "Pongest"

	width = 1280
	height = 1280

	speed_b = 6.6667
	speed_m_b = 20
	size_font = 512
	size_l = 14

	factor_rack = 1.05
	factor_wall = 0.5
	racketCount = 4

	iPosR1 = ( width * (1 / 2), gi.Game.size_b			, "x" )
	iPosR2 = ( width - gi.Game.size_b, height * (1 / 2)	, "y" )
	iPosR3 = ( width * (1 / 2), height - gi.Game.size_b	, "x" )
	iPosR4 = ( gi.Game.size_b, height * (1 / 2)			, "y" )

	iPosB1 = ( width * (1 / 2), height * (1 / 2) )

	def initRackets(self):
		# setting up rackets :             id, game, _x            , _y            , _w         , _h
		self.rackets.append( go.GameObject( 1, self, self.iPosR1[0], self.iPosR1[1], self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 2, self, self.iPosR2[0], self.iPosR2[1], self.size_b, self.size_r ))
		self.rackets.append( go.GameObject( 3, self, self.iPosR3[0], self.iPosR3[1], self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 4, self, self.iPosR4[0], self.iPosR4[1], self.size_b, self.size_r ))

		self.rackets[0].setSpeeds( self.speed_r, 0 )
		self.rackets[1].setSpeeds( 0, self.speed_r )
		self.rackets[2].setSpeeds( self.speed_r, 0 )
		self.rackets[3].setSpeeds( 0, self.speed_r )


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.iPosB1[0], self.iPosB1[1], self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b * (1 / 3), self.speed_b )
		self.balls[0].setDirs( 1, -1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handlePygameInputs(self, key): #		NOTE : DEBUG
		# player 1
		if (self.controlers[0].mode == gi.gc.df.PLAYER):
			if key == df.KS:
				self.makeMove( 1, gi.df.STOP )
				self.makeMove( 3, gi.df.STOP )
			elif key == df.KA:
				self.makeMove( 1, gi.df.LEFT )
				self.makeMove( 3, gi.df.LEFT )
			elif key == df.KD:
				self.makeMove( 1, gi.df.RIGHT )
				self.makeMove( 3, gi.df.RIGHT )

		# player 2
		if (self.controlers[1].mode == gi.gc.df.PLAYER):
			if key == df.LEFT:
				self.makeMove( 2, gi.df.STOP )
				self.makeMove( 4, gi.df.STOP )
			elif key == df.UP:
				self.makeMove( 2, gi.df.UP )
				self.makeMove( 4, gi.df.UP )
			elif key == df.DOWN:
				self.makeMove( 2, gi.df.DOWN )
				self.makeMove( 4, gi.df.DOWN )


	# bouncing off the rackets
	def checkRackets(self, ball):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):
				if (rack.id == 1):
					ball.setPosY( rack.getPosY() + self.size_b ) # '+' because the ball is going under
					ball.bounceOnRack( rack, "y" )

				elif (rack.id == 2):
					ball.setPosX( rack.getPosX() - self.size_b ) # '-' because the ball is going left
					ball.bounceOnRack( rack, "x" )

				elif (rack.id == 3):
					ball.setPosY( rack.getPosY() - self.size_b ) # '-' because the ball is going over
					ball.bounceOnRack( rack, "y" )

				elif (rack.id == 4):
					ball.setPosX( rack.getPosX() + self.size_b ) # '+' because the ball is going right
					ball.bounceOnRack( rack, "x" )

				self.scorePoint( rack.id, gi.df.HITS )


	# bouncing on the walls (walls are absent in Pongester)
	def checkWalls(self, ball):
		pass


	# scoring a goal
	def checkGoals(self, ball):
		if ball.getTop() <= 0 or ball.getBottom() >= self.height or ball.getLeft() <= 0 or ball.getRight() >= self.width:
			# increasing score
			if (self.last_ponger > 0):
				self.scorePoint( self.last_ponger, gi.df.GOALS )

			# checking how to respawn the ball
			if self.last_ponger == 1 or ( self.last_ponger == 0 and ball.fx < 0 and ball.fy < 0 ):
				ball.setDirs( -ball.fx, -1 )
				ball.setSpeeds( self.speed_b * (1 / 3), self.speed_b )

			elif self.last_ponger == 2 or ( self.last_ponger == 0 and ball.fx > 0 and ball.fy < 0 ):
				ball.setDirs( 1, -ball.fy )
				ball.setSpeeds( self.speed_b, self.speed_b * (1 / 3) )

			elif self.last_ponger == 3 or ( self.last_ponger == 0 and ball.fx > 0 and ball.fy > 0 ):
				ball.setDirs( -ball.fx, 1 )
				ball.setSpeeds( self.speed_b * (1 / 3), self.speed_b )

			elif self.last_ponger == 4 or ( self.last_ponger == 0 and ball.fx < 0 and ball.fy > 0 ):
				ball.setDirs( -1, -ball.fy )
				ball.setSpeeds( self.speed_b, self.speed_b * (1 / 3) )

			self.respawnBall( ball )


	def respawnBall(self, ball):
		ball.setPos(self.width * (1 / 2), self.height * (1 / 2))


	def drawLines(self):
		pg.draw.line( self.win, df.COL_FNT, ( 0, 0 ),  ( self.width, self.height ), self.size_l )
		pg.draw.line( self.win, df.COL_FNT, ( 0, self.height), ( self.width, 0 ), self.size_l )


	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, df.COL_FNT)
		text2 = self.font.render(f'{self.scores[1]}', True, df.COL_FNT)
		text3 = self.font.render(f'{self.scores[2]}', True, df.COL_FNT)
		text4 = self.font.render(f'{self.scores[3]}', True, df.COL_FNT)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 2), self.height * (1 / 5) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (4 / 5), self.height * (1 / 2) )))
		self.win.blit( text3, text3.get_rect( center = ( self.width * (1 / 2), self.height * (4 / 5) )))
		self.win.blit( text4, text4.get_rect( center = ( self.width * (1 / 5), self.height * (1 / 2) )))


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Pongest(1)

	if cfg.DEBUG_MODE:
		g.setWindow( pg.display.set_mode( (Pongest.width, Pongest.height) ))
		pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()