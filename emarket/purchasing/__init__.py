__all__ = ["PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE",
           "PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE",
           "PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE"]

PURCHASE_MESSAGE_FOR_OWNER_TEMPLATE = "User {username} ({usermail}) ordered the {productname} for the price of {price}"
PURCHASE_MESSAGE_FOR_PURCHASER_TEMPLATE = """
    You ordered the {productname} for the price of {price}, if owner {username}({usermail}) will approve the purchase,
     he send mail for you
"""
PRODUCT_IS_OVER_WARNING_MESSAGE_TEMPLATE = """
    The product {productname} has ended, now it will NOT BE DISPLAYED to users, if you have new units of goods, 
    change the corresponding field (products count)
"""
