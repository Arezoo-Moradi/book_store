from django import forms


class CodeForm(forms.Form):
    code_input = forms.CharField(label='کد تخفیف', max_length=100)
