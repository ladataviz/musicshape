import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
from music21 import instrument, midi, note, chord, pitch
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import os
import glob
import csv


def open_midi(midi_path, remove_drums):
    # There is an one-line method to read MIDIs
    # but to remove the drums we need to manipulate some
    # low level MIDI events.
    mf = midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    if (remove_drums):
        for i in range(len(mf.tracks)):
            mf.tracks[i].events = [
                ev for ev in mf.tracks[i].events if ev.channel != 10]

    return midi.translate.midiFileToStream(mf)


def print_parts_countour(midi, file):
    with open(file+'.csv', 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(
            ['NoteOctave', 'Note', 'Instrument', 'Position'])
        for i in range(len(midi.parts)):
            pos = 0
            for nt in midi.parts[i].flat.notes:
                if isinstance(nt, note.Note):
                    if midi.parts[i].partName != None:
                        filewriter.writerow(
                            [nt.nameWithOctave, nt.name, midi.parts[i].partName, pos])
                        pos += 1


os.chdir("./MIDIs")

for file in glob.glob("*.mid"):
    base_midi = open_midi(file, True)
    print_parts_countour(base_midi, file)
