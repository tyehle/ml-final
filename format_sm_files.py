
def __extract_title(line):
    pass

def __extract_author(line):
    pass

def __extract_clef(line):
    pass

def __extract_time_signature(line):
    pass

def __extract_piece(line, sheet_music):
    pass

def __extract_measure(line, sheet_music):
    pass

def __extract_note(line, sheet_music):
    pass

def open_sm_file(filename, sheet_music):

    piece = open(filename, 'r')

    for line in piece:
        sheet_music.assign_title(__extract_title(line))
        sheet_music.assign_author(__extract_author(line))
        sheet_music.assign_clef(__extract_clef(line))
        __extract_piece(line, sheet_music)

    piece.close()



def save_sm_file(filename):
    pass