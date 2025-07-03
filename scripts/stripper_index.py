# scripts/stripper_index.py

def compute_stripper_index(oil_price, transport_cost, rig_count, differential, production_cost):
    """
    Indicateur synthétique simulant la rentabilité moyenne des stripper wells.

    Paramètres :
    - oil_price : prix spot WTI
    - transport_cost : coût estimé de transport ($/baril)
    - rig_count : nombre de rigs actifs
    - differential : spread WTI vs Brent ou WTI vs LLS
    - production_cost : coût variable moyen des stripper wells

    Retourne :
    - index_value : score (0 à 100) de stress sectoriel
    """

    net_margin = oil_price - transport_cost - production_cost + differential

    # pondération (empirique, modifiable)
    margin_score = max(min(net_margin / 30, 1), 0) * 50
    rig_score = max(min(rig_count / 600, 1), 0) * 30
    spread_score = max(min((differential + 5) / 10, 1), 0) * 20  # recentrer sur [-5 ; +5]

    index_value = margin_score + rig_score + spread_score
    return round(index_value, 1)
