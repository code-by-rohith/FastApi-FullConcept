from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    tittle : str
    body : str
