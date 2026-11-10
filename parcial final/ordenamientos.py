
import pygame
import random
import sys
import time
import math

pygame.init()

# =========================================================
# 1. CONFIGURACIÓN
# =========================================================

WIDTH, HEIGHT = 1200, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SORTLAB PRO | Cyber Algorithm System")

clock = pygame.time.Clock()

# Paleta cyberpunk
BG = (5, 10, 17)
PANEL = (11, 22, 32)
PANEL2 = (15, 31, 43)
BORDER = (25, 70, 75)

WHITE = (225, 245, 245)
GRAY = (115, 150, 155)
GREEN = (50, 255, 140)
CYAN = (0, 225, 255)
PURPLE = (175, 80, 255)
RED = (255, 65, 95)
ORANGE = (255, 175, 50)
DARK_GREEN = (15, 75, 55)

font_title = pygame.font.SysFont("consolas", 34, bold=True)
font_subtitle = pygame.font.SysFont("consolas", 14)
font_normal = pygame.font.SysFont("consolas", 17)
font_small = pygame.font.SysFont("consolas", 12)
font_number = pygame.font.SysFont("consolas", 17, bold=True)
font_big = pygame.font.SysFont("consolas", 26, bold=True)

# =========================================================
# 2. VARIABLES
# =========================================================

original = random.sample(range(10, 100), 10)
current = original.copy()

frames = []
frame_index = 0

running_animation = False
paused = False

algorithm = "SYSTEM READY"
status = "Esperando instrucciones..."

comparisons = 0
swaps = 0
iterations = 0
passes = 0

start_time = 0
elapsed_time = 0

speed = 260
last_frame = 0

compare_mode = False
compare_phase = 0

results = {
    "Burbuja": {"comparisons": 0, "iterations": 0, "swaps": 0},
    "Seleccion": {"comparisons": 0, "iterations": 0, "swaps": 0}
}

# =========================================================
# 3. FUNCIONES DE DIBUJO
# =========================================================

def draw_text(text, font, color, x, y):
    image = font.render(str(text), True, color)
    screen.blit(image, (x, y))


def panel(x, y, w, h, color=PANEL):
    rect = pygame.Rect(x, y, w, h)

    pygame.draw.rect(
        screen, color, rect, border_radius=12
    )

    pygame.draw.rect(
        screen, BORDER, rect, 1, border_radius=12
    )


def glow_circle(x, y, radius, color):
    # Anillos exteriores para dar efecto neón
    for extra, alpha_color in [(9, 35), (5, 65)]:
        glow = tuple(min(255, int(c * alpha_color / 100))
                     for c in color)
        pygame.draw.circle(screen, glow, (x, y), radius + extra, 2)

    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, WHITE, (x, y), radius, 1)


def draw_background():
    screen.fill(BG)

    # Rejilla digital
    for x in range(0, WIDTH, 40):
        pygame.draw.line(
            screen, (10, 25, 31),
            (x, 0), (x, HEIGHT), 1
        )

    for y in range(0, HEIGHT, 40):
        pygame.draw.line(
            screen, (10, 25, 31),
            (0, y), (WIDTH, y), 1
        )

    # Líneas decorativas
    pygame.draw.line(screen, GREEN, (0, 120), (WIDTH, 120), 1)
    pygame.draw.line(screen, CYAN, (30, 122), (250, 122), 2)


def draw_button(x, y, w, h, label, color, enabled=True):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)

    active = enabled and rect.collidepoint(mouse)

    if not enabled:
        fill = (30, 42, 48)
        border = (55, 70, 75)
        text_color = GRAY
    elif active:
        fill = color
        border = WHITE
        text_color = BG
    else:
        fill = PANEL2
        border = color
        text_color = color

    pygame.draw.rect(screen, fill, rect, border_radius=8)
    pygame.draw.rect(screen, border, rect, 2, border_radius=8)

    image = font_small.render(label, True, text_color)
    screen.blit(
        image,
        (
            x + (w - image.get_width()) // 2,
            y + (h - image.get_height()) // 2
        )
    )

    return rect


def draw_stat(x, y, title, value, color):
    panel(x, y, 260, 75, PANEL2)

    pygame.draw.rect(
        screen, color,
        (x, y + 8, 4, 59),
        border_radius=2
    )

    draw_text(title, font_small, GRAY, x + 17, y + 12)
    draw_text(value, font_big, color, x + 17, y + 34)


# =========================================================
# 4. ALGORITMO BURBUJA
# =========================================================

def bubble_sort(data):
    arr = data.copy()
    steps = []

    comparisons_count = 0
    swaps_count = 0
    iterations_count = 0
    passes_count = 0

    n = len(arr)

    for i in range(n - 1):
        passes_count += 1
        changed = False

        for j in range(n - i - 1):
            iterations_count += 1
            comparisons_count += 1

            steps.append((
                arr.copy(),
                [j, j + 1],
                comparisons_count,
                swaps_count,
                iterations_count,
                passes_count,
                "COMPARE",
                list(range(n - i, n))
            ))

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps_count += 1
                changed = True

                steps.append((
                    arr.copy(),
                    [j, j + 1],
                    comparisons_count,
                    swaps_count,
                    iterations_count,
                    passes_count,
                    "SWAP",
                    list(range(n - i, n))
                ))

        steps.append((
            arr.copy(),
            [],
            comparisons_count,
            swaps_count,
            iterations_count,
            passes_count,
            "PASS",
            list(range(n - i - 1, n))
        ))

        if not changed:
            break

    steps.append((
        arr.copy(),
        [],
        comparisons_count,
        swaps_count,
        iterations_count,
        passes_count,
        "DONE",
        list(range(n))
    ))

    return steps


# =========================================================
# 5. ALGORITMO SELECCIÓN
# =========================================================

def selection_sort(data):
    arr = data.copy()
    steps = []

    comparisons_count = 0
    swaps_count = 0
    iterations_count = 0
    passes_count = 0

    n = len(arr)

    for i in range(n - 1):
        passes_count += 1
        minimum = i

        for j in range(i + 1, n):
            iterations_count += 1
            comparisons_count += 1

            steps.append((
                arr.copy(),
                [minimum, j],
                comparisons_count,
                swaps_count,
                iterations_count,
                passes_count,
                "COMPARE",
                list(range(i))
            ))

            if arr[j] < arr[minimum]:
                minimum = j

        if minimum != i:
            arr[i], arr[minimum] = arr[minimum], arr[i]
            swaps_count += 1

            steps.append((
                arr.copy(),
                [i, minimum],
                comparisons_count,
                swaps_count,
                iterations_count,
                passes_count,
                "SWAP",
                list(range(i))
            ))

        steps.append((
            arr.copy(),
            [],
            comparisons_count,
            swaps_count,
            iterations_count,
            passes_count,
            "PASS",
            list(range(i + 1))
        ))

    steps.append((
        arr.copy(),
        [],
        comparisons_count,
        swaps_count,
        iterations_count,
        passes_count,
        "DONE",
        list(range(n))
    ))

    return steps


# =========================================================
# 6. INICIAR Y CONTROLAR ALGORITMOS
# =========================================================

def start_algorithm(name):
    global frames, frame_index, running_animation, paused
    global algorithm, status, current
    global comparisons, swaps, iterations, passes
    global start_time, elapsed_time, last_frame

    if name == "Burbuja":
        frames = bubble_sort(original)
    else:
        frames = selection_sort(original)

    frame_index = 0
    running_animation = True
    paused = False

    algorithm = name.upper()
    status = "Ejecutando proceso..."

    current = original.copy()

    comparisons = 0
    swaps = 0
    iterations = 0
    passes = 0

    elapsed_time = 0
    start_time = time.perf_counter()
    last_frame = pygame.time.get_ticks()


def new_list():
    global original, current, running_animation
    global paused, compare_mode, status
    global comparisons, swaps, iterations, passes

    original = random.sample(range(10, 100), 10)
    current = original.copy()

    running_animation = False
    paused = False
    compare_mode = False

    comparisons = 0
    swaps = 0
    iterations = 0
    passes = 0

    status = "Nueva secuencia generada."

    results["Burbuja"] = {
        "comparisons": 0, "iterations": 0, "swaps": 0
    }
    results["Seleccion"] = {
        "comparisons": 0, "iterations": 0, "swaps": 0
    }


def reset():
    global current, running_animation, paused
    global compare_mode, status
    global comparisons, swaps, iterations, passes

    current = original.copy()

    running_animation = False
    paused = False
    compare_mode = False

    comparisons = 0
    swaps = 0
    iterations = 0
    passes = 0

    status = "Sistema reiniciado."


def start_comparison():
    global compare_mode, compare_phase, status

    compare_mode = True
    compare_phase = 1

    results["Burbuja"] = {
        "comparisons": 0, "iterations": 0, "swaps": 0
    }
    results["Seleccion"] = {
        "comparisons": 0, "iterations": 0, "swaps": 0
    }

    start_algorithm("Burbuja")
    status = "COMPARACIÓN: ejecutando Burbuja."


# =========================================================
# 7. PANEL DE BURBUJAS
# =========================================================

def draw_visualizer():
    panel(30, 140, 820, 420)

    draw_text(
        "LIVE SORTING VISUALIZER",
        font_normal, GREEN, 55, 160
    )

    draw_text(
        "10 DATA NODES // REAL-TIME PROCESSING",
        font_small, GRAY, 55, 188
    )

    # Estado de la acción
    if running_animation and frame_index > 0:
        action = frames[min(frame_index - 1, len(frames) - 1)][6]
    else:
        action = "STANDBY"

    action_colors = {
        "COMPARE": PURPLE,
        "SWAP": RED,
        "PASS": ORANGE,
        "DONE": GREEN,
        "STANDBY": CYAN
    }

    action_color = action_colors.get(action, CYAN)

    pygame.draw.rect(
        screen, PANEL2,
        (620, 158, 195, 38),
        border_radius=7
    )

    pygame.draw.rect(
        screen, action_color,
        (620, 158, 195, 38),
        1, border_radius=7
    )

    draw_text(
        "ACTION: " + action,
        font_small, action_color, 632, 170
    )

    # Línea de conexión entre nodos
    positions = []

    for i in range(10):
        x = 75 + i * 79
        y = 355
        positions.append((x, y))

    for i in range(9):
        pygame.draw.line(
            screen, (20, 90, 90),
            positions[i], positions[i + 1], 2
        )

    # Índices activos y posiciones ordenadas
    active = []
    fixed = []

    if running_animation and frame_index > 0:
        data = frames[min(frame_index - 1, len(frames) - 1)]
        active = data[1]
        fixed = data[7]

    elif not running_animation and current == sorted(original):
        fixed = list(range(10))

    for i, value in enumerate(current):
        x, y = positions[i]

        if i in active:
            if action == "SWAP":
                color = RED
            else:
                color = PURPLE
        elif i in fixed:
            color = GREEN
        else:
            color = CYAN

        # Efecto de brillo
        glow_circle(x, y, 26, color)

        # Número
        number = font_number.render(str(value), True, WHITE)
        screen.blit(
            number,
            (
                x - number.get_width() // 2,
                y - number.get_height() // 2
            )
        )

        draw_text(
            f"N{i + 1:02}",
            font_small, GRAY, x - 14, 398
        )

    # Barra de progreso
    pygame.draw.rect(
        screen, (25, 45, 50),
        (60, 465, 760, 9),
        border_radius=5
    )

    if running_animation and len(frames) > 0:
        progress = frame_index / len(frames)
    elif current == sorted(original):
        progress = 1
    else:
        progress = 0

    pygame.draw.rect(
        screen, GREEN,
        (60, 465, int(760 * progress), 9),
        border_radius=5
    )

    draw_text(
        f"PROGRESS: {int(progress * 100)}%",
        font_small, GREEN, 60, 485
    )

    draw_text(
        "INPUT: " + str(original),
        font_small, GRAY, 60, 520
    )


# =========================================================
# 8. PANEL DE ESTADÍSTICAS
# =========================================================

def draw_dashboard():
    panel(870, 140, 300, 420)

    draw_text(
        "SYSTEM METRICS",
        font_normal, CYAN, 895, 160
    )

    draw_text(
        "PERFORMANCE MONITOR",
        font_small, GRAY, 895, 188
    )

    draw_stat(890, 220, "COMPARACIONES", comparisons, PURPLE)
    draw_stat(890, 305, "INTERCAMBIOS", swaps, RED)
    draw_stat(890, 390, "ITERACIONES", iterations, ORANGE)

    if running_animation and not paused:
        shown_time = time.perf_counter() - start_time
    else:
        shown_time = elapsed_time

    panel(890, 475, 260, 65, PANEL2)

    draw_text("EXECUTION TIME", font_small, GRAY, 907, 484)
    draw_text(
        f"{shown_time:.3f} SEC",
        font_big, GREEN, 907, 506
    )


# =========================================================
# 9. LEYENDA DINÁMICA DE COLORES
# =========================================================

def draw_color_system():
    panel(30, 580, 1140, 85)

    draw_text(
        "COLOR SYSTEM // ACTION IDENTIFICATION",
        font_normal, GREEN, 55, 594
    )

    items = [
        ("IDLE / NORMAL", CYAN),
        ("COMPARISON", PURPLE),
        ("SWAP", RED),
        ("SORTED", GREEN),
        ("ITERATION", ORANGE)
    ]

    x_positions = [65, 285, 505, 725, 945]

    for (label, color), x in zip(items, x_positions):
        pygame.draw.rect(
            screen, color,
            (x, 630, 13, 13),
            border_radius=3
        )

        draw_text(
            label,
            font_small,
            WHITE,
            x + 22,
            630
        )


# =========================================================
# 10. CONTROLES
# =========================================================

def draw_controls():
    panel(30, 680, 1140, 95)

    draw_text(
        "CONTROL CENTER",
        font_normal, GREEN, 55, 695
    )

    enabled = not running_animation

    buttons = {}

    buttons["bubble"] = draw_button(
        55, 720, 145, 38,
        "01 // BUBBLE",
        CYAN, enabled
    )

    buttons["selection"] = draw_button(
        215, 720, 145, 38,
        "02 // SELECT",
        PURPLE, enabled
    )

    buttons["compare"] = draw_button(
        375, 720, 155, 38,
        "VS // COMPARE",
        GREEN, enabled
    )

    buttons["pause"] = draw_button(
        545, 720, 125, 38,
        "RESUME" if paused else "PAUSE",
        ORANGE, running_animation
    )

    buttons["new"] = draw_button(
        685, 720, 145, 38,
        "NEW DATA",
        CYAN, enabled
    )

    buttons["reset"] = draw_button(
        845, 720, 145, 38,
        "RESET",
        RED, enabled
    )

    buttons["faster"] = draw_button(
        1005, 720, 65, 38,
        "+ SPEED",
        GREEN, True
    )

    buttons["slower"] = draw_button(
        1080, 720, 65, 38,
        "- SPEED",
        ORANGE, True
    )

    return buttons


# =========================================================
# 11. COMPARACIÓN FINAL
# =========================================================

def finish_algorithm():
    global running_animation, elapsed_time
    global status, compare_mode

    running_animation = False
    elapsed_time = time.perf_counter() - start_time

    results[algorithm.title()] = {
        "comparisons": comparisons,
        "iterations": iterations,
        "swaps": swaps
    }

    status = f"{algorithm} COMPLETADO."

    if compare_mode:
        global compare_phase

        if compare_phase == 1:
            compare_phase = 2
            start_algorithm("Seleccion")
            status = "COMPARACIÓN: ejecutando Selección."

        else:
            compare_mode = False

            b = results["Burbuja"]["iterations"]
            s = results["Seleccion"]["iterations"]

            if b < s:
                winner = "BURBUJA"
            elif s < b:
                winner = "SELECCIÓN"
            else:
                winner = "EMPATE"

            status = f"RESULTADO FINAL: {winner}."

            print("\n========== RESULTADOS SORTLAB PRO ==========")
            print("Burbuja:", results["Burbuja"])
            print("Selección:", results["Seleccion"])
            print("Menos iteraciones:", winner)
            print("============================================\n")


# =========================================================
# 12. PANEL DE RESULTADOS
# =========================================================

def draw_footer():
    draw_text(
        "SORTLAB PRO  //  CYBER ALGORITHM SYSTEM",
        font_small, GRAY, 35, 785
    )

    draw_text(
        "STATUS: " + status,
        font_small, GREEN, 650, 785
    )


# =========================================================
# 13. BUCLE PRINCIPAL
# =========================================================

active_app = True

while active_app:

    clock.tick(60)

    draw_background()

    # Encabezado
    panel(30, 20, 1140, 90)

    draw_text(
        "SORTLAB",
        font_title, GREEN, 55, 32
    )

    draw_text(
        "PRO",
        font_title, CYAN, 245, 32
    )

    draw_text(
        "CYBER ALGORITHM VISUALIZER",
        font_small, GRAY, 58, 78
    )

    draw_text(
        "SYSTEM ONLINE  //  PYTHON ENGINE",
        font_small, GREEN, 800, 48
    )

    pygame.draw.circle(screen, GREEN, (1130, 63), 7)

    draw_visualizer()
    draw_dashboard()
    draw_color_system()

    buttons = draw_controls()
    draw_footer()

    # Eventos
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            active_app = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if buttons["bubble"].collidepoint(event.pos) and not running_animation:
                compare_mode = False
                start_algorithm("Burbuja")

            elif buttons["selection"].collidepoint(event.pos) and not running_animation:
                compare_mode = False
                start_algorithm("Seleccion")

            elif buttons["compare"].collidepoint(event.pos) and not running_animation:
                start_comparison()

            elif buttons["pause"].collidepoint(event.pos) and running_animation:
                paused = not paused

            elif buttons["new"].collidepoint(event.pos) and not running_animation:
                new_list()

            elif buttons["reset"].collidepoint(event.pos) and not running_animation:
                reset()

            elif buttons["faster"].collidepoint(event.pos):
                speed = max(40, speed - 40)

            elif buttons["slower"].collidepoint(event.pos):
                speed = min(1000, speed + 40)

    # Actualización de animación
    now = pygame.time.get_ticks()

    if running_animation and not paused:

        if now - last_frame >= speed:

            last_frame = now

            if frame_index < len(frames):

                (
                    current,
                    active_indices,
                    comparisons,
                    swaps,
                    iterations,
                    passes,
                    action,
                    fixed_indices
                ) = frames[frame_index]

                frame_index += 1

            else:
                finish_algorithm()

    pygame.display.flip()


pygame.quit()
sys.exit()
