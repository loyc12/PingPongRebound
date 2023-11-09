import pygame as pg
import GameObject as go
import GameInterface as gi

class Pongest(gi.Game):
	name = "Pongest"

	width = 2048
	height = 1024

	speed_b = 10

	factor_rack = 1.10
	gravity = 0

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


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 4), self.height * (3 / 4) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, (self.speed_b * (2 / 3) ))
		self.balls[0].setDirs( -1, -1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handleInputs(self, key):
		# player 1
		if key == pg.K_s:
			self.makeMove( 1, self.STOP )
			self.makeMove( 3, self.STOP )
		elif key == pg.K_a:
			self.makeMove( 1, self.LEFT )
			self.makeMove( 3, self.LEFT )
		elif key == pg.K_d:
			self.makeMove( 1, self.RIGHT )
			self.makeMove( 3, self.RIGHT )

		# player 2
		if key == pg.K_DOWN:
			self.makeMove( 2, self.STOP )
			self.makeMove( 4, self.STOP )
		elif key == pg.K_LEFT:
			self.makeMove( 2, self.LEFT )
			self.makeMove( 4, self.LEFT )
		elif key == pg.K_RIGHT:
			self.makeMove( 2, self.RIGHT )
			self.makeMove( 4, self.RIGHT )


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
				ball.collideWall( "y" )
				ball.dy *= self.factor_rack
				ball.clampSpeed()
				ball.collideRack( rack, "y" )
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
			if (self.last_ponger > 0):
				self.scores[self.last_ponger - 1] += 1
				ball.setDirs( -ball.fx, -ball.fy )
			else:
				if ball.fx < 0 and ball.fy < 0:
					ball.setDirs( 1, -1 )
				elif ball.fx > 0 and ball.fy < 0:
					ball.setDirs( 1, 1 )
				elif ball.fx > 0 and ball.fy > 0:
					ball.setDirs( -1, 1 )
				elif ball.fx < 0 and ball.fy > 0:
					ball.setDirs( -1, -1 )

			# reseting the ball's position & speed
			ball.setPos ( self.width / 2, self.height / 2 )
			ball.setSpeeds( (self.speed_b + ball.dx) / 2, (self.speed_b + ball.dy) / 3 )
			ball.clampSpeed()
			self.last_ponger = 0


	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )
		pg.draw.line( self.win, self.col_fnt, ( 0, self.height / 2 ), ( self.width, self.height / 2 ), self.size_l )


	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, self.col_fnt)
		text2 = self.font.render(f'{self.scores[1]}', True, self.col_fnt)
		text3 = self.font.render(f'{self.scores[2]}', True, self.col_fnt)
		text4 = self.font.render(f'{self.scores[3]}', True, self.col_fnt)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 4), self.height * (1 / 4) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (3 / 4), self.height * (1 / 4) )))
		self.win.blit( text3, text3.get_rect( center = ( self.width * (1 / 4), self.height * (3 / 4) )))
		self.win.blit( text4, text4.get_rect( center = ( self.width * (3 / 4), self.height * (3 / 4) )))


if __name__ == '__main__':
	g = Pongest()
	g.start()
	g.run()