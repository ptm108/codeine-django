from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsContentProviderOnly(BasePermission):
    '''
    View level check if requesting user is a ContentProvider
    '''

    def has_permission(self, request, view):
        return hasattr(request.user, 'content_provider')
    # end def
# end class


class IsContentProviderOrReadOnly(BasePermission):
    '''
    View level check for unsafe methods
    Check if requesting user is a ContentProvider
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'content_provider'):
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


class IsIndustryPartnerOnly(BasePermission):
    '''
    View level check if requesting user is a IndustryPartner
    '''

    def has_permission(self, request, view):
        return hasattr(request.user, 'industry_partner')
    # end def
# end class


class IsIndustryPartnerOrReadOnly(BasePermission):
    '''
    View level check for unsafe methods
    Check if requesting user is a IndustryPartner
    '''

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, 'industry_partner'):
            return True
        # end ifs
        return False
    # end def
# end class


class IsOwnerOnly(BasePermission):
    ''' 
    View level check if requesting user is owner (BaseUser)
    '''

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    # end def
# end class


class IsOwnerOnlyOrReadOnly(BasePermission):
    '''
    View level check for unsafe methods
    Check if requesting user is the owner of object (BaseUser)
    '''

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # end if
        return obj.user == request.user
# end class
