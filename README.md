# 🦷 Abstract Ontology Engine (Python + SQLAlchemy)

Este proyecto es un motor de gestión de taxonomías y ontologías diseñado bajo principios de abstracción y polijerarquía. Permite definir conceptos, establecer relaciones ponderadas (pesos) y llevar un registro de auditoría completo de cada cambio realizado.

Aunque incluye un caso de uso específico para **Odontología**, su núcleo está desacoplado para ser reutilizado en cualquier dominio de conocimiento.

## 🚀 Características Principales

- **Abstracción Total:** Los modelos de datos y la lógica de negocio están separados de los orígenes de datos mediante interfaces (`IDataLoader`).
- **Polijerarquía:** Un concepto (nodo) puede tener múltiples padres y múltiples hijos, permitiendo estructuras de red complejas.
- **Relaciones Ponderadas:** Cada relación (`Edge`) incluye un `weight` (float) y un `type` para definir la fuerza y naturaleza del vínculo (ej: "jerárquico", "correlación").
- **Versionado Nativo:** Soporte para múltiples versiones de la misma ontología, permitiendo evolucionar el conocimiento sin perder estados previos.
- **Audit Log (ChangeLog):** Registro automático de cada inserción, modificación o eliminación con timestamp UTC y metadatos JSON.
- **Seguridad de Sesiones:** Implementación con `scoped_session` de SQLAlchemy para garantizar la integridad de datos y evitar errores de sesiones huérfanas.

## 🛠️ Requerimientos Técnicos

- **Lenguaje:** Python 3.12+
- **ORM:** SQLAlchemy 2.0+
- **Base de Datos:** SQLite (generación automática del archivo `.db`)

## 📂 Estructura del Proyecto

- `ontology_engine.py`: Núcleo del motor. Contiene los modelos SQLAlchemy y la clase `OntologyEngine`.
- `test_ontology_engine.py`: Suite de pruebas unitarias.
- `example_dentistry.py`: Implementación de ejemplo para el dominio odontológico.
- `.gitignore`: Configuración para excluir archivos binarios y caché.

## ⚙️ Cómo Ejecutar

### 1. Instalación de dependencias
Asegúrate de tener `pip` actualizado:
```bash
pip install SQLAlchemy
```

### 2. Ejecutar el caso de uso (Odontología)
Crea una base de datos local y genera la taxonomía de ejemplo (Patología -> Periodoncia -> Gingivitis):
```bash
python3 example_dentistry.py
```

### 3. Ejecutar pruebas unitarias
Verifica la integridad del motor:
```bash
python3 test_ontology_engine.py
```

## 📥 Input / 📤 Output

### Input (Ejemplo de creación de nodo)
```python
engine.create_node(
    name="Gingivitis",
    metadata={"type": "Inflamatoria", "severity": "Moderate"}
)
```

### Output (Estructura de datos devuelta)
El motor devuelve diccionarios Python puros para facilitar la serialización (JSON) y el uso en APIs:
```json
{
    "id": 3,
    "name": "Gingivitis",
    "metadata": {"type": "Inflamatoria", "severity": "Moderate"},
    "version_id": 1
}
```

## 🔮 Mejoras Futuras y Escalabilidad

1.  **Integración con LLM (RAG):** Conectar este motor como una capa de conocimiento estructurado para modelos de lenguaje. La ontología puede servir para filtrar o jerarquizar el contexto enviado al LLM.
2.  **Exportación RDF/OWL:** Añadir exportadores para formatos estándar de la web semántica.
3.  **Visualización de Grafos:** Integrar librerías como `NetworkX` o `Pyvis` para generar mapas visuales de las relaciones.
4.  **API REST:** Exponer el `OntologyEngine` a través de FastAPI o Flask para su consumo remoto.
5.  **Validación de Ciclos:** Implementar algoritmos que detecten y eviten referencias circulares en jerarquías estrictas si el dominio lo requiere.

---
**Desarrollado como una solución profesional de Arquitectura de Datos.**
