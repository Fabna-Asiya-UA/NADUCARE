
from django.db import models
from django.contrib.auth.models import User


class Problem(models.Model):

    # Problem categories
    class Category(models.TextChoices):
        ROAD = 'Road', 'Road'
        WATER = 'Water', 'Water Supply'
        WASTE = 'Waste', 'Waste Management'
        ELECTRICITY = 'Electricity', 'Electricity'
        DRAINAGE = 'Drainage', 'Drainage'
        OTHER = 'Other', 'Other'

    # Problem status
    class Status(models.TextChoices):
        REPORTED = 'Reported', 'Reported'
        IN_PROGRESS = 'In Progress', 'In Progress'
        RESOLVED = 'Resolved', 'Resolved'

    # Kerala districts
    DISTRICTS = [
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('Kollam', 'Kollam'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Alappuzha', 'Alappuzha'),
        ('Kottayam', 'Kottayam'),
        ('Idukki', 'Idukki'),
        ('Ernakulam', 'Ernakulam'),
        ('Thrissur', 'Thrissur'),
        ('Palakkad', 'Palakkad'),
        ('Malappuram', 'Malappuram'),
        ('Kozhikode', 'Kozhikode'),
        ('Wayanad', 'Wayanad'),
        ('Kannur', 'Kannur'),
        ('Kasaragod', 'Kasaragod'),
    ]

    # Problem details
    title = models.CharField(max_length=200)
    description = models.TextField()
    district = models.CharField( max_length=30, choices=DISTRICTS)
    category = models.CharField( max_length=20,choices=Category.choices)
    location = models.CharField(max_length=200)
    photo = models.ImageField( upload_to='problem_photos/', blank=True, null=True)
    status = models.CharField( max_length=20, choices=Status.choices, default=Status.REPORTED)
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='reported_problems')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

