from django.db import models
import ete3
from covidMonitor.settings import MEDIA_URL


class Alignment(models.Model):
    """
    DESCRIPTION:
    Model to store all the information related to the alignment of a set of sequences.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    genomes_file = models.FileField(null=True, blank=True)
    alignment_file = models.FileField(null=True, blank=True)
    info_file = models.FileField(null=True, blank=True)
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
    info_file = models.FileField(null=True, blank=True)
    newick_structure = models.FileField(null=True, blank=True)
    objects = models.Manager()


class Representation(models.Model):
    """
    DESCRIPTION:
    Model to store the different visualizations of the same tree.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    tree = models.ForeignKey(Tree, null=True, blank=True, on_delete=models.SET_NULL, related_name='representations')
    image_url = models.URLField(null=True, blank=True)
    objects = models.Manager()

    # Methods
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        DESCRIPTION:
        Overwritten method manage the new objects creation.
        """

        # New objects creation
        if self.pk is None:
            f = self.tree.newick_structure
            file = f.open('r')
            newick_text = file.readlines()
            file.close()
            tree = ete3.Tree(newick_text[0])
            circular_style = ete3.TreeStyle()
            circular_style.mode = "c"
            circular_style.scale = 20
            image_url = MEDIA_URL + 'mytree.png'
            tree.render(image_url, w=2048, units='mm', tree_style=circular_style)
            self.image_url = image_url

        super().save()

