
import os
import subprocess

from covid_phylo.src.config import TREE_DIR


def tree_creator(selectname):
    """
    DESCRIPTION:
    A function create the tree inference and store the results in a subfolder within covid_phylo/tree/
    :param selectname: [string] name of the file to be put in the tree folder. The same as the name of the subfolder.
    :return: None
    """
    print('Executing tree inference')
    filename = selectname
    subfolder = selectname.split('.')[0]
    route = TREE_DIR / subfolder / filename
    # process = subprocess.run(['cd', 'covid_phylo/covid_phylo_data;', 'iqtree', '-s', f'{route}', '-bnni', '-nt', 'AUTO'])
    command = f'cd covid_phylo/covid_phylo_data; iqtree -s {route} -bnni -nt AUTO'
    returncode = subprocess.call(command, shell=True)
    file = open(selectname + '.treefile', 'r')
    newick_tree = file.read()
    file.close()
    print('Tree inference completed with exit code %d' % returncode)
    return newick_tree

def align_selector(aligns, n_genomes):
    """
    DESCRIPTION:
    Function to select the n alignments with the lowest number of gaps.
    :param aligns: [string] string with the content of the whole file.
    :param n_genomes: [integer] number of alignments to be taken.
    :return: the data of the file the selected number of instances.
    """

    data = aligns.split('>')[1::]  # The first element is an empty string

    # Take the best n models
    gaps = list(enumerate([model.count('-') for model in data]))
    data = '\n'.join(['>' + data[element[0]] for element in sorted(gaps, key=lambda x: x[1])[0:n_genomes]])

    return data

