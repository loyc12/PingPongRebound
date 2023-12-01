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