from cgitb import grey
import pygame
import math
import time

pygame.init()

WIDTH, HEIGHT =  1920, 1080
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
pluto_image = pygame.image.load("media/pluto.png")
comet_image = pygame.image.load("media/comet.png")



class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 90 / AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 day
	image = pygame.image.load('media/sun.png')

	def __init__(self, x, y, radius, color, mass, max_lines_draw):
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

		self.max_lines_draw = max_lines_draw


	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		# uncomment to draw lines, however, the program will run slower over time#
		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))
				
		
		# 	# drawing the lines
			updated_points = updated_points[-self.max_lines_draw:]
			pygame.draw.lines(win, self.color, False, updated_points, 1)
   
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
				# pygame.draw.line(win, DARK_GREY, (x, y), (WIDTH / 2, HEIGHT / 2), 2)

			
   

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
  
	def draw_line(self, win, color, x_in, y_in):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
		pygame.draw.line(win, color, (x, y), (x + x_in * 0.004, y+ x_in * 0.004), 5)

  
		


def main():
	run = True
	clock = pygame.time.Clock()
 
	sun = Planet(0, 0, 20, YELLOW, 1.98892 * 10**30, 0) 
	sun.sun = True

	# initializing planets
	# data from https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

	# planets are bigger than real in the graphics...
	# https://thinkzone.wlonk.com/SS/SolarSystemModel.php?obj=Sun&dia=30cm&lat=51.483439&lon=0.105579&table=y&map=y

	mercury = Planet(0.38709893 * Planet.AU, 0.0, 11, BLUE, 3.3011 * 10**23, 88)
	mercury.image = mercury_image
	mercury.y_vel = -47.36 * 1000

	venus = Planet(0.72333566 * Planet.AU, 0.0, 12, RED, 4.867 * 10**24, 225)
	venus.image = venus_image
	venus.y_vel = -35.02 * 1000

	earth = Planet(1.0 * Planet.AU, 0.0, 13, BLUE, 5.972 * 10**24, 365)
	earth.image = earth_image
	earth.y_vel = -29.78 * 1000

	mars = Planet(1.52371034 * Planet.AU, 0.0, 15, RED, 6.4171 * 10**23, 687)
	mars.image = mars_image
	mars.y_vel = -24.07 * 1000

	jupiter = Planet(5.20336301 * Planet.AU, 0.0, 27, BLUE, 1.8982 * 10**27, 4333)
	jupiter.image = jupiter_image
	jupiter.y_vel = -13.06 * 1000

	saturn = Planet(9.53667594 * Planet.AU, 0.0, 24, RED, 5.6846 * 10**26, 10760)
	saturn.image = saturn_image
	saturn.y_vel = -9.68 * 1000

	uranus = Planet(19.19126393 * Planet.AU, 0.0, 18, BLUE, 8.6832 * 10**25, 30690)
	uranus.image = uranus_image
	uranus.y_vel = -6.80 * 1000

	neptune = Planet(30.06992276 * Planet.AU, 0.0, 19, RED, 1.0241 * 10**26, 60195)
	neptune.image = neptune_image
	neptune.y_vel = -5.43 * 1000

	# well added pluto as it has some imapct on the grativational force as it's twice as massive as the comet.
	pluto = Planet(39.48211675 * Planet.AU, 0.0, 5, BLUE, 1.3022 * 10**22, 90560)
	pluto.image = pluto_image
	pluto.y_vel = -4.74 * 1000

	# comets

	comet_halley = Planet(0.586 * Planet.AU, 0, 10, WHITE, 2.2 * 10**14, 27500) # x value perihelion
	comet_halley.image = comet_image
	comet_halley.y_vel = -54.55 * 1000 

	


	# planets = list of planets
	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto,     comet_halley]

	bg_img = pygame.image.load('media/background.jpg').convert()
	bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))



	counter = 0
 
	list_of_times = []
	distance_between = []
	area_covered = []
	speed = []
	to_save = []

	# object_prev_x = 0
	# object_prev_y = 0

	while run:

		clock.tick(100000)

		#WIN.fill((0, 0, 0))

		# start = time.time()
		WIN.blit(bg_img,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		object = comet_halley # so dynamic, just change of which you want to calculate!
		object2 = sun

		# if object_prev_x == 0 and object_prev_y == 0:
		# 	object_prev_x = object.x
		# 	object_prev_y = object.y


  
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

		# print("Resultant Vector: " + str(resultant_speed_vector))
		
		# TODO: instead of the distance to sun, use the focous

  
  
		distance_to_sun = object.distance_to_sun
		# print(distance_to_sun)
		# distance to sun vector for object
		distance_to_sun_vector = ((object.x, object.y),(object.x + object.distance_to_sun_x, object.y + object.distance_to_sun_y))
  		# find distance_to_sun_vector
		distance_to_sun_vector = distance_to_sun_vector[1][0]-distance_to_sun_vector[0][0], distance_to_sun_vector[1][1]-distance_to_sun_vector[0][1]

		# print("Distance Vector: " + str(distance_to_sun_vector))
  
  
		# print("Distance to sun: " + str(object.distance_to_sun/149597871000))
  
		# angle between the two vectors resultant_speed_vector and distance_to_sun_vector
  
		###### TODO: Something is not right... ##### it's right now
		angle = math.acos((resultant_speed_vector[0]*distance_to_sun_vector[0] + resultant_speed_vector[1]*distance_to_sun_vector[1])/((math.sqrt(resultant_speed_vector[0]**2 + resultant_speed_vector[1]**2))*math.sqrt(distance_to_sun_vector[0]**2 + distance_to_sun_vector[1]**2)))
		# convert angle to degrees
		angle = angle * (180 / math.pi)
	

		# calculating velocity_perpendicular_to_sun
		# sin angle in degrees
		sin_angle = math.sin(angle * (math.pi / 180))

		velocity_perpendicular_to_sun = speed_calc * sin_angle # Resultant x sin theta
		# print("Velocity Perpendicular to Sun: " + str(velocity_perpendicular_to_sun))
  

		area_swpet = 0.5*(distance_to_sun*velocity_perpendicular_to_sun*Planet.TIMESTEP)
		# print("Area Covered: " + str(area_swpet))
		area_covered.append(area_swpet)



		# # distance covered from previous point to new point for object, this is what we get if we integrate the velocity
		# prev_point = (object_prev_x, object_prev_y)
		# new_point = (object.x, object.y)
		# # distance betwwen the two points
		# distance_between_points = (new_point[0] - prev_point[0], new_point[1] - prev_point[1])
		# distance_between_points = math.sqrt(distance_between_points[0]**2 + distance_between_points[1]**2)

		# object_prev_x = object.x
		# object_prev_y = object.y





		to_save.append(str(speed_calc) + "," + str(distance_to_sun) + "," + str(angle) + "," + str(area_swpet) + ",")
		

		# calcluate the distance between object and the sun
		#r = math.sqrt((sun.x - object.x) ** 2 + (sun.y - object.y) ** 2)

		# mass of sun -> 1.98892 * 10**30
		# G -> 6.67408 * 10**-11
		# AU -> 1.496 * 10**11
		# TODO: way to find the velocity according for ellipse...
		#temp = math.sqrt(  6.67408 * 10**-11 *  1.98892 * 10**30 * ( (2/r) - (1/(17.834 * 1.496 * 10**11))  ) )




		# print("Comet Halley: " + str(object.x) + "," + str(object.y))
		# print("Earth: " + str(earth.x) + "," + str(earth.y))

		# distance_between.append(str(math.sqrt((object2.x - object.x)**2 + (object2.y - object.y)**2))) ## might want to use this
		distance_between.append(distance_to_sun)



		pygame.display.update()


		# end = time.time()

		# if counter > 24500 and counter < 25500:
		# 	# save pygame screenshot with counter as filename
		# 	pygame.image.save(WIN, "screenshots/background/comet_halley_" + str(counter) + ".png")

		if counter > 25593: # determined by looking at the data, this is the point when at the first orbit, when it reaches where it started
			break

		counter += 1

	pygame.quit()

	f = open("distance_between.txt", "w")
	for i in distance_between:
		f.write(str(float(i)/149597871000)+"\n")
	f.close()

	f = open("speed.txt", "w")
	for i in speed:
		f.write(str(abs(i)/1000)+"\n")
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