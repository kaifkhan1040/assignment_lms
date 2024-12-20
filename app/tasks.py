# your_app/tasks.py

import os
import json
from datetime import datetime
from celery import shared_task
from .models import Author, Book, BorrowRecord
from django.conf import settings

@shared_task
def generate_report():
    print('running')
    try:
        total_authors = Author.objects.count()
        total_books = Book.objects.count()
        total_borrowed_books = BorrowRecord.objects.filter(return_date__isnull=True).count()
        report_data = {
            "total_authors": total_authors,
            "total_books": total_books,
            "total_borrowed_books": total_borrowed_books,
            "timestamp": datetime.now().isoformat()
        }

        timestamp = datetime.now().strftime('%Y%m%d')
        report_dir = os.path.join(settings.BASE_DIR, 'reports/')
        print('asy,,,,,,,,,,,,,,,,,,,',report_dir)
        file_name = f'{report_dir}/report_{timestamp}.json'
        with open(file_name, 'a') as file:
            json.dump(report_data, file)
        return file_name
    except Exception as e:
        raise e
