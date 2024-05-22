# forms.py

from django import forms

class MenuItemOptionForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, **kwargs):
        options = kwargs.pop('options', {})
        super(MenuItemOptionForm, self).__init__(*args, **kwargs)
        if options:  # Only add fields if options are provided
            for option, choices in options.items():
                self.fields[option] = forms.ChoiceField(
                    choices=[(choice, choice) for choice in choices],
                    label=option
                )
