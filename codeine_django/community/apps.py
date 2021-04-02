from django.apps import AppConfig


class CommunityConfig(AppConfig):
    name = 'community'
    
    def ready(self):
        import community.signals
    # end def
# end class