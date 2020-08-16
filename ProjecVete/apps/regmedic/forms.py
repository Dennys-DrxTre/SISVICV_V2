from django import forms
from .models import Cliente, Mascota, Consulta, Vacuna, Despa

#FORMS CLIENTES
class ClienteForm(forms.ModelForm):
    class Meta:
        model= Cliente
        fields = ['tipo','co_movil', 'cedula','nombre', 'apellido', 'movil' ,'tlf', 'correo','ocupacion','direccion','estado' ]

        widgets = {
            'tipo': forms.Select(attrs= {'class': 'form-control'}),
            'co_movil': forms.Select(attrs= {'class': 'form-control'}),
            'cedula': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Cédula', 'maxlength': '8'}),
            'nombre': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Nombres'}),
            'apellido': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Apellidos'}),
            'movil': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Celular', 'maxlength': '11'}),
            'tlf': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Teléfono', 'maxlength': '11'}),
            'correo': forms.EmailInput ( attrs= {'class': 'form-control ', 'placeholder': 'Correo Electrónico'}), 
            'ocupacion': forms.TextInput( attrs= {'class': 'form-control ', 'placeholder': 'Ocupación Laboral','required':'True'}),
            'direccion': forms.Textarea( attrs= {'class': 'form-control  textarea', 'placeholder': 'Dirección Habitacional','required':'True'}),
        }
#FORMS MASCOTAS
class MascotaForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(estado=True).order_by('nombre'))
    class Meta:
        model = Mascota
        fields = ['cliente', 'nombre', 'especie', 'razam', 'sexom','fnaci', 'peso', 'estado']
        widgets = {
            'cliente': forms.Select( attrs= {'class': 'custom-select', 'placeholder': 'Peso de la mascota', 'id': 'id_cliente'}),
            'nombre': forms.TextInput( attrs= {'class': 'form-control', 'placeholder': 'Nombre de la mascota'}),
            'fnaci': forms.DateInput( attrs= {'class': 'form-control', 'placeholder': 'Fecha de nacimiento de la mascota'}),
            'especie': forms.TextInput( attrs= {'class': 'form-control', 'placeholder': 'Especie de la mascota'}),
            'razam': forms.TextInput( attrs= {'class': 'form-control', 'placeholder': 'Raza de la mascota'}),
            'sexom': forms.TextInput( attrs= {'class': 'form-control', 'placeholder': 'Sexo de la mascota'}),
            'peso': forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Peso de la mascota', 'min':1}),
        }
        labels = {
            'peso': 'Peso (KG)',
            'cliente': 'Propietario de la mascota',
            'nombre':'Nombre de la Mascota',
            'estado':'Estado',
            'fnaci':'Fecha e Nacimiento',
            'especie':'Especie',
            'razam':'Raza',
            'sexom':'Sexo',

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['cliente'].empty_label = 'Seleccione el cliente'

#FORMS CONSULTAS
class ConsultaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.filter(estado=True).order_by('nombre'))
    class Meta:
        model = Consulta
        fields = [ 'mascota','motivo', 'sintomas', 'temp', 'frecar', 'freres','diapre', 'examen','trata', 'diadef']
        widgets = {
            'motivo': forms.TextInput( attrs= {'class': 'form-control  textarea', 'placeholder': 'Motivo de la consulta','required':'True'}),
            'sintomas': forms.TextInput( attrs= {'class': 'form-control  textarea', 'placeholder': 'Síntomas del paciente','required':'True'}),
            'diapre': forms.Textarea( attrs= {'class': 'form-control  textarea', 'placeholder': 'Diagnostico Presuntivo','rows':'5','required':'True'}),
            'temp': forms.NumberInput( attrs= {'class': 'form-control  textarea', 'placeholder': 'Temperatura del paciente','required':'True'}),
            'frecar': forms.NumberInput( attrs= {'class': 'form-control  textarea', 'placeholder': 'Frecuencia cardiaca','required':'True'}),
            'freres': forms.NumberInput( attrs= {'class': 'form-control  textarea', 'placeholder': 'Frecuencia respiratoria','required':'True'}),
            'examen': forms.Textarea( attrs= {'class': 'form-control  textarea', 'placeholder': 'Examenes realizados','rows':'5','required':'True'}),
            'diadef': forms.Textarea( attrs= {'class': 'form-control  textarea', 'placeholder': 'Diagnostico definitivo','rows':'5','required':'True'}),
            'trata': forms.Textarea( attrs= {'class': 'form-control  textarea', 'placeholder': 'Tratamientos aplicados','rows':'5','required':'True'}),
            'mascota': forms.Select(attrs= {'class': 'custom-select  textarea'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['mascota'].empty_label = 'Seleccione la mascota'

#FORMS VACUNACIONES

class VacunaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.filter(estado=True).order_by('nombre'))

    class Meta:
        model = Vacuna
        fields = ['mascota', 'nomva', 'dosis']
        widgets = {
            'mascota': forms.Select( attrs= {'class': 'custom-select'}), 
            'nomva': forms.TextInput( attrs= {'class': 'form-control textarea', 'placeholder': 'Nombre de la Vacuna','required':'True'}),
            'dosis': forms.NumberInput ( attrs= {'class': 'form-control textarea', 'placeholder': 'Dosis de la Vacuna','required':'True'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['mascota'].empty_label = 'Seleccione la mascota'

#FORMS DESPARASITACIONES

class DespaForm(forms.ModelForm):
    mascota = forms.ModelChoiceField(queryset=Mascota.objects.filter(estado=True).order_by('nombre'))

    class Meta:
        model = Despa
        fields = ['mascota', 'despa', 'descripcion']

        widgets = {
            'mascota': forms.Select( attrs= {'class': 'custom-select'}),
            'despa': forms.TextInput( attrs= {'class': 'form-control textarea', 'placeholder': 'Desparasitante','maxlength':'25','required':'True'}),
            'descripcion': forms.Textarea ( attrs= {'class': 'form-control textarea', 'placeholder': 'Descripcion de la Desparacitación','rows':'5','required':'True'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })
        self.fields['mascota'].empty_label = 'Seleccione la mascota'