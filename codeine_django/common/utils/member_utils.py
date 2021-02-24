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

    return courses.all()

# end def
