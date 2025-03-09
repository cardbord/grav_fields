import pygame
from math import sqrt, sin, cos, atan, log10, log, log2
from pygame.gfxdraw import filled_circle, aacircle
import numpy as np

pygame.init()
pygame.display.init()
_main_dis = pygame.display.get_desktop_sizes()[0]

dis = pygame.display.set_mode(_main_dis)

#v = sqrt(GM/r)
#a = GM/r^2 

#assuming metres per second, metres, kg and G = 6.67*10**-11

G = 6.67*10**(-11)
DAY = 86400
MINUTE = 60
HOUR = 3600


def logn(value):
     if value < 0:
          return log(abs(value)) * -1
     elif value == 0:
          return 0
     else:
          return log(value)

class body():
     def __init__(self, body_radius:int, body_mass:int, initial_pos:tuple=None, initial_velocity:float = None):
          self.m = body_mass
          
          self.r = body_radius
          
          self.pos = [initial_pos[0], initial_pos[1]] if initial_pos != None else [_main_dis[0]*3/4, _main_dis[1]*3/4]

          self.v = initial_velocity if initial_velocity != None else 100.0
          self.horz_v = 0
          self.vert_v = 0
          self.sv = 0
          self.scale = 9
          

     @property
     def mass(self):
          return self.m
     
     @property
     def radius(self):
          return self.r
     
     @property
     def velocity(self):
          return self.v

     @property
     def x(self):
          return self.pos[0]

     @property
     def y(self):
          return self.pos[1]
     
     @property
     def converted_x(self):
          return self.pos[0]//(10**self.scale)+_main_dis[0]//2
          #print(logn(self.pos[0]))
          #return logn(self.pos[0])*self.scale + _main_dis[0]//2


     @property
     def converted_y(self):
          return self.pos[1]//(10**self.scale)+_main_dis[1]//2

          #return logn(self.pos[1])*self.scale + _main_dis[1]//2
     
     def change_scale(self,new_scale):
          self.scale+=new_scale


#SOLAR SYSTEM INITS
     
SUN = body(6.96*10**8, 1.99*10**30 , (0,0))

MERCURY = body(2439700,3.29*10**23, (0.1, 5.7909*10**10))

VENUS = body(6.051*10**6, 4.87*10**24, (0.1,1.082*10**11))

EARTH = body(6.37*10**6, 5.97*10**24, (0.1, 1.496*10**11))
MOON = body(1737400,7.348*10**22,(0.1,1.496*10**11+3.844*10**8))

MARS = body(3.34*10**6,6.39*10**23,(0.1,2.28*10**11))

JUPITER = body(6.99*10**7,1.898*10**27,(0.1,7.784*10**11))

SATURN = body(5.823*10**7, 5.683*10**26, (0.1,1.4236*10**12))

URANUS = body(2.536*10**7, 8.681*10**25, (0.1,2.867*10**12))

NEPTUNE = body(2.462*10**7, 1.024*10**26, (0.1,4.884*10**12))



framerate=60
bodies = [SUN,MERCURY,VENUS,EARTH,MOON,MARS,JUPITER,SATURN,URANUS,NEPTUNE]
body_masses = []




clock=pygame.time.Clock()
while 1:
     dis.fill((0,0,0))
     clock.tick(framerate)

     for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

               if event.key == pygame.K_h:
                    if framerate == 60:
                         framerate = 10
                    else:
                         framerate = 60

               if event.key == pygame.K_s:
                    if framerate == 200:
                         framerate = 60
                    else:
                         framerate = 200

               

          elif event.type == pygame.MOUSEWHEEL:
               for b in bodies:
                    if b.scale > 8.2 or event.y == -1:
                         b.change_scale(-event.y/100)
                         b.scale = round(b.scale,4)
                         print(b.scale)

     for i in range(len(bodies)):
          for j in range(len(bodies)):
               if i == j:
                    pass
               else:
                    bbb = bodies[j]
                    obb = bodies[i]
                    m = bbb.m
                    
                    #assumed bbb is dominant over obb
                    

                    distance_between = sqrt((obb.x - bbb.x)**2 + (obb.y - bbb.y)**2)
                    a = (G*m)/(distance_between**2)
                    
                    v = sqrt(G*m/distance_between)
                    
                    if a < 0.000001: #below zero, don't care
                         pass
                    else:
                         
                         cy = obb.y - bbb.y
                         cx = obb.x - bbb.x

                         
                         
                         angle = atan(abs(cy) / abs(cx))
                         

                         

                         if obb.x > bbb.x:
                              vert_v = v*cos(angle)
                              
                              


                         else:
                              vert_v = -v*cos(angle)
                              
                              
                              
                         

                         if obb.y > bbb.y:
                              horz_v = -v*sin(angle)


                              

                         else:
                              horz_v = v*sin(angle)

                              
                         if obb.x > bbb.x and obb.y > bbb.y:
                              horz_v += a*cos(angle) * DAY / 2
                              vert_v += a*sin(angle) * DAY / 2
                              
                         elif obb.x < bbb.x and obb.y > bbb.y:
                              horz_v -= a*cos(angle) * DAY / 2
                              vert_v += a*sin(angle) * DAY / 2
                         
                         elif obb.x < bbb.x and obb.y < bbb.y:
                              horz_v -= a*cos(angle) * DAY / 2
                              vert_v -= a*sin(angle) * DAY / 2
                              
                         elif obb.x > bbb.x and obb.y < bbb.y:
                              horz_v += a*cos(angle) * DAY / 2
                              vert_v -= a*sin(angle) * DAY / 2

                         

                         obb.vert_v = vert_v
                         obb.horz_v = horz_v 

                         obb.pos = [obb.x-DAY*obb.horz_v, obb.y-DAY*obb.vert_v]

                         if framerate == 10:
                              print(f'obb>bbb x {obb.x > bbb.x},   obb>bbb y {obb.x > bbb.y},   a {a},   a*DAY = {a*DAY},   horz_v = {horz_v},   vert_v = {vert_v}')
                         

     rarr = []
     for body in bodies:


          #br = log(body.radius) 
          #lr = log(10**(body.scale-7))
          
          #hh = br / lr
          #g = round(hh)
          
          
          #pygame.draw.circle(dis,(255,0,0),(body.converted_x,body.converted_y),log(body.radius,body.scale))
          #filled_circle(dis,int(round(body.converted_x)),int(round(body.converted_y)),g-3,(255,0,0))
          #aacircle(dis,int(round(body.converted_x)),int(round(body.converted_y)),g-3,(255,0,0))
          filled_circle(dis,int(round(body.converted_x)),int(round(body.converted_y)),3,(255,0,0))
          aacircle(dis,int(round(body.converted_x)),int(round(body.converted_y)),3,(255,0,0))


     pygame.display.update()