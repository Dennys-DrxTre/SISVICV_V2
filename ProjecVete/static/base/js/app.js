const especie = document.getElementById('id_especie');

const canino = document.querySelector('.perros');
const fenino = document.querySelector('.gatos');

especie.addEventListener('click', e => {
     const opcion = especie.options[especie.selectedIndex].value;

     if (opcion == 'Canino') {
          canino.classList.add('activo');
     }else{
          canino.classList.remove('activo');
     }
     if (opcion == 'Felino') {
          fenino.classList.add('activo');
     }else{
          fenino.classList.remove('activo');
     }
});