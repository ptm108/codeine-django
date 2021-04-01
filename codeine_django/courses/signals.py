from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import CourseReview, Course, QuizResult, CourseMaterial, Enrollment, Chapter
from notifications.models import Notification, NotificationObject
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
    non_achievements = Achievement.objects.exclude(
        members_achievements__member=member).all()

    for non_achievement in non_achievements:
        passed = True

        # check through requirements
        for requirement in non_achievement.achievement_requirements.all():
            if requirement.stat in stats and stats[requirement.stat] < requirement.experience_point:
                print(requirement)
                passed = False
                break
            # end if
        # end for

        if passed:
            MemberAchievement(achievement=non_achievement,
                              member=member).save()
        # end if
    # end for
# end def


@receiver(post_save, sender=CourseMaterial)
def update_course_material(sender, instance, **kwargs):
    course = instance.chapter.course
    enrollments = Enrollment.objects.filter(course=course)
    title = f'Course {course.title} updated!'
    description = f'New/updated course material for chapter {instance.chapter.title}'
    photo = course.thumbnail
    notification_type = 'COURSE'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, course=course)
    notification.photo = photo
    notification.save()

    for enrollment in enrollments:
        print(enrollment)
        receiver = enrollment.member.user
        notification_object = NotificationObject(receiver=receiver, notification=notification)
        notification_object.save()
    # end for
# end def


@receiver(post_save, sender=Chapter)
def update_course_chapter(sender, instance, **kwargs):
    course = instance.course
    enrollments = Enrollment.objects.filter(course=course)
    title = f'Course {course.title} updated!'
    description = f'New/updated chapter for course {course.title}!'
    photo = course.thumbnail
    notification_type = 'COURSE'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, course=course)
    notification.photo = photo
    notification.save()

    for enrollment in enrollments:
        receiver = enrollment.member.user
        notification_object = NotificationObject(receiver=receiver, notification=notification)
        notification_object.save()
    # end for
# end def
