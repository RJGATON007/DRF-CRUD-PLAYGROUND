from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['genre', 'title', 'author']
    ordering_fields = ['published_date', 'genre', 'title', 'author', 'created_at']

    # Handle GET /api/v1/books/
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Example: filter by genre with ?genre=FIC
        genre = request.query_params.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)
        
        
    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
