from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest


# MASTER LIST
# TODO : allow racket control through sockets
# TODO : make an ai class to control the rackets throught the interface


# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)


if __name__ == '__main__':
	g = Pong()
	g.start()
	g.run()