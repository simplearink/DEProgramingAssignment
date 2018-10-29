import math


class Grid():
    def __init__(self, steps_amt, x0, y0, limit):
        self.x = [x0]
        self.y = [y0]
        self.delta = (limit - x0)/steps_amt
        self.steps_amt = steps_amt
        self.fill_x()

    def fill_x(self):
        """
        Method that fills x array from x0 to X with delta step
        """
        for i in range(1, self.steps_amt):
            self.x.append(self.x[i-1]+self.delta)

    def solution(self):
        """
        Method that solves DE

        """
        pass


class Exact(Grid):
    def __init__(self, steps_amt, x0, y0, limit):
        Grid.__init__(self, steps_amt, x0, y0, limit)
        self.const = 0
        self.solution()

    def calculate_const(self):
        """
        Method that calculates constant depending on IVP

        """
        self.const = (self.y[0] + self.x[0] - 1)*math.exp(-self.x[0])

    def solution(self):
        self.calculate_const()
        for i in range(1, len(self.x)):
            self.y.append(1 - self.x[i] + self.const*math.exp(-self.x[i])) #general sol is y = 1 - x + C/e^x


class Euler(Grid):
    def __init__(self, steps_amt, x0, y0, limit):
        Grid.__init__(self, steps_amt, x0, y0, limit)
        self.solution()

    def func(self, x, y):
        """
        Method that calculates value of right side of equation
        :param x: x value
        :param y: y value
        :return: value of right side of equation
        """
        f = -y - x
        return f

    def solution(self):
        for i in range(1, len(self.x)):
            f = self.func(self.x[i-1], self.y[i-1])
            self.y.append(self.y[i-1] + self.delta*f)


class ImprovedEuler(Euler):
    def __init__(self, steps_amt, x0, y0, limit):
        Euler.__init__(self, steps_amt, x0, y0, limit)

    def solution(self):
        for i in range(1, len(self.x)):
            f = self.func(self.x[i-1] + self.delta/2, self.y[i-1] + self.delta*self.func(self.x[i-1], self.y[i-1])/2)
            self.y.append(self.y[i-1] + self.delta*f)


class RungeKutta(Euler):
    def __init__(self, steps_amt, x0, y0, limit):
        Euler.__init__(self, steps_amt, x0, y0, limit)

    def solution(self):
        for i in range(1, len(self.x)):
            k1 = self.func(self.x[i-1], self.y[i-1])
            k2 = self.func(self.x[i-1] + self.delta/2, self.y[i-1] + self.delta*k1/2)
            k3 = self.func(self.x[i-1] + self.delta/2, self.y[i-1] + self.delta*k2/2)
            k4 = self.func(self.x[i-1] + self.delta, self.y[i-1] + self.delta*k3)

            delta_y = self.delta/6 * (k1+2*k2+2*k3+k4)

            self.y.append(self.y[i-1]+delta_y)


class Error:
    def __init__(self, target, object):
        self.target = target
        self.object = object
        self.error = []
        self.calculate_error()

    def calculate_error(self):
        """
        Method that calculates error
        """
        for i in range(len(self.target.y)):
            self.error.append(abs(self.object.y[i] - self.target.y[i]))