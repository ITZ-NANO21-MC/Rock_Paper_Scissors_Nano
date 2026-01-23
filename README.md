# Rock-Paper-Scissors AI Player

## Descripción

Este proyecto implementa un jugador avanzado de Piedra, Papel o Tijeras (RPS) que utiliza múltiples estrategias adaptativas para competir contra diversos bots predefinidos. El jugador está diseñado para lograr una tasa de victoria superior al 60% contra cada uno de los oponentes del sistema.

## Características

- **Estrategias múltiples**: Implementa cuatro estrategias diferentes que se rotan dinámicamente
- **Reconocimiento de patrones**: Analiza secuencias de jugadas para predecir movimientos
- **Análisis de frecuencia**: Identifica y contrarresta los movimientos más comunes del oponente
- **Anti-patrones**: Detecta y responde a estrategias de contramovimiento
- **Aleatoriedad controlada**: Incorpora elementos aleatorios para evitar ser predecible

## Estructura del Proyecto

```

Rock_Paper_Scissors_Nano/
├── main.py          # Punto de entrada principal
├── RPS.py           # Implementación del jugador adaptativo
├── RPS_game.py      # Lógica del juego y bots predefinidos
└── test_module.py   # Pruebas unitarias
```

## Bots Implementados

El proyecto incluye varios bots con diferentes estrategias:

- **quincy**: Repite un patrón fijo de jugadas
- **abbey**: Analiza los dos últimos movimientos para predecir el siguiente
- **kris**: Siempre contrarresta el último movimiento del oponente
- **mrugesh**: Utiliza el movimiento más frecuente de los últimos 10 turnos
- **random_player**: Realiza movimientos completamente aleatorios

## Uso

### Ejecución Básica
```bash
python main.py
```

### Jugar contra un bot
```python
# En main.py, descomenta una de estas líneas:
play(human, abbey, 20, verbose=True)      # Jugar interactivamente
play(human, random_player, 1000)          # Jugar contra jugador aleatorio
```

### Ejecutar pruebas
```python
# En main.py, descomenta:
main(module='test_module', exit=False)
```

## Estrategias del Jugador

El jugador adaptativo utiliza las siguientes estrategias:

1. **Reconocimiento de Patrones**: Analiza secuencias de 3, 4 y 5 movimientos
2. **Análisis de Frecuencia**: Identifica el movimiento más común del oponente
3. **Anti-Patrones**: Detecta cuando el oponente está contrarrestando movimientos
4. **Aleatoriedad Controlada**: Introduce variabilidad para evitar ser predecible

## Resultados

El jugador está diseñado para alcanzar al menos un 60% de victorias contra cada bot:

- Quincy: ≥ 60%
- Abbey: ≥ 60%
- Kris: ≥ 60%
- Mrugesh: ≥ 60%

## Personalización

Los parámetros del jugador pueden ajustarse en `RPS.py`:

```python
# Modificar estos parámetros en adaptive_player()
memory_length=10        # Longitud de la memoria histórica
pattern_lengths=[3,4,5] # Longitudes de patrones a analizar
```

## Requisitos

- Python 3.6 o superior
- Módulos estándar de Python (collections, random, unittest, numpy)

## Nota

Desarrollado como parte de un proyecto de inteligencia artificial para el juego de Piedra, Papel o Tijeras.
