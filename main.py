import Ping
import Pinger
import Pingest
import Pong
import Ponger
import Pongest
import astro


# MASTER LIST
# TODO : allow racket control through sockets
# TODO : make an ai class to control the rackets throught the interface


# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)


if __name__ == '__main__':
	g = Pingest()
	g.start()
	g.run()