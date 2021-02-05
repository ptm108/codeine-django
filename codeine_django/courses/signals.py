from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import CourseReview, Course


@receiver(post_save, sender=CourseReview)
def aggregate_ratings(sender, instance, **kwargs):
    course = instance.course
    reviews = CourseReview.objects.filter(course=course)

    course.rating = reviews.aggregate(Avg('rating'))['rating__avg']
    course.save()
# end def
