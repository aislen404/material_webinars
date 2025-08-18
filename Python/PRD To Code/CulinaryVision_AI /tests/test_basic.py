"""
Pruebas básicas para validar la estructura del proyecto.
"""
import pytest
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_project_structure():
    """Prueba que la estructura del proyecto sea correcta."""
    # Verificar que existen los directorios principales
    assert os.path.exists("config")
    assert os.path.exists("services")
    assert os.path.exists("models")
    assert os.path.exists("utils")
    assert os.path.exists("tests")
    
    # Verificar archivos principales
    assert os.path.exists("main.py")
    assert os.path.exists("requirements.txt")
    assert os.path.exists("README.md")
    assert os.path.exists("env.example")

def test_config_import():
    """Prueba que se puede importar el módulo de configuración."""
    try:
        from config.settings import settings
        assert settings is not None
        print("✅ Configuración importada correctamente")
    except ImportError as e:
        pytest.fail(f"No se pudo importar configuración: {e}")

def test_models_import():
    """Prueba que se pueden importar los modelos."""
    try:
        from models.ingredient import Ingrediente, ListaIngredientes
        from models.recipe import Receta, ColeccionRecetas
        from models.user_profile import PerfilUsuario
        assert Ingrediente is not None
        assert ListaIngredientes is not None
        assert Receta is not None
        assert ColeccionRecetas is not None
        assert PerfilUsuario is not None
        print("✅ Modelos importados correctamente")
    except ImportError as e:
        pytest.fail(f"No se pudieron importar modelos: {e}")

def test_services_import():
    """Prueba que se pueden importar los servicios."""
    try:
        from services.recipe_generator import RecipeGenerator
        assert RecipeGenerator is not None
        print("✅ Servicios importados correctamente")
    except ImportError as e:
        pytest.fail(f"No se pudieron importar servicios: {e}")

def test_utils_import():
    """Prueba que se pueden importar las utilidades."""
    try:
        from utils.validators import Validators
        from utils.helpers import Helpers
        assert Validators is not None
        assert Helpers is not None
        print("✅ Utilidades importadas correctamente")
    except ImportError as e:
        pytest.fail(f"No se pudieron importar utilidades: {e}")

def test_ingredient_model():
    """Prueba la creación de un ingrediente."""
    from models.ingredient import Ingrediente, EstadoIngrediente
    
    ingrediente = Ingrediente(
        nombre="tomate",
        cantidad=200.0,
        confianza=0.95,
        detectado=True,
        estado=EstadoIngrediente.FRESCO
    )
    
    assert ingrediente.nombre == "tomate"
    assert ingrediente.cantidad == 200.0
    assert ingrediente.confianza == 0.95
    assert ingrediente.detectado is True
    assert ingrediente.estado == EstadoIngrediente.FRESCO

def test_user_profile_model():
    """Prueba la creación de un perfil de usuario."""
    from models.user_profile import PerfilUsuario, NivelCulinario, RestriccionDietetica
    
    perfil = PerfilUsuario(
        nombre="Usuario Test",
        nivel_culinario=NivelCulinario.INTERMEDIO,
        tiempo_disponible=30,
        num_personas=2,
        restricciones_dieteticas=[RestriccionDietetica.VEGETARIANO]
    )
    
    assert perfil.nombre == "Usuario Test"
    assert perfil.nivel_culinario == NivelCulinario.INTERMEDIO
    assert perfil.tiempo_disponible == 30
    assert perfil.num_personas == 2
    assert len(perfil.restricciones_dieteticas) == 1
    assert perfil.es_vegetariano() is True

def test_helpers_functions():
    """Prueba las funciones auxiliares."""
    from utils.helpers import Helpers
    
    # Probar formateo de tiempo
    assert Helpers.format_time(30) == "30 min"
    assert Helpers.format_time(90) == "1h 30min"
    assert Helpers.format_time(120) == "2h"
    
    # Probar formateo de dificultad
    assert Helpers.format_difficulty(1) == "Muy fácil"
    assert Helpers.format_difficulty(3) == "Intermedio"
    assert Helpers.format_difficulty(5) == "Muy difícil"

def test_validators():
    """Prueba las funciones de validación."""
    from utils.validators import Validators
    
    # Probar validación de email
    assert Validators.validate_email("test@example.com") is True
    assert Validators.validate_email("invalid-email") is False
    
    # Probar validación de configuración de APIs
    api_config = Validators.validate_api_configuration()
    assert isinstance(api_config, dict)
    assert 'valid' in api_config
    assert 'available_services' in api_config

def test_recipe_model():
    """Prueba la creación de una receta."""
    from models.recipe import Receta, Instruccion, InformacionNutricional, IngredienteReceta
    from models.recipe import NivelDificultad, TipoCocina
    
    # Crear ingrediente de receta
    ingrediente = IngredienteReceta(
        nombre="tomate",
        cantidad="200g",
        unidad="gramos",
        detectado=True,
        esencial=True
    )
    
    # Crear instrucción
    instruccion = Instruccion(
        paso=1,
        accion="Cortar el tomate en rodajas",
        tiempo_estimado="5 min"
    )
    
    # Crear información nutricional
    info_nut = InformacionNutricional(
        calorias_por_porcion=150,
        proteinas_g=5.0,
        carbohidratos_g=20.0,
        grasas_g=2.0
    )
    
    # Crear receta
    receta = Receta(
        id=1,
        nombre="Ensalada de Tomate",
        descripcion_corta="Ensalada fresca y saludable",
        tiempo_preparacion_min=10,
        tiempo_coccion_min=0,
        tiempo_total_min=10,
        dificultad_estrellas=1,
        porciones=2,
        tipo_cocina=TipoCocina.MEDITERRANEA,
        ingredientes=[ingrediente],
        instrucciones=[instruccion],
        informacion_nutricional=info_nut,
        nivel_dificultad=NivelDificultad.PRINCIPIANTE
    )
    
    assert receta.nombre == "Ensalada de Tomate"
    assert receta.tiempo_total_min == 10
    assert len(receta.ingredientes) == 1
    assert len(receta.instrucciones) == 1
    assert receta.es_vegetariana() is True

if __name__ == "__main__":
    # Ejecutar pruebas básicas
    print("🧪 Ejecutando pruebas básicas...")
    
    test_project_structure()
    test_config_import()
    test_models_import()
    test_services_import()
    test_utils_import()
    test_ingredient_model()
    test_user_profile_model()
    test_helpers_functions()
    test_validators()
    test_recipe_model()
    
    print("✅ Todas las pruebas básicas pasaron!")
