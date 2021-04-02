from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CodeReviewCommentEngagement, ArticleCommentEngagement, CodeReviewComment, ArticleComment, CodeReviewEngagement, ArticleEngagement
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=CodeReviewCommentEngagement)
def update_code_review_comment_engagement(sender, instance, created, **kwargs):
    code_review = instance.comment.code_review
    base_user = instance.user

    if created:
        title = f'New like for your comment on {code_review}!'
        description = f'{base_user} liked your code review comment on {code_review}!'
        notification_type = 'CODE_REVIEW'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, code_review=code_review)
        notification.save()

        receiver = instance.comment.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=CodeReviewComment)
def update_code_review_comment(sender, instance, created, **kwargs):
    code_review = instance.code_review
    base_user = instance.user

    if created:
        title = f'New comment on your Code Review: {code_review}!'
        description = f'{base_user} left a comment on your {code_review}!\n {instance.comment}'
        notification_type = 'CODE_REVIEW'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, code_review=code_review)
        notification.save()

        receiver = code_review.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=CodeReviewEngagement)
def update_code_review_engagement(sender, instance, created, **kwargs):
    code_review = instance.code_review
    base_user = instance.user

    if created:
        title = f'New like on your Code Review: {code_review}!'
        description = f'{base_user} liked your Code Review: {code_review}!'
        notification_type = 'CODE_REVIEW'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, code_review=code_review)
        notification.save()

        receiver = code_review.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=ArticleCommentEngagement)
def update_article_comment_engagement(sender, instance, created, **kwargs):
    article = instance.comment.article
    base_user = instance.user

    if created:
        title = f'New like for your comment on {article}!'
        description = f'{base_user} liked your article comment on {article}!'
        notification_type = 'ARTICLE'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, article=article)
        notification.save()

        receiver = instance.comment.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def


@receiver(post_save, sender=ArticleComment)
def update_article_comment(sender, instance, created, **kwargs):
    article = instance.article
    base_user = instance.user

    if created:
        title = f'New comment on your Article: {article}!'
        description = f'{base_user} left a comment on your {article}!\n {instance.comment}'
        notification_type = 'ARTICLE'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, article=article)
        notification.save()

        receiver = article.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()

        if instance.reply_to is not None:
            title = f'New reply for comment on Article: {article}!'
            description = f'{base_user} left a reply to your comment on {article}!\n {instance.comment}'
            notification_type = 'ARTICLE'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, article=article)
            notification.save()

            receiver = instance.reply_to.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if
    # end if
# end def


@receiver(post_save, sender=ArticleEngagement)
def update_article_engagement(sender, instance, created, **kwargs):
    article = instance.article
    base_user = instance.user

    if created:
        title = f'New like on your Article: {article}!'
        description = f'{base_user} liked your Article: {article}!'
        notification_type = 'ARTICLE'
        notification = Notification(
            title=title, description=description, notification_type=notification_type, article=article)
        notification.save()

        receiver = article.user
        notification_object = NotificationObject(
            receiver=receiver, notification=notification)
        notification_object.save()
    # end if
# end def
