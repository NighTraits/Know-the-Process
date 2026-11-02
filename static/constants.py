
DESCRIPTION: str = """
    Consulta cualquier información sobre algún tramite gubernamental que necesites saber. 
    Cómo qué trámite corresponde a qué, cómo es el proceso, donde puedo hacerlo, y más.
"""

PROMPTS: list[str] = [
    "¿Cómo afilio mi empleado a la CSS?",
    "¿Cómo sé si en mi terreno es fertil?",
    "¿Qué tengo que hacer para saber si la tierra en mi terreno es fértil?",
    "¿puedo yo, siendo extranjero, alquilar un local en un aeropuerto?",
    "¿Dónde debo ir para realizar cualquier tipo de análisis de aguas?",
    "¿Cuáles datos personales puedo actualizar?",
]

COLLECTION = "tramites_db"
AGENT_MODEL = "gemini-3.5-flash-lite"
EMBEDDING_MODEL = "gemini-embedding-2"
