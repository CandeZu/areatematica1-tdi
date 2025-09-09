import tkinter as tk
from tkinter import messagebox

#Para calcular el valor que debe tener el dígito identificador a partir de los valores anteriores,
#Se deben de sumar los primeros 4 dígitos del cuit multimplicandolos por 5, 4, 3 y 2 respectivamente
#Y a eso sumarle la suma de los 6 siguientes dígitos del cuit multiplicados por 7, 6, 5, 4, 3 y 2 respectivamente
#Posteriormente al resultado se calcula su módulo 11.
#Y finalmente el valor resultante se divide por 11.
#De este último valor dependerá el dígito verificador:
# Si es 11, el dígito verificador será 0.
# Si es 10, el dígito verificador será 1.
# Si es 0, se deben de cambiar los primeros 2 valores por 23 y recalcular.
# Caso contrario, este valor será dígito verificador.
#Si no se cumple este valor para los datos ingresados, entonces el cuit ingresado está mal.

#Por ejemplo, para los primeros valores del cuit es 2012345678 el valor que se debe obtener es: 
#2 *5 + 0*4 + 1*3 + 2*2 + 3*7 + 4*6 + 5*5 + 6*4 + 7*3 + 8*2 = 
#148, a este valor ahora hay que sacar su módulo 11: 148 % 11 = 5
#Y a este valor le restamos 11: 11 - 5 = 6
#El dígito verificador es 6 por lo que el cuit es 20-12345678-6.

def validar_cuit(cuit):
    """
    Valida un número de CUIT/CUIL de Argentina.
    Retorna True si es válido, False en caso contrario.
    """
    # 1. Verifica que el CUIT tenga 11 dígitos y sea numérico.
    if not cuit.isdigit() or len(cuit) != 11:
        return False

    # 2. Separa los componentes del CUIT.

    base = cuit[:-1] # Los primeros 10 dígitos.
    digito_verificador = int(cuit[-1]) # El último dígito.

    # 3. Calcula el dígito verificador real.
    # Serie de coeficientes para la multiplicación.
    serie = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2] 
    suma = 0
    for i in range(10):
        suma += int(base[i]) * serie[i] 

    resto = suma % 11
    calculado = 11 - resto
    if calculado == 11:
        calculado = 0 
    elif calculado == 10:
        calculado = 9 # En este caso, el CUIT es inválido.

    # 4. Compara el dígito calculado con el ingresado.
    return calculado == digito_verificador

def verificar_cuit_ingresado():
    """
    Toma el valor del campo de entrada, lo valida y muestra
    un mensaje con el resultado.
    """
    cuit_ingresado = entry_cuit.get()
    if validar_cuit(cuit_ingresado):
        messagebox.showinfo("Resultado", f"El CUIT/CUIL '{cuit_ingresado}' es VÁLIDO.")
    else:
        messagebox.showerror("Resultado", f"El CUIT/CUIL '{cuit_ingresado}' es INVÁLIDO.")

# Ventana Principal

ventana = tk.Tk()
ventana.title("Validador de CUIT/CUIL")
ventana.geometry("350x150") # Tamaño de la ventana (ancho x alto)
ventana.resizable(False, False) # Evita que se pueda cambiar el tamaño.


label_instruccion = tk.Label(ventana, text="Ingrese el CUIT/CUIL (sin guiones):")
label_instruccion.pack(pady=10) 

entry_cuit = tk.Entry(ventana, width=20, font=("Arial", 12))
entry_cuit.pack(pady=5)

boton_validar = tk.Button(ventana, text="Validar", command=verificar_cuit_ingresado)
boton_validar.pack(pady=10)

#Mantiene la ventana abierta
ventana.mainloop()