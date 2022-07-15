from django.forms.widgets import Input


class SearchInput(Input):
    input_type = 'search'
    template_name = 'django/forms/widgets/text.html'