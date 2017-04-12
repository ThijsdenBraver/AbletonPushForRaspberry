#!/usr/bin/env python
import sys
import os
import pygame
import pygame.midi
from pygame.locals import *
# display a list of MIDI devices connected to the computer
def print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r
        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"
        print ("%2i: interface: %s, name: %s, opened: %s %s" %
               (i, interf, name, opened, in_out))
pygame.init()
pygame.fastevent.init()
event_get = pygame.fastevent.get
event_post = pygame.fastevent.post
pygame.midi.init()
print ("Available MIDI devices:")
print_device_info();
# Change this to override use of default input device
device_id = 2
if device_id is None:
    input_id = pygame.midi.get_default_input_id()
else:
    input_id = device_id
print ("Using input_id: %s" % input_id)
i = pygame.midi.Input( input_id )
print ("Logging started:")
going = True
while going:
    events = event_get()
    for e in events:
        if e.type in [QUIT]:
            going = False
        if e.type in [KEYDOWN]:
            going = False
        if e.type in [pygame.midi.MIDIIN]:
            # print information to console
            print ("Timestamp: " + str(e.timestamp) + "ms, Channel: " + str(e.data1) + ", Value: " + str(e.data2))
    # if there are new data from the MIDI controller
    if i.poll():
        midi_events = i.read(10)
        midi_evs = pygame.midi.midis2events(midi_events, i.device_id)
        for m_e in midi_evs:
            event_post( m_e )
