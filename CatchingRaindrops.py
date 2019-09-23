import pygame
from pygame.locals import *
from math import *   
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import random
import pygame.freetype 
class Drop:
    def __init__(self, cx, cy, r, num_segments, flag, gameDisplay):
        self.cx = cx
        self.cy = cy
        self.r  = r
        self.num_segments = num_segments
        self.flag = flag
        self.color1 = int(random.randrange(0, 10, 3)) 
        self.color2 = int(random.randrange(0, 10, 3)) 
        self.color3 = int(random.randrange(0, 10, 3)) 


    def drawCircle(self):
        if self.flag==0:
           
            glPolygonMode( GL_FRONT, GL_FILL )
            glColor3f(self.color1/10, self.color2/10, self.color3/10 )
            
            glBegin(GL_POLYGON)            
            for ii in range(0, self.num_segments):
                theta = 2.0 * 3.1415926 * (ii) / (self.num_segments);#get the current angle 
                x = self.r * cos(theta); #calculate the x component 
                y = self.r * sin(theta); #calculate the y component 
    
                glVertex2f(x + self.cx, y + self.cy); #output vertex 
            
            glEnd()
    
        
    def draweRect(x, y, width, height, c1, c2, c3):
        #glClear(GL_COLOR_BUFFER_BIT);
        glColor3f(c1,c2,c3);
        glLineWidth(30);
        
        glBegin(GL_POLYGON);
        glVertex2f(x-width/2,y+height/2);
        glVertex2f(x+width/2,y+height/2);
        glVertex2f(x+width/2,y-height/2);
        glVertex2f(x-width/2,y-height/2);
        glEnd();
         
    
        
    def river(height, circle_height, flag, color):
        factor = 0.2
        glClear(GL_COLOR_BUFFER_BIT);
        
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
        glColor3f(color[0], color[1], color[2] )
        glBegin(GL_POLYGON);
          
        #glBegin(GL_LINE_STRIP);
        for x in range( int(-3.0 / factor), int(3.0 / factor) ):
            if x!=0:
                #0.09
                glVertex2f((x*factor), 0.09*sin(x)+height);
                #0.0005
                x += 0.0005
                
        glVertex2f(3.0 / factor, -3); #output vertex 
        glVertex2f(3, -3); #output vertex
        
        glVertex2f(-3, -3.0 ); #output vertex 
        glVertex2f(-3, -3/ factor); #output vertex
    
        glEnd()
    
    def main():
        pygame.init()
        display = (800,600)
        gameDisplay = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        
    
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        glTranslatef(0.0,0.0, -5)
        
        #INITIALISE HEIGHTS AND POSITION
        drop_height = 2.7
        drop_radius = 0.26
        drop_falling_speed = 0.0189
        river_height = -1.5
        
        bar_x = 0
        bar_y = -0.125
        bar_width =2
        bar_height = 0.25
        
        drops = []
        flag = 0
        
        river_color = [0.2 , 0.5, 0.5]
        game_over_height = 1
        score = 0
        seed = 30
        
        # GAME
        while True:
            
            # WHEN THE GAME ENDS DISPLAY SCORE
            if river_height>=game_over_height:
                screen = pygame.display.set_mode((800, 600), DOUBLEBUF)
                GAME_FONT = pygame.freetype.Font(None, 24)
                running =  True
    
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            pygame.quit()
    
                    #screen.fill((255,255,255))
                    # You can use `render` and then blit the text surface ...
                    text_surface, rect = GAME_FONT.render("Game Over!", (255, 255, 255))
    
                    screen.blit(text_surface, (350, 250))
                    # or just `render_to` the target surface.
                    GAME_FONT.render_to(screen, (350, 300), "Score : "+str(score), (255, 255, 255))
    
                    pygame.display.flip()
                    
    
                
            # WHILE THE GAME IS BEING PLAYED SHOW THE GAME SCREEN
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    if bar_x >= -3:
                        bar_x = bar_x -0.5
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    if bar_x <= 3:
                        bar_x = bar_x +0.5
                elif event.type == KEYDOWN and event.key == K_UP :
                    if bar_y <= 2:
                        bar_y = bar_y +0.5
                elif event.type == KEYDOWN and event.key == K_DOWN :
                    if bar_y - 0.5 >=river_height:
                        bar_y = bar_y - 0.5
                
                    
            #glRotatef(1, 12.5, 0.01, 0)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            
            #DISPLAY THE RIVER
            river(river_height, drop_height, flag, river_color)
            
            #RANDOM DROP LOCATIONS
            x=[-2.1, -0.9, 0.3, 0.9, 2.1]
            l=[1,2,3,4,5]
            random.seed(seed)
            seed =+1
            
            # GAME 
            for i in range(0,5):
                x_c = random.choice(x) 
                h =int(random.choice(l))
                l.remove(h)
                
                drops.append(Drop(x_c , drop_height-0.7*h, drop_radius, 100, flag, gameDisplay))
                if(drops[i].cy > river_height):                
                    drops[i].cy -= drop_falling_speed
                    drops[i].drawCircle()
                    #COLLISION DETECTION
                    if drops[i].cy <= river_height+0.1 or (bar_x-1 <=drops[i].cx<= bar_x+1 and bar_y-0.125 <= drops[i].cy-drops[i].r <= bar_y+0.125):
                        #COLLISION OF DROP WITH BAR
                        if bar_x-1 <=drops[i].cx<= bar_x+1 and bar_y-0.125 <= drops[i].cy-drops[i].r <= bar_y+0.125:
                            score +=1
                        #COLLISION OF DROP WITH RIVER
                        if drops[i].cy <= river_height+0.1:
                            river_color = [drops[i].color1/10, drops[i].color2/10, drops[i].color3/10]
                            river_height +=0.03
                            bar_y +=0.03  
                        #DELETE THE DROP 
                        del drops[i]
                        #INSERT A NEW THE DROP 
                        drops.insert(i, Drop(-1.9+0.9*i , 2.9, drop_radius, 100, flag, gameDisplay))
                    pass
              
            # DISPLAY THE BAR
            draweRect(bar_x, bar_y, bar_width, bar_height, 153/255, 98/255, 4/255)
            
            # DISPLAY THE SIDE BAR FOR MAX LEVEL
            draweRect(-2.5, game_over_height,0.5, 0.125 ,0.5, 0.35, 0.05)
            draweRect(2.5, game_over_height, 0.5, 0.125, 0.5, 0.35, 0.05)
            
          
               
            pygame.time.wait(10)
    
            pygame.display.flip()     
            
    
main()
  
