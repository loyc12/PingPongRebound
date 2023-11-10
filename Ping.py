import pygame as pg
import GameObject as go
import GameInterface as gi

class Ping(gi.Game):
	name = "Ping"

	width = 1280
	height = 1280

	factor_wall = 0.90


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (2 / 4), self.height - (3 * self.size_b), self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )


	# bouncing off the rackets
	def checkRackets(self, ball):
		for i in range(len(self.rackets)):
			rack = self.rackets[i]
			if ball.overlaps( rack ):
				ball.collideWall( "y" )
				ball.dy *= self.factor_rack
				ball.clampSpeed()
				ball.collideRack( rack, "y" )
				ball.setPos( ball.box.centerx, rack.box.centery - self.size_b ) # '-' because the ball is going above the racket
				self.scores[0] += 1


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= self.height:
			self.scores[0] = 0
			ball.setDirs( -ball.fx, 1 )
			ball.setPos( ball.box.centerx, 0 )
			ball.setSpeeds( (ball.dx + self.speed_b) / 2, 0)
			ball.clampSpeed()

	def drawLines(self):
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( 0 , self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( self.width, 0 ), ( self.width, self.height ), self.size_l * 2 )
		pg.draw.line( self.win, self.col_fnt, ( 0, 0 ), ( self.width, 0 ), self.size_l * 2 )


if __name__ == '__main__':
	g = Ping()
	g.start()
	g.run()