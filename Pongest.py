import pygame as pg
import GameObject as go
import GameInterface as gi

class Pongest(gi.Game):
	name = "Pongest"

	width = 1280
	height = 1280

	speed_b = 7.5
	speed_m_b = 15
	size_font = 512

	factor_rack = 1.05
	factor_wall = 0.5
	racketCount = 4

	def initRackets(self):
		# setting up rackets :             id, game, _x                      , _y                       , _w         , _h
		self.rackets.append( go.GameObject( 1, self, self.width * (1 / 2)    , self.size_b              , self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 2, self, self.width - self.size_b, self.height * (1 / 2)    , self.size_b, self.size_r ))
		self.rackets.append( go.GameObject( 3, self, self.width * (1 / 2)    , self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 4, self, self.size_b             , self.height * (1 / 2)    , self.size_b, self.size_r ))

		self.rackets[0].setSpeeds( self.speed_r, 0 )
		self.rackets[1].setSpeeds( 0, self.speed_r )
		self.rackets[2].setSpeeds( self.speed_r, 0 )
		self.rackets[3].setSpeeds( 0, self.speed_r )


	def initControlers(self):
		self.addBot("bot 1")
		self.addBot("bot 2")
		self.addBot("bot 3")
		self.addBot("bot 4")


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (1 / 2), self.height * (1 / 2) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b * (1 / 3), self.speed_b )
		self.balls[0].setDirs( 1, -1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handlePygameInputs(self, key): #		NOTE : DEBUG
		# player 1
		if (self.controlers[0].mode == gi.gc.ad.PLAYER):
			if key == pg.K_s:
				self.makeMove( 1, gi.ad.STOP )
				self.makeMove( 3, gi.ad.STOP )
			elif key == pg.K_a:
				self.makeMove( 1, gi.ad.LEFT )
				self.makeMove( 3, gi.ad.LEFT )
			elif key == pg.K_d:
				self.makeMove( 1, gi.ad.RIGHT )
				self.makeMove( 3, gi.ad.RIGHT )

		# player 2
		if (self.controlers[1].mode == gi.gc.ad.PLAYER):
			if key == pg.K_LEFT:
				self.makeMove( 2, gi.ad.STOP )
				self.makeMove( 4, gi.ad.STOP )
			elif key == pg.K_UP:
				self.makeMove( 2, gi.ad.UP )
				self.makeMove( 4, gi.ad.UP )
			elif key == pg.K_DOWN:
				self.makeMove( 2, gi.ad.DOWN )
				self.makeMove( 4, gi.ad.DOWN )


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

				self.scorePoint( rack.id, gi.ad.HITS )


	# bouncing on the walls (walls are absent in Pongester)
	def checkWalls(self, ball):
		pass


	# scoring a goal
	def checkGoals(self, ball):
		if ball.getTop() <= 0 or ball.getBottom() >= self.height or ball.getLeft() <= 0 or ball.getRight() >= self.width:
			# increasing score
			if (self.last_ponger > 0):
				self.scorePoint( self.last_ponger, gi.ad.GOALS )

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
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ),  ( self.width, self.height ), self.size_l )
		pg.draw.line( self.win, self.col_fnt, ( 0, self.height), ( self.width, 0 ), self.size_l )


	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, self.col_fnt)
		text2 = self.font.render(f'{self.scores[1]}', True, self.col_fnt)
		text3 = self.font.render(f'{self.scores[2]}', True, self.col_fnt)
		text4 = self.font.render(f'{self.scores[3]}', True, self.col_fnt)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 2), self.height * (1 / 5) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (4 / 5), self.height * (1 / 2) )))
		self.win.blit( text3, text3.get_rect( center = ( self.width * (1 / 2), self.height * (4 / 5) )))
		self.win.blit( text4, text4.get_rect( center = ( self.width * (1 / 5), self.height * (1 / 2) )))


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Pongest(True)

	g.setWindow(pg.display.set_mode((1280, 1280)))
	pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()