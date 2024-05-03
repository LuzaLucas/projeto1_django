from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tag.models import Tag
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from typing import Any

from ..serializers import TagSerializer, RecipeSerializer
from ..models import Recipe


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 12
    
    
class RecipeAPIv2ViewSet(ModelViewSet):    
    queryset = Recipe.objects.get_published() # type: ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    
    def get_serializer_class(self):
        return super().get_serializer_class()
    
    def get_serializer(self, *args, **kwargs):
        return super().get_serializer(*args, **kwargs)
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs) #type: ignore
        context["example"] = 'new context bitches'
        return context
    
    
    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', None) #type: ignore
        
        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)
        
        return qs


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
