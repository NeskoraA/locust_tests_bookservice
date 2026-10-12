from faker import Faker
from locust import HttpUser, task, TaskSet, SequentialTaskSet, constant_throughput
import random


fake = Faker('ru_RU')

print(fake.name())


class BookTests(TaskSet):
    @task(5)
    def get_books(self):
        self.client.get('/api/books')

    @task(5)
    def get_authors(self):
        self.client.get('/api/authors')

    @task(5)
    def get_reviews(self):
        self.client.get('/api/reviews')

    @task
    def add_author(self):
        author_data = {
            'firstName': fake.first_name_male(),
            'surname': fake.last_name_male(),
            'lastName': fake.middle_name_male(),
        }

        self.client.post('/api/authors', json=author_data)

    @task
    def add_book(self):
        book_data = {
            'title': fake.word().capitalize(),
            'publicationYear': str(fake.date()),
            'authorId': fake.random_int(min=1, max=50),
            'genreId': fake.random_int(min=1, max=10),
            'publisherId': fake.random_int(min=1, max=10),
        }

        self.client.post('/api/books', json=book_data)

    @task
    def add_review(self):
        review_data = {
            'comment': fake.text(max_nb_chars=150),
            'rate': fake.random_int(min=1, max=5),
            'userId': fake.random_int(min=1, max=50),
            'bookId': fake.random_int(min=1, max=50),
        }

        self.client.post('/api/reviews', json=review_data)


class WebsiteUser(HttpUser):
    wait_time = constant_throughput(1)

    tasks = [
        BookTests
    ]
