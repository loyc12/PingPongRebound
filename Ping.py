import pygame as pg
import GameObject as go
import GameInterface as gi

class Ping(gi.Game):
	name = "Ping"

	width = 1280
	height = 1280

	gravity = 0.3
	factor_rack = 1.0
	factor_wall = 0.6

	score_mode = gi.ad.HITS


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 8), self.size_b, self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, 0)
		self.balls[0].setDirs( 1, 1 )

	def respawnBall(self, ball):
		ball.setDirs( -ball.fx, 1 )
		ball.setPos( (self.width + ball.getPosX()) / 3, self.size_b )
		ball.setSpeeds( (ball.dx + self.speed_b) / 3, 0 )


if __name__ == '__main__':
	g = Ping()
	g.debugMode = True
	g.start()
	g.run()