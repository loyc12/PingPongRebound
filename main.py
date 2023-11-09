import Pongest as p

# MASTER LIST
# TODO : try with websockets (?)
# TODO : make an ai class to control the rackets throught the interface
# TODO : split logic and rendering
# TODO : allow racket control through sockets

# MINOR LIST
# TODO : make an 'asteroids' game (solo)
# TODO : make the ball restart's trajectory more random in Pong-type games
# TODO : add sound effects to collisions (in GameObject class)

def main():

	g = p.Pongest()
	g.start()
	g.run()


if __name__ == '__main__':
	main()