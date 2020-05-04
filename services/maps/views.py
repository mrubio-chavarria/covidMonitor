import zipfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Tree, Alignment, Representation
from .serializers import TreeSerializer
from django.core.files import File
from covidMonitor.settings import MEDIA_URL, BASE_DIR, COVID_PHYLO_ROOT
from .utils import preprocess
import pyqtgraph as pg


class MapViewSet(viewsets.ModelViewSet):
    """
    DESCRIPTION:
    Class to set the CBV approach of the app.
    """

    # Attributes
    queryset = Tree.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = TreeSerializer

    # Methods
    def base_view(self, tag, alignment):
        """
        DESCRIPTION:
        The basic scheme of every view.
        """
        aligned_file = COVID_PHYLO_ROOT + '/' + 'fasta' + '/' + alignment
        # Obtain the processed alignment
        processed_file = preprocess(aligned_file, True, tag)
        align, flag = Alignment.objects.get_or_create(tag=tag)
        print(flag)
        align.genomes_file = aligned_file
        align.processed_file = processed_file
        align.save()
        # Obtain the tree
        tree, flag = Tree.objects.get_or_create(tag=tag)
        print(flag)
        print(tree.layout)
        tree.alignment = align
        tree.newick_method(processed_file, tag)
        # Obtain the map
        map, flag = Representation.objects.get_or_create(tag=tag)
        print(flag)
        map.tree = tree
        map.render_map(tag)
        image = '/static/' + map.image_url.split('/')[-1]
        image = {'image': image}
        return image

    @action(detail=False, methods=['GET', ])
    def button_complete(self, request):
        """
        DESCRIPTION:
        View to render the map of the complete genome.
        """
        # Initial data
        tag = 'complete_genome'
        alignment = 'complete_20200502024515_aligned'
        image = self.base_view(tag, alignment)
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_S(self, request):
        """
        DESCRIPTION:
        View to render the button S response.
        """
        # Initial data
        tag = 'geneS_genome'
        alignment = 'china_20200504041407_aligned'
        image = self.base_view(tag, alignment)
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_N(self, request):
        """
        DESCRIPTION:
        View to render the button N response.
        """
        # Initial data
        tag = 'geneN_genome'
        alignment = 'spain_20200504021458_aligned'
        image = self.base_view(tag, alignment)
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_M(self, request):
        """
        DESCRIPTION:
        View to render the button M response.
        """
        # Initial data
        tag = 'geneM_genome'
        alignment = 'china_20200504041407_aligned'
        image = self.base_view(tag, alignment)
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def filter_pi(self, request):
        """
        DESCRIPTION:
        View to render the filter pi response.
        """
        print(Tree.objects.values_list('layout', flat=True))
        Tree.objects.update(layout='pi')
        print(Tree.objects.values_list('layout', flat=True))
        return redirect('/', request)

    @action(detail=False, methods=['GET', ])
    def filter_mu(self, request):
        """
        DESCRIPTION:
        View to render the filter mu response.
        """
        print(Tree.objects.values_list('layout', flat=True))
        Tree.objects.update(layout='mu')
        print(Tree.objects.values_list('layout', flat=True))
        return redirect('/', request)

    @action(detail=False, methods=['GET', ])
    def filter_ro(self, request):
        """
        DESCRIPTION:
        View to render the filter ro response.
        """
        print(Tree.objects.values_list('layout', flat=True))
        Tree.objects.update(layout='ro')
        print(Tree.objects.values_list('layout', flat=True))
        return redirect('/', request)

    @action(detail=False, methods=['GET', ])
    def download(self, request):
        """
        DESCRIPTION:
        View to download all the files of a tree within an already created
        """
        response = HttpResponse(content_type='application/zip')
        zf = zipfile.ZipFile(response, 'w')

        # Create the zipfile in memory using writestr
        zf.write('styles/sample.txt', arcname='sample.txt')

        # Set the name of the file
        filename = 'test_file' + '.zip'

        # Return as zipfile
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


@action(detail=False, methods=['GET', ], permission_classes=(AllowAny, ))
def home_view(request):
    """
    DESCRIPTION:
    The only FBV to redirect to the original home_view
    """
    # image = {'image': 'https://picsum.photos/1024/756'}
    image = {}
    return render(request, 'home.html', image)

