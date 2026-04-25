from . import external_module


def calculate_delivery(weight: int, distance: int):
    base_price = external_module.get_base_delivery_price()
    weight_price = weight * 10
    distance_price = distance * 5
    return base_price + weight_price + distance_price
