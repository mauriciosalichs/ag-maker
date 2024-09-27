import pygame
import tkinter as tk
from tkinter import filedialog

# Inicializar Pygame
pygame.init()

# Configurar la pantalla de Pygame
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Drag and Drop PNG")

# Colores
WHITE = (255, 255, 255)

# Variable para almacenar la imagen cargada
image = None
image_rect = None
image_path = ""


# Función para abrir el diálogo de selección de archivos
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    file_path = filedialog.askopenfilename(
        title="Select PNG file",
        filetypes=[("PNG files", "*.png")]
    )
    root.destroy()  # Destruir la ventana principal de Tkinter
    return file_path


# Bucle principal
running = True
dragging = False
offset_x, offset_y = 0, 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:  # Presiona 'O' para abrir el diálogo de selección de archivos
                image_path = open_file_dialog()
                if image_path:
                    image = pygame.image.load(image_path)
                    image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botón izquierdo del mouse
                if image_rect and image_rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = image_rect.x - event.pos[0]
                    offset_y = image_rect.y - event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Botón izquierdo del mouse
                dragging = False
                if image_rect:
                    print(f"Image path: {image_path}")
                    print(f"Image position: {image_rect.topleft}")

        if event.type == pygame.MOUSEMOTION:
            if dragging and image_rect:
                image_rect.x = event.pos[0] + offset_x
                image_rect.y = event.pos[1] + offset_y

    # Dibujar el fondo
    screen.fill(WHITE)

    # Dibujar la imagen
    if image:
        screen.blit(image, image_rect)

    pygame.display.flip()

# Salir de Pygame
pygame.quit()
