import asyncio as asy

try:
	from games import *
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg

except ModuleNotFoundError:
	from game.PingPongRebound.games import *
	import game.PingPongRebound.cfg as cfg



# MASTER LIST
# TODO : have GI call game.connector.getEvent() instead of pygame's event system
# TODO : use different gameLock whne useful instead of dictLock

# FUNCTION LIST

# DEBUG LIST
# TODO : recheck the ai predictive function to see why there is slight missajustments

# MINOR LIST
# TODO : make sure to always put player 1 and 2 in opposite teams
# TODO : rework the ball respawn trajectory everywhere
# TODO : add a "mode" argument to game.respawnBall() and use it when initializing the ball
# TODO : add double-sided gravity to 4 player ping games (so they're actual ping game lol)
# TODO : add sound effects to collisions (in GameObject class)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)
# TODO : make an 'asteroids' game (solo)

async def debugTester( Initialiser ):
	if cfg.DEBUG_MODE:
		pg.init()
		g = Initialiser(1)

		print ( g.getInitInfo() )

		g.setWindow(pg.display.set_mode((g.width, g.height)))
		pg.display.set_caption(g.name)

		g.printControlers()
		g.addPlayer( "Player 1", 1 )
		g.printControlers()
		g.start()
		g.printControlers()

		print ( g.getUpdateInfo() )

		g.run()

		print ( g.getEndInfo() )

	else:
		print ( "Cannot run game : debug mode is off" )


if __name__ == '__main__':
	asy.run(debugTester( Pong ))
