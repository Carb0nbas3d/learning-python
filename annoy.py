import subprocess  # as sp
import time as ti
import random #as ra
import playsound

commands = ["xteddy","xalex","xbobo","xbrummi","xcherubino","xduck","xhedgehog","xklitze","xnamu","xorca","xpenguin","xpuppy","xruessel","xtrouble","xtuxxy"]
for x in range(50):
	geo = "400x400+{}+{}".format(random.randint(0,1200), random.randint(0,800))
	subprocess.Popen([random.choice(commands), "-geometry", geo,"-noquit","-float"])
	playsound.playsound("jump{}.wav".format(random.randint(8,12)))
	ti.sleep(0.025)
