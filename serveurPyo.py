#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 00:10:38 2020

@author: j
"""

from pyo import *

s = Server()




inputs, outputs = pa_get_devices_infos()
"""on récupère la liste des périphériques audio"""
for index in sorted(outputs.keys()):
    """pour chaque périphérique"""
    if outputs[index]['name'] == 'pulse' :
        """si le périphérique s'appele 'pulse'"""
        x = index
        """on sauvegarde son index"""
s.setOutputDevice(x)
"""on conecte le serveur son au périphérique grace à la sauvegarde de son
index"""


s.boot()
s.start()
s.setMidiInputDevice(1)

# Default arguments of the Notein object.
# - 10 voices of polyphony, which means that this object will manage
#   10 pitch/velocity streams simultaneously.
# - scale=0 means that the pitch information will be MIDI numbers.
#   Use 1 for Hertz and 2 for transposition factors.
# - first and last arguments are the lowest and highest MIDI notes
#   that this object will handle. This is useful to split the complete
#   range over multiple processes.
# - channel is the MIDI channel this object will listen to. 0 means all
#   channels.
# - The mul argument affects velocities, which are already normalized
#   between 0 and 1.
notes = Notein(poly=10, scale=0, first=0, last=127, channel=0, mul=1)

# User can show a keyboard widget to supply MIDI events.
#notes.keyboard()

# Notein["pitch"] retrieves pitch streams.
# Converts MIDI pitch to frequency in Hertz.
freqs = MToF(notes["pitch"])

# Notein["velocity"] retrieves normalized velocity streams.
# Applies a portamento on the velocity changes.
amps = Port(notes["velocity"], risetime=0.5, falltime=0.5, mul=0.3)
#amps = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=2, mul=.5)


# Creates two groups of oscillators (10 per channel), slightly detuned.
sigL = Sine(freq=freqs, mul=amps).out()
#sigR = Sine(freq=freqs, phase = 0.2, mul=amps)

#sigL = RCOsc(freq=freqs, sharp=0.5, mul=amps)
#sigR = RCOsc(freq=freqs*1.003, sharp=0.5, mul=amps)

# Mixes the 10 voices per channel to a single stream and send the
# signals to the audio output.
#outL = sigL.mix(1).out()
#outR = sigR.mix(1).out(1)

# Notein["trigon"] sends a trigger when a voice receive a noteon.
# Notein["trigoff"] sends a trigger when a voice receive a noteoff.

# These functions are called when Notein receives a MIDI note event.
def noteon(voice):
    "Print pitch and velocity for noteon event."
    pit = int(notes["pitch"].get(all=True)[voice])
    vel = int(notes["velocity"].get(all=True)[voice] * 127)
#    print("Noteon: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

def noteoff(voice):
    "Print pitch and velocity for noteoff event."
    pit = int(notes["pitch"].get(all=True)[voice])
    vel = int(notes["velocity"].get(all=True)[voice] * 127)
#    print("Noteoff: voice = %d, pitch = %d, velocity = %d" % (voice, pit, vel))

# TrigFunc calls a function when it receives a trigger. Because notes["trigon"]
# contains 10 streams, there will be 10 caller, each one with its own argument,
# taken from the list of integers given at `arg` argument.
tfon = TrigFunc(notes["trigon"], noteon, arg=list(range(10)))
tfoff = TrigFunc(notes["trigoff"], noteoff, arg=list(range(10)))

#sine = Sine(freq=400, mul=.1).out()




s.gui(locals())
