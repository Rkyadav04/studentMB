import random
from django.core.management.base import BaseCommand
from faker import Faker
from student.models import Student
from django.utils import timezone

fake = Faker()

class Command(BaseCommand):
    help = 'Seed student table with unique IDs'

    def add_arguments(self, parser):
        parser.add_argument('--total', type=int, help='Number of students to seed', default=100000)

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        students = []

        # Get the highest student_id number so far (assuming format "S#####")
        existing_ids = Student.objects.values_list('student_id', flat=True)
        numeric_ids = [int(s[1:]) for s in existing_ids if s.startswith('S') and s[1:].isdigit()]
        start_id = max(numeric_ids) + 1 if numeric_ids else 10000

        for i in range(start_id, start_id + total):
            student = Student(
                student_id=f"S{i}",
                name=fake.name(),
                course=random.choice(['B.Tech', 'M.Tech', 'MBA', 'B.Sc', 'M.Sc']),
                contact=fake.phone_number()[:15],
                last_result=random.choice(['Pass', 'Fail', 'Distinction']),
                email=fake.unique.email(),
                status=random.choice(['Active', 'Inactive']),
                is_deleted=False,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            students.append(student)

        Student.objects.bulk_create(students)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total} new students.'))

