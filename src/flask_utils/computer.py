def compute_vat(vat, rate):
    return vat * rate / 100


def compute_total_vat(vat_code):
    total = 0
    total += compute_vat(vat_code.vat_5_5, 5.5)
    total += compute_vat(vat_code.vat_10, 10)
    total += compute_vat(vat_code.vat_20, 20)
    return total


def compute_average_vat(vat_code):
    return compute_total_vat(vat_code) / 100


def compute_without_tax(with_tax=None, vat_code=None):
    if with_tax is None:
        return 0
    if vat_code is None:
        return with_tax
    return round(with_tax / (1 + compute_average_vat(vat_code)))
