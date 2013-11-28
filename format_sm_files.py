
import music_sheet as ms

def __trim_string(line):
    line = line.strip()
    line = line.rstrip()
    return line

def __remove_tags(line, end_tag):
    tag = end_tag.replace('/', '')
    line = line.replace(tag, '')
    line = line.replace(end_tag, '')
    return line

def __extract_attribute(line, attribute):
    tag = '</' + attribute + '>'
    line = __trim_string(line)
    line = __remove_tags(line, tag)
    line = line.strip()
    return line

def __extract_title(line):
    return __extract_attribute(line, 'title')

def __extract_author(line):
    return __extract_attribute(line, 'author')

def __extract_clef(line):
    line = __extract_attribute(line, 'clef')

    clef = ''
    for enums in ms.Clef:
        if line.upper() == enums.name:
            clef = enums

    return clef

def __extract_time_signature(line):
    line = __trim_string(line)
    line = __remove_tags(line, '</time>')
    line = line.strip()
    return line

def __extract_piece(piece, sheet_music):
    line = '<piece>'
    while '</piece>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<measure>' in line:
            sheet_music.create_measure()
            __extract_measure(piece, sheet_music)

def __extract_measure(piece, sheet_music):
    line = '<measure>'
    while '</measure>' not in line:
        line = piece.readline()
        line = __trim_string(line)
        if '<note>' in line:
            note_type, pitch, accidental = __extract_note(piece, sheet_music)
            sheet_music.add_note_to_measure(note_type, str(pitch), accidental)

def __extract_note(piece, sheet_music):
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
        if "<piece>" in line:
            __extract_piece(piece, sheet_music)
            break
    piece.close()



def save_sm_file(filename, music_sheet):
    pass
