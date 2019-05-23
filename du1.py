import subprocess
import random


legend={
"."   : "a tile in the dungeon where you can walk on (floor)",
"#"   : "a wall, you can't go through it even when you go faster (trust me I've tried)",
"@"   : "you, less important then the ground",
"M"   : "don't try to touch those [censored] [even more censored] unless you're really good",
"b"   : "bed, it misses you at 3:00 am",
"c"   : "chest, there are cookies inside unless the censoring guy ate all of them [I'm sorry]",
"$"   : "cash, if you collect enough of it, you're gonna make a robber happy one day",
"d"   : "doors you are supposed to open...",
"D"   : "and doors you're not supposed to open, that includes the [censored] COOKIE JAR",
"S"   : "Sphynx, asks many questions but answers only one: when are we ever going to need this?",
"t"   : "Trapdoor,                                                                          there's no low quality joke here",
"W"   : "Water you can't swim in...",
"w"   : "...and water where you can, but don't forget that we are in medevial times were water is a pretty effective poison, just drink something with    alkohol",
"N"   : "Somebody who is so kind to not hate you (That does not mean he likes you)",
"k"   : "Shelf",
"l"   : "Counter, when I last checked him he was at 12947",
"N"   : "killer dogs they are fast and deadly",
"q"   : "a barrel that expands under heat very, very fast"

}

riddles = ["What is (2+3*7483+4498-22+90!-(2*(-2))*0?",
           "Who ate all the Cookies?",
           "What is (2+3*7483+4498-22+90!-(2*(-2))/0?",

           ]

answers = ["0", 
           "(doesn't matter the censoring guy is going to overwrite it with an apology)"
           "(do you know maths?)"
           
           ]


level1 = """
############################################################
#...........b#$$$....cc..............#.....................#
#...........b#$$.....................#......#########.MMM..#
#............#$......................########f#...#.#.M$M..#
#............#.......................#...M..#.#.#.#.#..M...#
#....................................#......#...#...#......#
######D#######.......................#.######.#######......#
#.......qq...........................#........#............#
D............M......q....S...........###.#########.#########
#....................................#.#.#########.........#
######D#######.......................#.#.............#####.#
#............#.......................#.############..#.#...#
#............#.......................#............#..#.#...#
#............#.......................############....#.....#
#............#.......................#.....................#
#............#.............................................#
############################################################
"""
level2 = """
############################################################
#.............#..............WWWWWW........................#
#k...lllllllll#..............WWWWWW......##########........#
#k............#..............WWWWWW......#$$$.....#........#
#.............#..............WWWWWW......#...w....#........#
#k............#..............WWWWWW......#........#........#
#k............#..............WWWWWW...............#........#
#.............#..............WWWWWW......##########........#
#k............#..............WWWWWW........................#
#k............#.....................N......................#
#.............#..............WWWWWW........................#
#.............#..............WWWWWW........................#
#######..######..............WWWWWW........................#
#............................WWWWWW........................#
d............................WWWWWW........................#
d............................WWWWWW........................#
#............................WWWWWW........................#
############################################################
"""
#the neutral entity here only lets you pass for 10 bucks

level3 = """
###################################
#.............................#...#
#.............................D...d
#.............................#...d
#.............................#####
#.................................#
d.................................#
#...............$$$...............#
#...............$$$...............#
#...............$$$...............#
#.................................#
#.................................#
#.................................#
#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW#
#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM#
###################################
"""
#the narrator screams "CG(Censoring guy),IT'S NOT A CHALLENGE TO WIN A GAME OF CHESS TO A MONSTER, player would you please step outside and proof my point?" the moment you step out all the monsters at the back of the room run toward you and drown"

level4 = """
##########
#N.......d
#........#
#........#
d........d
##########
"""
#Narrator (panickly):Run! Run! Think of Super Mario"

class Monster():
    number = 0
    zoo = {}
    
    def __init__(self, x, y, z):
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        self.x = x
        self.y = y
        self.z = z
        
        self.hp = 100
        self.char = "M"
        
    def ai(self, playerpos=None):
        if playerpos is not None:
             # searching player
             pass
        else:
             pass
     
class Hero(Monster):
    def __init__(self, x,y ,z):
        Monster.__init__(self,x,y,z)
        self.hp = 800
        self.char = "@"

class Sphynx(Monster):
    
    def __init___(self, x, y, z):
         Monster.__init__(self, x, y, z)
    
         self.active = True
         self.hp = 400
         self.char= "S"   
         
def help():
    for item in legend:
         print("item:", item)
         subprocess.run(["espeak", item])
         subprocess.run(["espeak", legend[item]])


def game():
    # ------- prepare dungeon ------
    levels = (level1, level2, level3, level4)
    level = []
    
    for z, l in enumerate(levels):
        mylevel = []
        for y, line in enumerate(l.splitlines()):
            myline = []
            for x, char in enumerate(line):
                if char == "S":
                    Sphynx(x,y,z)
                    myline.append(".")
                elif char == "M":
                    Monster(x,y,z)
                    myline.append(".")
                #elif char == "H":
                #   Dog(x,y,z)
                #   myline.append(".")
                else:
                    myline.append(char)
            mylevel.append(myline) 
        level.append(mylevel)
    
    # -------- game engine -----
    hero = Hero(1,2,0)
    
    while hero.hp > 0:
        for y, line in enumerate(level[hero.z]):
            for x, char in enumerate(line):
                # monster?
                for m in Monster.zoo.values():
                    if m.z == hero.z and m.y == y and m.x==x and m.hp >0:
                        print(m.char, end="")
                        break
                else:
                    print(char, end="")
            print()
        command = input(">>>")
        dx = 0
        dy = 0
        if command == "a":
            dx = -1
        if command == "d":
            dx = 1
        if command == "w":
            dy = -1
        if command == "s":
            dy = 1
        # ------ can the hero move as he want? ------
        tile = level[hero.z][hero.y+dy][hero.x+dx]
        if tile == "#" or tile == "D":
            print("I told ya I've tried")
            dx = 0
            dy = 0
        # ------ is a Monster blocking the path ? ----
        for m in Monster.zoo.values():
            if m.number == hero.number:
                continue 
            if m.z != hero.z:
                continue
            if m.hp <= 0:
                continue
            if hero.y + dy == m.y and hero.x + dx == m.x:
                print("a Monster is blocking your path")
                #fight(hero, m)
                dx = 0
                dy = 0
            if tile =="f":
                hero.z += 1
        # ------ magic movement ? triggered something ? -----
        if hero.z == 2 and hero.x == 33 and hero.y == 3 and (dx != 0 or dy != 0):
            # big D changes into small d
            level[2][3][30] = "d"
        # ---------- movement is allowed ----
        hero.x += dx
        hero.y += dy
        # --------- hero stand on something interesting ? ------
        what = level[hero.z][hero.y][hero.x]
        if what == "b":
            print("you found a bed and sleep a bit")
            # if destroyed: level[hero.z][hero.y][hero.x] = "."
        if what == "d" and hero.z == 1:
            hero.z += 1
            hero.x = 33
            hero.y = 3
                   
            
      
if __name__ == "__main__":
    game()
