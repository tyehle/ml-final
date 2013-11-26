"""
Author : Kyle Ray
Date   : November 2013

The music sheet class contains all the information about
a song extracted and classified. This will also store and
load music sheets from storage for use in future
classifications.
"""

from collections import deque
from enum import Enum

class NoteType(Enum):
    """ Length_Type is an enum that gives the length of the note
        as either full, half, quater, or some lower length. """
    FULL = 1
    HALF = 2
    QUATER = 3
    EIGTH = 4
    SIXTEENTH = 5
    THIRTY_SECOND = 6
    SIXTY_FOURTH = 7

class Accidentals(Enum):
    """ Accidentals are in front of the note and modify the pitch. This
        enum will show what accidental, if there is one, of the note will
        be. """
    NONE = 0
    FLAT = 1
    SHARP = 2
    NATURAL = 3
    DOUBLE_FLAT = 4
    DOUBLE_SHARP = 5

class Clef(Enum):
    """ This enum will represent a clef used at the begining of a line to
        denote the pitch type. Even though we will only use Treble and Bass,
        all the possible clefs will be used in case this code is ever expanded
        to match more than one piece of music. """
    TREBLE = 1
    BASS = 2
    FRENCH_VIOLIN = 3
    BARITONE_F = 4
    SUB_BASS = 5
    ALTO = 6
    TENOR = 7
    BARITONE_C = 8
    MEZZO_SOPRANO = 9
    SOPRANO = 10
    OCTAVE = 11
    NEUTRAL = 12
    TABLATURE = 13

class Note(object):
    """ Note acts as a C struct as it only contains information about the note
        in the music sheet class. It will contain the type of note, pitch of
        the note, length of the note, and the accidental in front of the note.

        note_type should be in the form of the Note_Type enum and should only
        contain one of the fields of that enum.

        pitch should be in the form of a string and denotes the pitch letter.
        It can be 'A', 'B', etc or if its a rest, then it should read 'Rest'

        metronome should denote the beats per minute and is denoted by the
        length of the line on a note that is not a full note. It should be
        in the form of an int.

        accidental changes pitch and should be in the form of the
        Accidentals enum and should only contain one of the fields of
        the enum. """
    def __init__(self, note_type, pitch, metronome, accidental):
        """ This will initialize the Note "struct". """
        self.note_type = note_type
        self.pitch = pitch
        self.metronome = metronome
        self.accidental = accidental

class MusicSheet(object):
    """ Music_Sheet is an abstraction of the data from a sheet of music and
        represents a musical composition. """
    def __init__(self, filename):
        """ This will initalize the Sheet Music by either loading one from
            the computer or creating a new one by scratch depending on if
            the user supplied a filename. """
        if type(filename) == str:
            self.load_file(filename)
        else:
            self.title = ''
            self.author = ''
            self.clef = None
            self.measure = None

    def assign_title(self, title):
        """ This will assign the title of piece. """
        self.title = title

    def assign_author(self, author):
        """ This will assign the author of the piece. """
        self.author = author

    def assign_clef(self, clef):
        """ This will assign the clef of the piece. """
        self.clef = clef

    def assign_measure(self, measure):
        """ This will assign the measure of the piece. """
        self.measure = measure

    def add_note(self, note_type, pitch, metronome, accidental):
        """ This will add a new note to the end of the measure. """
        pass

    def save_file(self, filename):
        """ This will save the Sheet Music to a file so that it can be loaded
            and used again for classification. """
        pass

    def load_file(self, filename):
        """ This will load a sheet music file from the computer to be used for
            the classification data. """
        pass
