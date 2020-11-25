import main as ln
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

from tkinter import ttk
import pylab
from PIL import ImageTk, Image

# import main as mn


class RungeKuttaGUI:
    def __init__(self, window):
        self.window = window
        self.fig, self.graph_axes = pylab.subplots()
        self.fig.subplots_adjust(left=0.07, right=0.95, top=0.95, bottom=0.2)
        self.graph_axes.grid()

    def run(self):
        self.window.title("Задание №11")
        self.window.geometry("700x700")
        self.mount_components()

    def mount_components(self):
        self.button = ttk.Button(master=self.window, command=self.on_click)
        self.button.configure(text="График")
        self.button.place(x=50, y=0)

        self.button1 = ttk.Button(master=self.window, command=self.table)
        self.button1.configure(text="Таблица")
        self.button1.place(x=150, y=0)

        self.button1 = ttk.Button(master=self.window, command=self.description)
        self.button1.configure(text="Условия задачи")
        self.button1.place(x=250, y=0)

        self.error_control = BooleanVar()
        self.error_control.set(0)
        self.error_checkbutton = Checkbutton(
            tk, text=" - Контроль локальной погрешности", variable=self.error_control, onvalue=True, offvalue=False
        )
        self.error_checkbutton.place(x=50, y=30)

        self.x0_label = ttk.Label(self.window)
        self.x0_label.configure(text="x0")
        # self.x0_label.pack()
        self.x0_label.place(x=400, y=25)

        self.x0_entry = ttk.Entry(self.window, width=10)
        self.x0_entry.insert(END, 0)
        self.x0_entry.place(x=400, y=50)
        # self.x0_entry.pack()

        self.y0_label = ttk.Label(self.window)
        self.y0_label.configure(text="y0")
        self.y0_label.place(x=400, y=75)

        self.y0_entry = ttk.Entry(self.window, width=10)
        self.y0_entry.insert(END, 1)
        self.y0_entry.place(x=400, y=100)

        self.h_label = ttk.Label(self.window)
        self.h_label.configure(text="Шаг (h):")
        self.h_label.place(x=400, y=125)

        self.h_entry = ttk.Entry(self.window, width=10)
        self.h_entry.insert(END, 0.1)
        self.h_entry.place(x=400, y=150)

        self.x_label = ttk.Label(self.window)
        self.x_label.configure(text="x")
        self.x_label.place(x=400, y=175)

        self.x_entry = ttk.Entry(self.window, width=10)
        self.x_entry.insert(END, 1)
        self.x_entry.place(x=400, y=200)

        self.error_label = ttk.Label(self.window)
        self.error_label.configure(text="Макс. погрешность")
        self.error_label.place(x=50, y=55)

        self.error_entry = ttk.Entry(self.window)
        self.error_entry.insert(END, 0)
        self.error_entry.place(x=50, y=80)

        self.iter_num_label = ttk.Label(self.window)
        self.iter_num_label.configure(text="Число шагов: ")
        self.iter_num_label.place(x=50, y=115)

        self.iter_num_entry = ttk.Entry(self.window)
        self.iter_num_entry.insert(END, 0)
        self.iter_num_entry.place(x=50, y=140)

        self.right_limit_label = ttk.Label(self.window)
        self.right_limit_label.configure(text="Предел отрезка интегрирования: ")
        self.right_limit_label.place(x=50, y=175)

        self.right_limit_entry = ttk.Entry(self.window)
        self.right_limit_entry.insert(END, 0)
        self.right_limit_entry.place(x=50, y=200)

        self.k_label = ttk.Label(self.window)
        self.k_label.configure(text="k")
        self.k_label.place(x=550, y=25)

        self.k_default = StringVar()
        self.k_default.set("175")
        self.k_entry = ttk.Entry(self.window, width=10, textvariable=self.k_default)
        self.k_entry.insert(END, 1)
        self.k_entry.place(x=550, y=50)

        self.f_label = ttk.Label(self.window)
        self.f_label.configure(text="f")
        self.f_label.place(x=550, y=75)

        self.f_default = StringVar()
        self.f_default.set("0.3")
        self.f_entry = ttk.Entry(self.window, width=10, textvariable=self.f_default)
        self.f_entry.insert(END, 1)
        self.f_entry.place(x=550, y=100)

        self.m_label = ttk.Label(self.window)
        self.m_label.configure(text="m")
        self.m_label.place(x=550, y=125)

        self.m_default = StringVar()
        self.m_default.set("0.045")
        self.m_entry = ttk.Entry(self.window, width=10, textvariable=self.m_default)
        self.m_entry.insert(END, 1)
        self.m_entry.place(x=550, y=150)

    def on_click(self):
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x = float(self.x_entry.get())
        e = float(self.error_entry.get())
        h = float(self.h_entry.get())
        k = float(self.k_entry.get())
        m = float(self.m_entry.get())
        f = float(self.f_entry.get())
        iter_num = int(self.iter_num_entry.get())
        right_limit = float(self.right_limit_entry.get())

        x_values, y1_values, _, _, _, _, _, y2_values, _ = ln.num_sol_3_task(
            k, f, m, iter_num, ln.f_1, ln.f_2, x0, y0, y0, x, h, e, True
        )

        self.draw(x_values, y1_values)
        self.draw(x_values, y2_values)

    def draw(self, x_values, y_values, clear=False):
        if clear:
            self.graph_axes.clear()
        self.graph_axes.plot(x_values, y_values)
        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=0, y=250)

    def table(self):
        x0 = int(self.x0_entry.get())
        y0 = int(self.y0_entry.get())
        x = float(self.x_entry.get())
        h = float(self.h_entry.get())
        e = float(self.error_entry.get())
        k = float(self.k_entry.get())
        m = float(self.m_entry.get())
        f = float(self.f_entry.get())
        iter_num = int(self.iter_num_entry.get())
        right_limit = float(self.right_limit_entry.get())

        x_values, y1_values, _, errors, H, c1, c2, y2_values, _ = ln.num_sol_3_task(
            k, f, m, iter_num, ln.f_1, ln.f_2, x0, y0, y0, x, h, e, self.error_control.get()
        )

        diff = list(map(lambda x: x[0] - x[1], zip(y1_values, y2_values)))

        values = [
            x_values,
            y1_values,
            y2_values,
            diff,
            errors,
            [max(errors)] * len(errors),
            c1,
            c2,
            H
        ]

        headers = ["x", "v", "v2", "v-v2", "LE", "max LE", "c1", "c2", "H"]

        values_and_headers = [[headers[i]] + x for i, x in enumerate(values)]

        total_rows = len(values_and_headers)
        total_columns = len(values_and_headers[0])

        self.table_root = Tk()
        self.canvas_table = Canvas(self.table_root, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas_table, background="#ffffff")
        self.scrollbar = Scrollbar(
            self.table_root, orient="vertical", command=self.canvas_table.yview
        )
        self.canvas_table.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_table.pack(side="left", fill="both", expand=True)
        self.canvas_table.create_window((8, 8), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", self.on_frame_configure)

        self.table = Table(
            self.table_root, self.frame, values_and_headers, total_rows, total_columns
        )

    def description(self):
        self.description_root = Tk()
        self.description_canvas = Canvas(self.description_root, width=694, height=475)      
        self.img = ImageTk.PhotoImage(Image.open("description.png"), master=self.description_root)
        self.description_canvas.create_image(20, 20, anchor=NW, image=self.img) 
        self.description_canvas.pack()
        mainloop()

    def on_frame_configure(self, event):
        self.canvas_table.configure(scrollregion=self.canvas_table.bbox("all"))
        self.canvas_table.pack()


class Table:
    def __init__(self, root, frame, lst, total_rows, total_columns):

        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(frame, width=20, fg="black", font=("Arial", 12))

                self.e.grid(row=j, column=i)
                self.e.insert(END, lst[i][j])


if __name__ == "__main__":
    tk = Tk()
    style = ttk.Style(tk)
    style.configure('Test.TLabel', background='white')
    app = RungeKuttaGUI(window=tk)
    app.run()
    tk.mainloop()
