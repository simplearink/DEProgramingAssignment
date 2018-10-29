from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plots import *
from tkinter import *


class DEApplication(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('900x800')  # Set Size of App Window
        self.resizable(width=False, height=False)
        self.winfo_toplevel().title("Differential Equation Solver")
        self.error_message = Label(self, text="error")

        equation = Label(self, text="Equation: y' = - y - x")
        equation.config(font=("Courier", 18))
        equation.place(x=40, y=70)

        #Fields

        Label(self, text="x0").grid(row=0, padx=80, pady=(150, 0))
        Label(self, text="y0").grid(row=1, padx=80)
        Label(self, text="X").grid(row=2, padx=80)
        Label(self, text="N").grid(row=3, padx=80)

        #Fields to enter values of x0, y0, X and N

        self.x0 = Entry(self, width=5)
        self.y0 = Entry(self, width=5)
        self.X = Entry(self, width=5)
        self.N = Entry(self, width=5)

        self.x0.grid(row=0, column=1, pady=(150, 0))
        self.y0.grid(row=1, column=1)
        self.X.grid(row=2, column=1)
        self.N.grid(row=3, column=1)
        button = Button(self, text="Build", command=self.build_graphs)
        button.grid(row=4, column=1, padx=(70, 70))

        Label(self, text="Solutions graph").place(x=550, y=100)
        Label(self, text="Local errors graph").place(x=550, y=550)
        Label(self, text="Error from N graph").place(x=100, y=550)

        #Labels and entries for ErrorAnalysis graph
        self.N_title = Label(self, text="Dependence of error from N")
        self.N_from_label = Label(self, text="From")
        self.N_from_entry = Entry(self, width=5)
        self.N_to_label = Label(self, text="To")
        self.N_to_entry = Entry(self, width=5)

        self.resize_button = Button(self, text="Resize", command=self.resize_handler)

    def build_graphs(self):
        try:
            solution = ProblemSolver(int(self.N.get()), float(self.x0.get()), float(self.y0.get()), float(self.X.get()))
            self.err_of_n(1, int(self.N.get()))
            self.error_message['text'] = ""
            self.N_title['text'] = "Dependence of error from N"
            self.N_from_entry.delete(0, 'end')
            self.N_from_entry.insert(END, 1)
            self.N_to_entry.delete(0, 'end')
            self.N_to_entry.insert(END, self.N.get())
            if (self.N_from_entry.get() and self.N_to_entry):
                pass
        except ValueError as e:
            self.error_message['text'] = "Invalid input. Try again!"
            self.error_message.place(x=80, y=245)

        plane1 = FigureCanvasTkAgg(solution.build_plot().figure, self)
        plane1.get_tk_widget().place(x=470, y=20)

        plane2 = FigureCanvasTkAgg(solution.build_local_error_graph().figure, self)
        plane2.get_tk_widget().place(x=470, y=370)

        self.N_title.place(x=125, y=320)

        self.N_from_label.place(x=73, y=340)
        self.N_from_entry.place(x=110, y=340)

        self.N_to_label.place(x=211,y=340)
        self.N_to_entry.place(x=230, y=340)

        self.resize_button.place(x=330, y=335)


    def err_of_n(self, n_from, n_to):
        errs = ErrorAnalysis(float(self.x0.get()), float(self.y0.get()), float(self.X.get()), n_from, n_to)

        errs.generate_error_array('exact')
        errs.generate_error_array('euler')
        errs.generate_error_array('improved_euler')
        errs.generate_error_array('runge_kutta')

        plane3 = FigureCanvasTkAgg(errs.build_err_graph().figure, self)
        plane3.get_tk_widget().place(x=0, y=370)

    def resize_handler(self):
        try:
            if self.N_from_entry.get() > self.N_to_entry.get():
                raise ValueError("From value > to value! Try again!")
            if self.N_to_entry.get() > self.N.get():
                raise ValueError("Not existing N. Try again!")
            self.err_of_n(int(self.N_from_entry.get()), int(self.N_to_entry.get()))
            self.N_title['text'] = "The resized graph"
        except ValueError as e:
            self.N_title['text'] = e.args[0]


if __name__ == '__main__':
    app = DEApplication()
    while True:
        try:
            app.mainloop()
        except UnicodeDecodeError:
            continue
