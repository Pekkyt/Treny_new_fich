def calculate_delivery(weight: int, distance: int):
    base_price = 100
    weight_price = weight * 10
    distance_price = distance * 5
    return base_price + weight_price + distance_price
