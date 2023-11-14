import pygame as pg
import GameObject as go
import GameInterface as gi

class Ponger(gi.Game):
	name = "Ponger"

	def initRackets(self):
		# setting up rackets :             id, game, _x                  , _y                       , _w         , _h
		self.rackets.append( go.GameObject( 1, self, self.width * (1 / 4), self.size_b		        , self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 2, self, self.width * (3 / 4), self.size_b	            , self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 3, self, self.width * (1 / 4), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets.append( go.GameObject( 4, self, self.width * (3 / 4), self.height - self.size_b, self.size_r, self.size_b ))

		self.rackets[0].setSpeeds( self.speed_r, 0 )
		self.rackets[1].setSpeeds( self.speed_r, 0 )
		self.rackets[2].setSpeeds( self.speed_r, 0 )
		self.rackets[3].setSpeeds( self.speed_r, 0 )

		self.racketCount = 4


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


	def handlePygameInputs(self, key):
		# player 1
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
		if key == pg.K_DOWN:
			self.makeMove( 2, gi.ad.STOP )
			self.makeMove( 4, gi.ad.STOP )
		elif key == pg.K_LEFT:
			self.makeMove( 2, gi.ad.LEFT )
			self.makeMove( 4, gi.ad.LEFT )
		elif key == pg.K_RIGHT:
			self.makeMove( 2, gi.ad.RIGHT )
			self.makeMove( 4, gi.ad.RIGHT )


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos()

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= self.height and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= self.width and rack.fx > 0):
			rack.collideWall( "stop" )

		# prevent racket from crossing the middle line
		if (rack.id == 1 or rack.id == 3) and rack.box.right > self.width / 2:
			rack.collideWall( "stop" )
			rack.setPos( (self.width - self.size_r) / 2, rack.box.centery )
		elif (rack.id == 2 or rack.id == 4) and rack.box.left < self.width / 2:
			rack.collideWall( "stop" )
			rack.setPos( (self.width + self.size_r) / 2, rack.box.centery )

		rack.clampPos()


	# bouncing off the rackets
	def checkRackets(self, ball):
		for rack in self.rackets: #		copies the racket's data
			if ball.overlaps( rack ):
				if (rack.id == 1 or rack.id == 2):
					ball.setPos( ball.box.centerx, rack.box.centery + self.size_b ) # '+' because the ball is going under
				elif (rack.id == 3 or rack.id == 4):
					ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going over
				ball.collideRack( rack, "y" )
				ball.dy *= self.factor_rack
				ball.clampSpeed()
				self.last_ponger = rack.id


	# bouncing on the walls
	def checkWalls(self, ball):
		# bouncing off the sides
		if ball.box.left <= 0 or ball.box.right >= self.width:
			ball.collideWall( "x" )
			ball.dx *= self.factor_wall
			ball.clampSpeed()


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.top <= 0 or ball.box.bottom >= self.height:
			# checking who scored
			if ball.box.right <= self.width / 2:
				if self.last_ponger > 0:
					self.scores[1] += 1
				ball.setDirs( -1, -1 )
				ball.setPos ( self.width * (3 / 4), self.height * (3 / 4) )
			elif ball.box.left >= self.width / 2:
				if self.last_ponger > 0:
					self.scores[0] += 1
				ball.setDirs( 1, 1 )
				ball.setPos ( self.width * (1 / 4), self.height * (1 / 4) )

			# reseting the ball's speed
			ball.setSpeeds( ( self.speed_b + ball.dx ) * (1 / 2), self.speed_b * (2 / 3) )
			ball.clampSpeed()
			self.last_ponger = 0


	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( 0, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( self.width / 2, 0 ), ( self.width / 2, self.height ), self.size_l )
		pg.draw.line( self.win, self.col_fnt, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2)


	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, self.col_fnt)
		text2 = self.font.render(f'{self.scores[1]}', True, self.col_fnt)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 4), self.height * (2 / 4) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (3 / 4), self.height * (2 / 4) )))


if __name__ == '__main__':
	g = Ponger()
	g.start()
	g.run()