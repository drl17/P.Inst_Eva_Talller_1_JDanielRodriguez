import tkinter as tk
import mysql.connector

class CajeroAutomatico:
    def __init__(self, nombreproyecto):
        #Generamos el objeto (interfaz), le asignamos un tamaño y el nombre
        self.nombreproyecto = nombreproyecto
        self.nombreproyecto.geometry("400x300")
        self.nombreproyecto.title("Cajero Automático")

        #Se genera el mensaje de bienvenida
        self.mensaje_label = tk.Label(nombreproyecto, text="Bienvenido al cajero automático")
        self.mensaje_label.pack()
        
        # Generamos los botones para las diferentes funciones del cajero automático
        self.crear_cuenta_button = tk.Button(nombreproyecto, text="Crear Cuenta", command=self.crearcuenta)
        self.crear_cuenta_button.pack()
        
        self.iniciar_sesion_button = tk.Button(nombreproyecto, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.iniciar_sesion_button.pack()
        
        self.depositar_button = tk.Button(nombreproyecto, text="Depositar", command=self.depositar)
        self.depositar_button.pack()
        
        self.retirar_button = tk.Button(nombreproyecto, text="Retirar", command=self.retirar)
        self.retirar_button.pack()
        
        self.mostrar_saldo_button = tk.Button(nombreproyecto, text="Mostrar Saldo", command=self.mostrar_saldo)
        self.mostrar_saldo_button.pack()

        # Conexión a la base de datos MySQL
        self.conn = mysql.connector.connect(
            host="localhost",
            user="jdaniel_17",
            password="Unalmed_2010",
            database="PInst_Eva_Talller_1_Cajero"
        )
        self.c = self.conn.cursor()
        
        # Crear tabla de usuarios si no existe
        self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(50) NOT NULL UNIQUE,
                            password VARCHAR(50) NOT NULL,
                            saldo DECIMAL(10, 2) NOT NULL DEFAULT 0
                         )''')
                
    def crearcuenta(self):
        username = input("Por favor ingrese su nombre de usuario: ")

    # Verificar si el nombre de usuario ya existe en la base de datos
        
        self.c.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        if self.c.fetchone():
            print("El nombre de usuario ya existe. Por favor, elija un nuevo nombre de usuario.")
            return
        password = input("Ingrese su contraseña: ")
    # Insertar el nuevo usuario en la base de datos
        self.c.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
        self.conn.commit()
        print("Cuenta creada con éxito.")
    
    def iniciar_sesion(self):
        username = input("Ingrese su nombre de usuario: ")
        password = input("Ingrese su contraseña: ")
    # Verificar si el nombre de usuario y la contraseña coinciden en la base de datos
        self.c.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (username, password))
        if self.c.fetchone():
            print("Inicio de sesión exitoso.")
        # Continuar con las operaciones del cajero automático
        else:
            print("Nombre de usuario o contraseña incorrectos.")
    
    def depositar(self):
        username = input("Ingrese su nombre de usuario: ")
        cantidad = int(input("Ingrese la cantidad a depositar: "))
    # Verificar si el usuario existe en la base de datos
        self.c.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        usuario = self.c.fetchone()
        if usuario:
            saldo_actual = usuario[3]
            nuevo_saldo = saldo_actual + cantidad
        # Actualizar el saldo del usuario en la base de datos
            self.c.execute("UPDATE usuarios SET saldo = %s WHERE username = %s", (nuevo_saldo, username))
            self.conn.commit()
            print(f"Depósito de ${cantidad} realizado con éxito. Saldo actual: ${nuevo_saldo}")
        else:
            print("Usuario no encontrado.")

    def retirar(self):
        username = input("Ingrese su nombre de usuario: ")
        cantidad = int(input("Ingrese la cantidad a retirar: "))
        # Verificar si el usuario existe en la base de datos
        self.c.execute("SELECT * FROM usuarios WHERE username = %s", (username,))
        usuario = self.c.fetchone()
        if usuario:
            saldo_actual = usuario[3]
            if saldo_actual >= cantidad:
                nuevo_saldo = saldo_actual - cantidad
                # Actualizar el saldo del usuario en la base de datos
                self.c.execute("UPDATE usuarios SET saldo = %s WHERE username = %s", (nuevo_saldo, username))
                self.conn.commit()
                print(f"Retiro de ${cantidad} realizado con éxito. Su saldo actual es: ${nuevo_saldo}")
            else:
                print("Saldo insuficiente. Por favor consulte su saldo nuevamente para retirar una cantidad adecuada.")
        else:
            print("Usuario no encontrado.")

    def mostrar_saldo(self):
        username = input("Ingrese su nombre de usuario: ")
        # Obtener el saldo del usuario desde la base de datos
        self.c.execute("SELECT saldo FROM usuarios WHERE username = %s", (username,))
        resultado = self.c.fetchone()
        if resultado:
            saldo_actual = resultado[0]
            print(f"Su saldo actual es: ${saldo_actual}")
        else:
            print("Usuario no encontrado.")

# Inicializar la aplicación
nombreproyecto = tk.Tk()
cajero_app = CajeroAutomatico(nombreproyecto)
nombreproyecto.mainloop()