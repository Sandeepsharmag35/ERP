from decimal import Decimal
from product.models import Product, ProductUoM, UoM


class UnitConversionService:
    @staticmethod
    def convert_qty(value: Decimal, from_uom: UoM, to_uom: UoM) -> Decimal:
        """
        Convert quantity between different units of measure using SI units as intermediate

        Args:
            value: The quantity to convert
            from_uom: Source UoM object
            to_uom: Target UoM object

        Returns:
            Converted quantity in target UoM

        Example:
            convert_qty(1, box_uom, ea_uom) -> 10  # if 1 box = 10 each
        """
        if from_uom == to_uom:
            return value

        # First convert to SI units
        si_value = value * from_uom.conversion_to_si

        # Then convert from SI to target UoM
        result = si_value / to_uom.conversion_to_si

        # If converting between UoMs for same product, use direct factor
        try:
            product_uom = ProductUoM.objects.get(product__base_uom=from_uom, uom=to_uom)
            result = value * product_uom.factor
        except ProductUoM.DoesNotExist:
            pass

        return result
