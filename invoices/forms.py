from django import forms

class MultipleZipUploadForm(forms.Form):
    dummy = forms.CharField(required=False)  # champ factice pour afficher un formulaire


    def clean(self):
        cleaned_data = super().clean()
        files = self.files.getlist('files')  # on récupère les fichiers manuellement
        if not files:
            raise forms.ValidationError("Aucun fichier sélectionné.")
        for f in files:
            if not f.name.endswith('.zip'):
                raise forms.ValidationError(f"{f.name} n’est pas un fichier ZIP.")
        cleaned_data['files'] = files
        return cleaned_data
