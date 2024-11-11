# controle_frequencia/forms.py
from django import forms
from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "As senhas não coincidem.")

class UploadTurmaForm(forms.Form):
    arquivo = forms.FileField(
        label='Selecione o arquivo de turmas (CSV ou XLSX)',
        required=True
    )
    
    def clean_turma_file(self):
        file = self.cleaned_data.get('turma_file')
        # Adicione validações específicas do arquivo aqui, se necessário
        return file
