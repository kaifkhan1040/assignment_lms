from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author,Book
from django.urls import reverse

class AuthorViewSetTests(APITestCase):

    def setUp(self):
        """Create an initial Author object for testing."""
        self.author_data = {'name': 'www'}
        self.author = Author.objects.create(**self.author_data)
        self.url = reverse('authorview-list')  

    def test_create_author(self):
        """Test creating an author through the API."""
        data = {'name': 'kaif khan'}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Author created successfully!')

        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(Author.objects.latest('id').name, 'kaif khan')

    def test_update_author(self):
        """Test updating an existing author through the API."""
        update_data = {'name': 'www (Updated)'}
        url = reverse('authorview-detail', kwargs={'pk': self.author.id})  

        response = self.client.put(url, update_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Author updated successfully!')

        self.author.refresh_from_db()
        self.assertEqual(self.author.name, 'www (Updated)')

