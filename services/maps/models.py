from django.db import models
import ete3
from covid_phylo.src.iqtree import tree_creator
from covidMonitor.settings import IMAGES_DIR
from ete3 import NodeStyle


class Alignment(models.Model):
    """
    DESCRIPTION:
    Model to store all the information related to the alignment of a set of sequences.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    genomes_file = models.URLField(null=True, blank=True)
    processed_file = models.URLField(null=True, blank=True)
    info_file = models.FileField(null=True, blank=True)
    tag = models.CharField(max_length=20, default='default_tag')
    objects = models.Manager()


class Tree(models.Model):
    """
    DESCRIPTION:
    Model to store all the information related to the tree provided an alignment.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    alignment = models.ForeignKey(Alignment, null=True, blank=True, on_delete=models.CASCADE, related_name='trees')
    newick_structure = models.CharField(null=True, blank=True, max_length=2000000)
    # It is not implemented any unique constraint but it is supposed that the following attribute could be PK
    tag = models.CharField(max_length=20, default='default_tag')
    layout = models.CharField(max_length=2, default='pi')
    objects = models.Manager()

    # Methods
    def newick_method(self, url, tag):
        """
        DESCRIPTION:
        A method that, provided the url of an alignment file, creates the newick tree.
        """
        self.newick_structure = tree_creator(url, tag)
        self.save()


class Representation(models.Model):
    """
    DESCRIPTION:
    Model to store the different visualizations of the same tree.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    tree = models.ForeignKey(Tree, null=True, blank=True, on_delete=models.SET_NULL, related_name='representations')
    image_url = models.URLField(max_length=2000, null=True, blank=True)
    tag = models.CharField(max_length=20, default='default_tag')
    layout = models.CharField(max_length=2, default='pi')
    objects = models.Manager()

    # Methods
    def render_map(self):
        """
        DESCRIPTION:
        A method to, given the newick structure, render the whole map.
        :return: None.
        """
        # Obtain the tree
        newick = self.tree.newick_structure
        tree = ete3.Tree(newick)
        # Set the layout
        if self.tree.layout == 'pi':
            style = ete3.TreeStyle()
            style.mode = 'c'
            style.scale = 2
        elif self.tree.layout == 'mu':
            style = ete3.TreeStyle()
            style.mode = 'r'
            style.scale = 2
        else:
            style = ete3.TreeStyle()
            style.mode = 'c'
            style.scale = 4
        # Store images
        image_url = IMAGES_DIR + '/' + f'{self.tag}.png'
        # Set static node style
        nstyle = NodeStyle()
        flag = self.tag[-2::]
        style.show_leaf_name = True
        if flag == 'mu':
            nstyle["fgcolor"] = "darkred"
        else:
            nstyle["fgcolor"] = "darkblue"
        nstyle["shape"] = "sphere"
        nstyle["size"] = 10
        nstyle["hz_line_type"] = 1
        nstyle["hz_line_color"] = "#cccccc"
        for n in tree.traverse():
            n.set_style(nstyle)
        # Render image
        width = 2048
        if flag == 'mu':
            width = 0.5*width
        tree.render(image_url, w=width, units='mm', tree_style=style)
        self.image_url = image_url
        self.save()


