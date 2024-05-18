from django.core.management.base import BaseCommand
from faker import Faker
from datetime import datetime
import random
from accounts.models import User, Profile
from blog.models import Post, Category

category_list = ["adventure", "python", "Django", "IT"]


class Command(BaseCommand):
    help = "Inserting dummy data into the database"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(email=self.fake.email(), password="fake@test")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.bio = self.fake.paragraph(nb_sentences=3)
        profile.save()

        for name in category_list:
            # Preventing creation of duplicate categories
            Category.objects.get_or_create(name=name)

        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.fake.sentence(nb_words=12),
                content=self.fake.paragraph(nb_sentences=6),
                category=Category.objects.get(name=random.choice(category_list)),
                published=random.choice([True, False]),
                published_date=datetime.now(),
            )
