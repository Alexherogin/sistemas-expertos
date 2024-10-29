import re
import tkinter as tk
from tkinter import ttk
import itertools

class Nodo:
    def __init__(self, valor, izquierda=None, derecha=None):
        self.valor = valor
        self.izquierda = izquierda
        self.derecha = derecha

def descomponer_proposicion(proposicion):
    partes = re.split(r'\s+(y|and|o|or)\s+', proposicion)
    proposiciones_simples = []
    operador = None

    for parte in partes:
        if parte.lower() in ["y", "and"]:
            operador = "AND"
        elif parte.lower() in ["o", "or"]:
            operador = "OR"
        else:
            proposiciones_simples.append(parte.strip())

    return proposiciones_simples, operador

def construir_arbol(proposiciones_simples, operador):
    if operador == "AND":
        return Nodo(proposiciones_simples[0], 
                    Nodo("Verdadero", Nodo(proposiciones_simples[1], Nodo("Verdadero"), Nodo("Falso"))),
                    Nodo("Falso", Nodo(proposiciones_simples[1], Nodo("Verdadero"), Nodo("Falso"))))
    elif operador == "OR":
        return Nodo(proposiciones_simples[0], 
                    Nodo("Verdadero", Nodo(proposiciones_simples[1], Nodo("Verdadero"), Nodo("Falso"))),
                    Nodo("Falso", Nodo(proposiciones_simples[1], Nodo("Verdadero"), Nodo("Falso"))))
    return None

def evaluar_proposicion(proposiciones_simples, operador):
    valores = []
    for proposicion in proposiciones_simples:
        while True:
            valor = input(f"¿Es '{proposicion}' verdadera o falsa? (true/false): ").strip().lower()
            if valor in ["true", "false"]:
                valores.append(valor == "true")
                break
            else:
                print("Por favor, ingresa 'true' o 'false'.")

    if operador == "AND":
        resultado = all(valores)
    elif operador == "OR":
        resultado = any(valores)
    else:
        resultado = None

    return resultado, valores

def imprimir_arbol(nodo, nivel=0):
    if nodo is not None:
        imprimir_arbol(nodo.derecha, nivel + 1)
        print(' ' * 4 * nivel + '-> ' + nodo.valor)
        imprimir_arbol(nodo.izquierda, nivel + 1)

def dibujar_arbol(canvas, nodo, x, y, dx, dy, valores, nivel=0):
    if nodo is not None:
        color = "red" if (nivel == 0 and valores[0]) else "blue" if (nivel == 1) else "black"
        canvas.create_text(x, y, text=nodo.valor, font=("Arial", 12, "bold"), fill=color)
        if nodo.izquierda:
            canvas.create_line(x, y, x - dx, y + dy, arrow=tk.LAST, fill="red" if (nivel == 0 and valores[0]) else "blue" if (nivel == 1 and valores[1]) else "green" if (nivel == 2 and valores[1]) else "black")
            dibujar_arbol(canvas, nodo.izquierda, x - dx, y + dy, dx // 2, dy, valores, nivel + 1)
        if nodo.derecha:
            canvas.create_line(x, y, x + dx, y + dy, arrow=tk.LAST, fill="red" if (nivel == 0 and not valores[0]) else "blue" if (nivel == 2 and not valores[1]) else "green" if (nivel == 1 and valores[1]) else "black")
            dibujar_arbol(canvas, nodo.derecha, x + dx, y + dy, dx // 2, dy, valores, nivel + 1)

def mostrar_arbol_grafico(arbol, valores):
    ventana = tk.Tk()
    ventana.title("Árbol de Estados")
    canvas = tk.Canvas(ventana, width=800, height=600, bg="white")
    canvas.pack()
    dibujar_arbol(canvas, arbol, 400, 50, 200, 100, valores)
    ventana.mainloop()

def generar_tabla_verdad(proposiciones_simples, operador):
    variables = ['p', 'q']
    combinations = list(itertools.product([True, False], repeat=len(proposiciones_simples)))

    def evaluate_proposition(*args):
        if operador == "AND":
            return all(args)
        elif operador == "OR":
            return any(args)
        return None

    truth_table = []
    for combination in combinations:
        result = evaluate_proposition(*combination)
        truth_table.append((*combination, result))

    return truth_table

def mostrar_tabla_verdad(truth_table):
    ventana = tk.Tk()
    ventana.title("Tabla de Verdad")
    tree = ttk.Treeview(ventana, columns=[f"p{i+1}" for i in range(len(truth_table[0])-1)] + ["Resultado"], show="headings")
    for i in range(len(truth_table[0])-1):
        tree.heading(f"p{i+1}", text=f"p{i+1}")
    tree.heading("Resultado", text="Resultado")

    for row in truth_table:
        tree.insert("", tk.END, values=row)

    tree.pack()
    ventana.mainloop()

# Ejemplo de uso
num_proposiciones = int(input("¿Cuántas proposiciones deseas evaluar? "))
proposiciones = []
for i in range(num_proposiciones):
    proposicion = input(f"Introduce la proposición {i+1}: ")
    proposiciones.append(proposicion)

proposicion_compuesta = " y ".join(proposiciones)
proposiciones_simples, operador = descomponer_proposicion(proposicion_compuesta)
arbol = construir_arbol(proposiciones_simples, operador)
resultado, valores = evaluar_proposicion(proposiciones_simples, operador)

print("Árbol de proposiciones:")
imprimir_arbol(arbol)

print("\nResultado de la evaluación:", resultado)
mostrar_arbol_grafico(arbol, valores)

tabla_verdad = generar_tabla_verdad(proposiciones_simples, operador)
mostrar_tabla_verdad(tabla_verdad)
