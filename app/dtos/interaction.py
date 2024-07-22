from app.dtos import BaseResponse


class InteractionResponse(BaseResponse):
    identifier: int
    input: str
    output: str
