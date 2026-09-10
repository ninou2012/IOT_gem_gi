import time

def run_optimization():
    """
    Exécute les calculs lourds de ré-optimisation des tournées.
    Simule un délai de traitement sans bloquer le rendu graphique de la carte.
    """
    # Simulation du temps de calcul de l'algorithme
    time.sleep(1.5) 
    
    # Retourne le nouvel état à injecter dans l'application
    return "✅ Routes optimisées avec succès"
