# Especificación: Know the Process PTY


## 1. Problema y usuario

- **¿Qué problema resolvéis?**

    El gobierno de Panamá dispone de plataformas que provee información sobre los trámites gubernamentales. Sin embargo, no hay manera de encontrarlo sin conocer el término al que se le identifica dicho proceso.

- **¿Quién tiene el problema?** 

    Los ciudadanos de Panamá.

- **¿Cómo lo resuelve hoy?**

    Hoy en día, para conocer el cómo realizar un trámite se debe:
    - Consultar a alguien quien haya realizado dicho trámite con anterioridad y, esperar que el proceso sea igual. 
    - Búscar en una lista de +2k trámites disponibles en la página digital del gobierno.
    - Búsqueda exhaustiva en internet, ya sea redes sociales o guía escrito por los ciudadanos.
    - Ir presencial al posible lugar donde se realiza dicho trámite y recibir las indicaciones. Frecuetemente, se debe regresar por falta de documento o requerir cita previa.

- **¿Qué le molesta?**
    
    El proceso del trámite en si es casi inmediato, sin embargo, uno termina perdiendo más tiempo investigando. 
    
    En el peor de los casos, terminamos regresando otro día por falta de algún documento o, al disponer de un documento en su plataforma, se require llevarlo impreso.

- **¿Qué parte resuelve la IA?**
    
    Encontrar el el trámite a buscar, entre todos los existentes, y proveer información de la misma al usuario. Lo que no existe en la lista se queda por fuera.


## 2. Qué hace la app
1. Busca que trámite va acorde a la pregunta del usuario.
2. Provee las indicaciones y con que institución se realizar el trámite.
5. Responde que no sabe cuando el trámite especificado no se encuentra en la base de datos.


## 3. Entradas y salidas
- **Usuario**: pregunta/consulta sobre un trámite escrita con sus palabras.
- **Agente**: respuesta detallada sobre le trámite encontrado en la base de datos.
- **Ejemplo**:
    - **Usuario**: "¿Qué debo hacer para sacar mi cédula por primera vez?"
    - **Agente**: *\*provee texto sobre los requisitos del trámite e institución encargada\**


## 4. ¿Qué pieza de IA usa? - RAG
1. Embedding con ``gemini-embedding-001``, para la generación del Chroma, cada vez que se actualiza el [db.json](/static/db.json). Esta se queda en el repositorio para evitar el consumo masivo de token, en ingesta del documento, por cada despliegue de la applicación.
2. Embedding con ``gemini-embedding-001`` para la búsqueda semántica con respecto al Chroma.
3. Redacción con ```gemini-3.5-flash-lite```. Es con el que se ha estado usando a lo largo de las actividades.
4. Instrucciones para el modelo (system prompt):
    - Responde en español usando SOLO lo que se encuentra en el database.
    - Siempre usa la tool () de busqueda en la database antes de responder.
    - Solo usa información recibida de la tool.
    - Si no se encuentra una respuesta, di que no sabes.

## 5. Flujo del usuario
1. El usuario entra y ver la página principal.
2. El usuario selecciona una de las preguntas pre-definidos.
3. La app lo redirige a la página de chat con el agente.
4. Se realiza la pregunta al agente y el usuario recibe la respuesta.


## 6. Restricciones
- Coste cero: capa gratuita de la API y despliegue gratuito en Streamlit Community Cloud.
- La clave de la API va en secretos, nunca en el código.
- Sin datos personales reales.
- Lenguaje sencillo, para alguien sin conocimientos técnicos.
- Límite de 100 documentos en la base de datos.



## 7. Criterios de aceptación
| Entrada | Resultado esperado |
| --- | --- |
| "¿Cómo sé si en mi terreno es fertil?" | Di que puede realizar un Análisis de Fertilidad de Suelo. |
| "¿Dónde puedo comprar una escavadora?" | Di que esa información no corresponde a trámites gubernamentales. |
| Clave inválida | mensaje claro, sin traza de error en pantalla. |


## 8. Fuera de alcance
Existe ~2.5k de traḿites en la página del gobierno. Si bien, se puede lograr localmente con el [data_ingest.py](/scripts/data_ingest.py), esta data es masiva en comparación con los tokens disponibles. Dado el caso, se movería a un vector DB como tal.


## 9. Despliegue
Streamlit Community Cloud