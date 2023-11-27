from master import cfg
if cfg.DEBUG_MODE:
	from master import pg
from master import go
from master import gi

class Pi(gi.Game):
	name = "Pi"

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


if __name__ == '__main__': #		NOTE : DEBUG

	pg.init()
	g = Pi(1)

	if cfg.DEBUG_MODE:
		g.setWindow( pg.display.set_mode( (Pi.width, Pi.height) ))
		pg.display.set_caption(g.name)


	#g.addPlayer( "Player 1", 1 )

	g.start()
	g.run()