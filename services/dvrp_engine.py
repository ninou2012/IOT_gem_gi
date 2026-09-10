import requests
import polyline
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

OSRM_TABLE_URL = "https://router.project-osrm.org/table/v1/driving"
OSRM_ROUTE_URL = "https://router.project-osrm.org/route/v1/driving"

def get_osrm_distance_matrix(locations):
    coord_string = ";".join([f"{lon},{lat}" for lat, lon in locations])
    url = f"{OSRM_TABLE_URL}/{coord_string}?annotations=distance"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return [[int(val) for val in row] for row in response.json()['distances']]
    except Exception:
        pass
    size = len(locations)
    return [[0 for _ in range(size)] for _ in range(size)]

def get_osrm_route_geometry(coord_start, coord_end):
    url = f"{OSRM_ROUTE_URL}/{coord_start[1]},{coord_start[0]};{coord_end[1]},{coord_end[0]}?overview=full"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            encoded_polyline = response.json()['routes'][0]['geometry']
            return polyline.decode(encoded_polyline)
    except Exception:
        pass
    return [coord_start, coord_end]

def run_optimization():
    depot_g7 = (48.8566, 2.3522)
    livraisons = [
        (48.8738, 2.2950), 
        (48.8340, 2.3800), 
        (48.8606, 2.3376)  
    ]
    all_locations = [depot_g7] + livraisons
    
    distance_matrix = get_osrm_distance_matrix(all_locations)
    
    data = {
        'distance_matrix': distance_matrix,
        'num_vehicles': 2,
        'depot': 0
    }

    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    
    solution = routing.SolveWithParameters(search_parameters)

    routes_path_geometry = []

    if solution:
        styles_urgence = {
            "Critique": [255, 0, 0, 200],     
            "Normal": [0, 0, 255, 200]       
        }
        
        styles_gabarit = {
            "Poids Lourd": 8,                  
            "Véhicule Léger": 4                
        }

        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            node_sequence = []
            while not routing.IsEnd(index):
                node_sequence.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            node_sequence.append(manager.IndexToNode(index))
            
            urgence = "Critique" if vehicle_id == 0 else "Normal"
            gabarit = "Poids Lourd" if vehicle_id == 0 else "Véhicule Léger"

            for i in range(len(node_sequence) - 1):
                start_pt = all_locations[node_sequence[i]]
                end_pt = all_locations[node_sequence[i+1]]
                
                if start_pt == end_pt and start_pt == depot_g7:
                    continue
                    
                detailed_path = get_osrm_route_geometry(start_pt, end_pt)
                pydeck_path = [[pt[1], pt[0]] for pt in detailed_path]
                
                routes_path_geometry.append({
                    "path": pydeck_path,
                    "color": styles_urgence[urgence],
                    "width": styles_gabarit[gabarit],
                    "tooltip_info": f"Camion {vehicle_id + 1} ({gabarit}) — Urgence: {urgence}"
                })
                
        return "✅ Calcul effectué avec succès", routes_path_geometry
    return "❌ Erreur d'optimisation", []
