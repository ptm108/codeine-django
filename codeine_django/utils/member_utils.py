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
        subscription = MembershipSubscription.objects.filter(
            member=member, payment_transaction__payment_status='COMPLETED').first()
        if subscription:
            if subscription.expiry_date < pytz.utc.localize(timezone.now().today()):
                member.membership_tier = 'FREE'
                member.save()
            else:
                member.membership_tier = 'PRO'
                member.save()
            # end if-else
        else:
            member.membership_tier = 'FREE'
            member.save()
        # end if-else
    except ObjectDoesNotExist:
        member.membership_tier = 'FREE'
        member.save()
    # end try-except
# end def


def get_average_skill_set(member_list):
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

    if len(member_list) <= 0:
        return stats
    # end if

    for member in member_list:
        stats['PY'] += member.stats['PY']
        stats['JAVA'] += member.stats['JAVA']
        stats['JS'] += member.stats['JS']
        stats['CPP'] += member.stats['CPP']
        stats['CS'] += member.stats['CS']
        stats['HTML'] += member.stats['HTML']
        stats['CSS'] += member.stats['CSS']
        stats['RUBY'] += member.stats['RUBY']
        stats['SEC'] += member.stats['SEC']
        stats['DB'] += member.stats['DB']
        stats['FE'] += member.stats['FE']
        stats['BE'] += member.stats['BE']
        stats['UI'] += member.stats['UI']
        stats['ML'] += member.stats['ML']
    # end for

    stats['PY'] /= len(member_list)
    stats['JAVA'] /= len(member_list)
    stats['JS'] /= len(member_list)
    stats['CPP'] /= len(member_list)
    stats['CS'] /= len(member_list)
    stats['HTML'] /= len(member_list)
    stats['CSS'] /= len(member_list)
    stats['RUBY'] /= len(member_list)
    stats['SEC'] /= len(member_list)
    stats['DB'] /= len(member_list)
    stats['FE'] /= len(member_list)
    stats['BE'] /= len(member_list)
    stats['UI'] /= len(member_list)
    stats['ML'] /= len(member_list)

    return stats
# end def
