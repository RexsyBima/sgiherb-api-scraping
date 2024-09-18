from ast import Attribute
from dataclasses import dataclass


@dataclass
class SgiherbProduct:

    id: int
    displayName: str
    isAvailableToPurchase: bool
    partNumber: str
    rootCategoryId: int
    rootCategoryName: str
    url: str
    urlName: str
    discountPrice: float
    listPrice: float
    brandCode: str
    brandName: str
    brandUrl: str
    primaryImageIndex: int

    def __post_init__(self):
        try:
            self.listPrice = float(self.listPrice.removeprefix("$"))
            self.discountPrice = float(self.discountPrice.removeprefix("$"))
        except AttributeError:
            pass
