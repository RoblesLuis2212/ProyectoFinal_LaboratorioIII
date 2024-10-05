import os
import os.path as path
import time
import random

#Funcion que creara los archivos en caso de que no existan
def CrearArchivos():
    ArchivoGerente = open("Gerente.txt","w")
    ArchivoEmpleado = open("Empleados.txt","w")
    ArchivoContraseña = open("Contraseñas.txt","w")
    ArchivoCliente = open("Clientes.txt","w")
    ArchivoDireccion = open("Direccion.txt","w")
    ArchivoID = open("IdClientes.txt","w")
    ArchivoPedidos = open("Pedidos.txt","w")
    Precios = open("Precios.txt","w")
    
    #Cuando el sistema arranque por primera vez se solicitara al gerente que se registre
    UsuarioGerente = input("Ingrese un DNI: ")
    ContraseñaGerente = input("Ingrese una contraseña: ")
    ArchivoGerente.write(UsuarioGerente + '\n')
    ArchivoContraseña.write(ContraseñaGerente + '\n')
    print("Sistema Iniciado Correctamente")
    
    ArchivoGerente.close()
    ArchivoEmpleado.close()
    ArchivoContraseña.close()
    ArchivoCliente.close()
    ArchivoDireccion.close()
    ArchivoID.close()
    ArchivoPedidos.close()
    Precios.close()
    
    time.sleep(2)
    LimpiarConsola()
    MenuClientes()

#Funcion que limpia consola (¿Se ve en el nombre NO? No hacia falta el comentario)
def LimpiarConsola():
    os.system('cls')


#Funcion Registrarse
def Registro():
    print("------Registro-----")
    Nombre = input("Ingrese su DNI: ")
    if not Nombre:
        print("El campo no puede estar vacio")
        Registro()
    rol = input("Ingrese un rol: ")
    if not rol:
        print("El campo rol no puede estar vacio")
        Registro()

    LeerClientes = open("Clientes.txt","r")
    LeerContraseñas = open("Contraseñas.txt","r")

    ListaClientes = LeerClientes.readlines()
    ListaContraseñas = LeerContraseñas.readlines()

    if Nombre + '\n' in ListaClientes:
        LimpiarConsola()
        print("El Nombre de usuario ya existe, intentelo nuevamente")
        Registro()
    
    Clave = GenerarClave(rol)

    LeerGerente = open("Clientes.txt","a")
    LeerContraseñas = open("Contraseñas.txt","a")
    LeerGerente.write(Nombre + '\n')

    ContraseñaCifrada = cifrar_contraseña(Clave)
    LeerContraseñas.write(ContraseñaCifrada + '\n')

    
    
    LeerGerente.close()
    LeerContraseñas.close()
    print("Usuario generado correctamente,Gracias por elegirnos")
    print(f"Su contraseña es {Clave}")
    time.sleep(3)
    LimpiarConsola()
    MenuClientes()

#Esta funcion permitira al cliente ingresar al sistema
def LoginClientes():
    print("-----INICIAR SESION----")
    #Aqui solicitaremos los datos correspondientes para validar los datos (DNI y Contraseña)
    Usuario = input("Ingrese su DNI: ")
    #En caso de que los campos No esten vacios
    if not Usuario:
        LimpiarConsola()
        print("Error el campo no puede estar vacio")
        LoginClientes()
    Contraseña = input("Ingrese su contraseña: ")
    if not Contraseña:
        LimpiarConsola()
        print("Error el campo no puede estar vacio")
        LoginClientes()

    #Abrimos los archivos en modo lectura
    AbrirClientes = open("Clientes.txt","r")
    AbrirContraseñas = open("Contraseñas.txt","r")
    #Convertimos los archivos en listas
    ListaClientes = AbrirClientes.readlines()
    ListaContraseña = AbrirContraseñas.readlines()

    #Verificamos si los usuarios existen en los archivos
    if Usuario + '\n' in ListaClientes:
        indice = ListaClientes.index(Usuario + '\n') #Obtenemos el indice de la lista
        #Utilizamos la funcion 'descrifrar_contraseña' para poder validar las credenciales
        ContraseñaDescrifrada = descifrar_contraseña(ListaContraseña[indice].strip())
        if ContraseñaDescrifrada == Contraseña:
            LimpiarConsola()
            #Aqui se verifican las longitudes de las contraseñas para determinar el Rol del usuario
            if len(Contraseña) == 8:
                LimpiarConsola()
                MenuGerente()
            elif len(Contraseña) == 6:
                LimpiarConsola()
                MenuEmpleados()
            elif len(Contraseña) == 4:
                LimpiarConsola()
                MenuClientes()
    else:
        LimpiarConsola()
        print("Error usuario o contraseña incorrecta")
        LoginClientes()

#Esta funcion sera la que va a verificar que los archivos donde se almacenara la informacion existen
def Instalador(): #Si los archivos existen iniciara el sistema
    if path.exists("Gerente.txt"):
        print("Archivos encontrados accediendo al sistema...")
        time.sleep(2)
        LimpiarConsola()
        MenuInicio()
    else: #En caso de que no existan se crearan los archivos
        print("Archivo inexistentes...")
        print("Creando Archivos...")
        time.sleep(3)
        CrearArchivos()
        MenuInicio()
        print("Archivos creados exitosamente")

#Menu para clientes
def MenuClientes():
    print("------MENU DEL DIA-----")
    print("1.Menu De Comida")
    print("2.Realizar Pedido")
    print("3.Salir")
    opcion = int(input("Seleccione una opcion: "))
    
    if opcion == 1:
        LimpiarConsola()
        pass
    elif opcion == 2:
        LimpiarConsola()
        MenuComidas()
    elif opcion == 3:
        LimpiarConsola()
        MenuInicio()


#Menu de inicio del sistema (Para clientes)
def MenuInicio():
    print("----SISTEMA GASTRONOMICO-----")
    print("1.Iniciar Sesion")
    print("2.Registrarse")
    print("3.Salir")
    opcion = int(input("Seleccione una opcion: "))

    if opcion == 1:
        LimpiarConsola()
        LoginClientes()
    elif opcion == 2:
        LimpiarConsola()
        Registro()
    elif opcion == 3:
        LimpiarConsola()
        print("Hasta luego vuelva pronto")
        exit()


#Este es el menu de las comidas
def MenuComidas():
    print("----Menu Comidas----")
    #Abrimos los archivos en modo lectura
    ArchivoPlatos = open("Platos.txt","r")
    ArchivoPrecios = open("Precios.txt","r")
    
    #Convertimos a los archivos en listas
    Platos = ArchivoPlatos.readlines()
    Precios = ArchivoPrecios.readlines()

    #Inicializamos un indice en 0 y utilizamos un bucle while para recorrer la lista
    indice = 0
    while indice < len(Platos):
        print(f"{indice + 1} {Platos[indice].strip()}")
        indice = indice + 1
    ArchivoPlatos.close()
    
    #solicitamos al usuario que seleccione una opcion y manejamos los errores con un condicional (Se podria usar try-catch)
    opcion = int(input("Seleccione una opcion: "))
    if opcion < 1 or opcion > len(Platos):
        LimpiarConsola()
        print("Error opcion invalida")
        MenuComidas() #Se utiliza la recursividad para volver a llamar a mostrar el menu en caso de error
    
    #Agregamos los pedidos realizados a los archivos correspondientes
    AgregarComida = open("Pedidos.txt","a")
    AgregarPrecio = open("Precios.txt","a")
    AgregarComida.write(f"{Platos[opcion - 1].strip()}\n")
    AgregarPrecio.write(f"{Precios[opcion - 1].strip()}\n")

    #Preguntamos al usuario si desea seleccionar otro pedido
    Respuesta = input("¿Desea agregar otro plato o seleccionar otra porcion Mas?")
    if Respuesta == 'si':
        LimpiarConsola()
        MenuComidas()
    #En caso de seleccionar 'no'
    elif Respuesta == 'no':
        AgregarPrecio.close() #Cerramos el archivo para guardar los datos
        total = SumarPrecios() #El total del pedido se calcula llamando a la funcion 'SumarPrecios'
        LimpiarConsola()
        print(f"Pedido registrado exitosamente el total de la compra es {total}") #Se muestra el total por pantalla
        FormaDePago()

#Esta funcion calculara el monto total del pedido del cliente
def SumarPrecios():
    total = 0
    LeerPrecios = open("Precios.txt","r")
    for Linea in LeerPrecios:
        precio_str = Linea.strip().replace("$","")
        if precio_str:
            precio = float(precio_str)
            total += precio
    return total

#Esta funcion le permitira elegir al cliente de que manera abonar lo que consumira
def FormaDePago():
    print("----Seleccione Un Metodo De Pago-----")
    print("1.Efectivo")
    print("2.Transferencia")
    print("3.Debito")
    print("4.Credito")
    opcion = int(input("Seleccione El Metodo De Pago: "))
    if opcion >= 1 and opcion <= 4:
        print("Pago realizado correctamente")
        time.sleep(3)
        LimpiarConsola()
        GenerarID()

#Menu para Empleados
def Empleado():
    print("------BIENVENIDOS EMPLEADOS------")
    print("1.Registrar Venta")
    print("2.Salir")
    opcion = int(input("Seleccione una opcion: "))

    if opcion == 1:
        print("Venta Registrada, sigue asi esclavo")
    elif opcion == 2:
        exit()

#Esta funcion es la que mostrara los platos disponibles a los clientes
def MostrarPlatos():
    ArchivoPlatos = open("Platos.txt","r")
    Platos = ArchivoPlatos.readlines()

    if Platos:
        print("Los platos disponibles son: ")
        i = 0
        while i < len(Platos):
            print(f"{i}. {Platos[i].strip()}")
            i = i + 1
    else:
        print("No hay platos disponibles en el menu")

#Esta funcion agregara los platos includios en la lista del mismo nombre al archivo (Platos.txt)
def DefinirPlatos(platos):
    ArchivoPlatos = open("Platos.txt","a")
    indice = 0
    while indice < len(platos):
        ArchivoPlatos.write(f"{platos[indice]}\n")
        indice = indice + 1
    ArchivoPlatos.close()

#Generamos una lista con los platos por defecto (Modificables)
Platos = ["Fideo Tallarin Con Salsa","Guiso De Lentejas","Lomitos","Hamburguesas"]
DefinirPlatos(Platos)

#Esta funcion es la que permite al gerente poder modificar los platos disponibles
def ModificarPlatos(platos_modificar):
    MostrarPlatos()
    opcion = int(input("Seleccione el número de la opción que desea modificar: "))
    if opcion < 1 or opcion > len(Platos):
        print("Opción inválida.")
        return
    nuevo_nombre = input("Ingrese el nuevo nombre del plato: ")
    Platos[opcion - 1] = nuevo_nombre + '\n'
    DefinirPlatos(Platos)



#Esta funcion cifrara la contraseña generada
def cifrar_contraseña(clave):
    caracteres = "abcdefghijklmnopqrstuvwxyz"
    lista_plana = list(caracteres)
    lista_cifrada = lista_plana[::-1]  # Reversa de la lista plana

    cifrada = ""
    for char in clave:
        if char in lista_plana:
            index = lista_plana.index(char)
            cifrada += lista_cifrada[index]
        else:
            cifrada += char  # Mantener caracteres no alfabéticos sin cambios
    return cifrada

#Esta funcion es la que descifra la contraseña para poder validar el login
def descifrar_contraseña(contraseña_cifrada):
    caracteres = "abcdefghijklmnopqrstuvwxyz"
    lista_plana = list(caracteres)
    lista_cifrada = lista_plana[::-1]  # Reversa de la lista plana

    descifrada = ""
    for char in contraseña_cifrada:
        if char in lista_cifrada:
            index = lista_cifrada.index(char)
            descifrada += lista_plana[index]
        else:
            descifrada += char  # Mantener caracteres no alfabéticos sin cambios
    return descifrada


#Menu para gerentes
def MenuGerente():
    print("-----Bienvenido Gerente------")
    print("1.Modificar Plato")
    print("2.Total De Recaudacion")
    print("3.Salir")
    opcion = int(input("Seleccione una opcion: "))
    #Establecemos esta condicion para controlar los errores en caso de ingresar una opcion incorrecta
    if opcion < 1 or opcion > 4:
        LimpiarConsola()
        print("Error opcion invalida")
        MenuGerente()
    if opcion == 1:
        MostrarPlatos()
        IndicePlato = int(input("Seleccione el número del plato que desea modificar: "))
        ModificarPlatos(IndicePlato)
        LimpiarConsola()
        print("Plato modificado exitosamente.")
        LimpiarConsola()
        MenuGerente()
    if opcion == 2:
        LimpiarConsola()
        print(TotalRecaudado_Dia)
    
#Esta funcion pertenece al menu del gerente y mostrara el total recaudado al final del dia
def TotalRecaudado_Dia():
    Total = SumarPrecios()
    print(f"Lo total recaudado del dia es {Total}")
    time.sleep(3)
    LimpiarConsola()

#Menu correspondiente a los empleados
def MenuEmpleados():
    while True:
        print("-----MENU EMPLEADOS-----")
        print("1. Registrar Venta")
        print("2. Ver Total de Ventas")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            RegistrarVenta()
        elif opcion == "2":
            print("Funcionalidad no implementada")
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

#Funcion con la que empleado podra registrar una venta realizada
def RegistrarVenta():
    LimpiarConsola()
    print("Registrando venta aguarde un instante...")
    time.sleep(2)
    ArchivoVentas = open("Ventas.txt","a")
    ArchivoVentas.write("Venta realiza")

#Esta funcion generara una clave aleatoria cuando se registre un nuevo usuario
def GenerarClave(rol):

    Caracteres = 'abcdefghijklmnñopqrstuvwxyz'
    listaCaracteres = list(Caracteres)
    Clave = ''

    if rol == 'Gerente':
        longitud = 8
    elif rol == 'Empleado':
        longitud = 6
    elif rol == 'Cliente':
        longitud = 4

    i = 0
    while i < longitud:
        Clave = Clave + random.choice(listaCaracteres)
        i = i + 1

    return Clave

#Esta funcion generara un ID aleatorio al pedido del usuario 
def GenerarID():
    a = 0
    b = 99999999

    ID_Aleatorio = (random.randint(a,b))
    #Almacenamos el ID del pedido en un archivo
    GuardarID = open("IdClientes.txt","a")
    GuardarID.write(str(ID_Aleatorio) + '\n')
    LimpiarConsola()
    print("Generando ID aguarde un momento...")
    time.sleep(3)
    LimpiarConsola()
    print(f"ID generada correctamente su id es {ID_Aleatorio}")


Instalador()
