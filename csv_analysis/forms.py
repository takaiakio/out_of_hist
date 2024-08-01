from django import forms

class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル')
    lsl = forms.FloatField(label='下限規格値（LSL）', required=False)
    usl = forms.FloatField(label='上限規格値（USL）', required=False)
