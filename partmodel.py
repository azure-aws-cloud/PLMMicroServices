from typing import Optional
from pydantic import BaseModel
import json

class PartModel(BaseModel):
    # Optional for creation
    part_id: Optional[int] = None # Optional for creation
    part_name: str
    part_number: str
    quantity: int
    lifecycle_state: str



# # create an instance of part model without id
# part = PartModel(part_name="GEAR",part_number="GEAR 1000",
#                  quantity =100,
#                  lifecycle_state="approved")
# part_dict = part.model_dump()
# part_json_pretty = json.dumps(part_dict, indent=2)
# print(part_json_pretty)


