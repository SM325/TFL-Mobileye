# tfl-mobileye

run the Controller module, to start the simulation

####the project include 4 phases
###### 1. Detect light sources candidates
Input:
	* Current frame - one png image
output:
	* candidates - vector of N positions
	* auxiliary – vector of N colors {green, red}

###### 2. Calculate candidate probability and decide if is a traffic light using neural net
inputs:
	* Current frame - one png image
	* candidates  - output from Part 1
	* auxiliary – output from Part 1

outputs: 
	* TrafficLights - vector of K positions notice K <= N
	* auxiliary – vector of K colors


###### 3. Find distance of the traffic lights
input: 
	* Previous and current frames - two png images
	* Two vectors of TrafficLights positions – from Part 2
	* Two auxiliary vectors – from Part 2
	* EM matrix, Principal point, focal length
output: 
	* Distance – vector of K lengthes of traffic lights
	
	
###### 4. integration of th previous parts
