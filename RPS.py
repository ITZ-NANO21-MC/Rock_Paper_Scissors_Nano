import random
from collections import defaultdict, deque
import numpy as np

player_state = None  # Variable global para mantener el estado

def adaptive_player(prev_play, opponent_history=[], memory_length=10, pattern_lengths=[3, 4, 5], 
                   stats=None, loss_counter=0, last_strategy=None, strategy_history=None):
    
    # Inicialización de estructuras
    if stats is None:
        stats = {
            'pattern_counts': defaultdict(int),
            'move_counts': defaultdict(int),
            'history': deque(maxlen=memory_length)
        }
    
    if strategy_history is None:
        strategy_history = deque(maxlen=5)
    
    # Registrar jugada anterior
    if prev_play:
        opponent_history.append(prev_play)
        stats['history'].append(prev_play)
        stats['move_counts'][prev_play] += 1
    
    # Estrategias disponibles
    strategies = {
        'pattern_recognition': strategy_pattern_recognition,
        'frequency_analysis': strategy_frequency_analysis,
        'anti_pattern': strategy_anti_pattern,
        'randomized': strategy_randomized
    }
    
    # Cambiar estrategia después de 3 pérdidas
    if loss_counter >= 3:
        last_strategy = random.choice(list(strategies.keys()))
        loss_counter = 0
        strategy_history.append(last_strategy)
    
    # Rotación de estrategias si usamos la misma mucho tiempo
    if not last_strategy:
        last_strategy = 'frequency_analysis'
    elif len(strategy_history) >= 3 and len(set(strategy_history)) == 1:
        last_strategy = random.choice([s for s in strategies.keys() if s != last_strategy])
    
    # Obtener movimiento
    move = strategies[last_strategy](opponent_history, stats)
    
    # Variar jugadas si hay muchos empates
    if len(opponent_history) >= 2 and opponent_history[-1] == opponent_history[-2]:
        move = random.choice([m for m in ['R', 'P', 'S'] if m != move])
    
    # Aleatoriedad controlada si estamos perdiendo
    if loss_counter >= 1 and random.random() < min(0.3, loss_counter * 0.1):
        move = random.choice(['R', 'P', 'S'])
    
    return move, {
        'stats': stats,
        'loss_counter': loss_counter,
        'last_strategy': last_strategy,
        'strategy_history': strategy_history
    }


# Estrategia 1: Reconocimiento de patrones complejos
def strategy_pattern_recognition(opponent_history, stats):
    if len(opponent_history) < max(stats['pattern_lengths']):
        return random.choice(['R', 'P', 'S'])
    
    # Analizar múltiples longitudes de patrón
    predictions = []
    for length in stats['pattern_lengths']:
        if len(opponent_history) >= length:
            last_pattern = ''.join(opponent_history[-length:])
            # Buscar patrones similares en el historial
            similar_patterns = [p for p in stats['pattern_counts'] 
                              if p.startswith(last_pattern[:-1])]
            if similar_patterns:
                most_common = max(similar_patterns, key=lambda x: stats['pattern_counts'][x])
                predictions.append(most_common[-1])
    
    # Elegir la predicción más frecuente entre todos los patrones
    if predictions:
        predicted_move = max(set(predictions), key=predictions.count)
    else:
        predicted_move = random.choice(['R', 'P', 'S'])
    
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response.get(predicted_move, random.choice(['R', 'P', 'S']))

# Estrategia 2: Análisis de frecuencia
def strategy_frequency_analysis(opponent_history, stats):
    if not stats['move_counts']:
        return random.choice(['R', 'P', 'S'])
    
    # Movimiento más frecuente del oponente
    most_common_move = max(stats['move_counts'], key=stats['move_counts'].get)
    
    # Contrarrestar el movimiento más común
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[most_common_move]

# Estrategia 3: Anti-patrones
def strategy_anti_pattern(opponent_history, stats):
    if len(opponent_history) < 3:
        return random.choice(['R', 'P', 'S'])
    
    # Detectar si el oponente está contrarrestando nuestros movimientos
    last_move = opponent_history[-1]
    ideal_counter = {'P': 'S', 'R': 'P', 'S': 'R'}
    
    # Si el oponente está respondiendo a nuestros patrones
    if len(opponent_history) >= 4:
        our_last = opponent_history[-2]  # Simulando que responde a nosotros
        if ideal_counter.get(our_last, None) == last_move:
            # Jugamos el movimiento que vencería a su respuesta esperada
            return ideal_counter[last_move]
    
    return strategy_frequency_analysis(opponent_history, stats)

# Estrategia 4: Aleatoriedad controlada
def strategy_randomized(opponent_history, stats):
    # 70% de seguir estrategia base, 30% de aleatoriedad
    if random.random() < 0.7:
        return strategy_frequency_analysis(opponent_history, stats)
    return random.choice(['R', 'P', 'S'])

def player(prev_play, opponent_history=[]):
    global player_state
    
    # Llamar a nuestra función avanzada
    move, player_state = adaptive_player(
        prev_play,
        opponent_history,
        memory_length=10,
        pattern_lengths=[3, 4, 5],
        stats=player_state['stats'] if player_state else None,
        loss_counter=player_state['loss_counter'] if player_state else 0,
        last_strategy=player_state['last_strategy'] if player_state else None,
        strategy_history=player_state['strategy_history'] if player_state else deque(maxlen=5)
    )
    
    return move  # Solo devolver el movimiento, no el estado

# Para depuracion
def debug_player(prev_play, opponent_history=[]):
    global player_state
    print(f"Estado actual: {player_state}")
    move, player_state = adaptive_player(
        prev_play,
        opponent_history,
        memory_length=10,
        pattern_lengths=[3, 4, 5],
        stats=player_state['stats'] if player_state else None,
        loss_counter=player_state['loss_counter'] if player_state else 0,
        last_strategy=player_state['last_strategy'] if player_state else None,
        strategy_history=player_state['strategy_history'] if player_state else deque(maxlen=5)
    )
    print(f"Proximo movimiento: {move}")
    return move
