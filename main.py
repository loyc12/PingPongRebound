import asyncio
import Ping
import Pong
import Pongers


# MASTER LIST
# TODO : compile into webAssembly with pybox
# TODO : make an 'interface' class to reroute the key events to, for future web use
# TODO : make an ai class to control the rackets throught the interface
# TODO : split logic and rendering
# TODO : allow racket control through sockets

# MINOR LIST
# TODO : use rect center for positioning (in GameObject class)
# TODO : make an array of balls and rackets instead, so that the number can vary during runtime
# TODO : make the ball restart's trajectory more random
# TODO : add sound effects to collisions (in GameObject class)

def main():

	#asyncio.run( Ping.run() )
	asyncio.run( Pong.run() )
	#asyncio.run( Pongers.run() )

if __name__ == '__main__':
	main()