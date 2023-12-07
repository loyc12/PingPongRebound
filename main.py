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
# TODO : send team info and player info somewhere at the end
# TODO : see if adding a rule for bounce randomess coud help avoid bots getting stuck
# TODO : review bot bounce calculations
# TODO : rework the ball respawn trajectory everywhere

# FUNCTION LIST
# TODO : add a broadcast()function to GM to send updates with

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
		pg.display.set_caption( g.name )

		g.addPlayer( "Player 1", 1 )

		g.start()

		g.run()

	else:
		print( "Cannot run game : debug mode is off" )


if __name__ == '__main__':
	asy.run( debugTester( Pong ))
