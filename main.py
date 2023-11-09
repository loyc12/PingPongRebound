import Pingest as p

# MASTER LIST
# TODO : try with websockets (?)
# TODO : make an ai class to control the rackets throught the interface
# TODO : split logic and rendering
# TODO : allow racket control through sockets

# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)


if __name__ == '__main__':
	g = p.Pingest()
	g.start()
	g.run()