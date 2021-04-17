from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CodeReviewCommentEngagement, ArticleCommentEngagement, CodeReviewComment, ArticleComment, CodeReviewEngagement, ArticleEngagement
from notifications.models import Notification, NotificationObject


@receiver(post_save, sender=CodeReviewCommentEngagement)
def update_code_review_comment_engagement(sender, instance, created, **kwargs):
    code_review = instance.comment.code_review
    base_user = instance.user

    if created:
        if base_user.id == instance.comment.user.id:
            pass
        else:        
            title = f'New like for your comment on Code Review {code_review.title}!'
            description = f'{base_user.first_name} {base_user.last_name} liked your Code Review comment on {code_review.title}!'
            notification_type = 'CODE_REVIEW'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, code_review=code_review)
            notification.save()

            receiver = instance.comment.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else
    # end if
# end def


@receiver(post_save, sender=CodeReviewComment)
def update_code_review_comment(sender, instance, created, **kwargs):
    code_review = instance.code_review
    base_user = instance.user

    if created:
        if base_user.id == code_review.user.id:
            pass
        else:
            title = f'New comment on your Code Review {code_review.title}!'
            description = f'{base_user.first_name} {base_user.last_name} left a comment on your Code Review {code_review.title}!'
            notification_type = 'CODE_REVIEW'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, code_review=code_review)
            notification.save()

            receiver = code_review.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else

        if instance.parent_comment is not None:
            receiver = instance.parent_comment.user
            if base_user.id == receiver.id:
                pass
            else:
                title = f'New reply on to your comment on Code Review {code_review.title}!'
                description = f'{base_user.first_name} {base_user.last_name} left a reply to your comment on Code Review {code_review.title}!'
                notification_type = 'CODE_REVIEW'
                notification = Notification(
                    title=title, description=description, notification_type=notification_type, code_review=code_review)
                notification.save()

                notification_object = NotificationObject(
                    receiver=receiver, notification=notification)
                notification_object.save()
            # end if-else
        # end if

    # end if
# end def


@receiver(post_save, sender=CodeReviewEngagement)
def update_code_review_engagement(sender, instance, created, **kwargs):
    code_review = instance.code_review
    base_user = instance.user

    if created:
        if base_user.id == code_review.user.id:
            pass
        else:
            title = f'New like on your Code Review {code_review.title}!'
            description = f'{base_user.first_name} {base_user.last_name} liked your Code Review {code_review.title}!'
            notification_type = 'CODE_REVIEW'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, code_review=code_review)
            notification.save()

            receiver = code_review.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else
    # end if
# end def


@receiver(post_save, sender=ArticleCommentEngagement)
def update_article_comment_engagement(sender, instance, created, **kwargs):
    article = instance.comment.article
    base_user = instance.user

    if created:
        if base_user.id == instance.comment.user.id:
            pass
        else:
            title = f'New like for your comment on Article {article.title}!'
            description = f'{base_user.first_name} {base_user.last_name} liked your Article comment on {article.title}!'
            notification_type = 'ARTICLE'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, article=article)
            notification.save()

            receiver = instance.comment.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else
    # end if
# end def


@receiver(post_save, sender=ArticleComment)
def update_article_comment(sender, instance, created, **kwargs):
    article = instance.article
    base_user = instance.user

    if created:
        if base_user.id == article.user.id:
            pass
        else:
            title = f'New comment on your Article {article.title}!'
            description = f'{base_user.first_name} {base_user.last_name} left a comment on your Article {article.title}!'
            notification_type = 'ARTICLE'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, article=article)
            notification.save()

            receiver = article.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else

        if instance.reply_to is not None:
            receiver = instance.reply_to.user
            if base_user.id == receiver.id:
                pass
            else:
                title = f'New reply on to your comment on Article {article.title}!'
                description = f'{base_user.first_name} {base_user.last_name} left a reply to your comment on Article {article.title}!'
                notification_type = 'ARTICLE'
                notification = Notification(
                    title=title, description=description, notification_type=notification_type, article=article)
                notification.save()

                notification_object = NotificationObject(
                    receiver=receiver, notification=notification)
                notification_object.save()
            # end if-else
        # end if
    # end if
# end def


@receiver(post_save, sender=ArticleEngagement)
def update_article_engagement(sender, instance, created, **kwargs):
    article = instance.article
    base_user = instance.user

    if created:
        if base_user.id == article.user.id:
            pass
        else:
            title = f'New like on your Article {article.title}!'
            description = f'{base_user.first_name} {base_user.last_name} liked your Article {article.title}!'
            notification_type = 'ARTICLE'
            notification = Notification(
                title=title, description=description, notification_type=notification_type, article=article)
            notification.save()

            receiver = article.user
            notification_object = NotificationObject(
                receiver=receiver, notification=notification)
            notification_object.save()
        # end if-else
    # end if
# end def
