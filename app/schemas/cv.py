from pydantic import BaseModel


class CVResponse(BaseModel):
    id: str
    file_name: str
    file_path: str

    class Config:
        from_attributes = True