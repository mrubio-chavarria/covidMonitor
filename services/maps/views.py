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
    @action(detail=False, methods=['GET', 'POST'])
    def home_view(self, request):
        """
        DESCRIPTION:
        View to render the home page.
        """
        return render(request, 'home.html')


@action(detail=False, methods=['GET', 'POST'], permission_classes=(AllowAny,))
def home_view(request):
    """
    DESCRIPTION:
    The only FBV to redirect to the original home_view
    """
    return redirect('/maps/home_view')

