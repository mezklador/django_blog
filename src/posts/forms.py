from django import forms
from django.utils import timezone

from .models import Post

"""
FROM: http://stackoverflow.com/questions/27321692/override-a-django-generic-class-based-view-widget#answer-27322032
You can declare Form Class here for all CBV implied in forms
"""


class PostForm(forms.ModelForm):
    """
    # AUTOMAGICALLY: little html select heleper in Form to choose each element of a date
    # ADDITIONS:
        - year's selector in a range of 5 years before today & 10 years after today
        - default date in selector: today's timestamp
    """
    published_at = forms.DateField(
        widget=forms.SelectDateWidget(years=range(timezone.now().year - 5, timezone.now().year + 10)),
        initial=timezone.now().date()
    )

    """
    FROM: http://stackoverflow.com/questions/18738486/control-the-size-textarea-widget-look-in-django-admin#answer-18738715
    styling form fields
    """

    class Meta:
        model = Post
        fields = ['title',
                  'category',
                  'content',
                  'picture',
                  'draft',
                  'published_at']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10,
                                             'cols': 1,
                                             'class': 'pure-u-1-1',
                                             'id': 'content'
                                             }),
            'title': forms.TextInput(attrs={'class': 'pure-u-1-1',
                                            'id': 'title'
                                            })
        }

    """
    # this a way to declare another rendering view (not perfect)
    def as_pure(self):
        return self._html_output(
            normal_row = "<fieldset>%(label)s%(field)s %(help_text)s %(errors)s</fieldset>",
            error_row = "<p class='error'>%s</p>",
            row_ender = "",
            help_text_html = "<p class='helper-text'>%s</p>",
            errors_on_separate_row = False
        )
    """
