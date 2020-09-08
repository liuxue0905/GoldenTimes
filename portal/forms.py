from django import forms


class ExcelForms(forms.Form):
    file = forms.FileField(required=True)


class RecordSearchForm(forms.Form):
    title = forms.CharField()


class ArtistListForm(forms.Form):
    name = forms.CharField(required=False)
    type = forms.IntegerField(required=False)
    # has_records = forms.BooleanField(initial=True, required=False)
    record__isnull = forms.CharField(required=False)
