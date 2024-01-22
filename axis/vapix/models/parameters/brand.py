"""Brand parameters from param.cgi."""

from dataclasses import dataclass
from typing import Any, Self, cast

from typing_extensions import TypedDict

from .param_cgi import ParamItem


class BrandT(TypedDict):
    """Represent a brand object."""

    Brand: str
    ProdFullName: str
    ProdNbr: str
    ProdShortName: str
    ProdType: str
    ProdVariant: str
    WebURL: str


@dataclass
class BrandParam(ParamItem):
    """Brand parameters."""

    brand: str
    """Device branding."""

    prodfullname: str
    """Device product full name."""

    prodnbr: str
    """Device product number."""

    prodshortname: str
    """Device product short name."""

    prodtype: str
    """Device product type."""

    prodvariant: str
    """Device product variant."""

    weburl: str
    """Device home page URL."""

    @classmethod
    def decode(cls, data: BrandT) -> Self:
        """Decode dictionary to class object."""
        return cls(
            id="brand",
            brand=data["Brand"],
            prodfullname=data["ProdFullName"],
            prodnbr=data["ProdNbr"],
            prodshortname=data["ProdShortName"],
            prodtype=data["ProdType"],
            prodvariant=data["ProdVariant"],
            weburl=data["WebURL"],
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> dict[str, Self]:
        """Create objects from dict."""
        return {"0": cls.decode(cast(BrandT, data))}