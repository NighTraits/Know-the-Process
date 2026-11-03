
SYSTEM_PROMPT = (
    "Responde en español usando SOLO lo que se encuentra en el database."
    "Siempre usa la tool de busqueda en la database antes de responder."
    "Solo usa información recibida de la tool."
    "Si no se encuentra una respuesta, dí que no sabes."
)

DESCRIPTION: str = """
    Consulta información sobre algún trámite gubernamental que necesites saber. 
    Ya sea, compra o alquiler de propiedades, venta de algún servicio o producto, afiliación con la CSS y más.
"""

PROMPTS: list[str] = [
    "¿Necesito un permiso para vender árbolitos de navidad por mi casa?",
    "¿Cómo obtengo mi cédula por primera vez?",
    "¿Qué tengo que hacer para renovar la placa de mi vehículo?",
    "¿Qué necesito y donde debo ir para actualizar mi pasaporte?",
    "¿Cómo afilio mi empleado a la CSS?",
    "¿Puede un representante legal solicitar el cambio del RUC de mi comercio?",
    "¿Cuáles son los requisitos para afiliar a cada integrante de mi familia a la CSS?",
    "¿Qué es un salvoconducto y para que sirve?",
]