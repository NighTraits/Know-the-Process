# AGENTS.md - Know the Process

## Qué es este proyecto
Asistente que responde consultas con respecto a procesos de traḿites gubernamentales, empleando unicamente la información que se encuentra en el documento `static/db.json`; o, los archivos en `chroma_db/`.

## Cómo está hecho
- Python 3.14.10
- Instalar dependencias: `pip install -e .`
- Levantar la app: `streamlit run app.py`
- Pantallas:
    - views/archive.py
    - views/chat.py
    - views/details.py
    - views/home.py
- Interfaz: Streamlit, desplegada en Streamlit Community Cloud.
- IA: `Langchain-google-genai` y `langchain-chroma`. Los dos modelos están en las constantes `AGENT_MODELAGENT_MODEL` y `EMBEDDING_MODEL`.
- Búsqueda semántica sobre a la base de datos vectorial úbicado en `chroma_db/` bajo la constante `COLLECTION`.
- Archivos: `app.py`, `pyproject.toml` y este fichero. La especificación completa está en `especificacion.md`, léela antes de proponer cambios.


## Reglas
- Responde en español usando SOLO lo que se encuentra en el database.
- Siempre usa la tool de busqueda en la database antes de responder.
- Solo usa información recibida de la tool.
- Si no se encuentra una respuesta, di que no sabes.


## Cómo comprobar que funciona
- streamlit run app.py con .streamlit/secrets.toml en local.
- Casos de prueba (entrada → lo que esperamos):
    1. "¿Cómo sé si en mi terreno es fertil?" → Puedes realizar un Análisis de Fertilidad de Suelo.
    2. "¿Dónde puedo comprar una escavadora?" → Di que no sabes.
    3. Clave inválida → mensaje claro, sin traza de error en pantalla.


## Qué no hacer
- No cambies los modelos ni metas una base de datos vectorial sin preguntar.
- No toques los documentos en `chroma_db/` y `static/db.json`. Es la base de datos vectorial base para los modelos.
- No hagas push ni redespliegues sin avisar y hayas recibido aprobación de ella.