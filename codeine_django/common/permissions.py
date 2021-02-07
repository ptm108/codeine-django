from rest_framework.permissions import BasePermission

class IsContentProviderOnly(BasePermission):
    '''
    View level check if requesting user is a ContentProvider
    ''' 
    def has_permission(self, request, view):
        return request.user.content_provider is not None
    # end def
# end class

class IsMemberOnly(BasePermission):
    '''
    View level check if requesting user is a Member
    '''
    def has_permission(self, request, view):
        return request.user.member is not None
    # end def
# end class

class IsIndustryPartnerOnly(BasePermission):
    '''
    View level check if requesting user is a IndustryPartner
    '''
    def has_permission(self, request, view):
        return request.user.industry_parter is not None
    # end def
# end class
