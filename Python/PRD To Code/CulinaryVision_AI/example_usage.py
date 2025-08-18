"""
Ejemplo de uso de CulinaryVision AI
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from main import CulinaryVisionAI
from models.user_profile import PerfilUsuario, NivelCulinario, RestriccionDietetica

def ejemplo_basico():
    """Ejemplo básico de uso de la aplicación."""
    print("🍳 Ejemplo básico de CulinaryVision AI")
    print("=" * 50)
    
    try:
        # Inicializar la aplicación
        app = CulinaryVisionAI()
        print("✅ Aplicación inicializada correctamente")
        
        # Obtener información del sistema
        system_info = app.get_system_info()
        print(f"📊 Versión: {system_info['version']}")
        print(f"🔧 Servicios disponibles: {system_info['apis']['available_services']}")
        
        # Crear un perfil de usuario
        perfil = PerfilUsuario(
            nombre="Chef Ejemplo",
            nivel_culinario=NivelCulinario.INTERMEDIO,
            tiempo_disponible=45,
            num_personas=3,
            restricciones_dieteticas=[RestriccionDietetica.VEGETARIANO]
        )
        print(f"👤 Perfil creado: {perfil.nombre} ({perfil.nivel_culinario.value})")
        
        # Lista de ingredientes de ejemplo (en lugar de imágenes)
        ingredientes_ejemplo = ["tomate", "cebolla", "ajo", "pasta", "queso"]
        print(f"🥕 Ingredientes de ejemplo: {', '.join(ingredientes_ejemplo)}")
        
        # Obtener sugerencias de ingredientes
        sugerencias = app.get_ingredient_suggestions(ingredientes_ejemplo)
        print(f"💡 Sugerencias: {', '.join(sugerencias)}")
        
        print("\n✅ Ejemplo básico completado exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en ejemplo básico: {e}")

def ejemplo_perfil_usuario():
    """Ejemplo de creación y uso de perfiles de usuario."""
    print("\n👤 Ejemplo de perfiles de usuario")
    print("=" * 50)
    
    # Perfil principiante
    perfil_principiante = PerfilUsuario(
        nombre="Cocinero Principiante",
        nivel_culinario=NivelCulinario.PRINCIPIANTE,
        tiempo_disponible=20,
        num_personas=2,
        nivel_picante=1
    )
    
    # Perfil vegetariano
    perfil_vegetariano = PerfilUsuario(
        nombre="Chef Vegetariano",
        nivel_culinario=NivelCulinario.AVANZADO,
        tiempo_disponible=60,
        num_personas=4,
        restricciones_dieteticas=[RestriccionDietetica.VEGETARIANO],
        preferencia_proteinas=True
    )
    
    # Perfil sin gluten
    perfil_sin_gluten = PerfilUsuario(
        nombre="Cocinero Sin Gluten",
        nivel_culinario=NivelCulinario.INTERMEDIO,
        tiempo_disponible=30,
        num_personas=2,
        restricciones_dieteticas=[RestriccionDietetica.SIN_GLUTEN],
        alergenos=["gluten"]
    )
    
    perfiles = [perfil_principiante, perfil_vegetariano, perfil_sin_gluten]
    
    for perfil in perfiles:
        print(f"\n👤 {perfil.nombre}:")
        print(f"   Nivel: {perfil.nivel_culinario.value}")
        print(f"   Tiempo: {perfil.tiempo_disponible} min")
        print(f"   Personas: {perfil.num_personas}")
        print(f"   Vegetariano: {perfil.es_vegetariano()}")
        print(f"   Sin gluten: {perfil.tiene_restriccion_gluten()}")
        print(f"   Preferencias: {perfil.obtener_preferencias_texto()}")

def ejemplo_validaciones():
    """Ejemplo de validaciones del sistema."""
    print("\n🔍 Ejemplo de validaciones")
    print("=" * 50)
    
    from utils.validators import Validators
    from utils.helpers import Helpers
    
    # Validar emails
    emails = ["usuario@ejemplo.com", "email-invalido", "test@domain.co.uk"]
    for email in emails:
        es_valido = Validators.validate_email(email)
        print(f"📧 {email}: {'✅' if es_valido else '❌'}")
    
    # Validar configuración de APIs
    api_config = Validators.validate_api_configuration()
    print(f"\n🔧 Configuración de APIs:")
    print(f"   Válida: {'✅' if api_config['valid'] else '❌'}")
    print(f"   Servicios: {api_config['available_services']}")
    if api_config['warnings']:
        print(f"   Advertencias: {api_config['warnings']}")
    
    # Formateo de datos
    print(f"\n⏰ Formateo de tiempo:")
    tiempos = [15, 45, 90, 120]
    for tiempo in tiempos:
        formateado = Helpers.format_time(tiempo)
        print(f"   {tiempo} min → {formateado}")
    
    print(f"\n⭐ Formateo de dificultad:")
    dificultades = [1, 2, 3, 4, 5]
    for diff in dificultades:
        formateado = Helpers.format_difficulty(diff)
        print(f"   {diff} estrellas → {formateado}")

def ejemplo_recetas():
    """Ejemplo de creación de recetas."""
    print("\n📋 Ejemplo de recetas")
    print("=" * 50)
    
    from models.recipe import Receta, Instruccion, InformacionNutricional, IngredienteReceta
    from models.recipe import NivelDificultad, TipoCocina
    from utils.helpers import Helpers
    
    # Crear ingredientes
    ingredientes = [
        IngredienteReceta(nombre="tomate", cantidad="300g", unidad="gramos", detectado=True),
        IngredienteReceta(nombre="mozzarella", cantidad="200g", unidad="gramos", detectado=True),
        IngredienteReceta(nombre="albahaca", cantidad="10", unidad="hojas", detectado=True),
        IngredienteReceta(nombre="aceite de oliva", cantidad="2", unidad="cucharadas", detectado=False)
    ]
    
    # Crear instrucciones
    instrucciones = [
        Instruccion(paso=1, accion="Cortar los tomates en rodajas", tiempo_estimado="5 min"),
        Instruccion(paso=2, accion="Cortar la mozzarella en láminas", tiempo_estimado="3 min"),
        Instruccion(paso=3, accion="Alternar tomate y mozzarella en un plato", tiempo_estimado="2 min"),
        Instruccion(paso=4, accion="Agregar hojas de albahaca y aceite de oliva", tiempo_estimado="1 min")
    ]
    
    # Crear información nutricional
    info_nut = InformacionNutricional(
        calorias_por_porcion=250,
        proteinas_g=15.0,
        carbohidratos_g=8.0,
        grasas_g=18.0,
        fibra_g=3.0
    )
    
    # Crear receta
    receta = Receta(
        id=1,
        nombre="Caprese Clásico",
        descripcion_corta="Ensalada italiana fresca y deliciosa",
        tiempo_preparacion_min=10,
        tiempo_coccion_min=0,
        tiempo_total_min=10,
        dificultad_estrellas=1,
        porciones=4,
        tipo_cocina=TipoCocina.ITALIANA,
        ingredientes=ingredientes,
        instrucciones=instrucciones,
        informacion_nutricional=info_nut,
        nivel_dificultad=NivelDificultad.PRINCIPIANTE,
        consejos_chef=["Usar tomates maduros para mejor sabor", "Servir a temperatura ambiente"],
        variaciones=["Agregar pesto para más sabor", "Sustituir mozzarella por burrata"]
    )
    
    # Mostrar información de la receta
    print(f"🍽️  {receta.nombre}")
    print(f"📝 {receta.descripcion_corta}")
    print(f"⏰ Tiempo: {Helpers.format_time(receta.tiempo_total_min)}")
    print(f"⭐ Dificultad: {Helpers.format_difficulty(receta.dificultad_estrellas)}")
    print(f"👥 Porciones: {receta.porciones}")
    print(f"🌍 Tipo: {receta.tipo_cocina.value}")
    print(f"🥬 Vegetariana: {'✅' if receta.es_vegetariana() else '❌'}")
    print(f"🌱 Vegana: {'✅' if receta.es_vegana() else '❌'}")
    
    print(f"\n🥕 Ingredientes:")
    for ingrediente in receta.ingredientes:
        detectado = "✅" if ingrediente.detectado else "❌"
        print(f"   {detectado} {ingrediente.cantidad} {ingrediente.unidad} de {ingrediente.nombre}")
    
    print(f"\n📋 Instrucciones:")
    for instruccion in receta.instrucciones:
        print(f"   {instruccion.paso}. {instruccion.accion} ({instruccion.tiempo_estimado})")
    
    print(f"\n💡 Consejos del chef:")
    for consejo in receta.consejos_chef:
        print(f"   • {consejo}")
    
    print(f"\n🔄 Variaciones:")
    for variacion in receta.variaciones:
        print(f"   • {variacion}")

def main():
    """Función principal del ejemplo."""
    print("🚀 CulinaryVision AI - Ejemplos de Uso")
    print("=" * 60)
    
    # Ejecutar ejemplos
    ejemplo_basico()
    ejemplo_perfil_usuario()
    ejemplo_validaciones()
    ejemplo_recetas()
    
    print("\n" + "=" * 60)
    print("✅ Todos los ejemplos completados exitosamente!")
    print("\n💡 Para usar la aplicación con imágenes reales:")
    print("   python main.py imagen1.jpg imagen2.jpg --save --verbose")
    print("\n📚 Para más información, consulta el README.md")

if __name__ == "__main__":
    main()
