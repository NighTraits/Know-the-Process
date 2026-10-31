
from pydantic import TypeAdapter
import json
from pathlib import Path
from models.data_schema import IContent


def get_data()-> list[IContent] | None:
    
    STORE = Path("static/db.json")
    if not STORE.exists():
        return None
    
    data = json.loads(STORE.read_text())
    
    return TypeAdapter(list[IContent]).validate_python(data)
    
    
    