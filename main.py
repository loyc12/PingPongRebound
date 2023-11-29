try:
	from Pi import Pi
	from Po import Po
	from Ping import Ping
	from Pong import Pong
	from Pinger import Pinger
	from Ponger import Ponger
	from Pingest import Pingest
	from Pongest import Pongest
	from GameInterface import Game

	import asyncio as asy
	import cfg
	if cfg.DEBUG_MODE:
		from master import pg

except ModuleNotFoundError:
	from game.PingPongRebound.Pi import Pi
	from game.PingPongRebound.Po import Po
	from game.PingPongRebound.Ping import Ping
	from game.PingPongRebound.Pong import Pong
	from game.PingPongRebound.Pinger import Pinger
	from game.PingPongRebound.Ponger import Ponger
	from game.PingPongRebound.Pingest import Pingest
	from game.PingPongRebound.Pongest import Pongest
	from game.PingPongRebound.GameInterface import Game

	import asyncio as asy
	import game.PingPongRebound.cfg as cfg



# MASTER LIST
# TODO : add gameUpdate dict in GI to be edited and return with getInfo
# TODO : add queues for gameManager to receive/send messages (gameStartInfo, gameEndInfo, playerEvents)

# FUNCTION LIST
# TODO : have bot remember where it last saw the ball (to allow : one scan per second, N moves per second)
# TODO : implement static game info accessors in GM

# DEBUG LIST
# TODO : use different self.____Lock like mutexes to protect dicts and individual games
# TODO : see what's up with asy.sleep() crashing in coroutines when called for the first time

# MINOR LIST
# TODO : rework the ball respawn trajectory everywhere
# TODO : make sure to always put player 1 and 2 in oposite teams
# TODO : add a "mode" argument to game.respawnBall() and use it when initializing the ball
# TODO : add double-sided gravity to 4 player ping games (so they're actual ping game lol)
# TODO : add sound effects to collisions (in GameObject class)
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)

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
		print ( "Debug mode is off" )


if __name__ == '__main__':
	asy.run(debugTester( Pong ))
