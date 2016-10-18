from django.conf import settings

def main_title(request):
    """
    FROM: http://stackoverflow.com/questions/433162/can-i-access-constants-in-settings-py-from-templates-in-django#answer-433209
    """
    return dict(MAIN_TITLE=settings.MAIN_TITLE)