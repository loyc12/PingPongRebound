from Ping import Ping
from Pinger import Pinger
from Pingest import Pingest
from Pong import Pong
from Ponger import Ponger
from Pongest import Pongest
from Pongester import Pongester



# MASTER LIST
# TODO : implement (get data)
# TODO : make an ai class to control the rackets throught the interface
# TODO : allow racket control through sockets
# TODO : add a game start and game over screen


# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make obstacles type GameObjects in the base class (and use them in pongester)
# TODO : add gravity to pingest  (to make it an actua ping game lol)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)


if __name__ == '__main__':

	g = Pong()
	g.start()
	g.run()
