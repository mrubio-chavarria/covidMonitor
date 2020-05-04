
from pathlib import Path
from covid_phylo.src.iqtree import align_selector
from covidMonitor.settings import STRUCTURES_DIR

def aux_counter(text):
    for align in text.split('>'):
        row = align.split('\n')
        new_row = []
        tag = ''
        i = 0
        for chunk in row:
            if i == 0:
                tag = chunk
                i += 1
                continue
            new_row.append(chunk)
        if len(new_row) != 0:
            yield tag, ''.join(new_row)


def positions_extractor(aligns, n):
    for align in aligns:
        yield align[n]


def positions_analyzer(aligns):
    positions = range(0, len(aligns[0]))
    for pos in positions:
        poss = list(set(positions_extractor(aligns, pos)))
        if len(poss) > 2:
            yield int(pos)

def tags_divider(row_aligns, flag=False):
    """
    DESCRIPTION:
    True to return the tags.
    """
    for align in row_aligns:
        if flag:
            yield align[0].split(' ')[0]
        else:
            yield align[1]


def aligns_filter(aligns, positions, tags):
    for i in range(0, len(aligns)):
        chunk = [aligns[i][pos] for pos in positions]
        yield f'>{tags[i]}\n' + ''.join(chunk)


def preprocess(url_file, reduction, tag):

    file = open(url_file, 'r')
    text = file.read()
    file.close()

    if reduction:
        text = align_selector(text, 100)

    row_aligns = list(aux_counter(text))
    aligns = list(tags_divider(row_aligns))
    tags = list(tags_divider(row_aligns, True))

    positions = list(positions_analyzer(aligns))

    align_buffer = list(aligns_filter(aligns, positions, tags))
    align_buffer = '\n'.join(align_buffer)
    route = STRUCTURES_DIR + f'/{tag}'
    Path(route).mkdir(exist_ok=True)
    fileroute = route + f'/{tag}.txt'
    file = open(fileroute, 'w')
    file.write(align_buffer)
    file.close()

    return fileroute
