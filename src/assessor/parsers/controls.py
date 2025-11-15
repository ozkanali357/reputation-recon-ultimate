from pydantic import BaseModel
from typing import List, Dict, Any

class Control(BaseModel):
    id: str
    name: str
    description: str
    category: str
    implementation: str
    effectiveness: str

def parse_controls(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Input: {"controls": {"encryption": True, "multi_factor_authentication": False}}
    Output: {"encryption": True, "multi_factor_authentication": False}
    """
    return dict(data.get("controls", {}))