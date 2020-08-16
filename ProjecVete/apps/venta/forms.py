from django import forms


class VentaEncForm(forms.ModelForm):
    fechaV = forms.DateInput()
    
    class Meta:
        model=""
        fields=['cliente','fechaV','observacion','total','sub_total','descuento']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['fechaV'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        self.fields['sub_total'].widget.attrs['readonly'] = True
        self.fields['descuento'].widget.attrs['readonly'] = True