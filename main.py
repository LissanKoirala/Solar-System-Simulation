from bdb import Breakpoint
from itertools import count
from turtle import speed
import pygame
import math
import time
import numpy as np

pygame.init()

WIDTH, HEIGHT =  800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

# load the media
sun_image = pygame.image.load("media/sun.png")
mercury_image = pygame.image.load("media/mercury.png")
venus_image = pygame.image.load("media/venus.png")
earth_image = pygame.image.load("media/earth.png")
mars_image = pygame.image.load("media/mars.png")
jupiter_image = pygame.image.load("media/jupiter.png")
saturn_image = pygame.image.load("media/saturn.png")
uranus_image = pygame.image.load("media/uranus.png")
neptune_image = pygame.image.load("media/neptune.png")
comet_image = pygame.image.load("media/comet.png")



class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 10 / AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 day
	image = pygame.image.load('media/sun.png')

	def __init__(self, x, y, radius, color, mass):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0
		self.distance_to_sun_x = 0
		self.distance_to_sun_y = 0

		self.x_vel = 0
		self.y_vel = 0


	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		# uncomment to draw lines, however, the program will run slower over time#
		# if len(self.orbit) > 2:
		# 	updated_points = []
		# 	for point in self.orbit:
		# 		x, y = point
		# 		x = x * self.SCALE + WIDTH / 2
		# 		y = y * self.SCALE + HEIGHT / 2
		# 		updated_points.append((x, y))
				
		
		# # 	# drawing the lines
		# 	pygame.draw.lines(win, self.color, False, updated_points, 1)
   
		# draw the resultant velocity
		if not self.sun:
			if self.radius == 10: # if comet halley... as it has radius 10
				# resultant
				pygame.draw.line(win, RED, (x, y), (x + self.x_vel * 0.004, y + self.y_vel * 0.004), 3)
				
				# only draw the x velocity
				pygame.draw.line(win, WHITE, (x, y), (x + self.x_vel * 0.004, y), 2)
				# only draw the y velocity
				pygame.draw.line(win, WHITE, (x, y), (x, y + self.y_vel * 0.004), 2)

				# draw a to the center of the sun
				pygame.draw.line(win, DARK_GREY, (x, y), (400, 400), 2)

			
   

		# pygame.draw.circle(win, self.color, (x, y), self.radius)
		# scale the image with self.radius
		win.blit(pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2)), (x - self.radius, y - self.radius))
		# draw the image
		#win.blit(self.image, (x - self.radius, y - self.radius))
		
		# rendering the distance of the planet to the sun
		# if not self.sun:
		# 	distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
		# 	win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance
			self.distance_to_sun_x = distance_x
			self.distance_to_sun_y = distance_y

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))
  
	def draw_line(self, color, x_in, y_in):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
		pygame.draw.line(WIN, color, (x, y), (x + x_in, y + y_in), 1)
		


def main():
	run = True
	clock = pygame.time.Clock()
 
	sun = Planet(0, 0, 20, YELLOW, 1.98892 * 10**30) 
	sun.sun = True

	# initializing planets
	# data from https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

	# planets are bigger than real in the graphics...
	# https://thinkzone.wlonk.com/SS/SolarSystemModel.php?obj=Sun&dia=30cm&lat=51.483439&lon=0.105579&table=y&map=y

	mercury = Planet(0.38709893 * Planet.AU, 0.0, 11, RED, 3.3011 * 10**23)
	mercury.image = mercury_image
	mercury.y_vel = -47.36 * 1000

	venus = Planet(0.72333566 * Planet.AU, 0.0, 12, BLUE, 4.867 * 10**24)
	venus.image = venus_image
	venus.y_vel = -35.02 * 1000

	earth = Planet(1.0 * Planet.AU, 0.0, 13, WHITE, 5.972 * 10**24)
	earth.image = earth_image
	earth.y_vel = -29.78 * 1000

	mars = Planet(1.52371034 * Planet.AU, 0.0, 15, RED, 6.4171 * 10**23)
	mars.image = mars_image
	mars.y_vel = -24.07 * 1000

	jupiter = Planet(5.20336301 * Planet.AU, 0.0, 27, RED, 1.8982 * 10**27)
	jupiter.image = jupiter_image
	jupiter.y_vel = -13.06 * 1000

	saturn = Planet(9.53667594 * Planet.AU, 0.0, 24, BLUE, 5.6846 * 10**26)
	saturn.image = saturn_image
	saturn.y_vel = -9.68 * 1000

	uranus = Planet(19.19126393 * Planet.AU, 0.0, 18, BLUE, 8.6832 * 10**25)
	uranus.image = uranus_image
	uranus.y_vel = -6.80 * 1000

	neptune = Planet(30.06992276 * Planet.AU, 0.0, 19, BLUE, 1.0241 * 10**26)
	neptune.image = neptune_image
	neptune.y_vel = -5.43 * 1000

	# comets

	comet_halley = Planet(0.586 * Planet.AU, 0, 10, BLUE, 2.2 * 10**14) # x value perihelion
	comet_halley.image = comet_image
	comet_halley.y_vel = -54.55 * 1000 

	


	# planets = list of planets
	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune,     comet_halley]

	bg_img = pygame.image.load('media/background1.jpg')
	bg_img = pygame.transform.scale(bg_img,(800,800))



	counter = 0
 
	list_of_times = []
	distance_between = []
	area_covered = []
	speed = []
	to_save = []

	while run:

		clock.tick(100000)

		# WIN.fill((0, 0, 0))

		# start = time.time()
		WIN.blit(bg_img,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		object = comet_halley
		object2 = sun
  
		# print("X Vel: " + str(object.x_vel))
		# print("Y Vel: " + str(object.y_vel))
		# TODO: Draw the velocity vector on the graph
		
  

		speed_calc = math.sqrt(object.x_vel ** 2 + object.y_vel ** 2)

		# if object.x_vel and object.y_vel are in same direction, then the comet's resultant speed is positive
		if object.x_vel > 0 and object.y_vel > 0:
			speed_calc = abs(speed_calc)

		# if object.x_vel and object.y_vel are in opposite direction, then the comet's resultant speed is negative
		elif object.x_vel < 0 and object.y_vel < 0:
			speed_calc = -abs(speed_calc)



		speed.append(speed_calc)
		# print("Resultant: " + str(speed_calc))

		speed_vector = ((object.x, object.y),(object.x + object.x_vel, object.y + object.y_vel)) 
		# find resultant_speed_vector
		resultant_speed_vector = speed_vector[1][0]-speed_vector[0][0], speed_vector[1][1]-speed_vector[0][1]

		print("Resultant Vector: " + str(resultant_speed_vector))
		
		# TODO: instead of the distance to sun, use the focous

  
  
		distance_to_sun = object.distance_to_sun
		print(distance_to_sun)
		# distance to sun vector for object
		distance_to_sun_vector = ((object.x, object.y),(object.x + object.distance_to_sun_x, object.y + object.distance_to_sun_y))
  		# find distance_to_sun_vector
		distance_to_sun_vector = distance_to_sun_vector[1][0]-distance_to_sun_vector[0][0], distance_to_sun_vector[1][1]-distance_to_sun_vector[0][1]

		print("Distance Vector: " + str(distance_to_sun_vector))
  
  
		# print("Distance to sun: " + str(object.distance_to_sun/149597871000))
  
		# angle between the two vectors resultant_speed_vector and distance_to_sun_vector
  
		###### TODO: Something is not right... #####
		angle = math.acos((resultant_speed_vector[0]*distance_to_sun_vector[0] + resultant_speed_vector[1]*distance_to_sun_vector[1])/((math.sqrt(resultant_speed_vector[0]**2 + resultant_speed_vector[1]**2))*math.sqrt(distance_to_sun_vector[0]**2 + distance_to_sun_vector[1]**2)))

		# convert angle to degrees
		angle = angle * (180 / math.pi)
	
		print("Angle: " + str(angle))
  

		velocity_perpendicular_to_sun = speed_calc * angle # Resultant x sin theta
		print("Velocity Perpendicular to Sun: " + str(velocity_perpendicular_to_sun))
		object.draw_line(BLUE, object.x+velocity_perpendicular_to_sun, object.y+velocity_perpendicular_to_sun)
  

		area_swpet = 0.5*(distance_to_sun*velocity_perpendicular_to_sun*Planet.TIMESTEP)
		# print("Area Covered: " + str(area_swpet))
		area_covered.append(area_swpet)

		to_save.append(str(velocity_perpendicular_to_sun) + "," + str(distance_to_sun) + "," + str(angle) + "," + str(area_swpet) + ",")
		

		# calcluate the distance between object and the sun
		#r = math.sqrt((sun.x - object.x) ** 2 + (sun.y - object.y) ** 2)

		# mass of sun -> 1.98892 * 10**30
		# G -> 6.67408 * 10**-11
		# AU -> 1.496 * 10**11
		# TODO: way to find the velocity according for ellipse...
		#temp = math.sqrt(  6.67408 * 10**-11 *  1.98892 * 10**30 * ( (2/r) - (1/(17.834 * 1.496 * 10**11))  ) )




		# print("Comet Halley: " + str(object.x) + "," + str(object.y))
		# print("Earth: " + str(earth.x) + "," + str(earth.y))

		distance_between.append(str(math.sqrt((object2.x - object.x)**2 + (object2.y - object.y)**2)))

		pygame.display.update()


		# end = time.time()

		if counter > 50000:
			break

		counter += 1

	pygame.quit()

	f = open("distance_between.txt", "w")
	for i in distance_between:
		f.write(str(float(i)/149597871000)+"\n")
	f.close()

	f = open("speed.txt", "w")
	for i in speed:
		f.write(str(i)+"\n")
	f.close()
 
 
	f = open("area_covered.txt", "w")
	for i in area_covered:
		f.write(str(i)+"\n")
	f.close()
 
 
	f = open("to_save.csv", "w")
	for i in to_save:
		f.write(str(i)+"\n")
	f.close()
	

 
 
main()