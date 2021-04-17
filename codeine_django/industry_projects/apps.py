from django.apps import AppConfig


class IndustryProjectsConfig(AppConfig):
    name = 'industry_projects'

    def ready(self):
        import industry_projects.signals
    # end def
# end class
