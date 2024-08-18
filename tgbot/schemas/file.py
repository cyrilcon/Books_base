from pydantic import BaseModel, Field


class FileBase(BaseModel):
    """
    Base file model with common attributes.
    """

    format: str = Field(..., max_length=10, description="Format of the file")
    file_token: str = Field(..., max_length=255, description="Token of the book file")


class FileCreate(FileBase):
    """
    Schema for creating a new file.
    """

    pass


class FileUpdate(FileBase):
    """
    Schema for updating file information.
    """

    format: str | None = Field(None, max_length=10, description="Format of the file")
    file_token: str | None = Field(
        None, max_length=255, description="Token of the book file"
    )


class FileSchema(BaseModel):
    """
    Detailed file schema.
    """

    id_file: int = Field(..., description="Unique file identifier")
    format: str = Field(..., max_length=10, description="Format of the file")
    file_token: str = Field(..., max_length=255, description="Token of the book file")
