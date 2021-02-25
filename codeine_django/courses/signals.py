from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import CourseReview, Course, QuizResult
from utils.member_utils import get_member_stats


@receiver(post_save, sender=CourseReview)
def aggregate_ratings(sender, instance, **kwargs):
    course = instance.course
    reviews = CourseReview.objects.filter(course=course)

    course.rating = reviews.aggregate(Avg('rating'))['rating__avg']
    course.save()
# end def


@receiver(post_save, sender=QuizResult)
def update_stats(sender, instance, **kwargs):
    # update member stats
    member = instance.member
    member.stats = get_member_stats(member.user.id)
    member.save()

# end def
