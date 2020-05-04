import zipfile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Tree, Representation
from .serializers import TreeSerializer
from django.core.files import File
from covidMonitor.settings import MEDIA_URL, BASE_DIR
from .utils import preprocess



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
    @action(detail=False, methods=['GET', ])
    def home_view(self, request):
        """
        DESCRIPTION:
        View to render the home page.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_complete(self, request):
        """
        DESCRIPTION:
        View to render the button 1 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_2(self, request):
        """
        DESCRIPTION:
        View to render the button 2 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_3(self, request):
        """
        DESCRIPTION:
        View to render the button 3 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def button_4(self, request):
        """
        DESCRIPTION:
        View to render the button 4 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def filter_1(self, request):
        """
        DESCRIPTION:
        View to render the filter 1 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def filter_2(self, request):
        """
        DESCRIPTION:
        View to render the filter 2 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

    @action(detail=False, methods=['GET', ])
    def filter_3(self, request):
        """
        DESCRIPTION:
        View to render the filter 3 response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)

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
    image = {'image': 'https://picsum.photos/1024/756'}
    return render(request, 'home.html', image)

