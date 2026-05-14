from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks_app.models import TaskTemplate, AssignedTask
from staff.models import StaffProfile
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate recurring tasks for today'

    def handle(self, *args, **options):
        today = timezone.now().date()
        weekday = today.weekday()
        day_of_month = today.day

        templates = TaskTemplate.objects.all()
        created_count = 0

        for template in templates:
            # Check if this template should generate today
            if template.frequency == 'daily':
                should_generate = True
            elif template.frequency == 'weekly':
                should_generate = template.day_of_week == weekday
            elif template.frequency == 'monthly':
                should_generate = template.day_of_month == day_of_month
            elif template.frequency == 'one_time':
                should_generate = False
            else:
                should_generate = False

            if not should_generate:
                continue

            # Assign to all active staff
            active_staff = StaffProfile.objects.filter(is_active=True)
            for staff in active_staff:
                _, created = AssignedTask.objects.get_or_create(
                    staff=staff,
                    task_template=template,
                    assigned_date=today,
                    defaults={'is_completed': False}
                )
                if created:
                    created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Generated {created_count} tasks for {today}'))
