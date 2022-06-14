from bdb import Breakpoint
import pygame
import math
import time

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
	SCALE = 200 / AU  # 1AU = 100 pixels
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

		self.x_vel = 0
		self.y_vel = 0


	def draw(self, win):
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2

		# uncomment to draw lines, however, the program will run slower over time
  
		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

		# 	# drawing the lines
			pygame.draw.lines(win, self.color, False, updated_points, 2)

		# pygame.draw.circle(win, self.color, (x, y), self.radius)
		# scale the image with self.radius
		win.blit(pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2)), (x - self.radius, y - self.radius))
		# draw the image
		#win.blit(self.image, (x - self.radius, y - self.radius))
		
		# rendering the distance of the planet to the sun
		if not self.sun:
			distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

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


def main():
	run = True
	clock = pygame.time.Clock()
 
	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30) 
	sun.sun = True

	# initializing planets
	# data from https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html

	mercury = Planet(0.38709893 * Planet.AU, 0.0, 5, RED, 3.3011 * 10**23)
	mercury.image = mercury_image
	mercury.y_vel = -47.36 * 1000

	venus = Planet(0.72333566 * Planet.AU, 0.0, 10, BLUE, 4.867 * 10**24)
	venus.image = venus_image
	venus.y_vel = -35.02 * 1000

	earth = Planet(1.0 * Planet.AU, 0.0, 15, WHITE, 5.972 * 10**24)
	earth.image = earth_image
	earth.y_vel = -29.78 * 1000

	mars = Planet(1.52371034 * Planet.AU, 0.0, 20, RED, 6.4171 * 10**23)
	mars.image = mars_image
	mars.y_vel = -24.07 * 1000

	jupiter = Planet(5.20336301 * Planet.AU, 0.0, 50, RED, 1.8982 * 10**27)
	jupiter.image = jupiter_image
	jupiter.y_vel = -13.06 * 1000

	saturn = Planet(9.53667594 * Planet.AU, 0.0, 80, BLUE, 5.6846 * 10**26)
	saturn.image = saturn_image
	saturn.y_vel = -13.06 * 1000

	uranus = Planet(19.19126393 * Planet.AU, 0.0, 120, BLUE, 8.6832 * 10**25)
	uranus.image = uranus_image
	uranus.y_vel = -6.80 * 1000

	neptune = Planet(30.06992276 * Planet.AU, 0.0, 150, BLUE, 1.0241 * 10**26)
	neptune.image = neptune_image
	neptune.y_vel = -5.43 * 1000

	# comets

	comet_halley = Planet(0.586 * Planet.AU, 0.0, 20, WHITE, 2.2 * 10**14) # x value perihelion
	comet_halley.image = comet_image
	comet_halley.y_vel = -54.55 * 1000 

	


	# planets = list of planets
	planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune,     comet_halley]

	bg_img = pygame.image.load('media/background1.jpg')
	bg_img = pygame.transform.scale(bg_img,(800,800))



	#f = open("just_with_lines.txt", "w")

	#counter = 0
 
	#list_of_times = []

	while run:

		clock.tick(1000)

		# WIN.fill((0, 0, 0))

		# start = time.time()
		WIN.blit(bg_img,(0,0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		print("Comet Halley: " + str(comet_halley.x) + "," + str(comet_halley.y))
		print("Earth: " + str(earth.x) + "," + str(earth.y))
		print("X difference: " + str(earth.x - comet_halley.x))
		print("X difference: " + str(earth.y - comet_halley.y))

		pygame.display.update()
		# end = time.time()

		#list_of_times.append(end-start)

		# if counter > 30000:
		# 	break
		
		# counter += 1


	pygame.quit()
	
    # writing into file
	# for i in list_of_times:
	# 	f.write(str(i)+"\n")

	# f.close()

main()