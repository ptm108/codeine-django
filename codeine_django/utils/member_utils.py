from common.models import Member
from courses.models import Course
from django.db.models import Q, Sum


def get_member_stats(pk):
    member = Member.objects.get(user_id=pk)

    courses = Course.objects.filter(enrollments__member=member)  # courses member is enrolled in
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
