"""
author: Horst JENS
email: horstjens@gmail.com
contact: see http://spielend-programmieren.at/de:kontakt
license: gpl, see http://www.gnu.org/licenses/gpl-3.0.de.html
download: 
idea: clean python3/pygame template using pygame.math.vector2

"""
import pygame
#import math
import random
import os
import time
#import operator
import math
#import vectorclass2d as v
#import textscroller_vertical as ts
#import subprocess
#remember700

"""Best game: 10 waves by Ines"""

def make_text(msg="pygame is cool", fontcolor=(255, 0, 255), fontsize=42, font=None):
    """returns pygame surface with text. You still need to blit the surface."""
    myfont = pygame.font.SysFont(font, fontsize)
    mytext = myfont.render(msg, True, fontcolor)
    mytext = mytext.convert_alpha()
    return mytext

def write(background, text, x=50, y=150, color=(0,0,0),
          fontsize=None, center=False):
        """write text on pygame surface. """
        if fontsize is None:
            fontsize = 24
        font = pygame.font.SysFont('mono', fontsize, bold=True)
        fw, fh = font.size(text)
        surface = font.render(text, True, color)
        if center: # center text around x,y
            background.blit(surface, (x-fw//2, y-fh//2))
        else:      # topleft corner is x,y
            background.blit(surface, (x,y))

def elastic_collision(sprite1, sprite2):
        """elasitc collision between 2 VectorSprites (calculated as disc's).
           The function alters the dx and dy movement vectors of both sprites.
           The sprites need the property .mass, .radius, pos.x pos.y, move.x, move.y
           by Leonard Michlmayr"""
        if sprite1.static and sprite2.static:
            return 
        dirx = sprite1.pos.x - sprite2.pos.x
        diry = sprite1.pos.y - sprite2.pos.y
        sumofmasses = sprite1.mass + sprite2.mass
        sx = (sprite1.move.x * sprite1.mass + sprite2.move.x * sprite2.mass) / sumofmasses
        sy = (sprite1.move.y * sprite1.mass + sprite2.move.y * sprite2.mass) / sumofmasses
        bdxs = sprite2.move.x - sx
        bdys = sprite2.move.y - sy
        cbdxs = sprite1.move.x - sx
        cbdys = sprite1.move.y - sy
        distancesquare = dirx * dirx + diry * diry
        if distancesquare == 0:
            dirx = random.randint(0,11) - 5.5
            diry = random.randint(0,11) - 5.5
            distancesquare = dirx * dirx + diry * diry
        dp = (bdxs * dirx + bdys * diry) # scalar product
        dp /= distancesquare # divide by distance * distance.
        cdp = (cbdxs * dirx + cbdys * diry)
        cdp /= distancesquare
        if dp > 0:
            if not sprite2.static:
                sprite2.move.x -= 2 * dirx * dp
                sprite2.move.y -= 2 * diry * dp
            if not sprite1.static:
                sprite1.move.x -= 2 * dirx * cdp
                sprite1.move.y -= 2 * diry * cdp

class Flytext(pygame.sprite.Sprite):
    def __init__(self, x, y, text="hallo", color=(255, 0, 0),
                 dx=0, dy=-50, duration=2, acceleration_factor = 1.0, delay = 0, fontsize=22):
        """a text flying upward and for a short time and disappearing"""
        self._layer = 7  # order of sprite layers (before / behind other sprites)
        pygame.sprite.Sprite.__init__(self, self.groups)  # THIS LINE IS IMPORTANT !!
        self.text = text
        self.r, self.g, self.b = color[0], color[1], color[2]
        self.dx = dx
        self.dy = dy
        self.x, self.y = x, y
        self.duration = duration  # duration of flight in seconds
        self.acc = acceleration_factor  # if < 1, Text moves slower. if > 1, text moves faster.
        self.image = make_text(self.text, (self.r, self.g, self.b), fontsize)  # font 22
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.time = 0 - delay

    def update(self, seconds):
        self.time += seconds
        if self.time < 0:
            self.rect.center = (-100,-100)
        else:
            self.y += self.dy * seconds
            self.x += self.dx * seconds
            self.dy *= self.acc  # slower and slower
            self.dx *= self.acc
            self.rect.center = (self.x, self.y)
            if self.time > self.duration:
                self.kill()      # remove Sprite from screen and from groups

class Mouse(pygame.sprite.Sprite):
    def __init__(self, radius = 50, color=(255,0,0), x=320, y=240,
                    startx=100,starty=100, control="mouse", ):
        """create a (black) surface and paint a blue Mouse on it"""
        self._layer=10
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.radius = radius
        self.color = color
        self.startx=startx
        self.starty=starty
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.delta = -10
        self.age = 0
        self.pos = pygame.mouse.get_pos()
        self.move = 0
        self.tail=[]
        self.create_image()
        self.rect = self.image.get_rect()
        self.control = control # "mouse" "keyboard1" "keyboard2"
        self.pushed = False

    def create_image(self):

        self.image = pygame.surface.Surface((self.radius*0.5, self.radius*0.5))
        delta1 = 12.5
        delta2 = 25
        w = self.radius*0.5 / 100.0
        h = self.radius*0.5 / 100.0
        # pointing down / up
        for y in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,0+y),(50*w,15*h+y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,15*h+y),(65*w,0+y),2)
    
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (35*w,100*h-y),(50*w,85*h-y),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (50*w,85*h-y),(65*w,100*h-y),2)
        # pointing right / left                 
        for x in (0,2,4):
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (0+x,35*h),(15*w+x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (15*w+x,50*h),(0+x,65*h),2)
            
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (100*w-x,35*h),(85*w-x,50*h),2)
            pygame.draw.line(self.image,(self.r-delta2,self.g,self.b),
                         (85*w-x,50*h),(100*w-x,65*h),2)
        self.image.set_colorkey((0,0,0))
        self.rect=self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self, seconds):
        if self.control == "mouse":
            self.x, self.y = pygame.mouse.get_pos()
        elif self.control == "keyboard1":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_w]:
                self.y -= delta
            if pressed[pygame.K_s]:
                self.y += delta
            if pressed[pygame.K_a]:
                self.x -= delta
            if pressed[pygame.K_d]:
                self.x += delta
        elif self.control == "keyboard2":
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RSHIFT]:
                delta = 2
            else:
                delta = 9
            if pressed[pygame.K_UP]:
                self.y -= delta
            if pressed[pygame.K_DOWN]:
                self.y += delta
            if pressed[pygame.K_LEFT]:
                self.x -= delta
            if pressed[pygame.K_RIGHT]:
                self.x += delta
        elif self.control == "joystick1":
            pass
        elif self.control == "joystick2":
            pass
        if self.x < 0:
            self.x = 0
        elif self.x > PygView.width:
            self.x = PygView.width
        if self.y < 0:
            self.y = 0
        elif self.y > PygView.height:
            self.y = PygView.height
        self.tail.insert(0,(self.x,self.y))
        self.tail = self.tail[:128]
        self.rect.center = self.x, self.y
        self.r += self.delta   # self.r can take the values from 255 to 101
        if self.r < 151:
            self.r = 151
            self.delta = 10
        if self.r > 255:
            self.r = 255
            self.delta = -10
        self.create_image()

class VectorSprite(pygame.sprite.Sprite):
    """base class for sprites. this class inherits from pygames sprite class"""
    number = 0
    numbers = {} # { number, Sprite }

    def __init__(self, **kwargs):
        self._default_parameters(**kwargs)
        self._overwrite_parameters()
        pygame.sprite.Sprite.__init__(self, self.groups) #call parent class. NEVER FORGET !
        self.number = VectorSprite.number # unique number for each sprite
        VectorSprite.number += 1
        VectorSprite.numbers[self.number] = self
        self.create_image()
        self.distance_traveled = 0 # in pixel
        self.rect.center = (-300,-300) # avoid blinking image in topleft corner
        if self.angle != 0:
            self.set_angle(self.angle)

    def _overwrite_parameters(self):
        """change parameters before create_image is called""" 
        pass

    def _default_parameters(self, **kwargs):    
        """get unlimited named arguments and turn them into attributes
           default values for missing keywords"""

        for key, arg in kwargs.items():
            setattr(self, key, arg)
        if "layer" not in kwargs:
            self._layer = 4
        else:
            self._layer = self.layer
        if "static" not in kwargs:
            self.static = False
        if "pos" not in kwargs:
            self.pos = pygame.math.Vector2(random.randint(0, PygView.width),-50)
        if "move" not in kwargs:
            self.move = pygame.math.Vector2(0,0)
        if "radius" not in kwargs:
            self.radius = 5
        if "width" not in kwargs:
            self.width = self.radius * 2
        if "height" not in kwargs:
            self.height = self.radius * 2
        if "color" not in kwargs:
            #self.color = None
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if "hitpoints" not in kwargs:
            self.hitpoints = 10
        self.hitpointsfull = self.hitpoints # makes a copy
        if "mass" not in kwargs:
            self.mass = 1
        if "damage" not in kwargs:
            self.damage = 1
        if "bounce_on_edge" not in kwargs:
            self.bounce_on_edge = False
        if "kill_on_edge" not in kwargs:
            self.kill_on_edge = False
        if "angle" not in kwargs:
            self.angle = 0 # facing right?
        if "max_age" not in kwargs:
            self.max_age = None
        if "max_distance" not in kwargs:
            self.max_distance = None
        if "picture" not in kwargs:
            self.picture = None
        if "bossnumber" not in kwargs:
            self.bossnumber = None
        if "kill_with_boss" not in kwargs:
            self.kill_with_boss = False
        if "sticky_with_boss" not in kwargs:
            self.sticky_with_boss = False
        if "mass" not in kwargs:
            self.mass = 15
        if "upkey" not in kwargs:
            self.upkey = None
        if "downkey" not in kwargs:
            self.downkey = None
        if "rightkey" not in kwargs:
            self.rightkey = None
        if "leftkey" not in kwargs:
            self.leftkey = None
        if "speed" not in kwargs:
            self.speed = None
        if "age" not in kwargs:
            self.age = 0 # age in seconds
        if "warp_on_edge" not in kwargs:
            self.warp_on_edge = False

    def kill(self):
        if self.number in self.numbers:
           del VectorSprite.numbers[self.number] # remove Sprite from numbers dict
        pygame.sprite.Sprite.kill(self)

    def create_image(self):
        if self.picture is not None:
            self.image = self.picture.copy()
        else:
            self.image = pygame.Surface((self.width,self.height))
            self.image.fill((self.color))
        self.image = self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect= self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height

    def rotate(self, by_degree):
        """rotates a sprite and changes it's angle by by_degree"""
        self.angle += by_degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def set_angle(self, degree):
        """rotates a sprite and changes it's angle to degree"""
        self.angle = degree
        oldcenter = self.rect.center
        self.image = pygame.transform.rotate(self.image0, self.angle)
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = oldcenter

    def update(self, seconds):
        """calculate movement, position and bouncing on edge"""
        # ----- kill because... ------
        if self.hitpoints <= 0:
            self.kill()
        if self.max_age is not None and self.age > self.max_age:
            self.kill()
        if self.max_distance is not None and self.distance_traveled > self.max_distance:
            self.kill()
        # ---- movement with/without boss ----
        if self.bossnumber is not None:
            if self.kill_with_boss:
                if self.bossnumber not in VectorSprite.numbers:
                    self.kill()
            if self.sticky_with_boss:
                boss = VectorSprite.numbers[self.bossnumber]
                #self.pos = v.Vec2d(boss.pos.x, boss.pos.y)
                self.pos = pygame.math.Vector2(boss.pos.x, boss.pos.y)
        self.pos += self.move * seconds
        self.distance_traveled += self.move.length() * seconds
        self.age += seconds
        self.wallbounce()
        self.rect.center = ( round(self.pos.x, 0), -round(self.pos.y, 0) )

    def wallbounce(self):
        # ---- bounce / kill on screen edge ----
        # ------- left edge ----
        if self.pos.x < 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = 0
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = PygView.width 
        # -------- upper edge -----
        if self.pos.y  > 0:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = 0
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = -PygView.height
        # -------- right edge -----                
        if self.pos.x  > PygView.width:
            if self.kill_on_edge:
                self.kill()
            elif self.bounce_on_edge:
                self.pos.x = PygView.width
                self.move.x *= -1
            elif self.warp_on_edge:
                self.pos.x = 0
        # --------- lower edge ------------
        if self.pos.y   < -PygView.height:
            if self.kill_on_edge:
                self.hitpoints = 0
                self.kill()
            elif self.bounce_on_edge:
                self.pos.y = -PygView.height
                self.move.y *= -1
            elif self.warp_on_edge:
                self.pos.y = 0

class Spaceship(VectorSprite):
    
    def _overwrite_parameters(self):
        self.mass =1000
        self.mines = 10
        if self.number == 0:
            self.color = (0,0,255)
        if self.number == 1:
            self.color = (255,0,0)
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.polygon(self.image, self.color, ((0,0),(50,25),(0,50),(25,25)))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()
        
    def fire(self):
        v = pygame.math.Vector2(100,0)
        v.rotate_ip(self.angle)
        v+=self.move
        p = pygame.math.Vector2(self.pos.x, self.pos.y)
        a=self.angle
        t=pygame.math.Vector2(25,0)
        t.rotate_ip(self.angle)
        Rocket(pos=p+t, move=v, angle=a, bossnumber=self.number, color=self.color)

        
class EvilMonster(VectorSprite):
    
    def _overwrite_parameters(self):
        self.rotdelta = 100
        self.rot = 255
        self.mass=1
        self.radius=25
        self.bounce_on_edge=True
    
    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, (255, 255, 0), (25,25), 25)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (10,10), 10)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (40,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.rot += self.rotdelta
        if self.rot > 255:
            self.rot = 255
            self.rotdelta *= -1
        if self.rot < 1:
            self.rot = 1
            self.rotdelta *= -1
       
    def update(self, seconds):
        #---ai----
        if random.random() < 0.01:
            v = pygame.math.Vector2(1,0)
            v.rotate_ip(random.randint(0,360))
            v *= random.random()*50
            self.move += v
        VectorSprite.update(self, seconds)
        oldcenter = self.rect.center
        self.create_image() 
        self.rect.center = oldcenter
        self.set_angle(self.angle)
       
    def kill(self):
        Explosion(pos=self.pos,fragments=100, color=(128, 0, 128),max_age=2.5)
        VectorSprite.kill(self)   
        
class Levelboss(EvilMonster):
    
    def _overwrite_parameters(self):
        EvilMonster._overwrite_parameters(self)
        self.radius = 40
        self.mass = 5000
        self.hitpoints = 50

    def create_image(self):
        self.image = pygame.Surface((80,80))
        pygame.draw.circle(self.image, (255, 255, 0), (40,40), 40)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (10,10), 10)
        pygame.draw.circle(self.image, (self.rot, 0, 0), (70,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.rot += self.rotdelta
        if self.rot > 255:
            self.rot = 255
            self.rotdelta *= -1
        if self.rot < 1:
            self.rot = 1
            self.rotdelta *= -1


class Powerup(VectorSprite):
    
    
    def _overwrite_parameters(self):
        x=random.randint(0,PygView.width)
        y=random.randint(0,PygView.height)
        self.pos=pygame.math.Vector2(x,-y)
    
    def create_image(self):
        self.image=pygame.Surface((30,30))
        pygame.draw.circle(self.image, (0,255,0), (15,15), 15)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
 
    
    
    
    
    
    
class Mine(VectorSprite):    
    
    def _overwrite_parameters(self):
        self.rotdelta = 10
        self.rot = 255
        self.mass=100
        self.radius=10
        
    
    def create_image(self):
        self.image = pygame.Surface((20,20))
        # umfang 
        pygame.draw.circle(self.image, (1,1,1), (10,10), 10)
        # auge
        pygame.draw.circle(self.image, (self.rot, 0, 0), (10,10), 5)
        #pygame.draw.circle(self.image, (self.rot, 0, 0), (40,10), 10)
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        self.rot += self.rotdelta
        if self.rot > 255:
            self.rot = 255
            self.rotdelta *= -1
        if self.rot < 1:
            self.rot = 1
            self.rotdelta *= -1
            
    def update(self, seconds):
        self.create_image()
        VectorSprite.update(self, seconds)

class Fireball(VectorSprite):
    
    def _overwrite_parameters(self):
        self.radius = 1
        self.max_age = 7
        self.damage = 5

    def create_image(self):
        self.image=pygame.Surface((500,500))
        pygame.draw.circle(self.image, (random.randint(200,255),random.randint(200,255),0), (250,250), int(self.radius))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()
        
    def update(self, seconds):
        VectorSprite.update(self, seconds)
        self.radius = (0+self.age) *150
        if self.radius > 100:
            self.kill()
        oldcenter = self.rect.center
        self.create_image() 
        self.rect.center = oldcenter
        
        


class Spark(VectorSprite):
    
    def create_image(self):
        self.image=pygame.Surface((10,5))
        pygame.draw.line(self.image, self.color, (0, random.randint(0,3)),(random.randint(1,10),3),random.randint(1,3))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.image0 = self.image.copy()

    

class Smoke(VectorSprite):

    def _overwrite_parameters(self):
        self.pos=pygame.math.Vector2(self.pos.x, self.pos.y)
        self.max_age=1.4

    def create_image(self):
        self.image = pygame.Surface((50,50))
        pygame.draw.circle(self.image, self.color, (25,25),
                           int(self.age*5))
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, seconds):
        VectorSprite.update(self, seconds)
        #if self.gravity is not None:
         #   self.move += self.gravity * seconds
        self.create_image()
        self.rect=self.image.get_rect()
        self.rect.center=(self.pos.x, -self.pos.y)
        c = int(self.age * 100)
        c = min(255,c)
        self.color=(c,c,c)

class Game():
    
    menuitems = ["exit", "upgrade", "options", "credits"]
    menuindex = 0
    upgradeitems = ["back", "single shot", "shotgun", "mashine gun","rocket", "sniper",
                    "mines", "speed", "HP", "lockdown", "escape pod", "invisibility",
                    "astromech", "driller"]
    creditmenu = ["Artworks and Creative","Samuel Wetter","Advising","Horst Jens","code by ", "Horst Jens and", "Samuel Wetter"]
    #menu =  { "upgrade": ["upgrade rockets", "upgbrade shield", "...."],
            #   "downgrade": [ ... ] ,
             # }

class Explosion():
    
    def __init__(self,pos,fragments=15,color=(255,0,0),startangle=0,endangle=360, max_age=0.5):
    
        for f in range(fragments):
            p=pygame.math.Vector2(pos.x,pos.y)
            m=pygame.math.Vector2(1,0)
            a=random.randint(startangle, endangle)
            m.rotate_ip(a)
            speed=random.randint(50,250)
            m*=speed
            Spark(pos=p,move=m,color=color,angle=a, max_age=random.random()*max_age)

class Rocket(VectorSprite):


    def _overwrite_parameters(self):
        self._layer = 1
        self.kill_on_edge=True    

    def create_image(self):
        self.image = pygame.Surface((10,5))
        pygame.draw.polygon(self.image, self.color,
            [(0,0),(7,0),(10,2),(10,3),(7,4),(0,4)])
        self.image.set_colorkey((0,0,0))
        self.image.convert_alpha()
        self.image0 = self.image.copy()
        self.rect = self.image.get_rect()


class PygView(object):
    width = 0
    height = 0

    def __init__(self, width=640, height=400, fps=30):
        """Initialize pygame, window, background, font,...
           default arguments """
        pygame.init()
        PygView.width = width    # make global readable
        PygView.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((255,255,255)) # fill background white
        self.clock = pygame.time.Clock()
        self.menuduration = 0
        self.menu = False
        self.fps = fps
        self.playtime = 0.0
        # ------ background images ------
        self.backgroundfilenames = [] # every .jpg file in folder 'data'
        try:
            for root, dirs, files in os.walk("data"):
                for file in files:
                    if file[-4:] == ".jpg" or file[-5:] == ".jpeg":
                        self.backgroundfilenames.append(file)
            random.shuffle(self.backgroundfilenames) # remix sort order
        except:
            print("no folder 'data' or no jpg files in it")
        #if len(self.backgroundfilenames) == 0:
        #    print("Error: no .jpg files found")
        #    pygame.quit
        #    sys.exit()
        PygView.bombchance = 0.015
        PygView.rocketchance = 0.001
        PygView.wave = 0
        self.age = 0
        # ------ joysticks ----
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for j in self.joysticks:
            j.init()
        self.paint()
        self.loadbackground()

    def loadbackground(self):
        
        try:
            self.background = pygame.image.load(os.path.join("data",
                 self.backgroundfilenames[PygView.wave %
                 len(self.backgroundfilenames)]))
        except:
            self.background = pygame.Surface(self.screen.get_size()).convert()
            self.background.fill((255,255,255)) # fill background white
            
        self.background = pygame.transform.scale(self.background,
                          (PygView.width,PygView.height))
        self.background.convert()
        

    def paint(self):
        """painting on the surface and create sprites"""
        self.allgroup =  pygame.sprite.LayeredUpdates() # for drawing
        #self.tracergroup = pygame.sprite.Group()
        #self.mousegroup = pygame.sprite.Group()
        #self.explosiongroup = pygame.sprite.Group()
        self.monstergroup = pygame.sprite.Group()
        self.rocketgroup = pygame.sprite.Group()
        self.playergroup = pygame.sprite.Group()
        self.minegroup = pygame.sprite.Group()
        self.fireballgroup = pygame.sprite.Group()
        self.powerupgroup = pygame.sprite.Group()
        self.flytextgroup=pygame.sprite.Group()
        
        EvilMonster.groups = self.allgroup
        Spaceship.groups = self.allgroup, self.playergroup
        #Mouse.groups = self.allgroup, self.mousegroup
        Mine.groups= self.allgroup, self.minegroup
        VectorSprite.groups = self.allgroup
        Flytext.groups = self.allgroup, self.flytextgroup
        #Explosion.groups= self.allgroup, self.explosiongroup
        Rocket.groups= self.allgroup, self.rocketgroup
        EvilMonster.groups= self.allgroup, self.monstergroup
        Fireball.groups= self.allgroup, self.fireballgroup
        Powerup.groups= self.allgroup, self.powerupgroup
        
   
        # ------ player1,2,3: mouse, keyboard, joystick ---
        #self.mouse1 = Mouse(control="mouse", color=(255,0,0))
        #self.mouse2 = Mouse(control='keyboard1', color=(255,255,0))
        #self.mouse3 = Mouse(control="keyboard2", color=(255,0,255))
        #self.mouse4 = Mouse(control="joystick1", color=(255,128,255))
        #self.mouse5 = Mouse(control="joystick2", color=(255,255,255))

        self.player1 =  Spaceship(warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2,-PygView.height/2))
        self.player2 =  Spaceship(warp_on_edge=True, pos=pygame.math.Vector2(PygView.width/2+100,-PygView.height/2))
        
        
        
        for x in range(20):
            EvilMonster( bounce_on_edge=True)

        
    def movement_indicator(self,vehicle,pygamepos, color=(0,200,0)):
        #----heading indicator
        pygame.draw.circle(self.screen,color,pygamepos,100,1)
        h=pygame.math.Vector2(100,0)
        h.rotate_ip(-vehicle.angle)
        target=pygamepos+h
        target=(int(target.x),int(target.y))
        pygame.draw.circle(self.screen,(0,128,0),target,3)           
       
        if vehicle.move.x ==0 and vehicle.move.y==0:
            return
        length=int(vehicle.move.length()/10)
        length=min(10,length)
        v=pygame.math.Vector2(100,0)
        v.rotate_ip(vehicle.move.angle_to(v))
        target=pygamepos+v
        pygame.draw.line(self.screen, color, pygamepos,target,length)
        
           
    def run(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(False)
        oldleft, oldmiddle, oldright  = False, False, False
        self.snipertarget = None
        gameOver = False
        exittime = 0
        self.levelcleared = False
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.playtime += seconds
            if gameOver:
                if self.playtime > exittime:
                    break
            #Game over?
            #if not gameOver:
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                   
                    if event.key==pygame.K_m: 
                        self.menurun()
            
                   
                    # ------ mine laying for player ------    
                    if event.key == pygame.K_c:
                        if self.player1.mines>0:
                            Mine(pos=pygame.math.Vector2(self.player1.pos.x, self.player1.pos.y),bossnumber=self.player1.number)
                            self.player1.mines-=1
                            
                    if event.key == pygame.K_KP0:
                        if self.player2.mines>0:
                            Mine(pos=pygame.math.Vector2(self.player2.pos.x, self.player2.pos.y),bossnumber=self.player2.number)
                            self.player2.mines-=1
                        #print("mine at ", self.player1.pos)
                    # PygView.width/2, PygView.height/2,  "set_angle: 135°", color=(255,0,0), duration = 3, fontsize=20)
                    # ---- stop movement for self.player1 -----
                    if event.key == pygame.K_r:
                        self.player1.move *= 0.1 # remove 90% of movement
                    if event.key == pygame.K_t:
                        self.player2.move *= 0.1
                    if event.key == pygame.K_f:
                        self.player1.move *= 0.1
                        self.player2.move *= 0.1
                    if event.key == pygame.K_g:
                        self.player1.move *=0
                    if event.key == pygame.K_j:
                        self.player2.move *=0
                    if event.key == pygame.K_h:
                        self.player1.move *=0
                        self.player2.move *=0
   
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            
            #--- create powerups -------
            if random.random()<0.01:
                Powerup(max_age=2)
            
            
            # ---- create minibosses when all evilmonsters are dead ---
            if not self.levelcleared:
                if len(self.monstergroup) == 0:
                    for x in range(4):
                        Levelboss()
                    self.levelcleared=True
            
            
            # --- line from eck to mouse ---
            #pygame.draw.line(self.screen, (random.randint(200,250),0,0), (self.player1.pos.x, -self.player1.pos.y), (self.mouse1.x, self.mouse1.y))

            # ------------ pressed keys ------
            pressed_keys = pygame.key.get_pressed()
            

            # if pressed_keys[pygame.K_LSHIFT]:
                # paint range circles for cannons
            if pressed_keys[pygame.K_a]:
                self.player1.rotate(3)
            if pressed_keys[pygame.K_d]:
                self.player1.rotate(-3)
            if pressed_keys[pygame.K_w]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.player1.angle)
                self.player1.move += v
                Smoke(pos=self.player1.pos)
            if pressed_keys[pygame.K_s]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.player1.angle)
                self.player1.move += -v
    
            if pressed_keys[pygame.K_LEFT]:
                self.player2.rotate(3)
            if pressed_keys[pygame.K_RIGHT]:
                self.player2.rotate(-3)
            if pressed_keys[pygame.K_UP]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.player2.angle)
                self.player2.move += v
                Smoke(pos=self.player2.pos)
            if pressed_keys[pygame.K_DOWN]:
                v = pygame.math.Vector2(1,0)
                v.rotate_ip(self.player2.angle)
                self.player2.move += -v
            #---- fire-----
            if pressed_keys[pygame.K_TAB]:
                self.player1.fire()
            if pressed_keys[pygame.K_SPACE]:
                self.player2.fire()
            if pressed_keys[pygame.K_x]:
                self.player1.fire()
                self.player2.fire()
            
          
                
            # ------ mouse handler ------
            #left,middle,right = pygame.mouse.get_pressed()
            #if oldleft and not left:
            #    self.launchRocket(pygame.mouse.get_pos())
            #if right:
            #    self.launchRocket(pygame.mouse.get_pos())
            #oldleft, oldmiddle, oldright = left, middle, right

            # ------ joystick handler -------
                       #if b == 0 and pushed:
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #elif b == 1 and pushed:
                       #    if not self.mouse4.pushed: 
                       #        self.launchRocket((mouses[number].x, mouses[number].y))
                       #        mouses[number] = True
                       #elif b == 1 and not pushed:
                       #    mouses[number] = False
            #pos1 = pygame.math.Vector2(pygame.mouse.get_pos())
            #pos2 = self.mouse2.rect.center
            #pos3 = self.mouse3.rect.center
            
            # write text below sprites
            write(self.screen, "FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)
            self.allgroup.update(seconds)

            # --------- collision detection between monster and rocket -----
            for m in self.monstergroup:
                crashgroup = pygame.sprite.spritecollide(m, self.rocketgroup,
                             False, pygame.sprite.collide_mask)
                for r in crashgroup:
                    m.hitpoints -= r.damage
                    elastic_collision(m,r)
                    Explosion(pos=r.pos, max_age=0.25)
                    r.kill()
            
            #---------collision detection between monster and player-------
            for p in self.playergroup:
                crashgroup = pygame.sprite.spritecollide(p, self.monstergroup,
                             False, pygame.sprite.collide_mask)
                for m in crashgroup:
                    elastic_collision(p,m) 
                    
            #--------collision detection between monster and monster-------
            for m in self.monstergroup:
                crashgroup = pygame.sprite.spritecollide(m, self.monstergroup,
                             False, pygame.sprite.collide_circle)
                for m2 in crashgroup:
                    if m.number < m2.number:
                        elastic_collision(m, m2)
            #----------collision detection between monster and mine----------
            for mi in self.minegroup:
                crashgroup = pygame.sprite.spritecollide(mi, self.monstergroup,
                             False, pygame.sprite.collide_circle)
                for mo in crashgroup:
                    diffvector = mo.pos - mi.pos
                    diffvector.normalize_ip()
                    #print("diffvec", diffvector)
                    mo.move = diffvector * 100
                    Fireball(pos=mi.pos)
                    mi.kill()
            #-----------collision detection between monster and fireball-----
            for f in self.fireballgroup:
                crashgroup = pygame.sprite.spritecollide(f, self.monstergroup,
                             False, pygame.sprite.collide_circle)
                for m in crashgroup:
                    m.hitpoints -= f.damage
                    #print("monsterdamage",m.number,m.hitpoints)
            #----------collision detection between player and powerup----
            for pl in self.playergroup:
                crashgroup=pygame.sprite.spritecollide(pl, self.powerupgroup,
                           False, pygame.sprite.collide_mask)
                for po in crashgroup:
                    po.kill()
                    pl.mines=10
            #--------------pvp-------
            #-----------issue-collision effects self
            #for p in self.playergroup:
             #   crashgroup = pygame.sprite.spritecollide(p, self.rocketgroup,
               #              False, pygame.sprite.collide_mask)
              #  for r in crashgroup:
                #    p.hitpoints -= r.damage
                 #   elastic_collision(p,r)
                  #  Explosion(pos=r.pos, max_age=0.25)
                   # r.kill()
                    
            # ----------- clear, draw , update, flip -----------------
            self.allgroup.draw(self.screen)

            self.movement_indicator(self.player1,(105,105))
            self.movement_indicator(self.player2,(1320,105))
            
            # --- Martins verbesserter Mousetail -----
            #for mouse in self.mousegroup:
             #   if len(mouse.tail)>2:
              #      for a in range(1,len(mouse.tail)):
               #         r,g,b = mouse.color
                #        pygame.draw.line(self.screen,(r-a,g,b),
                                     #mouse.tail[a-1],
                                     #mouse.tail[a],10-a*10//10)
            
            # -------- next frame -------------
            pygame.display.flip()
        #-----------------------------------------------------
        pygame.mouse.set_visible(True)    
        pygame.quit()


    def menurun(self):
        """The mainloop"""
        running = True
        pygame.mouse.set_visible(True)    
        self.menu = True
        oldleft, oldmiddle, oldright = False, False, False
        while running:
            milliseconds = self.clock.tick(self.fps) #
            seconds = milliseconds / 1000
            self.menuduration += seconds
            # -------- events ------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # ------- pressed and released key ------
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # ------ mine laying for player ------    
               
            # delete everything on screen
            self.screen.blit(self.background, (0, 0))
            # ---- wo ist die Maus ---
            x, y = pygame.mouse.get_pos()
            items = len(Game.menuitems)
            if y < 125:
                Game.menuindex = 0
            elif y < 175 and items > 1:
                Game.menuindex = 1
            elif y < 225 and items > 2:
                Game.menuindex = 2
            elif y < 275 and items > 3:
                Game.menuindex = 3
            elif y < 325 and items > 4:
                Game.menuindex = 4
            elif y < 375 and items > 5:
                Game.menuindex = 5
            elif y < 425 and items > 6:
                Game.menuindex = 6
            elif y < 475 and items > 7:
                Game.menuindex = 7
            elif y < 525 and items > 8:
                Game.menuindex = 8
            elif y < 575 and items > 9:
                Game.menuindex = 9
            elif y < 625 and items > 10:
                Game.menuindex = 10
            elif y < 675 and items > 11:
                Game.menuindex = 11
            elif y < 725 and items > 12:
                Game.menuindex = 12
            elif y < 775 and items > 13:
                Game.menuindex = 13
            # --- background rect for selected item ----
            pygame.draw.rect(self.screen, (255,0,255), (100, 100+Game.menuindex * 50 -25, 400, 50))
            # --- menu !!!! ----
            write(self.screen, "Menu", x=375, y=30,color=(255,0,255),
                  fontsize=48, center=True)
            for a,m in enumerate(Game.menuitems):
                write(self.screen, m , x=375, y=100+a*50, color=(1,1,1),
                      fontsize=32, center=True)
            # --- cursor ---
            write(self.screen, "-->", x = 150, y=100+Game.menuindex*50, 
                      color=(1,1,1), fontsize=32, center=True)
            # write text below sprites
            write(self.screen, "menu FPS: {:8.3}".format(
                self.clock.get_fps() ), x=10, y=10)
            self.flytextgroup.update(seconds)
            self.flytextgroup.draw(self.screen)
            
            # ------ mouse handler ------
            left,middle,right = pygame.mouse.get_pressed()
            if oldleft and not left:
                 t=Game.menuitems[Game.menuindex]
                 #Flytext(x=600,y=400, text=t)
                 #auswertung nach linksklick
                 if t == "exit":
                     return
                 elif t == "upgrade":
                     Game.menuitems = Game.upgradeitems
                 elif t == "credits":
                     Game.menuitems = Game.creditmenu
                 
            #    self.launchRocket(pygame.mouse.get_pos())
            #if right:
            #    self.launchRocket(pygame.mouse.get_pos())
            oldleft, oldmiddle, oldright = left, middle, right
            # -------- next frame -------------
            pygame.display.flip()
        # bye bye menu
        pygame.mouse.set_visible(False)    


if __name__ == '__main__':
    PygView(1430,800).run() # try PygView(800,600).run()
