# bookapp/views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from auth_app.custom_permission import IsHeadLibrarian, IsLibrarian, IsPatron
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q




class AddBookView(generics.CreateAPIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
class SearchBooksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, (IsHeadLibrarian | IsLibrarian | IsPatron)]
    serializer_class = BookSerializer

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            # Use Q objects for filtering
            return Book.objects.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(isbn__icontains=search_query)
            )
        return Book.objects.all()  
class RetrieveBookView(generics.RetrieveAPIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]  # Adjust based on your access control
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        book_id = self.kwargs.get('pk')
        if not book_id:
            raise NotFound("No ID provided to retrieve the book.")
        
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound(f"Book with ID {book_id} not found.")
        

class UpdateBooksView(generics.UpdateAPIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        return Response({"error": "GET method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_object(self):
        book_id = self.kwargs.get('pk')
        if not book_id:
            raise NotFound("No ID provided to update the book.")
        
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound(f"Book with ID {book_id} not found.")
    
class DeleteBooksView(generics.DestroyAPIView):
    permission_classes = [IsHeadLibrarian]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_object(self):
        # Retrieve the book by ID from the URL
        book_id = self.kwargs.get('book_id')
        if not book_id:
            raise NotFound("No ID provided to delete the book.")
        
        # Retrieve the book by ID
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            raise NotFound(f"Book with ID {book_id} not found.")

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Assuming you have a UserSerializer that includes the role
class BookListView(generics.ListAPIView):
    permission_classes = [IsHeadLibrarian | IsLibrarian | IsPatron]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        # Fetch the current user's role
        user_role = request.user.role if request.user.is_authenticated else ''
        
        # Get books and serialize them
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        
        # Include user role in the response
        return Response({
            'books': serializer.data,
            'current_user_role': user_role
        })
  