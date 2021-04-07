from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPartnerOnly(BasePermission):
    '''
    View level check if requesting user is a Partner
    '''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # end if
        return hasattr(request.user, 'partner')
    # end def

# end class


class IsPartnerOrReadOnly(BasePermission):
    '''
    View level check for unsafe methods
    Check if requesting user is a Partner
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'partner'):
            return True
        # end ifs
        return False
    # end def
# end class


class IsPartnerOrAdminOrReadOnly(BasePermission):
    '''
    View level check for unsafe methods
    Check if requesting user is a Partner
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and (hasattr(request.user, 'partner') or request.user.is_admin):
            return True
        # end ifs
        return False
    # end def
# end class


class IsMemberOnly(BasePermission):
    '''
    View level check if requesting user is a Member
    '''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # end if
        return hasattr(request.user, 'member')
    # end def
# end class


class IsMemberOrReadOnly(BasePermission):

    '''
    View level check for unsafe methods
    Check if requesting user is a Member
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'member'):
            return True
        # end ifs
        return False
    # end def
# end class


class IsMemberOrAdminOrReadOnly(BasePermission):

    '''
    View level check for unsafe methods
    Check if requesting user is a Member
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and (hasattr(request.user, 'member') or request.user.is_admin):
            return True
        # end ifs
        return False
    # end def
# end class


class IsMemberOrPartnerOnly(BasePermission):

    '''
    View level check for unsafe methods
    Check if requesting user is a Member or Partner
    '''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # end if
        return hasattr(request.user, 'member') or hasattr(request.user, 'partner')
    # end def
# end class


class IsMemberOrPartnerOrReadOnly(BasePermission):

    '''
    View level check for unsafe methods
    Check if requesting user is a Member or Partner
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        # end if
        return hasattr(request.user, 'member') or hasattr(request.user, 'partner')
    # end def
# end class


class AdminOrReadOnly(BasePermission):

    '''
    View level check for unsafe methods
    Check if requesting user is an Admin
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.is_admin:
            return True
        # end ifs
        return False
    # end def
# end class


class IsAdminOnly(BasePermission):
    '''
    View level check if requesting user is a Partner or Admin
    '''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # end if
        return request.user.is_admin
    # end def
# end class


class IsPartnerOrAdminOnly(BasePermission):
    '''
    View level check if requesting user is a Partner or Admin
    '''

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        # end if
        return hasattr(request.user, 'partner') or request.user.is_admin
    # end def
# end class
