
import json
from pathlib import Path

def get_data()-> dict[str, str] | None:
    
    STORE = Path("static/db.json")
    if not STORE.exists():
        return None
    
    data = json.loads(STORE.read_text())
    
    return data
    
    
    