from pydantic import BaseModel

# App එකෙන් එවන දත්ත වල හැඩය මේකයි කියලා API එකට කියනවා
class MechanicCreate(BaseModel):
    name: str
    skill: str
    distance: float
