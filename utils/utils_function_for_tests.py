def calculate_discount(order_total: float) -> float:
    """Рассчитать скидку на основе суммы заказа"""
    # Проблема: нет тестов, непонятно, работает ли правильно
    if order_total >= 10000:
        return order_total * 0.15  # 15% скидка
    elif order_total >= 5000:
        return order_total * 0.10  # 10% скидка
    elif order_total >= 1000:
        return order_total * 0.05  # 5% скидка
    else:
        return 0  # Нет скидки
