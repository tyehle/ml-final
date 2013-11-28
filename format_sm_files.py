
from music_sheet import NoteType
from music_sheet import Accidentals
from music_sheet import Clef

def __trim_string(line):
    line.strip()
    line.rstrip()
    return line

def __remove_tags(line, end_tag):
    tag = end_tag.replace('/', '')
    line = line.substring(tag, '')
    line = line.substring(end_tag, '')
    return line

def __extract_title(line):
    line = __trim_string(line)
    line = __remove_tags(line, '</title>')
    line = line.strip()
    return line

def __extract_author(line):
    line = __trim_string(line)
    line = __remove_tags(line, '</author>')
    line = line.strip()
    return line

def __extract_clef(line):
    line = __trim_string(line)
    line = __remove_tags(line, '</clef>')
    line = line.strip()

    clef = ''
    for enums in Clef:
        if line == enums.name:
            clef = enums

    return clef

def __extract_time_signature(line):
    line = __trim_string(line)
    line = __remove_tags(line, '</time>')
    line = line.strip()
    return line

def __extract_piece(piece, sheet_music):
    while '</piece>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<measure>' in line:
            sheet_music.create_measure()
            __extract_measure(piece, sheet_music)

def __extract_measure(piece, sheet_music):
    while '</measure>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<note>' in line:
            note_type, pitch, accidental = __extract_note(piece, sheet_music)	
            sheet_music.add_note_to_measure(note_type, pitch, accidental)

def __extract_note(piece, sheet_music):
    line = piece.readline()
    line = __trim_string(line)

    note_type = None
    pitch = ''
    accidental = None

    while '</note>' not in line:
        if '<type>' in line:
            line = __remove_tags(line, '</type>')
            line = __trim_string(line)
            for enums in NoteType:
                if enums.name == line:
                    note_type = enums
        if '<pitch>' in line:
            line = __remove_tags(line, '</type>')
            line = __trim_string(line)
            pitch = line
        if '<accidental>' in line:
            for enums in Accidentals:
                if enums.name == line:
                    accidental = enums

    return note_type, pitch, accidental


def open_sm_file(filename, sheet_music):

    piece = open(filename, 'r')

    while True:
        try:
            if "<title>" in line:
                sheet_music.assign_title(__extract_title(line))
            if "<author>" in line:
                sheet_music.assign_author(__extract_author(line))
            if "<clef>" in line:
	            sheet_music.assign_clef(__extract_clef(line))
            if "<piece>" in line:
                __extract_piece(piece, sheet_music)
        except EOFError:
            break
    piece.close()



def save_sm_file(filename):
    pass
