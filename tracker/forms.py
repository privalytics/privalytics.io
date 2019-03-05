from datetime import timedelta, datetime

from django import forms
from bootstrap_daterangepicker import widgets, fields
from django.utils.timezone import make_aware


class DateRangeForm(forms.Form):
    date_range = fields.DateRangeField(
        input_formats=['%d/%m/%Y'],
        widget=widgets.DateRangeWidget(
            format='%d/%m/%Y'
        )
    )

    def clean(self):
        super(DateRangeForm, self).clean()
        start_date = self.cleaned_data['date_range'][0]
        end_date = self.cleaned_data['date_range'][1]
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.min.time())
        end_date = end_date + timedelta(days=1)
        start_date = make_aware(start_date)
        end_date = make_aware(end_date)
        self.cleaned_data['date_range'] = (start_date, end_date)