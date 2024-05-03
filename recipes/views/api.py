from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tag.models import Tag
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from ..serializers import TagSerializer, RecipeSerializer
from ..models import Recipe


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 12
    
    
class RecipeAPIv2ViewSet(ModelViewSet):    
    queryset = Recipe.objects.get_published() # type: ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
