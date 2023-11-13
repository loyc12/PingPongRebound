import pygame as pg
import GameObject as go
import GameInterface as gi

class Pinger(gi.Game):
	name = "Pinger"

	speed_b = 10
	factor_rack = 0.95


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (1 / 4), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )

		self.rackets.append( go.GameObject( 2, self, self.width * (3 / 4), self.height - self.size_b, self.size_r, self.size_b ))
		self.rackets[1].setSpeeds( self.speed_r, 0 )

		self.racketCount = 2


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


	def handleInputs(self, key):
		# player 1
		if key == pg.K_s:
			self.makeMove( 1, gi.ad.STOP )
		elif key == pg.K_a:
			self.makeMove( 1, gi.ad.LEFT )
		elif key == pg.K_d:
			self.makeMove( 1, gi.ad.RIGHT )

		# player 2
		if key == pg.K_DOWN:
			self.makeMove( 2, gi.ad.STOP )
		elif key == pg.K_LEFT:
			self.makeMove( 2, gi.ad.LEFT )
		elif key == pg.K_RIGHT:
			self.makeMove( 2, gi.ad.RIGHT )


	def moveRacket(self, rack):
		rack.clampSpeed()
		rack.updatePos()

		# prevent racket from going off screen
		if (rack.box.top <= 0 and rack.fy < 0) or (rack.box.bottom >= self.height and rack.fy > 0):
			rack.collideWall( "stop" )
		if (rack.box.left <= 0 and rack.fx < 0) or (rack.box.right >= self.width and rack.fx > 0):
			rack.collideWall( "stop" )

		# prevent racket from crossing the middle line
		if rack.id == 1 and rack.box.right > self.width / 2:
			rack.collideWall( "stop" )
			rack.setPos( (self.width - self.size_r) / 2, rack.box.centery )
		elif rack.id == 2 and rack.box.left < self.width / 2:
			rack.collideWall( "stop" )
			rack.setPos( (self.width + self.size_r) / 2, rack.box.centery )

		rack.clampPos()


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= self.height:
			# checking who scored
			if ball.box.right < self.width / 2:
				if self.last_ponger > 0:
					self.scores[1] += 1
				ball.setDirs( -1, -1 )
			elif ball.box.left > self.width / 2:
				if self.last_ponger > 0:
					self.scores[0] += 1
				ball.setDirs( 1, -1 )

			# reseting the ball's position & speed
			ball.setPos( self.width * (1 / 2), self.height * (2 / 3) )
			ball.setSpeeds( (ball.dx + self.speed_b) / 3, self.speed_b * 2 )
			ball.clampSpeed()
			self.last_ponger = 0


	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( self.width / 2, 0 ),  ( self.width / 2, self.height ), self.size_l )

		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )



	def drawScores(self):
		text1 = self.font.render(f'{self.scores[0]}', True, self.col_fnt)
		text2 = self.font.render(f'{self.scores[1]}', True, self.col_fnt)

		self.win.blit( text1, text1.get_rect( center = ( self.width * (1 / 4), self.height * (2 / 4) )))
		self.win.blit( text2, text2.get_rect( center = ( self.width * (3 / 4), self.height * (2 / 4) )))


if __name__ == '__main__':
	g = Pinger()
	g.start()
	g.run()