from random import random, seed, choice
from scamp import *
import random
import time
import json
from procedural import *

s = Session()

s.tempo = 120

try:
    drum = s.new_midi_part('drums', 1)
    p_bass = s.new_midi_part('Electric Bass (pick)', 2)
    d_guitar = s.new_midi_part('Distortion Guitar', 3)
except:
    drum = s.new_part('drums')
    p_bass = s.new_part('Electric Bass (pick)')
    d_guitar = s.new_part('Distortion Guitar')
    



#Negative note means: a silence with the duration of said note

def play_guitar(notas, rythm):
    for d in range(len(rythm)):
        if rythm[d] < 0.0:
            if type(notas[d]) == int:
                d_guitar.play_note(notas[d], 0.0, (rythm[d]* -1))
            else:
                d_guitar.play_chord(notas[d], 0.0, (rythm[d]* -1))
        else:
            if type(notas[d]) == int:
                d_guitar.play_note(notas[d], 1.0, rythm[d])
            else:
                d_guitar.play_chord(notas[d], 1.0, rythm[d])

def play_bass(notas, rythm):
    for d in range(len(rythm)):
        if rythm[d] < 0.0:
            p_bass.play_note(notas[d], 0.0, (rythm[d]* -1))
        else:
            p_bass.play_note(notas[d], 1.0, rythm[d])

def play_snare(notas):
    for d in range(len(notas)):
        if notas[d] < 0.0:
            drum.play_note(38, 0.0, (notas[d]* -1))
        else:
            drum.play_note(38, 1.0, notas[d])
        

def play_kick_drum(notas):
    for d in range(len(notas)):
        if notas[d] < 0.0:
            drum.play_note(36, 0.0, (notas[d] * -1))
        else:
            drum.play_note(36, 1.0, notas[d])

def play_cimbal(notas):
    for d in range(len(notas)):
        if notas[d] < 0.0:
            drum.play_note(58, 0.0, (notas[d] * -1))
        else:
            drum.play_note(58, 1.0, notas[d])

def play_hhat(notas):
    for d in range(len(notas)):
        if notas[d] < 0.0:
            drum.play_note(42, 0.0, (notas[d] * -1))
        else:
            drum.play_note(42, 1.0, notas[d])


def play_song(song):

    string = song['string']
    perc = song['perc']
    song_length = len(string['rythm'])

    
    for i in range(0, song_length - 1):

        s.fork(play_guitar, args=[string['guitar_notes'][i], string['rythm'][i]])
        #s.fork(play_bass, args=[string['bass'][i], string['b_rythm'][i]])
        s.fork(play_kick_drum, args=[perc['kick'][i]])
        s.fork(play_hhat, args=[perc['hhat'][i]]) 
        s.fork(play_snare, args=[perc['snare'][i]])
        s.fork(play_cimbal, args=[perc['cimbal'][i]])

        s.wait_for_children_to_finish()
            
        
composer = Procedural()
song = composer.composer()
play_song(song)