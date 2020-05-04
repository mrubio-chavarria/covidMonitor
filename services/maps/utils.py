
from covidMonitor.settings import BASE_DIR

def aux_counter(text):
    for align in text.split('>'):
        row = align.split('\n')
        new_row = []
        i = 0
        for chunk in row:
            if i == 0:
                i += 1
                continue
            new_row.append(chunk)
        if len(new_row) != 0:
            yield ''.join(new_row)


def positions_extractor(aligns, n):
    for align in aligns:
        yield align[n]


def positions_analyzer(aligns):
    positions = range(0, len(aligns[0]))
    for pos in positions:
        poss = list(set(positions_extractor(aligns, pos)))
        if len(poss) > 2:
            yield int(pos)


def aligns_filter(aligns, positions):
    for align in aligns:
        chunk = [align[pos] for pos in positions]
        yield '>Tag\n' + ''.join(chunk)


def preprocess(url_file):

    file = open(url_file, 'r')
    text = file.read()
    file.close()

    aligns = list(aux_counter(text))
    positions = list(positions_analyzer(aligns))

    align_buffer = list(aligns_filter(aligns, positions))
    align_buffer = '\n'.join(align_buffer)
    file = open(BASE_DIR + '/' + 'temporary_alignment.txt', 'w')
    file.write(align_buffer)
    file.close()


