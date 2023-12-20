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
# TODO : overhaul the ball respawn mechanic (needs to know who to respawn at explicitly)
# TODO : add a respawn queue to know who to respawn at next
# TODO : have respawn trajectories be stored in an array in game interface
# TODO : make the ball receiver change after N missed shots
# TODO : rework ball respawn trajectory in pongest

# FUNCTION LIST

# DEBUG LIST

# MINOR LIST
# TODO : make obstacles type GameObjects in the base class( and use them in pongester )
# TODO : add sound effects to collisions( in GameObject class )
# TODO : make an 'asteroids' game( solo )

async def debugTester( Initialiser ):

	if cfg.DEBUG_MODE:
		pg.init()
		g = Initialiser( 1 )

		g.setWindow( pg.display.set_mode(( g.width, g.height )))
		pg.display.set_caption( g.type )

		if cfg.ADD_DEBUG_PLAYER:
			g.addPlayer( "Player 1", 1 )

		g.start()

		await g.run()

	else:
		print( "Cannot run game : debug mode is off" )


if __name__ == '__main__':
	asy.run( debugTester( Pinger ))