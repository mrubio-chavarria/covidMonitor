from django.db import models
import ete3
from covid_phylo.src.iqtree import tree_creator
from covidMonitor.settings import IMAGES_DIR


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
    def render_map(self, name_image):
        """
        DESCRIPTION:
        A method to, given the newick structure, render the whole map.
        :return: None.
        """
        # Obtain the tree
        newick = self.tree.newick_structure
        tree = ete3.Tree(newick)
        print(self.layout)
        # Set the layout
        if self.tree.layout == 'pi':
            circular_style = ete3.TreeStyle()
            circular_style.mode = 'c'
            circular_style.scale = 20
        elif self.tree.layout == 'mu':
            circular_style = ete3.TreeStyle()
            circular_style.mode = 'r'
            circular_style.scale = 0.2
        else:
            circular_style = ete3.TreeStyle()
            circular_style.mode = 'c'
            circular_style.scale = 40
        # Store images
        image_url = IMAGES_DIR + '/' + f'{name_image}.png'
        tree.render(image_url, w=2048, units='mm', tree_style=circular_style)
        self.image_url = image_url
        self.save()


