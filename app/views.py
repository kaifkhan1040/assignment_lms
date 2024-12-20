from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Author,Book,BorrowRecord
from .serializers import AuthorSerializer,BookSerializer,BorrowRecordSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from rest_framework.views import APIView
import os
from django.conf import settings
from django.http import JsonResponse
from .tasks import generate_report

# Create your views here.
class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Author created successfully!"
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Author updated successfully!"
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data['message'] = "Author deleted successfully!"
        return response

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        isbn = request.data.get('isbn')
        if Book.objects.filter(isbn=isbn).exists():
            raise ValidationError({"isbn": "This ISBN is already taken by another book."})
        
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Book created successfully!"
        return response

    def update(self, request, *args, **kwargs):
        isbn = request.data.get('isbn')
        book_instance = self.get_object()  
        if Book.objects.filter(isbn=isbn).exclude(id=book_instance.id).exists():
            raise ValidationError({"isbn": "This ISBN is already taken by another book."})
        
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Book updated successfully!"
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data['message'] = "Book deleted successfully!"
        return response
        
class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.all()
    serializer_class = BorrowRecordSerializer

    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies <= 0:
            return Response({"error": "No available copies of this book"}, status=status.HTTP_400_BAD_REQUEST)

        book.available_copies -= 1
        book.save()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            borrow_record = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        borrow_record = self.get_object()

        if borrow_record.return_date is not None:
            return Response({"error": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrow_record.return_date = date.today()
        borrow_record.save()
        book = borrow_record.book
        book.available_copies += 1
        book.save()

        serializer = self.get_serializer(borrow_record)

        return Response({
            "message": "Book successfully returned",
            "book": book.title,
            "available_copies": book.available_copies,
            "return_date": borrow_record.return_date
        }, status=status.HTTP_200_OK)


class ReportGenerateView(APIView):
    def post(self, request, *args, **kwargs):
        task = generate_report.apply_async()
        return JsonResponse({
            "message": "Report generation started",
            "task_id": task.id
        }, status=status.HTTP_202_ACCEPTED)

    def get(self, request, *args, **kwargs):
        print(settings.BASE_DIR)
        report_dir = os.path.join(settings.BASE_DIR, 'reports/')
        
        print('path',report_dir)
        report_files = sorted(
            [f for f in os.listdir(report_dir) if f.endswith('.json')],
            reverse=True
        )
        print('hoho ho',report_files)
        if report_files:
            latest_report = report_files[0]
            report_path = os.path.join(report_dir, latest_report)

            with open(report_path, 'r') as file:
                report_data = json.load(file)

            return JsonResponse(report_data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "No reports available"}, status=status.HTTP_404_NOT_FOUND)

