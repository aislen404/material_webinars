// JavaScript accesible 
// Función para mostrar mensaje
function mostrarMensaje() {
    alert('¡Bienvenido a nuestro sitio web accesible!');
}

// Validación de formulario accesible
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const nombreInput = document.getElementById('nombre');
    const emailInput = document.getElementById('email');
    
    // Validación en tiempo real
    nombreInput.addEventListener('blur', function() {
        validarCampo(this, 'El nombre es obligatorio');
    });
    
    emailInput.addEventListener('blur', function() {
        validarEmail(this);
    });
    
    // Validación al enviar
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let esValido = true;
        
        if (!validarCampo(nombreInput, 'El nombre es obligatorio')) {
            esValido = false;
        }
        
        if (!validarEmail(emailInput)) {
            esValido = false;
        }
        
        if (esValido) {
            alert('Formulario enviado correctamente');
            form.reset();
        }
    });
    
    function validarCampo(campo, mensaje) {
        const errorElement = document.getElementById(campo.id + '-error');
        
        if (!campo.value.trim()) {
            campo.setAttribute('aria-invalid', 'true');
            errorElement.textContent = mensaje;
            errorElement.style.display = 'block';
            return false;
        } else {
            campo.setAttribute('aria-invalid', 'false');
            errorElement.textContent = '';
            errorElement.style.display = 'none';
            return true;
        }
    }
    
    function validarEmail(campo) {
        const errorElement = document.getElementById(campo.id + '-error');
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!campo.value.trim()) {
            campo.setAttribute('aria-invalid', 'true');
            errorElement.textContent = 'El email es obligatorio';
            errorElement.style.display = 'block';
            return false;
        } else if (!emailRegex.test(campo.value)) {
            campo.setAttribute('aria-invalid', 'true');
            errorElement.textContent = 'Por favor, introduce un email válido';
            errorElement.style.display = 'block';
            return false;
        } else {
            campo.setAttribute('aria-invalid', 'false');
            errorElement.textContent = '';
            errorElement.style.display = 'none';
            return true;
        }
    }
});

// Manejo de teclado para navegación
document.addEventListener('keydown', function(e) {
    // Escape para cerrar modales o alertas
    if (e.key === 'Escape') {
        // Lógica para cerrar elementos modales
    }
});