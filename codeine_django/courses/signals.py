from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import CourseReview, Course, QuizResult
from achievements.models import Achievement, MemberAchievement
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
    stats = get_member_stats(member.user.id)
    member.stats = stats
    member.save()

    # check for new achievements
    non_achievements = Achievement.objects.exclude(members_achievements__member=member).all()

    for non_achievement in non_achievements:
        passed = True

        # check through requirements
        for requirement in non_achievement.achievement_requirements.all():
            if requirement.coding_languages in stats and stats[requirement.coding_languages] < requirement.experience_point:
                print(requirement)
                passed = False
                break
            # end if
            if requirement.category in stats and stats[requirement.category] < requirement.experience_point:
                print(requirement)
                passed = False
                break
            # end if
        # end for

        if passed:
            MemberAchievement(achievement=non_achievement, member=member).save()
        # end if
    # end for
# end def
