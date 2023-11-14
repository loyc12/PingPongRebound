import pygame as pg
import GameObject as go
import GameInterface as gi

class Ping(gi.Game):
	name = "Ping"

	width = 1280
	height = 1280

	gravity = 0.4
	factor_rack = 1.00
	factor_wall = 0.80


	def initRackets(self):
		self.rackets.append( go.GameObject( 1, self, self.width * (2 / 4), self.height - (3 * self.size_b), self.size_r, self.size_b ))
		self.rackets[0].setSpeeds( self.speed_r, 0 )
		self.racketCount = 1


	def initControlers(self):
		self.addBot("bot 1")


	def initBalls(self):
		self.balls.append( go.GameObject( 1, self, self.width * (3 / 8), self.size_b, self.size_b, self.size_b ))
		self.balls[0].setSpeeds( self.speed_b, 0)
		self.balls[0].setDirs( 1, 1 )


	# scoring a goal
	def checkGoals(self, ball):
		if ball.box.bottom >= self.height:
			self.scores[0] = 0
			ball.setDirs( -ball.fx, 1 )
			ball.setPos( ball.box.centerx, self.size_b )
			ball.setSpeeds( (ball.dx + self.speed_b) / 3, 0 )
			ball.clampSpeed()


if __name__ == '__main__':
	g = Ping()
	g.start()
	g.run()