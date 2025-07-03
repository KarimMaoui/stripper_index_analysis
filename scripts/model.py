def is_profitable(oil_price, variable_cost):
    """
    Détermine si un puits stripper est rentable à un prix donné.
    
    Args:
        oil_price (float): Prix du baril de WTI (USD)
        variable_cost (float): Coût variable de production (USD)
        
    Returns:
        bool: True si rentable, False sinon
    """
    return oil_price >= variable_cost


def simulate_profitability_thresholds(price_range, cost_range):
    """
    Crée une matrice booléenne indiquant les combinaisons prix/coût rentables.
    
    Args:
        price_range (list): Liste de prix du WTI
        cost_range (list): Liste de coûts variables
        
    Returns:
        dict: Dictionnaire {coût : [True/False ...]} pour chaque prix
    """
    results = {}
    for cost in cost_range:
        results[cost] = [is_profitable(price, cost) for price in price_range]
    return results

