from django import forms
from haystack.forms import FacetedSearchForm


class TextSearchForm (FacetedSearchForm):

    start_date = forms.IntegerField(required=False)
    end_date = forms.IntegerField(required=False)

    def no_query_found (self):
        return self.searchqueryset.all()

    def search (self):
        sqs = super(TextSearchForm, self).search()
        if not self.is_valid():
            return self.no_query_found()
        start_date = self.cleaned_data['start_date']
        end_date = self.cleaned_data['end_date']
        if start_date and end_date:
            sqs = sqs.filter(date__range=(start_date, end_date))
        elif start_date:
            sqs = sqs.filter(date__gte=start_date)
        elif end_date:
            sqs = sqs.filter(date__lte=end_date)
        if self.load_all:
            sqs = sqs.load_all()
        return sqs
