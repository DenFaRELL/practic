import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка изображения")
        self.image = None
        self.processed_image = None
    
        menu = tk.Menu(root)
        root.config(menu=menu)
    
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выбрать изображение", command=self.select_image)
    
        webcam_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Веб-камера", menu=webcam_menu)
        webcam_menu.add_command(label="Сделать фото", command=self.take_photo)
    
        channel_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Операции с изображением", menu=channel_menu)
        channel_menu.add_command(label="Изображение в красном канале", command=lambda: self.show_channel('red'))
        channel_menu.add_command(label="Изображение в зелёном канале", command=lambda: self.show_channel('green'))
        channel_menu.add_command(label="Изображение в синем канале", command=lambda: self.show_channel('blue'))
        channel_menu.add_command(label="Добавить границы к изображению", command=self.add_edges_to_image)
        channel_menu.add_command(label="Изображение в оттенках серого", command=self.convert_to_gray)
        channel_menu.add_command(label="Нарисовать линию на изображении зелёным цветом", command=self.draw_line_on_image)
    
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
    
    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.png;*.jpg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)
        
    def take_photo(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if ret:
            self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)
        else:
            messagebox.showerror("Ошибка", "Не удалось подключиться к веб-камере")
    
    def display_image(self, image):
        image = cv2.resize(image, (400, 400))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # конвертация в RGB цветовое пространство
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo
    
    def show_channel(self, channel):
        if self.image is not None:
            if channel == 'red':
                self.processed_image = self.image.copy()
                self.processed_image[:, :, 0] = 0
                self.processed_image[:, :, 1] = 0
            elif channel == 'green':
                self.processed_image = self.image.copy()
                self.processed_image[:, :, 0] = 0
                self.processed_image[:, :, 2] = 0
            elif channel == 'blue':
                self.processed_image = self.image.copy()
                self.processed_image[:, :, 1] = 0
                self.processed_image[:, :, 2] = 0
            self.display_image(self.processed_image)
        else:
            messagebox.showerror("Ошибка", "Сначала выберите изображение")
    
    def add_edges_to_image(self):
        if self.image is not None:
            def submit():
                try:
                    edge_size = int(entry.get())
                    self.processed_image = cv2.copyMakeBorder(self.image, edge_size, edge_size, edge_size, edge_size, cv2.BORDER_CONSTANT, value=(0, 0, 0))
                    self.display_image(self.processed_image)
                    top.destroy()  # закрытие диалогового окна после ввода
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректный ввод. Размер границ должен быть целым числом.")

            top = tk.Toplevel()
            top.title("Введите размер границ")
            label = tk.Label(top, text="Введите размер границ:")
            label.pack()
            entry = tk.Entry(top)
            entry.pack()
            button = tk.Button(top, text="Подтвердить", command=submit)
            button.pack()
        else:
            messagebox.showerror("Ошибка", "Сначала выберите изображение")

    def convert_to_gray(self):
        if self.image is not None:
            self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.display_image(self.processed_image)
        else:
            messagebox.showerror("Ошибка", "Сначала выберите изображение")
    
    def draw_line_on_image(self):
        if self.image is not None:
            def submit():
                try:
                    x1 = int(x1_entry.get())
                    y1 = int(y1_entry.get())
                    x2 = int(x2_entry.get())
                    y2 = int(y2_entry.get())
                    thickness = int(thickness_entry.get())
                    self.processed_image = self.image.copy()
                    cv2.line(self.processed_image, (x1, y1), (x2, y2), (0, 255, 0), thickness)
                    self.display_image(self.processed_image)
                    top.destroy()  # закрытие диалогового окна после ввода
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректный ввод. Координаты и толщина линии должны быть целыми числами.")

            top = tk.Toplevel()
            top.title("Введите координаты и толщину линии")
            x1_label = tk.Label(top, text="Введите x координату точки 1:")
            x1_label.pack()
            x1_entry = tk.Entry(top)
            x1_entry.pack()
            y1_label = tk.Label(top, text="Введите y координату точки 1:")
            y1_label.pack()
            y1_entry = tk.Entry(top)
            y1_entry.pack()
            x2_label = tk.Label(top, text="Введите x координату точки 2:")
            x2_label.pack()
            x2_entry = tk.Entry(top)
            x2_entry.pack()
            y2_label = tk.Label(top, text="Введите y координату точки 2:")
            y2_label.pack()
            y2_entry = tk.Entry(top)
            y2_entry.pack()
            thickness_label = tk.Label(top, text="Введите толщину линии:")
            thickness_label.pack()
            thickness_entry = tk.Entry(top)
            thickness_entry.pack()
            button = tk.Button(top, text="Подтвердить", command=submit)
            button.pack()
        else:
            messagebox.showerror("Ошибка", "Сначала выберите изображение")
    
root = tk.Tk()
app = ImageProcessingApp(root)
root.mainloop()
