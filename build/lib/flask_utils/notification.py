import enum as _enum


class ProductEmailTemplateEnum(str, _enum.Enum):
    LEAD_RECEIPT = "lead_receipt"
    ORDER_CONFIRMATION = "order_confirmation"


def get_product_order_confirmation_template_id(product):
    confirmation_type = ProductEmailTemplateEnum.ORDER_CONFIRMATION.value
    return next(
        (
            template.template_id
            for template in product.email_templates
            if template.template_type == confirmation_type
        ),
        None,
    )
