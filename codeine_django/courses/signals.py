from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from .models import CourseReview, Course, QuizResult, CourseMaterial, Enrollment, Chapter, CourseComment, CourseCommentEngagement
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
def update_course_material(sender, instance, created, **kwargs):
    course = instance.chapter.course
    enrollments = Enrollment.objects.filter(course=course)
    title = f'Course {course.title} updated!'

    if created:
        description = f'New course material for chapter {instance.chapter.title}'
    else:
        description = f'Updated course material for chapter {instance.chapter.title}'
    # end if-else

    photo = course.thumbnail
    notification_type = 'COURSE'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, course=course)
    notification.photo = photo
    notification.save()

    for enrollment in enrollments:
        print(enrollment)
        receiver = enrollment.member.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end for
# end def


@receiver(post_save, sender=Chapter)
def update_course_chapter(sender, instance, created, **kwargs):
    course = instance.course
    enrollments = Enrollment.objects.filter(course=course)
    title = f'Course {course.title} updated!'

    if created:
        description = f'New chapter for course {course.title}!'
    else:
        description = f'Updated chapter for course {course.title}!'
    # end if-else

    photo = course.thumbnail
    notification_type = 'COURSE'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, course=course)
    notification.photo = photo
    notification.save()

    for enrollment in enrollments:
        receiver = enrollment.member.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end for
# end def


@receiver(post_save, sender=CourseComment)
def update_course_comment(sender, instance, created, **kwargs):
    course = instance.course_material.chapter.course

    if created:
        title = f'New comment on Course {course.title}!'
        description = f'New course comment on {instance.course_material}!'
    else:
        title = f'Updated comment on Course {course.title}!'
        description = f'Updated course comment on {instance.course_material}!'
    # end if-else

    photo = course.thumbnail
    notification_type = 'COURSE'
    notification = Notification(
        title=title, description=description, notification_type=notification_type, course=course)
    notification.photo = photo
    notification.save()

    receiver = course.partner.user
    notification_object = NotificationObject(
        receiver=receiver, notification=notification)
    notification_object.save()

    if instance.reply_to is not None:
        title = f'New reply for comment on Course: {course.title}!'
        description = f'{instance.user} left a reply to your comment on {course.title}!\n {instance.comment}'
        photo = course.thumbnail
        notification_type = 'COURSE'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, course=course)
        notification.photo = photo
        notification.save()

        receiver = instance.reply_to.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=CourseCommentEngagement)
def update_course_comment_engagement(sender, instance, created, **kwargs):
    course = instance.comment.course_material.chapter.course
    member = instance.member

    if created:
        title = f'New like for your comment on {course}!'
        description = f'{member} liked your course comment on {course}!'
        photo = course.thumbnail
        notification_type = 'COURSE'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, course=course)
        notification.photo = photo
        notification.save()

        receiver = instance.comment.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


# @receiver(post_save, sender=Course)
# def update_course(sender, instance, created, update_fields, **kwargs):
#     course = instance
#     title = f'Course {course.title} updated!'

#     if created:
#         description = f'New chapter for course {course.title}!'
#     else:
#         description = f'Updated chapter for course {course.title}!'
#     # end if-else

#     photo = course.thumbnail
#     notification_type = 'COURSE'
#     notification = Notification(
#         title=title, description=description, notification_type=notification_type, course=course)
#     notification.photo = photo
#     notification.save()

    # receiver = course.partner.user
    # notification_object = NotificationObject(receiver=receiver, notification=notification)
    # notification_object.save()
# end def
