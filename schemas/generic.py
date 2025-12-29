from typing import Dict, Any
from pydantic import RootModel


class Row(RootModel[Dict[str, Any]]):
    pass