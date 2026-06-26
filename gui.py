import tkinter as tk
from tkinter import ttk, messagebox
import math

# Импортируем ваш главный класс вычислений (если всё в одном файле, удалите эту строку)
from calculator import EngineeringCalc 

class CalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Инженерный калькулятор")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Инициализируем ваше вычислительное ядро
        self.calculator = EngineeringCalc()
        self.create_widgets()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)
        
        # Старые вкладки
        self.arithmetic_tab = ttk.Frame(self.tabs)
        self.trigonometry_tab = ttk.Frame(self.tabs)
        
        # Новые вкладки на основе вашего кода
        self.integration_tab = ttk.Frame(self.tabs)
        self.matrix_tab = ttk.Frame(self.tabs)
        self.graph_tab = ttk.Frame(self.tabs)
        
        # Вкладка истории
        self.history_tab = ttk.Frame(self.tabs)
        
        # Добавление вкладок в панель
        self.tabs.add(self.arithmetic_tab, text="Базовая математика")
        self.tabs.add(self.trigonometry_tab, text="Тригонометрия")
        self.tabs.add(self.integration_tab, text="Интегрирование")
        self.tabs.add(self.matrix_tab, text="Матрицы")
        self.tabs.add(self.graph_tab, text="Графики")
        self.tabs.add(self.history_tab, text="История")
        
        self.tabs.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Инициализация интерфейса каждой вкладки
        self.create_arithmetic_tab()
        self.create_trigonometry_tab()
        self.create_integration_tab()
        self.create_matrix_tab()
        self.create_graph_tab()
        self.create_history_tab()

    # ---------- 1. БАЗОВАЯ МАТЕМАТИКА ----------
    def create_arithmetic_tab(self):
        title = ttk.Label(self.arithmetic_tab, text="Базовая математика", font=("Arial", 16))
        title.pack(pady=10)
        
        input_frame = ttk.Frame(self.arithmetic_tab)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Первое число:").grid(row=0, column=0, padx=5, pady=5)
        self.first_number_entry = ttk.Entry(input_frame, width=20)
        self.first_number_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Второе число:").grid(row=1, column=0, padx=5, pady=5)
        self.second_number_entry = ttk.Entry(input_frame, width=20)
        self.second_number_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Операция:").grid(row=2, column=0, padx=5, pady=5)
        self.arithmetic_operation = ttk.Combobox(
            input_frame, 
            values=["Сложение (+)", "Вычитание (-)", "Умножение (*)", "Деление (/)"],
            state="readonly", width=17
        )
        self.arithmetic_operation.grid(row=2, column=1, padx=5, pady=5)
        self.arithmetic_operation.current(0)
        
        ttk.Button(self.arithmetic_tab, text="Вычислить", command=self.calculate_arithmetic).pack(pady=10)
        self.arithmetic_result_label = ttk.Label(self.arithmetic_tab, text="Результат: ", font=("Arial", 13))
        self.arithmetic_result_label.pack(pady=10)

    def calculate_arithmetic(self):
        try:
            a = self.get_float_from_entry(self.first_number_entry, "первое число")
            b = self.get_float_from_entry(self.second_number_entry, "второе число")
            op = self.arithmetic_operation.get()
            
            if op == "Сложение (+)": result = self.calculator.arithmetic.AddOperation(a, b)
            elif op == "Вычитание (-)": result = self.calculator.arithmetic.SubOperation(a, b)
            elif op == "Умножение (*)": result = self.calculator.arithmetic.MulOperation(a, b)
            elif op == "Деление (/)": result = self.calculator.arithmetic.DivOperation(a, b)
                
            self.arithmetic_result_label.config(text=f"Результат: {result}")
            self.update_history()
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- 2. ТРИГОНОМЕТРИЯ ----------
    def create_trigonometry_tab(self):
        title = ttk.Label(self.trigonometry_tab, text="Тригонометрия", font=("Arial", 16))
        title.pack(pady=10)
        
        input_frame = ttk.Frame(self.trigonometry_tab)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Угол/Значение:").grid(row=0, column=0, padx=5, pady=5)
        self.angle_entry = ttk.Entry(input_frame, width=20)
        self.angle_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Режим угла:").grid(row=1, column=0, padx=5, pady=5)
        self.angle_mode = ttk.Combobox(input_frame, values=["degrees", "radians"], state="readonly", width=17)
        self.angle_mode.grid(row=1, column=1, padx=5, pady=5)
        self.angle_mode.current(0)
        
        ttk.Label(input_frame, text="Функция:").grid(row=2, column=0, padx=5, pady=5)
        self.trigonometry_operation = ttk.Combobox(
            input_frame, 
            values=["sin", "cos", "tan", "cot", "asin", "acos", "atan", "acot"],
            state="readonly", width=17
        )
        self.trigonometry_operation.grid(row=2, column=1, padx=5, pady=5)
        self.trigonometry_operation.current(0)
        
        ttk.Button(self.trigonometry_tab, text="Вычислить", command=self.calculate_trigonometry).pack(pady=10)
        self.trigonometry_result_label = ttk.Label(self.trigonometry_tab, text="Результат: ", font=("Arial", 13))
        self.trigonometry_result_label.pack(pady=10)

    def calculate_trigonometry(self):
        try:
            raw_val = self.angle_entry.get().strip().replace(",", ".")
            if not raw_val: raise ValueError("Поле ввода пустое")
            
            operation = self.trigonometry_operation.get()
            mode = self.angle_mode.get()
            
            # Настройка под парсер знака градуса в вашем TrigCalculator
            if mode == "degrees" and operation in ["sin", "cos", "tan", "cot"]:
                angle_input = f"{raw_val}°"
            else:
                angle_input = float(raw_val)
            
            # Прямые функции
            if operation == "sin": result = self.calculator.trigonometry.SinOperation(angle_input)
            elif operation == "cos": result = self.calculator.trigonometry.CosOperation(angle_input)
            elif operation == "tan": result = self.calculator.trigonometry.TanOperation(angle_input)
            elif operation == "cot": result = self.calculator.trigonometry.CotOperation(angle_input)
            # Обратные функции (перевод результата в градусы, если выбран режим degrees)
            elif operation == "asin": result = self.calculator.trigonometry.AsinOperation(angle_input, to_degrees=(mode=="degrees"))
            elif operation == "acos": result = self.calculator.trigonometry.AcosOperation(angle_input, to_degrees=(mode=="degrees"))
            elif operation == "atan": result = self.calculator.trigonometry.AtanOperation(angle_input, to_degrees=(mode=="degrees"))
            elif operation == "acot": result = self.calculator.trigonometry.AcotOperation(angle_input, to_degrees=(mode=="degrees"))
                
            self.trigonometry_result_label.config(text=f"Результат: {result}")
            self.update_history()
        except Exception as error:
            messagebox.showerror("Ошибка", str(error))

    # ---------- 3. ИНТЕГРИРОВАНИЕ (НОВОЕ) ----------
    def create_integration_tab(self):
        title = ttk.Label(self.integration_tab, text="Численное интегрирование", font=("Arial", 16))
        title.pack(pady=10)
        
        input_frame = ttk.Frame(self.integration_tab)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Функция f(x):").grid(row=0, column=0, padx=5, pady=5)
        self.integ_func_combo = ttk.Combobox(
            input_frame, 
            values=["x**2 + 3*x (func1)", "x**2 + 3*x + 1 (func2)", "x**3 - 2*x + 5 (func3)", 
                    "sin(x) + cos(x) (func4)", "x**2 (square)", "sin(x) (sine)"],
            state="readonly", width=25
        )
        self.integ_func_combo.grid(row=0, column=1, padx=5, pady=5)
        self.integ_func_combo.current(4) # по умолчанию x**2
        
        ttk.Label(input_frame, text="Нижняя граница (a):").grid(row=1, column=0, padx=5, pady=5)
        self.integ_a_entry = ttk.Entry(input_frame, width=27)
        self.integ_a_entry.grid(row=1, column=1, padx=5, pady=5)
        self.integ_a_entry.insert(0, "0")
        
        ttk.Label(input_frame, text="Верхняя граница (b):").grid(row=2, column=0, padx=5, pady=5)
        self.integ_b_entry = ttk.Entry(input_frame, width=27)
        self.integ_b_entry.grid(row=2, column=1, padx=5, pady=5)
        self.integ_b_entry.insert(0, "2")
        
        ttk.Label(input_frame, text="Кол-во шагов разбиения (n):").grid(row=3, column=0, padx=5, pady=5)
        self.integ_n_entry = ttk.Entry(input_frame, width=27)
        self.integ_n_entry.grid(row=3, column=1, padx=5, pady=5)
        self.integ_n_entry.insert(0, "1000")
        
        ttk.Button(self.integration_tab, text="Интегрировать", command=self.calculate_integration).pack(pady=10)
        self.integ_result_label = ttk.Label(self.integration_tab, text="Результат (Площадь): ", font=("Arial", 13))
        self.integ_result_label.pack(pady=10)

    def calculate_integration(self):
        try:
            a = float(eval(self.integ_a_entry.get().replace(",", "."))) # поддержка констант типа math.pi
            b = float(eval(self.integ_b_entry.get().replace(",", ".")))
            n = int(self.integ_n_entry.get().strip())
            
            # Маппинг функций из вашего исходного кода
            func_name = self.integ_func_combo.get()
            # --- Продолжение метода calculate_integration ---
            if "func1" in func_name: func = lambda x: x**2 + 3*x
            elif "func2" in func_name: func = lambda x: x**2 + 3*x + 1
            elif "func3" in func_name: func = lambda x: x**3 - 2*x + 5
            elif "func4" in func_name: func = lambda x: math.sin(x) + math.cos(x)
            elif "square" in func_name: func = lambda x: x**2
            elif "sine" in func_name: func = math.sin
            
            result = self.calculator.integration.IntegrateOperation(func, a, b, n)
            self.integ_result_label.config(text=f"Результат (Площадь): {result}")
            self.update_history()
        except Exception as error:
            messagebox.showerror("Ошибка", f"Проверьте границы ввода: {error}")

    # ---------- 4. МАТРИЦЫ ----------
    def create_matrix_tab(self):
        title = ttk.Label(self.matrix_tab, text="Линейная алгебра (Матрицы)", font=("Arial", 16))
        title.pack(pady=5)
        
        desc = ttk.Label(self.matrix_tab, text="Формат ввода: [[1,2],[3,4]]", font=("Arial", 9, "italic"))
        desc.pack(pady=2)
        
        input_frame = ttk.Frame(self.matrix_tab)
        input_frame.pack(pady=5)
        
        ttk.Label(input_frame, text="Матрица A:").grid(row=0, column=0, padx=5, pady=5)
        self.matrix_a_entry = ttk.Entry(input_frame, width=40)
        self.matrix_a_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Матрица B (если нужна):").grid(row=1, column=0, padx=5, pady=5)
        self.matrix_b_entry = ttk.Entry(input_frame, width=40)
        self.matrix_b_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Скаляр (если нужен):").grid(row=2, column=0, padx=5, pady=5)
        self.matrix_scalar_entry = ttk.Entry(input_frame, width=40)
        self.matrix_scalar_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Операция над матрицами:").grid(row=3, column=0, padx=5, pady=5)
        self.matrix_op_combo = ttk.Combobox(
            input_frame, 
            values=["Сложение (A + B)", "Вычитание (A - B)", "Умножение на скаляр", 
                    "Умножение матриц (A * B)", "Транспонирование (A)", "Определитель (A)", "Обратная матрица (A)"],
            state="readonly", width=37
        )
        self.matrix_op_combo.grid(row=3, column=1, padx=5, pady=5)
        self.matrix_op_combo.current(0)
        
        ttk.Button(self.matrix_tab, text="Выполнить операцию", command=self.calculate_matrix).pack(pady=5)
        
        self.matrix_result_text = tk.Text(self.matrix_tab, width=50, height=5, font=("Courier", 11), state="disabled")
        self.matrix_result_text.pack(pady=5)

    def calculate_matrix(self):
        try:
            op = self.matrix_op_combo.get()
            
            def parse_m(entry_widget):
                text = entry_widget.get().strip()
                return eval(text) if text else None
            
            A = parse_m(self.matrix_a_entry)
            
            if op == "Сложение (A + B)":
                B = parse_m(self.matrix_b_entry)
                result = self.calculator.matrix.add_matrices(A, B)
            elif op == "Вычитание (A - B)":
                B = parse_m(self.matrix_b_entry)
                result = self.calculator.matrix.subtract_matrices(A, B)
            elif op == "Умножение на скаляр":
                scalar = float(self.matrix_scalar_entry.get().strip())
                result = self.calculator.matrix.multiply_by_scalar(A, scalar)
            elif op == "Умножение матриц (A * B)":
                B = parse_m(self.matrix_b_entry)
                result = self.calculator.matrix.multiply_matrices(A, B)
            elif op == "Транспонирование (A)":
                result = self.calculator.matrix.transpose(A)
            elif op == "Определитель (A)":
                result = self.calculator.matrix.determinant(A)
            elif op == "Обратная матрица (A)":
                result = self.calculator.matrix.inverse(A)
            
            self.matrix_result_text.config(state="normal")
            self.matrix_result_text.delete("1.0", tk.END)
            if isinstance(result, list):
                matrix_str = "\n".join(f"  {row}" for row in result)
                self.matrix_result_text.insert(tk.END, f"Результат:\n{matrix_str}")
            else:
                self.matrix_result_text.insert(tk.END, f"Результат: {result}")
            self.matrix_result_text.config(state="disabled")
            
            self.update_history()
        except Exception as error:
            messagebox.showerror("Ошибка матриц", f"Ошибка ввода/вычислений:\n{error}")

    # ---------- 5. ГРАФИКИ ----------
    def create_graph_tab(self):
        title = ttk.Label(self.graph_tab, text="Визуализация графиков функций", font=("Arial", 16))
        title.pack(pady=15)
        
        ttk.Label(self.graph_tab, text="Введите функции через запятую:", font=("Arial", 11)).pack(pady=5)
        
        self.graph_entry = ttk.Entry(self.graph_tab, width=50, font=("Arial", 11))
        self.graph_entry.pack(pady=5)
        self.graph_entry.insert(0, "x**2, np.sin(x), x**3 - 2*x")
        
        info_label = ttk.Label(
            self.graph_tab, 
            text="Используйте переменные 'x' и функции 'np.sin(x)', 'np.cos(x)'\n\n"
                 "После открытия окна нажимайте [ПРОБЕЛ] на клавиатуре,\n"
                 "чтобы циклически переключать отображение графиков!",
            justify="center", foreground="gray"
        )
        info_label.pack(pady=20)
        
        ttk.Button(self.graph_tab, text="Построить графики в Matplotlib", command=self.draw_graphs).pack(pady=15)

    def draw_graphs(self):
        try:
            functions_str = self.graph_entry.get().strip()
            if not functions_str: raise ValueError("Строка ввода пуста")
            
            funcs_list = [f.strip() for f in functions_str.split(",")]
            self.calculator.graph.PlotOperation(*funcs_list)
            self.update_history()
        except Exception as error:
            messagebox.showerror("Ошибка графиков", f"Не удалось построить график:\n{error}")

    # ---------- 6. ИСТОРИЯ ----------
    def create_history_tab(self):
        title = ttk.Label(self.history_tab, text="История вычислений", font=("Arial", 16))
        title.pack(pady=5)
        
        self.history_text = tk.Text(self.history_tab, width=75, height=18, font=("Courier", 10), state="disabled")
        self.history_text.pack(pady=5)
        
        button_frame = ttk.Frame(self.history_tab)
        button_frame.pack(pady=5)
        
        ttk.Button(button_frame, text="Обновить", command=self.update_history).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Очистить историю", command=self.clear_history).grid(row=0, column=1, padx=5)

    def update_history(self):
        self.history_text.config(state="normal")
        self.history_text.delete("1.0", tk.END)
        
        records = self.calculator._history._history
        
        if not records:
            self.history_text.insert(tk.END, "История пока пустая.")
        else:
            for index, record in enumerate(records, start=1):
                op_val = record['operation']
                res_val = record['result']
                
                if record['category'] == "Матрицы" and isinstance(res_val, list):
                    matrix_str = "\n".join(f"  {row}" for row in res_val)
                    line = f"{index}. [{record['category']}]\n{op_val} =\n{matrix_str}\n"
                else:
                    line = f"{index}. [{record['category']}] {op_val} = {res_val}\n"
                    
                self.history_text.insert(tk.END, line)
                self.history_text.insert(tk.END, "-"*60 + "\n")
                
        self.history_text.config(state="disabled")

    def clear_history(self):
        self.calculator.clear()
        self.update_history()
        messagebox.showinfo("История", "История успешно очищена.")

    # ---------- ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ----------
    def get_float_from_entry(self, entry, field_name):
        value = entry.get().strip().replace(",", ".")
        if value == "": raise ValueError(f"Поле '{field_name}' не должно быть пустым")
        return float(value)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
