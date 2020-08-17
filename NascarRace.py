import pygame, math, neat, sys, os
pygame.init()

# SET UP WINDOW
WIN_WIDTH = 500
WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Nascar Racer")

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()

class Car:

        radius = 5
        current_angle = 90 # North up is 90, East is 0
        color = BLUE
        distances = [0, 0, 0, 0, 0] # distances to edge of track

        def __init__(self):
                self.xpos = 385
                self.ypos = 250
        
        def update(self):
                self.xpos += math.cos(self.current_angle*math.pi/180)
                self.ypos -= math.sin(self.current_angle*math.pi/180)                               
        
        def draw(self, win):
                pygame.draw.circle(win, self.color, (int(self.xpos), int(self.ypos)), self.radius)

        def outsideBorder(self,x, y): # Uses equation of ellipse to check if car outside track
                if( ((((y-250)**2)/(240**2)) + (((x-250)**2)/(165**2))) > 1):
                        return True
                else:
                        return False

        def insideBorder(self,x,y): # Same as outsideBorder but for inner ellipse
                if( ((((y-250)**2)/(200**2)) + (((x-250)**2)/(125**2))) < 1):
                        return True
                else:
                        return False

        def collide(self, win): # Checks points around the car circle whether they are outside track limits
                angle_check = [self.current_angle, self.current_angle+90, self.current_angle-90]
                for angle in angle_check:
                        x_rad = self.xpos + self.radius*math.cos(angle*math.pi/180)
                        y_rad = self.ypos + self.radius*math.sin(angle*math.pi/180)
                        if(self.outsideBorder(x_rad, y_rad) or self.insideBorder(x_rad, y_rad)):
                                self.color = RED
                                return True
                self.color = BLUE
                return False

        def drawDistances(self, win): # draw lines from car to track edges
                angle_check = [self.current_angle, self.current_angle+45, self.current_angle+90, self.current_angle-45, self.current_angle-90]
                for ind, angle in enumerate(angle_check):
                        x , y = self.xpos , self.ypos
                        val_outer = (((y-250)**2)/(240**2)) + (((x-250)**2)/(165**2))
                        val_inner = (((y-250)**2)/(200**2)) + (((x-250)**2)/(125**2))
                        while(x < 500 and y <500 and win.get_at((int(x),int(y))) != BLACK): # < 500 to ensure x,y do no exceed the window bounds causing crash, not ideal but works
                                x += math.cos(angle*math.pi/180)
                                y -= math.sin(angle*math.pi/180)
                        
                        self.distances[ind] = math.sqrt(((x-self.xpos)**2) + ((y-self.ypos)**2)) # Store distances for use in NN
                        
                        x -= math.cos(angle*math.pi/180) # need to do this so the line doesnt cover up the black pixels
                        y += math.sin(angle*math.pi/180)
                        pygame.draw.line(win,RED, (self.xpos, self.ypos), (x,y), 2)

	
class Track:
        color = BLACK
        def __init__(self): # define the rects containing the ellipses
                self.inner_width = 250
                self.inner_height = 400
                self.outer_width = self.inner_width + 80
                self.outer_height = self.inner_height + 80
                self.inner_start_x = (500-self.inner_width)/2
                self.outer_start_x = (500-self.outer_width)/2
                self.inner_start_y = (500-self.inner_height)/2
                self.outer_start_y = (500-self.outer_height)/2

        def draw(self, win):
                pygame.draw.ellipse(win, self.color, (self.inner_start_x,self.inner_start_y,self.inner_width, self.inner_height), 5)
                pygame.draw.ellipse(win, self.color, (self.outer_start_x,self.outer_start_y,self.outer_width, self.outer_height), 5)

def draw_window(win, cars, track):
        win.fill(WHITE)
        pygame.draw.rect(win, BLACK, (0,0,WIN_WIDTH,WIN_HEIGHT), 2) # Surround window in black to help avoid crash when searching for back pixels
        track.draw(win)
        for car in cars:
                car.draw(win)
                car.drawDistances(win)
        pygame.display.update()

def main(genomes, config):
        # store nets, genomes, car population
        nets = []
        ge = []
        cars = []

        for _, g in genomes:
                net = neat.nn.FeedForwardNetwork.create(g,config)
                nets.append(net)
                cars.append(Car())
                g.fitness = 0
                ge.append(g)
        
	run = True
	track = Track()
	
	while run:		
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
				run = False
				pygame.quit()

		draw_window(win, cars, track)
		# Loop through car population, update, and decide whether to turn left
                for x, car in enumerate(cars):
                        car.update()
                        try:        
                                output = nets[x].activate((car.distances[0], car.distances[1], car.distances[2], car.distances[3], car.distances[4]))
                        except:
                                print(x)
                                print(car.distances)
                        if(output[0] > 0.5): # turn left                  
                                car.current_angle += 1
                                car.current_angle %= 360
                        ge[x].fitness += 0.1 # reward for surviving
                        if (car.collide(win) == True):
                                ge[x].fitness -= 1 # punish for crashing
                                cars.pop(x) # remove from population
                                nets.pop(x)
                                ge.pop(x)
                        
                if len(cars) < 1:
                        run = False
                        break
                
		clock.tick(60)

def run(config_path):
        print(config_path)
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
	
	p = neat.Population(config)
	
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	
	winner = p.run(main,50)

				
if __name__ == "__main__":
        local_dir = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(local_dir, "config_feedforward.txt")
        run(config_path)




