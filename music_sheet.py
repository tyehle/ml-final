"""
Author : Kyle Ray
Date   : November 2013

The music sheet class contains all the information about
a song extracted and classified. This will also store and
load music sheets from storage for use in future
classifications.
"""

from collections import deque
from collections import namedtuple
from flufl.enum import Enum
from format_sm_files import open_sm_file, save_sm_file

class NoteType(Enum):
    """ NoteType is an enum that gives the type of the note
        as either full, half, quater, or some lower length. """
    FULL = 1
    HALF = 2
    QUATER = 3
    EIGHT = 4
    SIXTEEN = 5
    THIRTY_SECOND = 6
    SIXTY_FOUR = 7

class Accidentals(Enum):
    """ Accidentals are in front of the note and modify the pitch. This
        enum will show what accidental, if there is one, of the note
        will be. """
    NONE = 1
    FLAT = 2
    SHARP = 3
    NATURAL = 4
    DOUBLE_FLAT = 5
    DOUBLE_SHARP = 6

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

# Note acts as a C struct as it only contains information about the note
# in the music sheet class. It will contain the type of note, pitch of
# the note, length of the note, and the accidental in front of the note.
#
# note_type should be in the form of the Note_Type enum and should only
# contain one of the fields of that enum.
#
# pitch should be in the form of a string and denotes the pitch letter.
# It can be 'A', 'B', etc or if its a rest, then it should read 'Rest'
#
# metronome should denote the beats per minute and is denoted by the\
# length of the line on a note that is not a full note. It should be
# in the form of an int.
#
# accidental changes pitch and should be in the form of the
# Accidentals enum and should only contain one of the fields of
# the enum.
Note = namedtuple('Note', ['note_type', 'pitch', 'accidental'])

# A measure is a series of notes confined by the time signature used for easy
# grouping of notes. Measure is just a glorified deque to make reading it
# easier in the MusicSheet class. This will act like a C struct.
Measure = namedtuple('Measure', 'notes')

class MusicSheet(object):
    """ Music_Sheet is an abstraction of the data from a sheet of music and
        represents a musical composition. """
    def __init__(self, filename):
        """ This will initalize the Sheet Music by either loading one from
            the computer or creating a new one by scratch depending on if
            the user supplied a filename. """
        self._title = 'Unknown'
        self._author = 'Unknown'
        self._clef = Clef.TREBLE
        self._time = [4, 4]
        self._measures = deque()

        if type(filename) == str:
            self.load_file(filename)

    def assign_title(self, title):
        """ This will assign the title of piece. """
        self._title = title

    def assign_author(self, author):
        """ This will assign the author of the piece. """
        self._author = author

    def assign_clef(self, clef):
        """ This will assign the clef of the piece. """
        if clef not in Clef:
            raise IllegalArgumentException("clef must be a valid type in"
                                           " enum Clef")
        self._clef = clef

    def assign_time_signature(self, time):
        """ This will assign the time signature of the piece.
            Two forms of the parameter will be expected for
            time signature. The first is a list or a tuple. The
            second is a string which both numbers must be seperated
            by a '|' character."""

        if type(time) is str:
            time = time.split('|')
        if time is tuple:
            time = list(tuple)

        for i in range(len(time)):
            time[i] = int(time[i])

        self._time = time

    def create_measure(self):
        """ This will add a new measure to the end of the compisiton
            so that more notes can be added. This is somewhat like
            adding a bar line."""
        self._measures.appendleft(Measure(deque()))

    def add_note_to_measure(self, note_type, pitch, accidental):
        """ This will append the note to the end of the last measure. This will
            not create a new measure should it reach the end of time signature.
            """
        if note_type not in NoteType:
            raise IllegalArgumentException("note_type must be a valid"
                                           " type from enum NoteType.")
        if type(pitch) is not str:
            raise IllegalArgumentException("pitch must be a string.")

        if accidental not in Accidentals:
            raise IllegalArgumentException("accidental must be a valid type"
                                           " from enum Accidental.")

        self._measures[len(self._measures) - 1].notes.appendleft(Note(note_type,
                                                                      pitch,
                                                                      accidental
                                                                      ))

    def save_file(self, filename):
        """ This will save the Sheet Music to a file so that it can be loaded
            and used again for classification. """
        save_sm_file(filename, self)

    def load_file(self, filename):
        """ This will load a sheet music file from the computer to be used for
            the classification data. """
        open_sm_file(filename, self)

    def get_title(self):
        """ This will return the title of the piece. """
        return self._title

    def get_author(self):
        """ This will return the author of the piece. """
        return self._author

    def get_clef(self):
        """ This will return the clef of the piece. """
        return self._clef

    def get_time(self):
        """ This will return the time signature of the piece. """
        return self._time

    def get_measures(self):
        """ This will return the measures of the piece. """
        return self._measures

class IllegalArgumentException(Exception):
    """ This exception will be called anytime the user gives the music_sheet
        class any argument that is not valid. """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
