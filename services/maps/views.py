from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from .models import Tree
from .serializers import TreeSerializer


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
    def button_1(self, request):
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
        View to render the download response.
        """
        image = {'image': 'https://picsum.photos/1024/756'}
        return render(request, 'home.html', image)


@action(detail=False, methods=['GET', ], permission_classes=(AllowAny, ))
def home_view(request):
    """
    DESCRIPTION:
    The only FBV to redirect to the original home_view
    """
    image = {'image': 'https://picsum.photos/1024/756'}
    return render(request, 'home.html', image)

