"""
Views for the recipe API.
"""
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers

# Allows to extend auto generated schema


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma separated list of IDs to filter.'
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe API."""

    serializer_class = serializers.RecipeDetailSerializer
    # set of objects available for this endpoint
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipes for authenticated users"""
        tags = self.request.query_params.get('tags')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return the serializer class for request."""

        # Use Recipe serializer for list request
        if self.action == 'list':
            return serializers.RecipeSerializer
        if self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.'
            )
        ]
    )
)
class TagViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # over ride this method to query for tags that are related to user

    def get_queryset(self):
        """Filter query set to authenticated user"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-name').distinct()
