from product.models import ProductUom, Uom
from decimal import Decimal


def convert_qty(product, from_uom_code, to_uom_code, value):
    """
    Convert a quantity from one UoM to another for a given product,
    using conversion via base unit (SI).
    """
    if from_uom_code == to_uom_code:
        return Decimal(value)

    from_uom = Uom.objects.get(code=from_uom_code)
    to_uom = Uom.objects.get(code=to_uom_code)

    from_factor = ProductUom.objects.get(product=product, uom=from_uom).factor
    to_factor = ProductUom.objects.get(product=product, uom=to_uom).factor

    base_qty = Decimal(value) * from_factor
    return base_qty / to_factor
