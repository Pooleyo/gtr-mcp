from pydantic import BaseModel

class Project(BaseModel):
    title: str
    abstractText: str 
    techAbstractText: str | None
    potentialImpact: str | None