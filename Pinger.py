from master import pg
from master import go
from master import gi
import Addons as ad

class Pinger(gi.Game):
	name = "Pinger"

	racketCount = 4

	def initRackets(self):
		# setting up rackets :             id, game, _x                  , _y                       , _w         , _h
		self.rackets.append( go.GameObject( 1, self, self.width * (2 / 7), self.size_b		        , self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 2, self, self.width * (5 / 7), self.size_b	            , self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 3, self, self.width * (2 / 7), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 4, self, self.width * (5 / 7), self.height - self.size_b, self.size_r, self.size_b ))

		self.rackets[0].setSpeeds( self.speed_r, 0 )
		self.rackets[1].setSpeeds( self.speed_r, 0 )
		self.rackets[2].setSpeeds( self.speed_r, 0 )
		self.rackets[3].setSpeeds( self.speed_r, 0 )


	def initControlers(self):
		self.addBot("bot 1")
		self.addBot("bot 2")
		self.addBot("bot 3")
		self.addBot("bot 4")


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (1 / 4), self.height * (1 / 4) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, self.speed_b * (2 / 3) )
		self.balls[0].setDirs( 1, 1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handlePygameInputs(self, key): #		NOTE : DEBUG
		# player 1
		if (self.controlers[0].mode == gi.gc.ad.PLAYER):
			if key == ad.KS:
				self.makeMove( 1, gi.ad.STOP )
				self.makeMove( 3, gi.ad.STOP )
			elif key == ad.KA:
				self.makeMove( 1, gi.ad.LEFT )
				self.makeMove( 3, gi.ad.LEFT )
			elif key == ad.KD:
				self.makeMove( 1, gi.ad.RIGHT )
				self.makeMove( 3, gi.ad.RIGHT )

		# player 2
		if (self.controlers[1].mode == gi.gc.ad.PLAYER):
			if key == ad.DOWN:
				self.makeMove( 2, gi.ad.STOP )
				self.makeMove( 4, gi.ad.STOP )
			elif key == ad.LEFT:
				self.makeMove( 2, gi.ad.LEFT )
				self.makeMove( 4, gi.ad.LEFT )
			elif key == ad.RIGHT:
				self.makeMove( 2, gi.ad.RIGHT )
				self.makeMove( 4, gi.ad.RIGHT )


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos(self.speed_m_r)

		# prevent racket from going off screen
		if (not rack.isInScreen()):
			rack.bounceOnWall( "stop" )

		# prevent racket from crossing the middle line
		if (rack.id == 1 or rack.id == 3) and rack.getRight() > self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX( (self.width - self.size_r) / 2 )
		elif (rack.id == 2 or rack.id == 4) and rack.getLeft() < self.width / 2:
			rack.bounceOnWall( "stop" )
			rack.setPosX( (self.width + self.size_r) / 2 )

		rack.clampPos()


	# bouncing off the rackets
	def checkRackets(self, ball):
		for rack in self.rackets: #		copies the racket's data
			if ball.isOverlaping( rack ):

				if (rack.id == 1 or rack.id == 2):
					ball.setPosY( rack.getPosY() + self.size_b ) # '+' because the ball is going under
				elif (rack.id == 3 or rack.id == 4):
					ball.setPosY( rack.getPosY() - self.size_b ) # '-' because the ball is going over

				ball.bounceOnRack( rack, "y" )
				self.scorePoint( rack.id, gi.ad.HITS )


	# bouncing on the walls
	def checkWalls(self, ball):
		# bouncing off the sides
		if ball.getLeft() <= 0 or ball.getRight() >= self.width:
			ball.bounceOnWall( "x" )


	# scoring a goal
	def checkGoals(self, ball):
		if ball.getTop() <= 0 or ball.getBottom() >= self.height:

			# checking who scored
			if ball.getRight() < self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 2, gi.ad.GOALS )
				ball.setDirs( -ball.fy, -1 )
				ball.setPos ( self.width * (3 / 4), self.height * (3 / 4) )

			if ball.getLeft() > self.width / 2:
				if self.last_ponger > 0:
					self.scorePoint( 1, gi.ad.GOALS )
				ball.setDirs( -ball.fy, 1 )
				ball.setPos ( self.width * (1 / 4), self.height * (1 / 4) )

			self.respawnBall( ball )


	def respawnBall(self, ball):
		ball.setSpeeds( ( self.speed_b + ball.dx ) * (1 / 2), self.speed_b * (2 / 3) )


	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( 0, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( self.width / 2, 0 ), ( self.width / 2, self.height ), self.size_l )
		pg.draw.line( self.win, self.col_fnt, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2)


	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, self.col_fnt)
		text2 = self.font.render(f'{self.scores[1]}', True, self.col_fnt)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 4), self.height * (2 / 4) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (3 / 4), self.height * (2 / 4) )))


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Pinger(True)

	g.setWindow(pg.display.set_mode((1280, 1280)))
	pg.display.set_caption(g.name)

	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()