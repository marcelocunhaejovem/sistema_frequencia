
# controle_frequencia/forms.py
from django import forms

class UploadTurmaForm(forms.Form):
    arquivo = forms.FileField(label='Selecione o arquivo de turmas (CSV, XLS, XLSX)', required=True)
