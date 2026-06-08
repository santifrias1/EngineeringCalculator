import sys
import math
import sympy as sp
import numpy as np
import scipy.stats as stats
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, 
                               QGridLayout, QPushButton, QLineEdit, QGroupBox, 
                               QComboBox, QTextEdit, QMessageBox, QSplitter)
from PySide6.QtCore import Qt

# ==========================================
# MÓDULO 1: CALCULADORA CIENTÍFICA
# ==========================================
class CalculadoraCientificaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.factores_conversion = {
            "Longitud": {"Metros": 1.0, "Kilómetros": 1000.0, "Centímetros": 0.01, "Millas": 1609.34, "Pulgadas": 0.0254},
            "Masa": {"Kilogramos": 1.0, "Gramos": 0.001, "Libras": 0.453592, "Onzas": 0.0283495}
        }
        self.setup_ui()

    def setup_ui(self):
        layout_principal = QHBoxLayout(self)
        
        widget_calc = QWidget()
        layout_calc = QVBoxLayout(widget_calc)
        
        self.pantalla = QLineEdit()
        self.pantalla.setAlignment(Qt.AlignRight)
        self.pantalla.setPlaceholderText("0")
        self.pantalla.setStyleSheet("color: black; font-size: 28px; padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout_calc.addWidget(self.pantalla)

        grid = QGridLayout()
        layout_calc.addLayout(grid)

        botones = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('log', 0, 3), ('ln', 0, 4),
            ('sinh', 1, 0), ('cosh', 1, 1), ('tanh', 1, 2), ('√', 1, 3), ('^', 1, 4),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('C', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('(', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), (')', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('EXP', 5, 2), ('+', 5, 3), ('=', 5, 4)
        ]

        for texto, fila, col in botones:
            btn = QPushButton(texto)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("font-size: 16px; font-weight: bold;")
            btn.clicked.connect(lambda checked, t=texto: self.procesar_click(t))
            grid.addWidget(btn, fila, col)
            
        layout_principal.addWidget(widget_calc, stretch=2)

        grupo_conversor = QGroupBox("Conversión de Unidades")
        layout_conv = QVBoxLayout(grupo_conversor)
        
        layout_conv.addWidget(QLabel("Categoría:"))
        self.combo_categoria = QComboBox()
        self.combo_categoria.setStyleSheet("color: black; background-color: white;")
        self.combo_categoria.addItems(self.factores_conversion.keys())
        self.combo_categoria.currentTextChanged.connect(self.actualizar_unidades)
        layout_conv.addWidget(self.combo_categoria)
        
        layout_conv.addWidget(QLabel("De:"))
        self.combo_origen = QComboBox()
        self.combo_origen.setStyleSheet("color: black; background-color: white;")
        layout_conv.addWidget(self.combo_origen)
        
        layout_conv.addWidget(QLabel("A:"))
        self.combo_destino = QComboBox()
        self.combo_destino.setStyleSheet("color: black; background-color: white;")
        layout_conv.addWidget(self.combo_destino)
        
        layout_conv.addWidget(QLabel("Valor a convertir:"))
        self.input_valor = QLineEdit()
        self.input_valor.setPlaceholderText("Ej: 15.5")
        self.input_valor.setStyleSheet("color: black; background-color: white;")
        layout_conv.addWidget(self.input_valor)
        
        btn_convertir = QPushButton("Convertir")
        btn_convertir.clicked.connect(self.convertir_unidades)
        layout_conv.addWidget(btn_convertir)
        
        layout_conv.addWidget(QLabel("Resultado:"))
        self.resultado_conv = QLineEdit()
        self.resultado_conv.setReadOnly(True)
        self.resultado_conv.setStyleSheet("color: black; font-weight: bold; background-color: #e8f4f8;")
        layout_conv.addWidget(self.resultado_conv)
        
        layout_conv.addStretch()
        layout_principal.addWidget(grupo_conversor, stretch=1)
        self.actualizar_unidades(self.combo_categoria.currentText())

    def procesar_click(self, texto):
        if texto == 'C': self.pantalla.clear()
        elif texto == '=': self.calcular_resultado()
        elif texto in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'log', 'ln', '√']:
            self.pantalla.setText(self.pantalla.text() + texto + '(')
        elif texto == '^': self.pantalla.setText(self.pantalla.text() + '**')
        elif texto == 'EXP': self.pantalla.setText(self.pantalla.text() + '*10**')
        else: self.pantalla.setText(self.pantalla.text() + texto)

    def calcular_resultado(self):
        expresion = self.pantalla.text().replace('√', 'math.sqrt')
        expresion = expresion.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
        expresion = expresion.replace('sinh', 'math.sinh').replace('cosh', 'math.cosh').replace('tanh', 'math.tanh')
        expresion = expresion.replace('ln', 'math.log').replace('log', 'math.log10')
        try:
            res = eval(expresion, {"__builtins__": None}, {"math": math})
            if isinstance(res, float) and res.is_integer(): res = int(res)
            self.pantalla.setText(str(res))
        except:
            self.pantalla.setText("Error")

    def actualizar_unidades(self, categoria):
        self.combo_origen.clear(); self.combo_destino.clear()
        self.combo_origen.addItems(list(self.factores_conversion[categoria].keys()))
        self.combo_destino.addItems(list(self.factores_conversion[categoria].keys()))

    def convertir_unidades(self):
        cat, orig, dest = self.combo_categoria.currentText(), self.combo_origen.currentText(), self.combo_destino.currentText()
        try:
            val = float(self.input_valor.text())
            res = (val * self.factores_conversion[cat][orig]) / self.factores_conversion[cat][dest]
            self.resultado_conv.setText(f"{res:.4f}")
        except: self.resultado_conv.setText("Valor inválido")

# ==========================================
# MÓDULO 2: ÁLGEBRA
# ==========================================
class AlgebraWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Expresión o Ecuación (use 'x', 'y'. Use '**' para potencias, '=' para ecuaciones):"))
        self.input_expr = QLineEdit()
        self.input_expr.setPlaceholderText("Ejemplo: (x**2 - 4) / (x - 2)   o bien   2*x + 5 = 15")
        self.input_expr.setStyleSheet("color: black; background-color: white; font-size: 18px; padding: 8px;")
        layout.addWidget(self.input_expr)

        self.combo_operacion = QComboBox()
        self.combo_operacion.setStyleSheet("color: black; background-color: white;")
        self.combo_operacion.addItems(["Simplificar", "Factorizar", "Resolver Ecuación"])
        layout.addWidget(self.combo_operacion)

        btn = QPushButton("Calcular")
        btn.setStyleSheet("font-weight: bold; background-color: #4CAF50; color: white; padding: 10px;")
        btn.clicked.connect(self.ejecutar)
        layout.addWidget(btn)

        self.res_text = QTextEdit()
        self.res_text.setReadOnly(True)
        self.res_text.setStyleSheet("color: black; font-size: 18px; padding: 10px; background-color: #f9f9f9;")
        layout.addWidget(self.res_text)

    def ejecutar(self):
        t, op = self.input_expr.text().strip(), self.combo_operacion.currentText()
        if not t: return
        try:
            if "=" in t:
                izq, der = t.split("=", 1)
                expr = sp.Eq(sp.sympify(izq), sp.sympify(der))
            else: expr = sp.sympify(t)

            if op == "Simplificar": res = sp.simplify(expr)
            elif op == "Factorizar": res = sp.factor(expr)
            elif op == "Resolver Ecuación":
                v = expr.free_symbols
                res = sp.solve(expr, list(v)[0]) if v else "Sin variables."
            self.res_text.setText(str(res))
        except Exception as e: self.res_text.setText(f"Error: {e}")

# ==========================================
# MÓDULO 3: ANÁLISIS MATEMÁTICO
# ==========================================
class AnalisisMatematicoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        layout.addLayout(grid)

        grid.addWidget(QLabel("Función f(x):"), 0, 0)
        self.input_expr = QLineEdit()
        self.input_expr.setPlaceholderText("Ej: sin(x)*exp(x)   o   1/x")
        self.input_expr.setStyleSheet("color: black; background-color: white;")
        grid.addWidget(self.input_expr, 0, 1, 1, 3)

        grid.addWidget(QLabel("Operación:"), 1, 0)
        self.combo_op = QComboBox()
        self.combo_op.setStyleSheet("color: black; background-color: white;")
        self.combo_op.addItems(["Derivada", "Integral Indefinida", "Integral Definida", "Límite", "Serie de Taylor"])
        self.combo_op.currentTextChanged.connect(self.actualizar_ui)
        grid.addWidget(self.combo_op, 1, 1, 1, 3)

        self.lbl_p1, self.input_p1 = QLabel("a:"), QLineEdit()
        self.lbl_p2, self.input_p2 = QLabel("b:"), QLineEdit()
        self.input_p1.setStyleSheet("color: black; background-color: white;")
        self.input_p2.setStyleSheet("color: black; background-color: white;")
        grid.addWidget(self.lbl_p1, 2, 0); grid.addWidget(self.input_p1, 2, 1)
        grid.addWidget(self.lbl_p2, 2, 2); grid.addWidget(self.input_p2, 2, 3)

        btn = QPushButton("Calcular Análisis")
        btn.setStyleSheet("font-weight: bold; background-color: #2196F3; color: white; padding: 10px;")
        btn.clicked.connect(self.ejecutar)
        layout.addWidget(btn)

        self.res_text = QTextEdit()
        self.res_text.setReadOnly(True)
        self.res_text.setStyleSheet("color: black; font-size: 18px; padding: 10px; background-color: #f9f9f9;")
        layout.addWidget(self.res_text)
        self.actualizar_ui()

    def actualizar_ui(self):
        op = self.combo_op.currentText()
        if op in ["Derivada", "Integral Indefinida"]:
            self.input_p1.setEnabled(False); self.input_p1.setPlaceholderText("N/A")
            self.input_p2.setEnabled(False); self.input_p2.setPlaceholderText("N/A")
        elif op == "Límite":
            self.input_p1.setEnabled(True); self.lbl_p1.setText("Tiende a:"); self.input_p1.setPlaceholderText("Ej: 0, oo (infinito)")
            self.input_p2.setEnabled(False); self.input_p2.setPlaceholderText("N/A")
        elif op == "Integral Definida":
            self.input_p1.setEnabled(True); self.lbl_p1.setText("Lím. Inf:"); self.input_p1.setPlaceholderText("Ej: 0")
            self.input_p2.setEnabled(True); self.lbl_p2.setText("Lím. Sup:"); self.input_p2.setPlaceholderText("Ej: 5 o pi")
        elif op == "Serie de Taylor":
            self.input_p1.setEnabled(True); self.lbl_p1.setText("Punto (a):"); self.input_p1.setPlaceholderText("Ej: 0")
            self.input_p2.setEnabled(True); self.lbl_p2.setText("Orden (n):"); self.input_p2.setPlaceholderText("Ej: 6")

    def ejecutar(self):
        t, op = self.input_expr.text().strip(), self.combo_op.currentText()
        if not t: return
        try:
            x = sp.Symbol('x')
            expr = sp.sympify(t)
            if op == "Derivada": res = sp.diff(expr, x)
            elif op == "Integral Indefinida": res = sp.integrate(expr, x)
            elif op == "Integral Definida": res = sp.integrate(expr, (x, sp.sympify(self.input_p1.text()), sp.sympify(self.input_p2.text())))
            elif op == "Límite": res = sp.limit(expr, x, sp.sympify(self.input_p1.text()))
            elif op == "Serie de Taylor": res = sp.series(expr, x, sp.sympify(self.input_p1.text() or '0'), int(self.input_p2.text() or '6')).removeO()
            self.res_text.setText(str(res))
        except Exception as e: self.res_text.setText(f"Error: {e}")

# ==========================================
# MÓDULO 4: GRAFICACIÓN
# ==========================================
class GraficosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        panel = QHBoxLayout()
        panel.addWidget(QLabel("f(x) ="))
        self.input_fx = QLineEdit("sin(x)")
        self.input_fx.setStyleSheet("color: black; background-color: white;")
        panel.addWidget(self.input_fx)
        
        panel.addWidget(QLabel("x min:"))
        self.input_xmin = QLineEdit("-10")
        self.input_xmin.setStyleSheet("color: black; background-color: white;")
        panel.addWidget(self.input_xmin)
        
        panel.addWidget(QLabel("x max:"))
        self.input_xmax = QLineEdit("10")
        self.input_xmax.setStyleSheet("color: black; background-color: white;")
        panel.addWidget(self.input_xmax)
        
        btn = QPushButton("Graficar")
        btn.setStyleSheet("font-weight: bold; background-color: #FF9800; color: white;")
        btn.clicked.connect(self.dibujar)
        panel.addWidget(btn)
        layout.addLayout(panel)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

    def dibujar(self):
        try:
            x_min, x_max = float(self.input_xmin.text()), float(self.input_xmax.text())
            self.ax.clear()
            x_sym = sp.Symbol('x')
            f_num = sp.lambdify(x_sym, sp.sympify(self.input_fx.text()), 'numpy')
            x_vals = np.linspace(x_min, x_max, 500)
            self.ax.plot(x_vals, f_num(x_vals), label=self.input_fx.text(), color="blue")
            self.ax.axhline(0, color='black',linewidth=1)
            self.ax.axvline(0, color='black',linewidth=1)
            self.ax.grid(True, linestyle='--', linewidth=0.5)
            self.ax.legend()
            self.canvas.draw()
        except Exception as e: QMessageBox.critical(self, "Error", str(e))

# ==========================================
# MÓDULO 5: MÉTODOS NUMÉRICOS
# ==========================================
class MetodosNumericosWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        grid = QGridLayout()
        layout.addLayout(grid)
        
        grid.addWidget(QLabel("Método Numérico:"), 0, 0)
        self.combo_metodo = QComboBox()
        self.combo_metodo.setStyleSheet("color: black; background-color: white;")
        self.combo_metodo.addItems(["Bisección (Raíces)", "Newton-Raphson (Raíces)", "Trapecio (Integración)"])
        self.combo_metodo.currentTextChanged.connect(self.actualizar_inputs)
        grid.addWidget(self.combo_metodo, 0, 1, 1, 3)

        grid.addWidget(QLabel("Función f(x):"), 1, 0)
        self.input_fx = QLineEdit()
        self.input_fx.setPlaceholderText("Ej: x**3 - x - 1")
        self.input_fx.setStyleSheet("color: black; background-color: white;")
        grid.addWidget(self.input_fx, 1, 1, 1, 3)

        self.lbl_a, self.input_a = QLabel("a:"), QLineEdit()
        self.lbl_b, self.input_b = QLabel("b:"), QLineEdit()
        self.lbl_tol, self.input_tol = QLabel("Tolerancia:"), QLineEdit("0.0001")
        
        self.input_a.setStyleSheet("color: black; background-color: white;")
        self.input_b.setStyleSheet("color: black; background-color: white;")
        self.input_tol.setStyleSheet("color: black; background-color: white;")

        grid.addWidget(self.lbl_a, 2, 0); grid.addWidget(self.input_a, 2, 1)
        grid.addWidget(self.lbl_b, 2, 2); grid.addWidget(self.input_b, 2, 3)
        grid.addWidget(self.lbl_tol, 3, 0); grid.addWidget(self.input_tol, 3, 1)

        btn = QPushButton("Calcular Iteraciones")
        btn.setStyleSheet("font-weight: bold; background-color: #673AB7; color: white; padding: 10px;")
        btn.clicked.connect(self.calcular)
        layout.addWidget(btn)

        self.salida_html = QTextEdit()
        self.salida_html.setReadOnly(True)
        self.salida_html.setStyleSheet("color: black; background-color: white; font-family: monospace;")
        layout.addWidget(self.salida_html)
        self.actualizar_inputs()

    def actualizar_inputs(self):
        m = self.combo_metodo.currentText()
        self.lbl_b.setText("N/A") if "Newton" in m else self.lbl_b.setText("b:")
        self.input_b.setEnabled(not "Newton" in m)
        self.lbl_tol.setText("Intervalos n:") if "Trapecio" in m else self.lbl_tol.setText("Tolerancia:")

    def calcular(self):
        m, expr_str = self.combo_metodo.currentText(), self.input_fx.text().strip()
        if not expr_str: return
        try:
            x = sp.Symbol('x')
            f = sp.lambdify(x, sp.sympify(expr_str), 'numpy')
            # Inyectamos color black directamente en el HTML para evitar problemas de temas oscuros
            html = "<style>th, td, body { padding: 5px; text-align: right; border-bottom: 1px solid #ddd; color: black; }</style><table width='100%'>"
            
            if "Bisección" in m:
                a, b, tol = float(self.input_a.text()), float(self.input_b.text()), float(self.input_tol.text())
                html += "<tr style='background-color:#e0e0e0'><th>Iter</th><th>a</th><th>b</th><th>c</th><th>Error</th></tr>"
                c = a
                for i in range(1, 101):
                    c_old = c
                    c = (a + b) / 2
                    error = abs(c - c_old) if i > 1 else abs(b - a)
                    html += f"<tr><td>{i}</td><td>{a:.4f}</td><td>{b:.4f}</td><td><b>{c:.4f}</b></td><td>{error:.5f}</td></tr>"
                    if f(c) == 0 or error < tol: break
                    if f(c) * f(a) < 0: b = c
                    else: a = c

            elif "Newton" in m:
                x0, tol = float(self.input_a.text()), float(self.input_tol.text())
                df = sp.lambdify(x, sp.diff(sp.sympify(expr_str), x), 'numpy')
                html += "<tr style='background-color:#e0e0e0'><th>Iter</th><th>x_n</th><th>f(x_n)</th><th>Error</th></tr>"
                for i in range(1, 101):
                    x1 = x0 - f(x0) / df(x0)
                    error = abs(x1 - x0)
                    html += f"<tr><td>{i}</td><td><b>{x0:.6f}</b></td><td>{f(x0):.6f}</td><td>{error:.6f}</td></tr>"
                    if error < tol: break
                    x0 = x1

            elif "Trapecio" in m:
                a, b, n = float(self.input_a.text()), float(self.input_b.text()), int(self.input_tol.text())
                h = (b - a) / n
                suma = f(a) + f(b)
                for i in range(1, n): suma += 2 * f(a + i * h)
                html += f"</table><h3 style='color:black;'>Área Aproximada: {(h / 2) * suma:.6f}</h3>"
                self.salida_html.setHtml(html)
                return

            self.salida_html.setHtml(html + "</table>")
        except Exception as e: self.salida_html.setText(str(e))

# ==========================================
# MÓDULO 6: ÁLGEBRA LINEAL Y MATRICES
# ==========================================
class AlgebraLinealWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Ingrese matrices separando columnas por espacios y filas por 'Enter'."))
        
        splitter = QSplitter(Qt.Horizontal)
        
        grupo_a = QGroupBox("Matriz A"); layout_a = QVBoxLayout(grupo_a)
        self.input_a = QTextEdit()
        self.input_a.setPlaceholderText("Ej:\n1 2\n3 4")
        self.input_a.setStyleSheet("color: black; background-color: white;")
        layout_a.addWidget(self.input_a)
        splitter.addWidget(grupo_a)
        
        grupo_b = QGroupBox("Matriz B / Vector"); layout_b = QVBoxLayout(grupo_b)
        self.input_b = QTextEdit()
        self.input_b.setPlaceholderText("Ej:\n5 6\n7 8")
        self.input_b.setStyleSheet("color: black; background-color: white;")
        layout_b.addWidget(self.input_b)
        splitter.addWidget(grupo_b)
        
        layout.addWidget(splitter)

        panel = QHBoxLayout()
        self.combo_op = QComboBox()
        self.combo_op.setStyleSheet("color: black; background-color: white;")
        self.combo_op.addItems(["Determinante (A)", "Matriz Inversa (A)", "Suma (A+B)", "Multiplicación (A*B)", "Resolver Ax = B"])
        panel.addWidget(self.combo_op)
        btn = QPushButton("Calcular"); btn.setStyleSheet("font-weight: bold; background-color: #E91E63; color: white;")
        btn.clicked.connect(self.calcular); panel.addWidget(btn)
        layout.addLayout(panel)

        self.res_text = QTextEdit(); self.res_text.setReadOnly(True)
        # Este lo mantenemos tipo consola (verde sobre negro) porque se lee bien y luce profesional
        self.res_text.setStyleSheet("font-family: monospace; font-size: 16px; background-color: #222; color: #0f0;")
        layout.addWidget(self.res_text)

    def calcular(self):
        try:
            def parse(t): return np.array([list(map(float, l.split())) for l in t.replace(',',' ').strip().split('\n') if l.strip()]) if t.strip() else None
            A, B, op = parse(self.input_a.toPlainText()), parse(self.input_b.toPlainText()), self.combo_op.currentText()
            if A is None: return self.res_text.setText("Error: Matriz A vacía.")
            
            if "Determinante" in op: res = str(np.round(np.linalg.det(A), 6))
            elif "Inversa" in op: res = str(np.round(np.linalg.inv(A), 4))
            elif "Suma" in op: res = str(A + B)
            elif "Multiplicación" in op: res = str(A @ B)
            elif "Resolver" in op: res = "Solución Vector X:\n" + str(np.round(np.linalg.solve(A, B), 4))
            self.res_text.setText(res)
        except Exception as e: self.res_text.setText(f"Error: {e}")

# ==========================================
# MÓDULO 7: PROBABILIDAD Y ESTADÍSTICA
# ==========================================
class EstadisticaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout_principal = QVBoxLayout(self)
        self.tabs_internas = QTabWidget()
        layout_principal.addWidget(self.tabs_internas)

        # Sub-pestaña 1: Estadística Descriptiva
        tab_desc = QWidget()
        layout_desc = QVBoxLayout(tab_desc)
        
        layout_desc.addWidget(QLabel("Ingrese los datos separados por comas:"))
        self.input_datos = QLineEdit()
        self.input_datos.setPlaceholderText("Ej: 12, 15.5, 14, 18, 20, 12")
        self.input_datos.setStyleSheet("color: black; background-color: white;")
        layout_desc.addWidget(self.input_datos)
        
        btn_desc = QPushButton("Calcular Estadística Descriptiva y Graficar")
        btn_desc.setStyleSheet("font-weight: bold; background-color: #00BCD4; color: white;")
        btn_desc.clicked.connect(self.calcular_descriptiva)
        layout_desc.addWidget(btn_desc)

        splitter_desc = QSplitter(Qt.Horizontal)
        
        self.res_desc = QTextEdit()
        self.res_desc.setReadOnly(True)
        self.res_desc.setStyleSheet("color: black; font-size: 16px; padding: 10px; background-color: #f0f8ff;")
        splitter_desc.addWidget(self.res_desc)

        self.fig_desc = Figure(figsize=(5,4))
        self.canvas_desc = FigureCanvasQTAgg(self.fig_desc)
        self.ax_desc = self.fig_desc.add_subplot(111)
        splitter_desc.addWidget(self.canvas_desc)
        
        layout_desc.addWidget(splitter_desc)
        self.tabs_internas.addTab(tab_desc, "Estadística Descriptiva")

        # Sub-pestaña 2: Distribuciones de Probabilidad
        tab_prob = QWidget()
        layout_prob = QVBoxLayout(tab_prob)
        
        panel_prob = QGridLayout()
        layout_prob.addLayout(panel_prob)
        
        panel_prob.addWidget(QLabel("Distribución:"), 0, 0)
        self.combo_dist = QComboBox()
        self.combo_dist.setStyleSheet("color: black; background-color: white;")
        self.combo_dist.addItems(["Normal (Continua)", "Binomial (Discreta)", "Poisson (Discreta)"])
        self.combo_dist.currentTextChanged.connect(self.actualizar_prob_inputs)
        panel_prob.addWidget(self.combo_dist, 0, 1)

        self.lbl_p1_prob, self.input_p1_prob = QLabel("Media (μ):"), QLineEdit("0")
        self.lbl_p2_prob, self.input_p2_prob = QLabel("Desv. Estándar (σ):"), QLineEdit("1")
        self.input_p1_prob.setStyleSheet("color: black; background-color: white;")
        self.input_p2_prob.setStyleSheet("color: black; background-color: white;")
        
        panel_prob.addWidget(self.lbl_p1_prob, 1, 0); panel_prob.addWidget(self.input_p1_prob, 1, 1)
        panel_prob.addWidget(self.lbl_p2_prob, 2, 0); panel_prob.addWidget(self.input_p2_prob, 2, 1)

        panel_prob.addWidget(QLabel("Valor de x (para evaluar prob):"), 3, 0)
        self.input_x_prob = QLineEdit("0")
        self.input_x_prob.setStyleSheet("color: black; background-color: white;")
        panel_prob.addWidget(self.input_x_prob, 3, 1)

        btn_prob = QPushButton("Calcular Probabilidad y Graficar")
        btn_prob.setStyleSheet("font-weight: bold; background-color: #009688; color: white;")
        btn_prob.clicked.connect(self.calcular_probabilidad)
        layout_prob.addWidget(btn_prob)

        splitter_prob = QSplitter(Qt.Horizontal)
        self.res_prob = QTextEdit()
        self.res_prob.setReadOnly(True)
        self.res_prob.setStyleSheet("color: black; font-size: 16px; padding: 10px; background-color: #e0f2f1;")
        splitter_prob.addWidget(self.res_prob)

        self.fig_prob = Figure(figsize=(5,4))
        self.canvas_prob = FigureCanvasQTAgg(self.fig_prob)
        self.ax_prob = self.fig_prob.add_subplot(111)
        splitter_prob.addWidget(self.canvas_prob)
        
        layout_prob.addWidget(splitter_prob)
        self.tabs_internas.addTab(tab_prob, "Probabilidades")

    def calcular_descriptiva(self):
        try:
            texto = self.input_datos.text().replace(' ', '')
            datos = np.array([float(x) for x in texto.split(',') if x])
            if len(datos) == 0: return

            media, mediana = np.mean(datos), np.median(datos)
            varianza, dev_std = np.var(datos, ddof=1), np.std(datos, ddof=1)
            q1, q2, q3 = np.percentile(datos, [25, 50, 75])
            try: moda_val = stats.mode(datos, keepdims=True).mode[0]
            except: moda_val = "N/A"

            res = f"--- Medidas de Tendencia Central ---\nMedia (Promedio): {media:.4f}\nMediana: {mediana:.4f}\nModa: {moda_val}\n\n"
            res += f"--- Medidas de Dispersión ---\nVarianza (Muestral): {varianza:.4f}\nDesviación Estándar: {dev_std:.4f}\n\n"
            res += f"--- Posición ---\nCuartiles: Q1={q1:.2f}, Q2={q2:.2f}, Q3={q3:.2f}\n"
            self.res_desc.setText(res)

            self.ax_desc.clear()
            self.ax_desc.hist(datos, bins='auto', color='#00BCD4', edgecolor='black', alpha=0.7)
            self.ax_desc.set_title("Histograma de Frecuencias")
            self.ax_desc.grid(axis='y', linestyle='--', alpha=0.7)
            self.canvas_desc.draw()
        except Exception as e: self.res_desc.setText(f"Error: Verifique el formato.\n{e}")

    def actualizar_prob_inputs(self):
        dist = self.combo_dist.currentText()
        if "Normal" in dist:
            self.lbl_p1_prob.setText("Media (μ):"); self.input_p1_prob.setText("0")
            self.lbl_p2_prob.setText("Desviación Estándar (σ):"); self.input_p2_prob.setEnabled(True)
        elif "Binomial" in dist:
            self.lbl_p1_prob.setText("Ensayos (n):"); self.input_p1_prob.setText("10")
            self.lbl_p2_prob.setText("Prob. de Éxito (p):"); self.input_p2_prob.setText("0.5")
            self.input_p2_prob.setEnabled(True)
        elif "Poisson" in dist:
            self.lbl_p1_prob.setText("Tasa (λ - lambda):"); self.input_p1_prob.setText("5")
            self.lbl_p2_prob.setText("N/A:"); self.input_p2_prob.setEnabled(False)

    def calcular_probabilidad(self):
        try:
            dist, x_val = self.combo_dist.currentText(), float(self.input_x_prob.text())
            self.ax_prob.clear()

            if "Normal" in dist:
                mu, sigma = float(self.input_p1_prob.text()), float(self.input_p2_prob.text())
                d = stats.norm(loc=mu, scale=sigma)
                res = f"Distribución Normal N({mu}, {sigma})\n\nEsperanza E(X): {d.mean():.4f}\nVarianza V(X): {d.var():.4f}\n\n"
                res += f"P(X < {x_val}) (Acumulada): {d.cdf(x_val):.6f}\nP(X > {x_val}): {1 - d.cdf(x_val):.6f}\n"
                x_graf = np.linspace(mu - 4*sigma, mu + 4*sigma, 200)
                self.ax_prob.plot(x_graf, d.pdf(x_graf), 'b-', lw=2)
                self.ax_prob.fill_between(x_graf, d.pdf(x_graf), where=(x_graf <= x_val), color='blue', alpha=0.3)

            elif "Binomial" in dist:
                n, p = int(float(self.input_p1_prob.text())), float(self.input_p2_prob.text())
                x_val = int(x_val)
                d = stats.binom(n, p)
                res = f"Distribución Binomial B({n}, {p})\n\nEsperanza E(X): {d.mean():.4f}\nVarianza V(X): {d.var():.4f}\n\n"
                res += f"P(X = {x_val}) (Puntual): {d.pmf(x_val):.6f}\nP(X <= {x_val}) (Acumulada): {d.cdf(x_val):.6f}\n"
                x_graf = np.arange(0, n+1)
                self.ax_prob.vlines(x_graf, 0, d.pmf(x_graf), colors='b', lw=5, alpha=0.5)
                self.ax_prob.plot(x_val, d.pmf(x_val), 'ro')

            elif "Poisson" in dist:
                lam, x_val = float(self.input_p1_prob.text()), int(x_val)
                d = stats.poisson(lam)
                res = f"Distribución Poisson Poisson({lam})\n\nEsperanza E(X): {d.mean():.4f}\nVarianza V(X): {d.var():.4f}\n\n"
                res += f"P(X = {x_val}) (Puntual): {d.pmf(x_val):.6f}\nP(X <= {x_val}) (Acumulada): {d.cdf(x_val):.6f}\n"
                x_graf = np.arange(0, max(15, int(lam*3)))
                self.ax_prob.vlines(x_graf, 0, d.pmf(x_graf), colors='g', lw=5, alpha=0.5)
                self.ax_prob.plot(x_val, d.pmf(x_val), 'ro')

            self.res_prob.setText(res)
            self.ax_prob.grid(True, linestyle=':', alpha=0.6)
            self.canvas_prob.draw()
            
        except Exception as e: self.res_prob.setText(f"Error de cálculo: {e}")

# ==========================================
# APP PRINCIPAL INTEGRADORA
# ==========================================
class CalculadoraIntegralApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica Integral para Ingeniería - v1.0")
        self.resize(1200, 800)
        
        # Opcional: Forzar un estilo global base para combatir los dark themes de Linux
        self.setStyleSheet("""
            QWidget { color: black; }
            QToolTip { color: black; background-color: #ffffe0; border: 1px solid black; }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        self.init_modules()

    def init_modules(self):
        self.tab_calculadora = QWidget()
        self.tabs.addTab(self.tab_calculadora, "Calculadora")
        QVBoxLayout(self.tab_calculadora).addWidget(CalculadoraCientificaWidget())

        self.tab_algebra = QWidget()
        self.tabs.addTab(self.tab_algebra, "Álgebra")
        QVBoxLayout(self.tab_algebra).addWidget(AlgebraWidget())
        
        self.tab_analisis = QWidget()
        self.tabs.addTab(self.tab_analisis, "Análisis Matemático")
        QVBoxLayout(self.tab_analisis).addWidget(AnalisisMatematicoWidget())
        
        self.tab_metodos = QWidget()
        self.tabs.addTab(self.tab_metodos, "Métodos Numéricos")
        QVBoxLayout(self.tab_metodos).addWidget(MetodosNumericosWidget())

        self.tab_matrices = QWidget()
        self.tabs.addTab(self.tab_matrices, "Álgebra Lineal")
        QVBoxLayout(self.tab_matrices).addWidget(AlgebraLinealWidget())

        self.tab_estadistica = QWidget()
        self.tabs.addTab(self.tab_estadistica, "Estadística y Probabilidad")
        QVBoxLayout(self.tab_estadistica).addWidget(EstadisticaWidget())

        self.tab_graficos = QWidget()
        self.tabs.addTab(self.tab_graficos, "Graficación 2D Libre")
        QVBoxLayout(self.tab_graficos).addWidget(GraficosWidget())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculadoraIntegralApp()
    window.show()
    sys.exit(app.exec())