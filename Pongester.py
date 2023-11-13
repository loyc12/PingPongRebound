import pygame as pg
import GameObject as go
import GameInterface as gi

class Pongester(gi.Game):
	name = "Pongester"

	width = 1280
	height = 1280

	speed_m = 30
	size_font = 512

	factor_rack = 1.05
	gravity = 0

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

		self.racketCount = 4


	def initControlers(self):
		self.addBot("bot 1")
		self.addBot("bot 2")
		self.addBot("bot 3")
		self.addBot("bot 4")


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 4), self.height * (1 / 4) , self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b * (1 / 2), self.speed_b )
		self.balls[0].setDirs( -1, 1 )


	def initScores(self):
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )
		self.scores.append( 0 )


	def handleInputs(self, key):
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
			if ball.overlaps( rack ):
				if (rack.id == 1):
					ball.setPos( ball.box.centerx, rack.box.centery + self.size_b ) # '+' because the ball is going under
					ball.collideWall( "y" )
					ball.collideRack( rack, "y" )
				elif (rack.id == 2):
					ball.setPos( rack.box.centerx - self.size_b, ball.box.centery ) # '-' because the ball is going left
					ball.collideWall( "x" )
					ball.collideRack( rack, "x" )
				elif (rack.id == 3):
					ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going over
					ball.collideWall( "y" )
					ball.collideRack( rack, "y" )
				elif (rack.id == 4):
					ball.setPos( rack.box.centerx + self.size_b, ball.box.centery ) # '+' because the ball is going right
					ball.collideWall( "x" )
					ball.collideRack( rack, "x" )

				ball.dy *= self.factor_rack
				ball.clampSpeed()
				self.last_ponger = rack.id


	# bouncing on the walls
	def checkWalls(self, ball):
		pass


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.top <= 0 or ball.box.bottom >= self.height or ball.box.left <= 0 or ball.box.right >= self.width:
			# checking who scored
			if ball.fx < 0 and ball.fy < 0:
				ball.setDirs( 1, -1 )
				ball.setSpeeds( self.speed_b * (1 / 2), self.speed_b )
				ball.setPos ( self.width * (1 / 4), self.height  * (3 / 4) )
				if (self.last_ponger > 0):
					self.scores[self.last_ponger - 1] += 1
			elif ball.fx > 0 and ball.fy < 0:
				ball.setDirs( 1, 1 )
				ball.setSpeeds( self.speed_b, self.speed_b * (1 / 2) )
				ball.setPos ( self.width * (1 / 4), self.height  * (1 / 4) )
				if (self.last_ponger > 0):
					self.scores[self.last_ponger - 1] += 1
			elif ball.fx > 0 and ball.fy > 0:
				ball.setDirs( -1, 1 )
				ball.setSpeeds( self.speed_b * (1 / 2), self.speed_b )
				ball.setPos ( self.width * (3 / 4), self.height  * (1 / 4) )
				if (self.last_ponger > 0):
					self.scores[self.last_ponger - 1] += 1
			elif ball.fx < 0 and ball.fy > 0:
				ball.setDirs( -1, -1 )
				ball.setSpeeds( self.speed_b, self.speed_b * (1 / 2) )
				ball.setPos ( self.width * (3 / 4), self.height  * (3 / 4) )
				if (self.last_ponger > 0):
					self.scores[self.last_ponger - 1] += 1

			if ball.box.top <= 0 or ball.box.bottom >= self.height:
				ball.setSpeeds( self.speed_b * (1 / 3), self.speed_b * (1 / 2) )
			elif ball.box.left <= 0 or ball.box.right >= self.width:
				ball.setSpeeds( self.speed_b * (1 / 2), self.speed_b * (1 / 3) )

			# reseting the ball's speed
			ball.clampSpeed()
			self.last_ponger = 0


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


if __name__ == '__main__':
	g = Pongester()
	g.start()
	g.run()