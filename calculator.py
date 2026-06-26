import matplotlib.pyplot as plt
import numpy as np

import math

class History:
    def __init__(self):
        self._history = []
    
    def add_records(self, category, operation, result):
        self._history.append({"category": category, "operation": operation, "result": result})
    
    def show(self):
        if not self._history:
            print("История пуста.")
            return

        def to_matrix_stack(matrix_obj):
            """Внутренний метод: превращает список списков в красивый столбик"""
            if isinstance(matrix_obj, list) and len(matrix_obj) > 0 and isinstance(matrix_obj[0], list):
                return "\n" + "\n".join(f"  {row}" for row in matrix_obj)
            return str(matrix_obj)

        for record in self._history:
            cat = record["category"]
            op = record["operation"]
            res = record["result"]

            if cat == "Матрицы":
                # Если операция содержит списки, мы можем их красиво пересобрать,
                # либо просто отдельно отформатировать результат в столбик:
                res_pretty = to_matrix_stack(res)
                
                # Выводим операцию, а результат переносим на новую строку в виде столбика
                print(f"[{cat}] {op} = {res_pretty}")
                print("-" * 40)
            else:
                # Для всех остальных калькуляторов вывод стандартный
                print(f"[{cat}] {op} = {res}")


    
    def clear(self):
        """Очищает список истории"""
        self._history.clear()  # Метод .clear() полностью опустошает список


class BasedCalculator:
    def __init__(self, history):
        self._history = history
    
    def AddOperation (self, a, b):
        result = a + b
        self._history.add_records(category = "Арифметика", operation = f"{a} + {b} ", result = result)
        return result 
    
    def SubOperation(self, a, b):
        result = a - b
        self._history.add_records(category = "Арифметика", operation = f"{a} - {b}", result = result)
        return result
    
    def MulOperation(self, a, b):
        result = a * b
        self._history.add_records(category = "Арифметика", operation = f"{a} * {b}", result = result)
        return result
    
    def DivOperation(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль невозможно!")
        result = a / b
        self._history.add_records(category = "Арифметика", operation = f"{a} / {b}", result = result)
        return result  


class TrigCalculator:
    def __init__(self, history):
        self._history = history

    def _parse_input(self, x):
        """Внутренний метод: проверяет и конвертирует градусы в радианы, если есть знак °"""
        if isinstance(x, str) and '°' in x:
            # Убираем знак градуса, пробелы и переводим в число
            degrees = float(x.replace('°', '').strip())
            return math.radians(degrees), f"{degrees}°"
        else:
            # Если передано число, считаем, что это радианы
            return float(x), f"{x} rad"
    
    def SinOperation(self, x):
        """Синус угла (принимает число для радиан или строку вроде '90°')"""
        rad_value, label = self._parse_input(x)
        result = math.sin(rad_value)
        self._history.add_records(category = "Тригонометрия", operation = f"sin({label})", result = result)
        return result

    def CosOperation(self, x):
        """Косинус угла"""
        rad_value, label = self._parse_input(x)
        result = math.cos(rad_value)
        self._history.add_records(category = "Тригонометрия", operation = f"cos({label})", result = result)
        return result

    def TanOperation(self, x):
        """Тангенс угла"""
        rad_value, label = self._parse_input(x)
        if math.isclose(math.cos(rad_value), 0, abs_tol=1e-9):
            raise ValueError(f"Тангенс для {label} не существует (деление на ноль)!")
        result = math.tan(rad_value)
        self._history.add_records(category = "Тригонометрия", operation = f"tan({label})", result = result)
        return result

    def CotOperation(self, x):
        """Котангенс угла"""
        rad_value, label = self._parse_input(x)
        if math.isclose(math.sin(rad_value), 0, abs_tol=1e-9):
            raise ValueError(f"Котангенс для {label} не существует (деление на ноль)!")
        result = 1 / math.tan(rad_value)
        self._history.add_records(category = "Тригонометрия", operation = f"cot({label})", result = result)
        return result

    # Для обратных функций (asin, acos и т.д.) ввод — это всегда просто число (значение), 
    # а вот результат возвращается в радианах. Для удобства добавим им перевод ответа в градусы.
    def AsinOperation(self, x, to_degrees=False):
        """Арксинус. Если to_degrees=True, вернет результат в градусах"""
        if not (-1 <= x <= 1):
            raise ValueError("Арксинус определен только для значений от -1 до 1!")
        result = math.asin(x)
        if to_degrees:
            deg_res = math.degrees(result)
            self._history.add_records(category = "Тригонометрия", operation = f"asin({x})", result = f"{deg_res}°")
            return f"{deg_res}°"
        self._history.add_records(category = "Тригонометрия", operation = f"asin({x})", result = result)
        return result

    def AcosOperation(self, x, to_degrees=False):
        """Арккосинус. Если to_degrees=True, вернет результат в градусах"""
        if not (-1 <= x <= 1):
            raise ValueError("Арккосинус определен только для значений от -1 до 1!")
        result = math.acos(x)
        if to_degrees:
            deg_res = math.degrees(result)
            self._history.add_records(category = "Тригонометрия", operation = f"acos({x})", result = f"{deg_res}°")
            return f"{deg_res}°"
        self._history.add_records(category = "Тригонометрия", operation = f"acos({x})", result = result)
        return result

    def AtanOperation(self, x, to_degrees=False):
        """Арктангенс. Если to_degrees=True, вернет результат в градусах"""
        result = math.atan(x)
        if to_degrees:
            deg_res = math.degrees(result)
            self._history.add_records(category = "Тригонометрия", operation = f"atan({x})", result = f"{deg_res}°")
            return f"{deg_res}°"
        self._history.add_records(category = "Тригонометрия", operation = f"atan({x})", result = result)
        return result

    def AcotOperation(self, x, to_degrees=False):
        """Арккотангенс. Если to_degrees=True, вернет результат в градусах"""
        result = math.pi / 2 - math.atan(x)
        if to_degrees:
            deg_res = math.degrees(result)
            self._history.add_records(category = "Тригонометрия", operation = f"acot({x})", result = f"{deg_res}°")
            return f"{deg_res}°"
        self._history.add_records(category = "Тригонометрия", operation = f"acot({x})", result = result)
        return result



## --- Демонстрация работы всех функций ---
#
## 1. Проверяем все функции базового калькулятора
#calc1 = BasedCalculator()
#calc1.AddOperation(3, 4)
#calc1.SubOperation(3, 4)
#calc1.MulOperation(3, 4)
#calc1.DivOperation(3, 4)
#
#print("История calc1 (Базовые операции):")
#for record in calc1.get_history():
#    print(record)
#
#
#print("\n" + "="*40 + "\n")
#
#
## 2. Проверяем абсолютно все функции тригонометрического калькулятора
#calc2 = TrigCalculator()
#
## Прямые тригонометрические функции (передаем градусы строкой или радианы числом)
#calc2.SinOperation("90°")          # Синус в градусах
#calc2.SinOperation(math.pi / 2)    # Синус в радианах
#
#calc2.CosOperation("0°")           # Косинус в градусах
#calc2.CosOperation(0)              # Косинус в радианах
#
#calc2.TanOperation("45°")          # Тангенс в градусах
#calc2.TanOperation(math.pi / 4)    # Тангенс в радианах
#
#calc2.CotOperation("45°")          # Котангенс в градусах
#calc2.CotOperation(math.pi / 4)    # Котангенс в радианах
#
## Обратные тригонометрические функции (принимают число)
## Можно вызывать стандартно (ответ в радианах) или с параметром to_degrees=True (ответ в градусах)
#calc2.AsinOperation(0.5)                   # Арксинус (ответ в радианах)
#calc2.AsinOperation(0.5, to_degrees=True)  # Арксинус (ответ в градусах)
#
#calc2.AcosOperation(0.5)                   # Арккосинус (ответ в радианах)
#calc2.AcosOperation(0.5, to_degrees=True)  # Арккосинус (ответ в градусах)
#
#calc2.AtanOperation(1)                     # Арктангенс (ответ в радианах)
#calc2.AtanOperation(1, to_degrees=True)    # Арктангенс (ответ в градусах)
#
#calc2.AcotOperation(1)                     # Арккотангенс (ответ в радианах)
#calc2.AcotOperation(1, to_degrees=True)    # Арккотангенс (ответ в градусах)

#print("История calc2 (Тригонометрия):")
#for record in calc2.get_history():
#    print(record)



class IntegrationCalculator:
    def __init__(self, history):
        self._history = history

    def IntegrateOperation(self, func, a, b, n=1000):
        if n <= 0:
            raise ValueError("Количество шагов разбиения должно быть больше нуля!")
        
        h = (b - a) / n
        total = 0.5 * (func(a) + func(b))
        for i in range(1, n):
            total += func(a + i * h)
        
        result = total * h
        func_name = getattr(func, '__name__', 'f(x)')
        self._history.add_records(category = "Интегрирование", operation = f"∫ от {a} до {b} для {func_name} (n={n})", result = result)
        return result



def func1(x):
    return x**2 + 3*x

def func2(x):
    return x**2 + 3*x + 1

def func3(x):
    return x**3 - 2*x + 5

def func4(x):
    return math.sin(x) + math.cos(x)

def func5(x):
    return 2*x**2 - 4*x + 1

def square(x):
    return x**2

def sine(x):
    return math.sin(x)

def exp_plus_x(x):
    return math.exp(x) + x

def linear(x):
    return 3*x + 1

def polynomial(x):
    return x**4 - 2*x**3 + 3*x**2 - 4*x + 5


#calc3 = IntegrationCalculator()
#
#calc3.IntegrateOperation(func1, 0, 2)
#calc3.IntegrateOperation(func2, 0, 2)
#calc3.IntegrateOperation(func3, -1, 2)
#calc3.IntegrateOperation(func4, 0, math.pi, n=5000)
#calc3.IntegrateOperation(func5, -1, 3)
#calc3.IntegrateOperation(square, 0, 2)
#calc3.IntegrateOperation(sine, 0, math.pi, n=5000)
#calc3.IntegrateOperation(exp_plus_x, 0, 1)
#calc3.IntegrateOperation(linear, 0, 2)
#calc3.IntegrateOperation(polynomial, 0, 1)

# Вывод истории в столбик
#print("История calc3 (Интегрирование):")
#for record in calc3.get_history():
#    print(record)

class MatrixCalculator:
    def __init__(self, history=None):
        self._history = history if history is not None else History()
    @property
    def history(self):
        return self._history
    
    def _validate_matrix(self, matrix, name="Матрица"):
        if not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
            raise ValueError(f"{name} должна быть списком списков.")
        if len(matrix) == 0 or len(matrix[0]) == 0:
            raise ValueError(f"{name} не может быть пустой.")
        row_len = len(matrix[0])
        for i, row in enumerate(matrix):
            if len(row) != row_len:
                raise ValueError(f"{name}: строка {i} имеет длину {len(row)} вместо {row_len}.")
            if not all(isinstance(x, (int, float)) for x in row):
                raise ValueError(f"{name}: все элементы должны быть числами.")

    def _same_size(self, A, B):
        return len(A) == len(B) and len(A[0]) == len(B[0])

    def add_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if not self._same_size(A, B):
            raise ValueError("Матрицы должны быть одного размера для сложения.")
        rows, cols = len(A), len(A[0])
        result = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]
        self._history.add_records(category = "Матрицы", operation = f"Сложение\n{A}\n+\n{B}", result = result)
        return result

    def subtract_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if not self._same_size(A, B):
            raise ValueError("Матрицы должны быть одного размера для вычитания.")
        rows, cols = len(A), len(A[0])
        result = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]
        self._history.add_records(category = "Матрицы", operation = f"Вычитание\n{A}\n-\n{B}",result = result )
        return result

    def multiply_by_scalar(self, matrix, scalar):
        self._validate_matrix(matrix)
        rows, cols = len(matrix), len(matrix[0])
        result = [[matrix[i][j] * scalar for j in range(cols)] for i in range(rows)]
        self._history.add_records(category = "Матрицы", operation = f"Умножение на скаляр {scalar}\n{matrix}",result = result)
        return result

    def multiply_matrices(self, A, B):
        self._validate_matrix(A, "A")
        self._validate_matrix(B, "B")
        if len(A[0]) != len(B):
            raise ValueError("Число столбцов A должно равняться числу строк B для умножения.")
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(cols_A)) for j in range(cols_B)] for i in range(rows_A)]
        self._history.add_records(category = "Матрицы", operation = f"Умножение\n{A}\n@\n{B}", result = result)
        return result

    def transpose(self, matrix):
        self._validate_matrix(matrix)
        rows, cols = len(matrix), len(matrix[0])
        result = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
        self._history.add_records(category = "Матрицы", operation = f"Транспонирование\n{matrix}", result = result)
        return result

    def determinant(self, matrix):
        self._validate_matrix(matrix)
        if len(matrix) != len(matrix[0]):
            raise ValueError("Определитель определён только для квадратных матриц.")
        def _det(m):
            if len(m) == 1:
                return m[0][0]
            if len(m) == 2:
                return m[0][0] * m[1][1] - m[0][1] * m[1][0]
            det_value = 0
            for col in range(len(m)):
                sign = (-1) ** col
                minor = [row[:col] + row[col+1:] for row in m[1:]]
                det_value += sign * m[0][col] * _det(minor)
            return det_value
        det_result = _det(matrix)
        self._history.add_records(category = "Матрицы", operation = f"Определитель\n{matrix}", result = det_result)
        return det_result

    def inverse(self, matrix):
        self._validate_matrix(matrix)
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Обратная матрица существует только для квадратныхматриц.")
        det = self.determinant(matrix)
        if det == 0:
            raise ValueError("Матрица вырождена, обратной не существует.")
        cofactors = []
        for i in range(n):
            cofactor_row = []
            for j in range(n):
                minor = [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
                cofactor = ((-1) ** (i + j)) * self._det_without_history(minor) # используем внутренний метод
                cofactor_row.append(cofactor)
            cofactors.append(cofactor_row)
        adjugate = [[cofactors[j][i] for j in range(n)] for i in range(n)]
        inv = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
        self._history.add_records(category = "Матрицы", operation = f"Обратная к\n{matrix}", result = inv)
        return inv

    def _det_without_history(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det_value = 0
        for col in range(len(matrix)):
            sign = (-1) ** col
            minor = [row[:col] + row[col+1:] for row in matrix[1:]]
            det_value += sign * matrix[0][col] * self._det_without_history(minor)
        return det_value


class InteractiveGraphCalculator:

    def __init__(self, history):
        self._history = history

        self.functions_to_plot = []
        self.plots_data = []
        self.current_index = 0

        self.x = np.linspace(-10, 10, 500)

        self.fig = None
        self.ax = None

    def PlotOperation(self, *functions):
        """
        Построение одного или нескольких графиков.

        Пример:
        calc.graph.PlotOperation(
            "np.sin(x)",
            "np.cos(x)",
            "x**2"
        )
        """

        self.functions_to_plot = list(functions)
        self.plots_data = []
        self.current_index = 0

        self.fig, self.ax = plt.subplots(figsize=(11, 6))
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)

        self.prepare_data()

        if self.plots_data:
            self.update_graph()
            plt.show()
        else:
            print("Нет корректных функций для построения.")

    def prepare_data(self):

        for expr in self.functions_to_plot:

            try:

                y = eval(
                    expr,
                    {"__builtins__": None},
                    {"np": np, "x": self.x}
                )

                self.plots_data.append({
                    "expr": expr,
                    "y": y,
                    "type": "single"
                })

                self._history.add_records(
                    "Графики",
                    f"Построение y={expr}",
                    "Успешно"
                )

            except Exception as e:

                self._history.add_records(
                    "Графики",
                    f"Построение y={expr}",
                    f"Ошибка: {type(e).__name__}"
                )

                print(f"Ошибка в функции {expr}")

        if self.plots_data:
            self.plots_data.append({
                "type": "history"
            })

    def update_graph(self):

        self.ax.clear()

        self.ax.axhline(0, color="black")
        self.ax.axvline(0, color="black")
        self.ax.grid(True)

        current = self.plots_data[self.current_index]

        if current["type"] == "single":

            self.ax.plot(
                self.x,
                current["y"],
                linewidth=2,
                label=f"y={current['expr']}"
            )

            self.ax.set_title(
                f"График {self.current_index+1} из {len(self.plots_data)-1}\n"
                "Пробел — следующий график"
            )

            y = current["y"][np.isfinite(current["y"])]

            if len(y):

                self.ax.set_ylim(
                    max(np.min(y)-1, -20),
                    min(np.max(y)+1, 20)
                )

            self.ax.legend()

        else:

            ymin = -5
            ymax = 5

            for plot in self.plots_data[:-1]:

                self.ax.plot(
                    self.x,
                    plot["y"],
                    label=f"y={plot['expr']}"
                )

                y = plot["y"][np.isfinite(plot["y"])]

                if len(y):

                    ymin = min(ymin, np.min(y)-1)
                    ymax = max(ymax, np.max(y)+1)

            self.ax.set_ylim(
                max(ymin, -30),
                min(ymax, 30)
            )

            self.ax.set_title(
                "Все графики\nПробел — вернуться к первому"
            )

            self.ax.legend(
                bbox_to_anchor=(1, 1),
                loc="upper left"
            )

        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")

        self.fig.canvas.draw()

    def on_key(self, event):

        if event.key == " ":

            self.current_index += 1

            if self.current_index >= len(self.plots_data):
                self.current_index = 0

            self.update_graph()




class EngineeringCalc:
    def __init__(self):
        self._history = History()
        self.arithmetic = BasedCalculator(self._history)
        self.trigonometry = TrigCalculator(self._history)
        self.integration = IntegrationCalculator(self._history)
        self.matrix = MatrixCalculator(self._history)
        self.graph = InteractiveGraphCalculator(self._history)

    def show_history(self):
        self._history.show()

    def clear(self):
        """Очищает список истории"""
        self._history.clear()  # Метод .clear() полностью опустошает список



calc1=EngineeringCalc()

calc1.arithmetic.AddOperation(2,3)
calc1.arithmetic.DivOperation(6, 3)
calc1.trigonometry.SinOperation("90°")
calc1.trigonometry.TanOperation(math.pi / 4)
calc1.integration.IntegrateOperation(func1, 0, 2)
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
calc1.matrix.add_matrices(A, B)
calc1.graph.PlotOperation("x**2 - 4",  # Функция №1 (Парабола)
        "np.sin(x) * 3")  # Функция №2 (Синусоида))
calc1.show_history()
calc1.clear()
calc1.show_history()