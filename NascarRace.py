import pygame, math, neat, sys, os
pygame.init()

# SET UP WINDOW
WIN_WIDTH = 500
WIN_HEIGHT = 500
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Race Car")

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BLACK = (0,0,0)

clock = pygame.time.Clock()

class Car:

        radius = 5
        current_angle = 90
        color = BLUE

        def __init__(self):
                self.xpos = 385
                self.ypos = 250
        
        def update(self):
                self.xpos += math.cos(self.current_angle*math.pi/180)
                self.ypos -= math.sin(self.current_angle*math.pi/180)                               
        
        def draw(self, win):
                pygame.draw.circle(win, self.color, (int(self.xpos), int(self.ypos)), self.radius)

        def outsideBorder(self,x, y):
                if( ((((y-250)**2)/(240**2)) + (((x-250)**2)/(165**2))) > 1):
                        return True
                else:
                        return False

        def insideBorder(self,x,y):
                if( ((((y-250)**2)/(200**2)) + (((x-250)**2)/(125**2))) < 1):
                        return True
                else:
                        return False

        def collide(self, win):
                angle_check = [self.current_angle, self.current_angle+90, self.current_angle-90]
                for angle in angle_check:
                        x_rad = self.xpos + self.radius*math.cos(angle*math.pi/180)
                        y_rad = self.ypos + self.radius*math.sin(angle*math.pi/180)
                        if(self.outsideBorder(x_rad, y_rad) or self.insideBorder(x_rad, y_rad)):
                                self.color = RED
                                return
                self.color = BLUE
                return

        def drawDistances(self, win):
                angle_check = [self.current_angle, self.current_angle+45, self.current_angle+90, self.current_angle-45, self.current_angle-90]
                for angle in angle_check:
                        x , y = self.xpos , self.ypos
                        while(win.get_at((int(x),int(y))) != BLACK):
                                x += math.cos(angle*math.pi/180)
                                y -= math.sin(angle*math.pi/180)
                        pygame.draw.line(win,RED, (self.xpos, self.ypos), (x,y), 2)

	
class Track:
        color = (0,0,0)
        def __init__(self):
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

def draw_window(win, car, track):
        win.fill((255,255,255))
        pygame.draw.rect(win, BLACK, (0,0,WIN_WIDTH,WIN_HEIGHT), 2)
        track.draw(win)
        car.draw(win)
        car.drawDistances(win)
        pygame.draw.line(win, (0,0,0), (0,490), (500,490), 2)
        pygame.display.update()

def main():
	run = True
	car = Car()
	track = Track()
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

		car.update()
		car.collide(win)
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			car.current_angle += 1
			car.current_angle %= 360
		if keys[pygame.K_RIGHT]:
			car.current_angle -= 1
			car.current_angle %= 360
		
		draw_window(win, car, track)
		
		clock.tick(60)
				
main()





