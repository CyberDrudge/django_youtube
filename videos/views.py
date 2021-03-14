from rest_framework import filters
from rest_framework.generics import ListAPIView

from .models import Video
from .serializer import VideoSerializer


# Create your views here.
class VideoListView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-publishTime']


class VideoSearchView(ListAPIView):
    serializer_class = VideoSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-publishTime']

    def get_queryset(self):
        query = self.request.query_params.get('query', "")
        return Video.objects.search(query)
