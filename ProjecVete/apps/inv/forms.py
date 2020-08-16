from django import forms
from .models import Departamento, Categoria, Producto

class DeparatamentoForm(forms.ModelForm):
    class Meta:
        model= Departamento
        fields = ['descripcion','estado']
        labels = {'descripcion':"Descripción del Departamento",'estado':"Estado"}
        widget = {'descripcion': forms.TextInput}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class CategoriaForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.filter(estado=True).order_by('descripcion'))
    class Meta:
        model= Categoria
        fields = ['departamento' ,'descripcion','estado']
        labels = {'descripcion':"Descripción de la Categoria",'estado':"Estado"}
        widget = {'descripcion': forms.TextInput(attrs={'pattern':'[A-Za-z- ]{2,50}'})}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
                'pattern':'[A-Za-z- ]{2,50}'
            })
        self.fields['departamento'].empty_label = 'Seleccione Departamento'

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.filter(estado=True).order_by('descripcion'))

    class Meta: 
        model = Producto
        fields = ['categoria', 'codigo' ,'nombre', 'stock', 'precioCompra', 'precioVenta', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput( attrs= {'class': 'form-control formulario', 'placeholder': 'Nombre del Producto'}),
            'codigo': forms.TextInput( attrs= {'class': 'form-control formulario', 'placeholder': 'Código del Producto',"pattern":'[0-9]{2,10}'}),
            'stock': forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Cantidad', 'min': '0'}),
            'precioCompra' : forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Precio de Compra', 'min': '1'}),
            'precioVenta': forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Precio de Venta', 'min': '1'}),
            'descripcion': forms.Textarea( attrs= {'class': 'form-control mb-3 textarea', 'placeholder': 'Descripcion del Producto','rows':'5', 'cols':'20'}),
            'categoria': forms.Select(attrs= {'class': 'custom-select  textarea'}),
        }
        
    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")
        if 'codigo' in self.changed_data:
            if Producto.objects.filter(codigo=codigo).exists():
                raise forms.ValidationError("Ya se ha registrado un producto con este codigo")
        return codigo 

        labels = {
            'departamento': 'Departamento',
            'codigo': 'Código del Producto',
            'nombre': 'Nombre del Producto',
            'stock': 'Cantidad del Producto',
            'precioCompra': 'Precio de Compra',
            'precioVenta': 'Precio de Venta',
            'descripcion': 'Descripcion del Producto',
            'departamento': 'Departamento',
            'estado':'Estado'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control',
            })
        self.fields['categoria'].empty_label = 'Seleccione la categoria'

class product_add_more(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['stock', 'precioCompra', 'precioVenta']
        widgets = {
            'stock': forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Cantidad', 'min': '0'}),
            'precioCompra' : forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Precio de Compra', 'min': '1'}),
            'precioVenta': forms.NumberInput( attrs= {'class': 'form-control', 'placeholder': 'Precio de Venta', 'min': '1'}),
        }
