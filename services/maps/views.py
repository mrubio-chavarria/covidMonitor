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
        align, flag = Alignment.objects.get_or_create(tag=tag)
        print(flag)
        # Obtain the processed alignment
        align.genomes_file = aligned_file
        if align.processed_file is None:
            print('No processed file found')
            print('Generating processed alignement')
            processed_file = preprocess(aligned_file, True, tag)
            align.processed_file = processed_file
            print('Generation completed')
        else:
            print('Processed file found')
            processed_file = align.processed_file
        align.save()
        # Obtain the tree
        tree, flag = Tree.objects.get_or_create(tag=tag)
        tree.alignment = align
        if tree.newick_structure is None:
            print('No newick structure found')
            print('Generating newick structure')
            tree.newick_method(processed_file, tag)
            print('Generation completed')
        else:
            print('Newick structure found')
        tree.save()
        # Obtain the map
        map, flag = Representation.objects.get_or_create(tag=tag+tree.layout)
        map.tree = tree
        if map.image_url is None:
            print('No map image found')
            print('Generating image')
            map.render_map()
            print('Generation completed')
        else:
            print('Map image found')
        map.save()
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
    def button_China(self, request):
        """
        DESCRIPTION:
        View to render the button S response.
        """
        # Initial data
        tag = 'china_genome'
        alignment = 'china_20200504041407_aligned'
        image = self.base_view(tag, alignment)
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def filter_pi(self, request):
        """
        DESCRIPTION:
        View to render the filter pi response.
        """
        Tree.objects.update(layout='pi')
        return redirect('/', request)

    @action(detail=False, methods=['GET', ])
    def filter_mu(self, request):
        """
        DESCRIPTION:
        View to render the filter mu response.
        """
        Tree.objects.update(layout='mu')
        return redirect('/', request)

    @action(detail=False, methods=['GET', ])
    def download(self, request):
        """
        DESCRIPTION:
        View to download all the files of a tree with all its data.
        """
        # Create our container
        response = HttpResponse(content_type='application/zip')
        zf = zipfile.ZipFile(response, 'w')

        # Read files
        tags = ['complete_genome', 'china_genome']
        filters = ['pi', 'mu']

        # Load the files
        for tag in tags:
            route_iqtree = f'structures/{tag}/{tag}.txt.iqtree'
            zf.write(route_iqtree, arcname=f'{tag}.txt.iqtree')
            for filter in filters:
                route_image = f'images/{tag}{filter}.png'
                zf.write(route_image, arcname=f'{tag}{filter}.png')

        # Set the name of the file
        filename = 'covidMonitor' + '.zip'

        # Return as zipfile
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(detail=False, methods=['GET', ])
    def db_reboot(self, request):
        """
        DESCRIPTION:
        View to empty the database.
        """
        Tree.objects.all().delete()
        Representation.objects.all().delete()
        Alignment.objects.all().delete()
        return redirect('/', request)


@action(detail=False, methods=['GET', ], permission_classes=(AllowAny, ))
def home_view(request):
    """
    DESCRIPTION:
    The only FBV to redirect to the original home_view
    """
    # image = {'image': 'https://picsum.photos/1024/756'}
    image = {}
    return render(request, 'home.html', image)

