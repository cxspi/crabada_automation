# Crabada Automation Bot
This bot was created the automate the process of playing the blockchain based P2E game Crabada. 

At first the software was only used by my partner and I, but later on further people onboarded the software. Therefore, I had to reprogram it to fit a SaaS model. 

The external clients are able to control the teams and nfts which are used in the game via 
a google spread. 

### Structure:

###### crabada: 

This file contains all of the scripts that power this software. It is composed of three sections:

** helpers **
** libs **
** loggers **

helpers - All the functions to manage the game status, situation of the team and the team's cycle.

libs - Handles all the requests made to the blockchain and server to fetch data, it also contains a file with all the ABIs of the contract. 

loggers - Contains logging config file


###### main:

'main' brings all of the scripts above together, and runs the main game loop. 
It is short but ensures all systems are working correctly. 