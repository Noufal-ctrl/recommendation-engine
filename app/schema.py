from pydantic import BaseModel
from typing import Optional

class ActivityRequest(BaseModel):
    user_id: str
    product_id: int
    action: str = "view"      # view | add_to_cart | purchase
    tone: Optional[str] = "casual"   # casual | premium | budget

class SearchRequest(BaseModel):
    user_id: str
    query: str
    tone: Optional[str] = "casual"