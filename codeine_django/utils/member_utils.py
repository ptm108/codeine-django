from common.models import Member, MembershipSubscription
from courses.models import Course
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import pytz


def get_member_stats(pk):
    member = Member.objects.get(user_id=pk)

    # courses member is enrolled in
    courses = Course.objects.filter(enrollments__member=member)
    courses = courses.filter(
        Q(assessment__quiz_results__member=member) &
        Q(assessment__quiz_results__passed=True)
    )
    courses = courses.distinct()

    stats = {
        'PY': 0,
        'JAVA': 0,
        'JS': 0,
        'CPP': 0,
        'CS': 0,
        'HTML': 0,
        'CSS': 0,
        'RUBY': 0,
        'SEC': 0,
        'DB': 0,
        'FE': 0,
        'BE': 0,
        'UI': 0,
        'ML': 0,
    }

    for course in courses:
        exp_points = course.exp_points
        for coding_language in course.coding_languages:
            stats[coding_language] += exp_points
        # end for
        for category in course.categories:
            stats[category] += exp_points
        # end for
    # end for

    return stats
# end def


def get_default_member_stats():
    return {
        'PY': 0,
        'JAVA': 0,
        'JS': 0,
        'CPP': 0,
        'CS': 0,
        'HTML': 0,
        'CSS': 0,
        'RUBY': 0,
        'SEC': 0,
        'DB': 0,
        'FE': 0,
        'BE': 0,
        'UI': 0,
        'ML': 0,
    }
# end def


def get_membership_tier(member):
    try:
        subscription = MembershipSubscription.objects.get(
            member=member, payment_transaction__payment_status='COMPLETED')
        print(subscription.expiry_date)
        print(timezone.now().today())
        if subscription.expiry_date < pytz.utc.localize(timezone.now().today()):
            member.membership_tier = 'FREE'
            member.save()
        else:
            member.membership_tier = 'PRO'
            member.save()
        # end if
    except ObjectDoesNotExist:
        member.membership_tier = 'FREE'
        member.save()
    # end try-except
# end def
