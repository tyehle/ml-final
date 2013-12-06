"""
Author : Kyle Ray
Date   : November 2013

This file contains helper functions used primarily to load and save .sm
file for use by the MusicSheet class. open_sm_file and save_sm_file should
be the only methods called from this file. All other methods are private
and used as helper methods.
"""

import music_sheet as ms
import os

def __trim_string(line):
    """ This is used to trim all special characters
        and lead and trailing white space from the
        line. """
    line = line.strip()
    line = line.rstrip()
    return line

def __remove_tags(line, end_tag):
    """ This will remove the tags used in a .sm file to specify
        attributes. Just give the ending tag verbatim. """
    tag = end_tag.replace('/', '')
    line = line.replace(tag, '')
    line = line.replace(end_tag, '')
    return line

def __extract_attribute(line, attribute):
    """ Given an attribute tag, this will get rid of all superfulous
        detail and return the string. """
    tag = '</' + attribute + '>'
    line = __trim_string(line)
    line = __remove_tags(line, tag)
    line = line.strip()
    return line

def __extract_title(line):
    """ This method will extract the title from the line. """
    return __extract_attribute(line, 'title')

def __extract_author(line):
    """ This method will extract the author from the line. """
    return __extract_attribute(line, 'author')

def __extract_clef(line):
    """ This method will extract the clef from the line and
        convert it to its proper enum. """
    line = __extract_attribute(line, 'clef')

    clef = None
    for enums in ms.Clef:
        if line.upper() == enums.name:
            clef = enums

    return clef

def __extract_time_signature(line):
    """ This method will extract the  time from the line. """
    return __extract_attribute(line, 'time')

def __extract_piece(piece, sheet_music):
    """ This method will extract the entire piece by breaking it down
        to its individual measures and extracting each note from there.
        It will then reconstruct the piece by adding each note to each
        measure in MusicSheet. """
    line = '<piece>'
    while '</piece>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<measure>' in line:
            sheet_music.create_measure()
            __extract_measure(piece, sheet_music)

def __extract_measure(piece, sheet_music):
    """ This will extract an individual measure by extracting each note in
        the measure and adding it to the measure in MusicSheet. """
    line = '<measure>'
    while '</measure>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<note>' in line:
            note_type, pitch, accidental = __extract_note(piece)
            sheet_music.add_note_to_measure(note_type, str(pitch), accidental)

def __extract_note(piece):
    """ This will extract a note by returning each of its attributes. """
    line = '<note>'

    note_type = None
    pitch = ''
    accidental = None

    while '</note>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<type>' in line:
            line = __remove_tags(line, '</type>')
            line = __trim_string(line)
            for enums in ms.NoteType:
                if enums.name == line.upper():
                    note_type = enums
                    break
        if '<pitch>' in line:
            line = __remove_tags(line, '</pitch>')
            line = __trim_string(line)
            pitch = line
        if '<accidental>' in line:
            line = __remove_tags(line, '</accidental>')
            line = __trim_string(line)
            for enums in ms.Accidentals:
                if enums.name == line.upper():
                    accidental = enums
                    break

    return note_type, pitch, accidental


def open_sm_file(filename, sheet_music):
    """ The will open a .sm file and extract all its attributes to create
        a MusicSheet class """
    piece = open(filename, 'r')

    while True:
        line = piece.readline()
        line = __trim_string(line)

        if "<title>" in line:
            sheet_music.assign_title(__extract_title(line))
        if "<author>" in line:
            sheet_music.assign_author(__extract_author(line))
        if "<clef>" in line:
            sheet_music.assign_clef(__extract_clef(line))
        if "<time>" in line:
            sheet_music.assign_time_signature(__extract_time_signature(line))
        if "<piece>" in line:
            __extract_piece(piece, sheet_music)
            break
    piece.close()



def save_sm_file(filename, music_sheet):
    """ This method will take the MusicSheet class and save its
        contents into the .sm file. """
    if '.sm' not in filename:
        return

    if os.path.exists(filename):
        os.remove(filename)

    piece = open(filename, 'w')

    title = music_sheet.get_title()
    author = music_sheet.get_author()
    clef = music_sheet.get_clef()
    time = music_sheet.get_time()
    measures = music_sheet.get_measures()

    piece.write('<title>' + title + '</title>\n')
    piece.write('<author>' + author + '</author>\n')
    piece.write('<clef>' + clef.name + '</clef>\n')
    piece.write('<time>' + str(time[0]) + '|' + str(time[1]) + '</time>\n')
    piece.write('<piece>\n')

    for measure in measures:
        piece.write('<measure>\n')
        for note in measure.notes:
            piece.write('<note>\n')
            piece.write('<type>' + note.note_type.name + '</type>\n')
            piece.write('<pitch>' + note.pitch + '</pitch>\n')
            piece.write('<accidental>' + note.accidental.name +
                        '</accidental>\n')
            piece.write('</note>\n')
        piece.write('</measure>\n')

    piece.write('</piece>\n')

    piece.close()
