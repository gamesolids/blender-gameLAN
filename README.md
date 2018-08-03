# blender-gameLAN
A set of scripts for setting up blender multiplayer network game.


This is not a production ready anything. It is a very trusting server, and a very dumb client. Do not expect this to run over the internet. The server has no security layer. It should be limited to 192.168.x.x addresses. Do Not run it under your public IP address. 



## source 
The basic python files you need for linking 2 players over a local network. It relies on UDP and loop to check for player updates. It is rubbish for more than 4 players. But for some reason, no less fun to play with.


## public
This is an example game using the gameLAN scripts. It allows you to host a game instance or join an already running instance. No magic, better machine should be the host, you still need to also be a client if you want to play, and not just host.

It also contains the GameSolids Blender Game Engine Manager. A simple tool library for helping with loading scenes, player skins, and prop libraries. 


