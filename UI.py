import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageColor

CELL_SIZE = 60
PIECE_RADIUS = 25
BOARD_SIZE = 8
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE

def create_smooth_circle(canvas, diameter, color):
    upscale = 4
    size = diameter * upscale
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Shadow
    shadow_offset = int(0.02 * size)
    shadow_color = (0, 0, 0, 100)
    draw.ellipse(
        (shadow_offset, shadow_offset, size - 1, size - 1),
        fill=shadow_color
    )

    # Main piece
    piece_color = color if isinstance(color, tuple) else ImageColor.getrgb(color)
    draw.ellipse((0, 0, size - shadow_offset*2, size - shadow_offset*2), fill=piece_color)

    # Downscale for anti-aliasing
    image = image.resize((diameter, diameter), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(image)
    canvas.images.append(tk_img)  # giữ tham chiếu
    return tk_img

def draw_board(canvas):
    for row in range(BOARD_SIZE - 1, -1, -1):
        for col in range(BOARD_SIZE):
            x1 = col * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, outline='black')

def update_ui(canvas, board):
    canvas.delete("piece")

    rotated = list(zip(*board))[::-1]
    board = [list(row) for row in rotated]   

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            cell = board[row][col]
            if cell == 1:  # Quân trắng
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                canvas.create_image(x, y, image=canvas.white_piece_img, tags="piece")
            elif cell == -1:  # Quân đen
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                canvas.create_image(x, y, image=canvas.black_piece_img, tags="piece")
            
def update_hint(canvas, hint):
    canvas.delete("hint")

    for x, y in hint:
        y = 7 - y
        x1 = x * CELL_SIZE + CELL_SIZE // 2
        y1 = y * CELL_SIZE + CELL_SIZE // 2
        canvas.create_oval(x1 - PIECE_RADIUS, y1 - PIECE_RADIUS, x1 + PIECE_RADIUS, y1 + PIECE_RADIUS, outline='yellow', tags="hint")

def setup_ui():
    # Tạo cửa sổ và canvas
    root = tk.Tk()
    root.title("Reversi Board")
    canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='#2cb87b')
    canvas.pack()
    canvas.images = []  # Để giữ ảnh không bị mất
    canvas.black_piece_img = create_smooth_circle(canvas, PIECE_RADIUS*2, "black")
    canvas.white_piece_img = create_smooth_circle(canvas, PIECE_RADIUS*2, "white")

    # Vẽ bàn cờ
    draw_board(canvas)
    
    return root, canvas
