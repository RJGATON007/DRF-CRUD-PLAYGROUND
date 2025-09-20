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


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

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
    
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)  # save to DB
            return Response(
                {
                    "message": "Book created successfully",
                    "book": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Book creation failed",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {"message": "Book updated successfully", "book": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Book update failed", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    
    
