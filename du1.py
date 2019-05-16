legend={
"."   : "a tile in the dungeon where you can walk on (floor)",
"#"   : "a wall, you can't go through it even when you try faster (trust me I've tried)",
"@"   : "you, less important then the ground",
"M"   : "don't try to touch those [censored] [even more censored] unless you're really good",
"b"   : "bed, it misses you at 3:00 am",
"c"   : "chest, there are cookies inside unless the censoring guy ate all of them [I'm sorry]",
"$"   : "cash, if you collect enough of it, you're gonna make a robber happy one day",
"d"   : "doors you are supposed to open...",
"D"   : "and doors you're not supposed to open, that includes the [censored] COOKIE JAR",
"S"   : "Sphynx, asks many questions but answers only one: when are we ever going to need this?",
"t"   : "Trapdoor,                                                                          there's no low quality joke here",
"W"   : "Water, but don't forget that we are in medevial times were water is a pretty effective poison, just drink something with alkohol",
"N"   : "Somebody who is so kind to not hate you",

}

riddles = ["What is (2+3*7483+4498-22+90!-(2*(-2))*0?",
           "Who ate all the Cookies?",
           
           ]

answers = ["0", 
           "he"
           
           ]


level1 = """
############################################################
#...........b#$$$....cc..............#.....................#
#...........b#$$.....................#......#########.MMM..#
#............#$......................########f#...#.#.M$M..#
#.....@......#.......................#...M..#.#.#.#.#..M...#
#............#.......................#......#...#...#......#
######D#######.......................#.######.#######......#
#.......bb...........................#........#............#
D............M......b....S...........###.#########.#########
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
#............................WWWWWW........................#
#............................WWWWWW......##########........#
#............................WWWWWW......#$$$.....#........#
#............................WWWWWW......#...w....#........#
#............................WWWWWW......#........#........#
#............................WWWWWW...............#........#
#............................WWWWWW......##########........#
#............................WWWWWW........................#
#...................................N......................#
#............................WWWWWW........................#
#............................WWWWWW........................#
#............................WWWWWW........................#
#............................WWWWWW........................#
#............................WWWWWW........................#
#............................WWWWWW........................#
#............................WWWWWW........................#
############################################################
"""

class Monster():
	number = 0
	zoo = {}
	
	def __init__(self, x, y, z):
		self.number = number
		Monster.number += 1
		Monster.zoo{self.number} = self
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
	 

class Sphynx(Monster):
	
	def __init___(self, x, y, z):
		 Monster.__init__(self, x, y, z)
	
	     self.active = True
	     self.hp = 400
	     self.char= "S"	  
	 
