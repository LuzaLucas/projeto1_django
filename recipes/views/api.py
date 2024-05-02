from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from tag.models import Tag
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from ..serializers import TagSerializer, RecipeSerializer
from ..models import Recipe


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 12


class RecipeAPIv2List(ListCreateAPIView):
    queryset = Recipe.objects.get_published() # type: ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    
    # def get(self, request):
    #     recipes = Recipe.objects.get_published()[:10] # type: ignore
    #     serializer = RecipeSerializer(
    #         instance=recipes,
    #         many=True,
    #         context={'request': request},
    #     )
    #     return Response(serializer.data)
        
    # def post(self, request):
    #     serializer = RecipeSerializer(
    #         data=request.data,
    #         context={'request': request}
    #         )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(
    #         author_id=1,
    #         category_id=1,
    #         tags=[1, 2, 4, 5],
    #     )
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED
    #     )


class RecipeAPIv2Detail(RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.get_published() # type: ignore
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv2Pagination
    
    # def get_recipe(self, pk):
    #     recipe = get_object_or_404(
    #         Recipe.objects.get_published(), # type: ignore
    #         pk=pk
    #     )
    #     return recipe
    
    # def get(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         many=False,
    #         context={'request': request},
    #     )
    #     return Response(serializer.data)

    # def patch(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     serializer = RecipeSerializer(
    #         instance=recipe,
    #         data=request.data,
    #         many=False,
    #         context={'request': request},
    #         partial=True,
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(
    #         serializer.data,
    #     )

    # def delete(self, request, pk):
    #     recipe = self.get_recipe(pk)
    #     recipe.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


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
