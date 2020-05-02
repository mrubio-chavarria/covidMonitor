from django.db import models


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


class Representation(models.Model):
    """
    DESCRIPTION:
    Model to store the different visualizations of the same tree.
    """

    # Attributes
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    tree = models.ForeignKey(Tree, null=True, blank=True, on_delete=models.SET_NULL, related_name='representations')
    image = models.ImageField(null=True, blank=True)

