from matplotlib.figure import Figure
from nummethods import *

class Plot:

    def __init__(self, title):
        self.figure = Figure(dpi=70)
        self.figure.suptitle(title)

    def build_graph(self, x, y, method):
        graph_plane = self.figure.add_subplot(111)
        graph_plane.set_xlabel('x')
        graph_plane.set_ylabel('y')
        graph_plane.plot(x, y, label=method)
        graph_plane.legend(loc='upper right')

    def build_local_err_graph(self, x, y, method):
        graph_plane = self.figure.add_subplot(111)
        graph_plane.set_xlabel('x')
        graph_plane.set_ylabel('local error')
        graph_plane.plot(x, y, label=method)
        graph_plane.legend(loc='upper right')

    def build_error_graph(self, method, x, y):
        graph_plane = self.figure.add_subplot(111)
        graph_plane.set_xlabel('N')
        graph_plane.set_ylabel('Max. error')
        graph_plane.plot(x, y, label=method)
        graph_plane.legend(loc='upper right')

class ProblemSolver:
    """
    ProblemSolver() class is made to calculate solutions of DE using 4 methods:
        1) Exact
    and numerical methods:
        2) Euler
        3) Improved Euler
        4) Runge-Kutta
    Also here local and max local errors are calculated
    """
    def __init__(self, steps_amt, x0, y0, limit):
        self.x0 = x0
        self.y0 = y0
        self.limit = limit
        self.steps_amt = steps_amt
        self.solutions = {}
        self.errors = {}
        self.solve_equation()
        self.calculate_local_errs()

    def solve_equation(self):
        exact = Exact(self.steps_amt, self.x0, self.y0, self.limit)
        euler = Euler(self.steps_amt, self.x0, self.y0, self.limit)
        improved_euler = ImprovedEuler(self.steps_amt, self.x0, self.y0, self.limit)
        rk = RungeKutta(self.steps_amt, self.x0, self.y0, self.limit)

        self.solutions['exact'] = exact
        self.solutions['euler'] = euler
        self.solutions['improved_euler'] = improved_euler
        self.solutions['runge_kutta'] = rk

    def build_plot(self):
        plots = Plot('Graphs')

        plots.build_graph(self.solutions['exact'].x, self.solutions['exact'].y, 'Exact')
        plots.build_graph(self.solutions['euler'].x, self.solutions['euler'].y, 'Euler')
        plots.build_graph(self.solutions['improved_euler'].x, self.solutions['improved_euler'].y, 'Improved Euler')
        plots.build_graph(self.solutions['runge_kutta'].x, self.solutions['runge_kutta'].y, "Runge-Kutta")

        return plots

    def calculate_local_errs(self):
        exact = Error(self.solutions['exact'], self.solutions['exact']).error
        euler = Error(self.solutions['exact'], self.solutions['euler']).error
        improved_euler = Error(self.solutions['exact'], self.solutions['improved_euler']).error
        rk = Error(self.solutions['exact'], self.solutions['runge_kutta']).error

        self.errors['exact'] = exact
        self.errors['euler'] = euler
        self.errors['improved_euler'] = improved_euler
        self.errors['runge_kutta'] = rk

    def calculate_max_err(self, method):
        max_err = max(self.errors[method])

        return max_err

    def build_local_error_graph(self):
        plots = Plot('Local errors')

        x = self.solutions['exact'].x

        plots.build_local_err_graph(x, self.errors['euler'], 'Euler')
        plots.build_local_err_graph(x, self.errors['improved_euler'], 'Improved Euler')
        plots.build_local_err_graph(x, self.errors['runge_kutta'], 'Runge-Kutta')

        return plots


class ErrorAnalysis:
    def __init__(self, x0, y0, limit, N_from, N_to):
        if N_from < 1:
            raise ValueError("Values < 1 are not allowed!")
        self.x0 = x0
        self.y0 = y0
        self.limit = limit
        self.start = N_from
        self.N = []
        self.errors = {}
        for i in range(N_from, N_to + 1):
            self.N.append(i)

    def generate_error_array(self, method):
        self.errors[method] = []

        for i in self.N:
            error = ProblemSolver(i, self.x0, self.y0, self.limit).calculate_max_err(method)
            self.errors[method].append(error)

    def build_err_graph(self):
        plots = Plot('Max Error from N')

        plots.build_error_graph('Euler', self.N, self.errors['euler'])
        plots.build_error_graph('Improved Euler', self.N, self.errors['improved_euler'])
        plots.build_error_graph('Runge-Kutta', self.N, self.errors['runge_kutta'])

        return plots
