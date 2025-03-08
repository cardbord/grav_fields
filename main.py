import pygame
from math import sqrt, sin, cos, tan, atan, pi



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
class body():
     def __init__(self, body_radius:int, body_mass:int, initial_pos:tuple=None, initial_velocity:float = None):
          self.m = body_mass
          
          self.r = body_radius
          
          self.pos = [initial_pos[0], initial_pos[1]] if initial_pos != None else [_main_dis[0]*3/4, _main_dis[1]*3/4]

          self.v = initial_velocity if initial_velocity != None else 100.0
          self.horz_v = 0
          self.vert_v = 0
          self.sv = 0

          

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
          return self.pos[0]//(10**9)+_main_dis[0]//2




     @property
     def converted_y(self):
          return self.pos[1]//(10**9)+_main_dis[1]//2
     
     



     
sun = body(6.96*10**8, 1.99*10**30 , (0,0))
earth = body(6.37*10**6, 5.97*10**24, (1.3747*10**11, 1*10**10))
mars = body(3.34*10**6,6.39*10**23,(2.28*10**11,0))


framerate=60
bodies = [sun,earth,mars]
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
                              horz_v += a*cos(angle) * DAY // 2
                              vert_v += a*sin(angle) * DAY // 2
                              
                         elif obb.x < bbb.x and obb.y > bbb.y:
                              horz_v -= a*cos(angle) * DAY // 2
                              vert_v += a*sin(angle) * DAY // 2
                         
                         elif obb.x < bbb.x and obb.y < bbb.y:
                              horz_v -= a*cos(angle) * DAY // 2
                              vert_v -= a*sin(angle) * DAY // 2
                              
                         elif obb.x > bbb.x and obb.y < bbb.y:
                              horz_v += a*cos(angle) * DAY // 2
                              vert_v -= a*sin(angle) * DAY // 2

                         

                         obb.vert_v = vert_v
                         obb.horz_v = horz_v 

                         obb.pos = [obb.x-DAY*obb.horz_v, obb.y-DAY*obb.vert_v]

                         if framerate == 10:
                              print(f'obb>bbb x {obb.x > bbb.x},   obb>bbb y {obb.x > bbb.y},   a {a},   a*DAY = {a*DAY},   horz_v = {horz_v},   vert_v = {vert_v}')
                         


     for body in bodies:
          
               
               
          pygame.draw.circle(dis,(255,0,0),(body.converted_x,body.converted_y),5)

     pygame.display.update()