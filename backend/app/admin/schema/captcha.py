from pydantic import Field

from backend.common.schema import SchemaBase


class GetCaptchaDetail(SchemaBase):
    """Captcha detail"""

    uuid: str = Field(description='Image unique identifier')
    img_type: str = Field(description='Image type')
    image: str = Field(description='Image content')
