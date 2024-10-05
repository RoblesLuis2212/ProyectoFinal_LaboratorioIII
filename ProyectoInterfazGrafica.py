from tkinter import *
from tkinter import messagebox
import os
import random
import os.path as path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Funcion que registrara al usuario tomando los datos de los textbox
def RegistrarUsuario(get_nombre,get_apellido,get_rol):
    nombre = get_nombre()
    apellido = get_apellido()
    rol = get_rol()
    ArchivoLogin = open("Login.txt","r")
    ListaLogin = ArchivoLogin.readlines()
    login = nombre + apellido
    if login + '\n' in ListaLogin:
        messagebox.showerror("Error","Usuario Ya Registrado")
        return
    else:
        if nombre  ==  "" and apellido == "" or rol == "":
            messagebox.showwarning("Advertencia","Advertencia,debe completar todos los campos")
        else:
            contraseña = GenerarContraseña(rol)
        ObtenerLogin(nombre,apellido,contraseña)

        #Mostramos el login y el usuario generado al usuario
        messagebox.showinfo("Informacion",f"Usuario generado correctamente \nLogin : {nombre + apellido}\nContraseña: {contraseña}")
        VentanaRegistro.destroy()
        root.deiconify()



#Diseño del menu empleados
def Menu_Empleados():
    #Diseño del SubMenu
    def SubMenuEmpleado():
        def Consultar_Pedido():
            id_pedido = EntradaID.get()
            login = EntradaLogin.get()
            Archivo_Pedidos = open("IDPedidos.txt","r")
            ArchivoLogin = open("Login.txt","r")
            ListaLogin = ArchivoLogin.readlines()
            ListaPedidos = Archivo_Pedidos.readlines()

            if id_pedido + '\n' in ListaPedidos and login + '\n' in ListaLogin :
                messagebox.showinfo("Informacion","Pedido registrado correctamente")
                Archivo_Ventas = open("Ventas.txt","a")
                Archivo_Ventas.write("Pedido con id "+id_pedido +' realizado por '+ login + '\n')
                Archivo_Ventas.close()

                ListaPedidos.remove(id_pedido + '\n')

                Archivo_Pedidos = open("IDPedidos.txt","w")
                Archivo_Pedidos.writelines(ListaPedidos)
                Archivo_Pedidos.close()
            else:
                messagebox.showerror("Error","Error,codigo de pedido inexistente o login incorrecto")

        global MenuRegistrarPedido
        MenuRegistrarPedido = Toplevel()
        MenuRegistrarPedido.title("Registrar Pedido")
        MenuRegistrarPedido.geometry("300x180")

        titulosubmenu = Label(MenuRegistrarPedido,text="Ingrese el ID del pedido",font=("verdana",10))
        titulosubmenu.place(x=80,y=20)

        EntradaID = Entry(MenuRegistrarPedido)
        EntradaID.place(x=100,y=50)

        labelLogin = Label(MenuRegistrarPedido,text="Login",font=("verdana",10))
        labelLogin.place(x=140,y=75)

        EntradaLogin = Entry(MenuRegistrarPedido)
        EntradaLogin.place(x=100,y=100)

        boton_consultar = Button(MenuRegistrarPedido,text="Consultar",command=Consultar_Pedido)
        boton_consultar.place(x=130,y=130)

    #Diseño del menu principal empleados
    global Ventana_Empleados
    Ventana_Empleados = Toplevel()
    Ventana_Empleados.title("Menu Empleados")
    Ventana_Empleados.geometry("600x400")
    Ventana_Empleados.config(bg="grey")


    titulo = Label(Ventana_Empleados,text="Menu Empleados",font=("verdana",15),bg="grey")
    titulo.place(x=230,y=20)

    boton_registrarPedido = Button(Ventana_Empleados,text="Registrar Pedido",width=25,height=2,command=SubMenuEmpleado)
    boton_registrarPedido.place(x=220,y=250)


    
#Ventana Del Menu De Comidas
def Ventana_MenuComidas():
    
    root.withdraw()

    #Esta funcion es la que agregara y mostrara el precio total del pedido en un Label
    def Agregar_Pedidos(plato,precio):
        global cantidad_pedidos,Total_Precio
        if cantidad_pedidos <= 10:
            lista_pedidos.insert(END,f"{plato} - {precio}")
            cantidad_pedidos = cantidad_pedidos + 1
            Total_Precio += int(precio)
            label_total.config(text=f"Total: ${Total_Precio}")
        else:
            messagebox.showinfo("Informacion","Se alcanzo el numero maximo de pedidos")

    #Se llamara a esta funcion cuando el usuario termine de seleccionar su pedido
    def Finalizar_Pedidos():
        ArchivoRecaudacion = open("Recaudacion.txt","a")
        ArchivoRecaudacion.write(str(Total_Precio) + '\n')
        direccion = EntradaDireccion.get()
        ArchivoDireccion = open("Direcciones.txt","a")
        ArchivoDireccion.write(direccion + '\n')
        id_Pedido = GenerarId_Pedido()
        Capturar_Seleccion()
        messagebox.showinfo("Informacion",f"Pedido registrado correctamente,su ID es {id_Pedido}")
    
    #Diseño del menu de comida
    global VentanaMenu
    VentanaMenu = Toplevel()
    VentanaMenu.title("Menu Comidas")
    VentanaMenu.geometry("700x540")
    # VentanaMenu.resizable(0,0)

    #Variables que tomaran el valor de los checkbox
    metodo_transferencia = IntVar()
    metodo_Debito = IntVar()
    metodo_Efectivo = IntVar()


    primerframe = Frame(VentanaMenu,bg="blue",width=700,height=100)
    primerframe.place(x=0,y=0)

    TituloMenu = Label(primerframe,text="Menu De Comidas",font=("verdana",16),bg="blue")
    TituloMenu.place(x=200,y=40)

    labelComidas = Label(VentanaMenu,text="Comidas",bg="red",font=("verdana",12))
    labelComidas.place(x=50,y=120)

    labelPrecios = Label(VentanaMenu,text="Precios",bg="red",font=("verdana",12))
    labelPrecios.place(x=270,y=120)

    labelOpcion = Label(VentanaMenu,text="Opcion",bg="red",font=("verdana",12))
    labelOpcion.place(x=430,y=120)

    labelMetodo = Label(VentanaMenu,text="Forma De Pago",bg="red",font=("verdana",12))
    labelMetodo.place(x=550,y=120)


    #Estas listas son las que contienen datos de los platos que se muestran en el Menu Cliente
    # Platos = ["Hamburguesa XXL","Guiso De Lentejas","Sandwich De Milanesa","Bombitas De Carne"]
    # Precios = ["5999","3000","4999","3500"]
    

    #El contenido de esta funcion se debe incluir dentro de la funcion instalador
    def Guardar_En_Archivos(platos,precios):
        Archivo_Platos = open("Platos.txt","w")
        Archivo_Precios = open("Precios.txt","w")

        i = 0
        while i < len(platos):
            Archivo_Platos.write(platos[i] + '\n')
            Archivo_Precios.write(precios[i] + '\n')
            i = i + 1
        Archivo_Platos.close()
        Archivo_Precios.close()
    # Guardar_En_Archivos(Platos,Precios)

    Archivo_Platos = open("Platos.txt","r")
    Archivo_Precios = open("Precios.txt","r")

    platos = Archivo_Platos.readlines()
    precios = Archivo_Precios.readlines()


    comida1 = Label(VentanaMenu,text=platos[0])
    comida1.place(x=50,y=160)

    comida2 = Label(VentanaMenu,text=platos[1])
    comida2.place(x=50,y=200)

    comida3 = Label(VentanaMenu,text=platos[2])
    comida3.place(x=50,y=240)

    comida4 = Label(VentanaMenu,text=platos[3])
    comida4.place(x=50,y=275)

    precio1 = Label(VentanaMenu,text=precios[0])
    precio1.place(x=280,y=155)

    precio2 = Label(VentanaMenu,text=precios[1])
    precio2.place(x=280,y=190)

    precio3 = Label(VentanaMenu,text=precios[2])
    precio3.place(x=280,y=235)

    precio4 = Label(VentanaMenu,text=precios[3])
    precio4.place(x=280,y=275)
    
    boton_agregar = Button(VentanaMenu,text="Agregar",command=lambda: Agregar_Pedidos(platos[0],precios[0]))
    boton_agregar.place(x=435,y=150)

    boton_agregar1 = Button(VentanaMenu,text="Agregar",command=lambda: Agregar_Pedidos(platos[1],precios[1]))
    boton_agregar1.place(x=435,y=180)

    boton_agregar2 = Button(VentanaMenu,text="Agregar",command=lambda: Agregar_Pedidos(platos[2],precios[2]))
    boton_agregar2.place(x=435,y=220)

    boton_agregar3 = Button(VentanaMenu,text="Agregar",command=lambda: Agregar_Pedidos(platos[3],precios[3]))
    boton_agregar3.place(x=435,y=265)

    
    radioTransferencia = Checkbutton(VentanaMenu,text="Transferencia",variable=metodo_transferencia)
    radioTransferencia.place(x=560,y=150)

    radioTarjetaDebito = Checkbutton(VentanaMenu,text="Tarjeta De Debito",variable=metodo_Debito)
    radioTarjetaDebito.place(x=560,y=180)

    radioEfectivo = Checkbutton(VentanaMenu,text="Efectivo",variable=metodo_Efectivo)
    radioEfectivo.place(x=560,y=210)

    labelDireccion = Label(VentanaMenu,text="Direccion")
    labelDireccion.place(x=560,y=250)

    EntradaDireccion = Entry(VentanaMenu)
    EntradaDireccion.place(x=560,y=270)


    lista_pedidos = Listbox(VentanaMenu)
    lista_pedidos.place(x=50, y=320, width=500, height=150)

    label_total = Label(VentanaMenu,text=f"Total: ${Total_Precio}",font=("verdana",12))
    label_total.place(x=50,y=490)

    borde_frame = Frame(VentanaMenu,bg="red",padx=2,pady=2,relief="raised",bd=3)
    borde_frame.place(x=190,y=480)

    boton_finalizar = Button(borde_frame,text="Finalizar Pedido",width=15,bg="white",fg="black",font=("Arial",10,"bold"),relief="flat",padx=10,pady=5,command=Finalizar_Pedidos)
    boton_finalizar.pack()

    boton_eliminar = Button(VentanaMenu,text="Eliminar",command=lambda:Eliminar_Pedido(lista_pedidos))
    boton_eliminar.place(x=560,y=320)

    def Eliminar_Pedido(listbox):
        seleccion = listbox.curselection()
        if seleccion:
            listbox.delete(seleccion[0])
            Actualizar_total()

    def Actualizar_total():
        global Total_Precio,cantidad_pedidos
        Total_Precio = 0
        cantidad_pedidos = 0

        for pedido in lista_pedidos.get(0,END):
            plato,precio = pedido.split("-")
            Total_Precio += int(precio)
            cantidad_pedidos += 1
        label_total.config(text=f"Total:{Total_Precio}") 




    #Esta funcion es la que va a capturar los valores seleccionados por el usuario
    def Capturar_Seleccion():
        Seleccionados = []
        if metodo_transferencia.get() == 1:
            Seleccionados.append("Transferencia")
        if metodo_Debito.get() == 1:
            Seleccionados.append("Tarjeta De Debito")
        if metodo_Efectivo.get() == 1:
            Seleccionados.append("Efectivo")
        print("El metodo seleccionado es: ",Seleccionados)


    #Esta funcion va a generar un ID aleatorio al pedido del usuario    
    def GenerarId_Pedido():
        Numeros = "0123456789"
        ListaNumeros = list(Numeros)
        ID = ""
        i = 0

        while i < 6:
            digito = random.choice(ListaNumeros)
            ID += digito
            i = i + 1
        Archivo_Id_Pedidos = open("IDPedidos.txt","a")
        Archivo_Id_Pedidos.write(ID + '\n')
        Archivo_Id_Pedidos.close()
        return ID

#Este es el menu del Gerente (Se ve en el nombre de la funcion no hacia falta escribirlo)
def MenuGerente():
    #Funcion que mostrar una ventana donde el gerente registrara a los empleados
    def RegistrarEmpleado():
        #Diseño de ventana de registro de empleados (Menu Gerente)
        global VentanaRegistroEmpleado
        VentanaRegistroEmpleado = Toplevel()
        VentanaRegistroEmpleado.title("Registro Empleado")
        VentanaRegistroEmpleado.geometry("600x400")
        VentanaRegistroEmpleado.config(bg="purple1")

        tituloVentana = Label(VentanaRegistroEmpleado,text="Registro Empleados",font=("verdana",18),bg="purple1")
        tituloVentana.place(x=180,y=20)

        Nombre_Empleado = Label(VentanaRegistroEmpleado,text="Nombre: ",font=("verdana",12),bg="purple1")
        Nombre_Empleado.place(x=200,y=240)

        ApellidoEmpleado = Label(VentanaRegistroEmpleado,text="Apellido: ",font=("verdana",12),bg="purple1")
        ApellidoEmpleado.place(x=200,y=270)

        Entrada_Nombre = Entry(VentanaRegistroEmpleado)
        Entrada_Nombre.place(x=285,y=240)

        Entrada_Apellido = Entry(VentanaRegistroEmpleado)
        Entrada_Apellido.place(x=285,y=270)

        imagen = PhotoImage(file="empleado.png")
        imagen_modi = imagen.subsample(4,4)

        myLabel = Label(VentanaRegistroEmpleado,image=imagen_modi,bg="purple1")
        myLabel.image = imagen_modi

        myLabel.place(x=230,y=80)

        boton_Registrar = Button(VentanaRegistroEmpleado,text="Registrar",width=25,height=2,command=lambda:RegistrarUsuario(Entrada_Nombre.get,Entrada_Apellido.get,lambda: "Empleado"))
        boton_Registrar.place(x=215,y=300)

    #Diseño de la interfaz para la modificacion de los platos
    def ModificarPlatos():
        global Ventana_ModificarPlatos
        Ventana_ModificarPlatos = Toplevel()
        Ventana_ModificarPlatos.title("Modificar Platos")
        Ventana_ModificarPlatos.geometry("800x400")
        Ventana_ModificarPlatos.config(bg="DarkOrange1")

        titulo = Label(Ventana_ModificarPlatos,text="Modificacion De Platos",font=("verdana",18),bg="DarkOrange1")
        titulo.place(x=270,y=30)

        imagen = PhotoImage(file="modiplato.png")
        imagen_modi = imagen.subsample(4,4)

        myLabel = Label(Ventana_ModificarPlatos,image=imagen_modi,bg="DarkOrange1")
        myLabel.image = imagen_modi

        myLabel.place(x=300,y=80)

        labelPlato = Label(Ventana_ModificarPlatos,text="Plato 1",bg="DarkOrange1",font=("verdana",12))
        labelPlato.place(x=75,y=210)

        EntradaPlato = Entry(Ventana_ModificarPlatos)
        EntradaPlato.place(x=50,y=230)

        labelPrecio = Label(Ventana_ModificarPlatos,text="Precio 1",bg="DarkOrange1",font=("verdana",12))
        labelPrecio.place(x=75,y=250)

        EntradaPrecio = Entry(Ventana_ModificarPlatos)
        EntradaPrecio.place(x=50,y=270)


        labelPlato2 = Label(Ventana_ModificarPlatos,text="Plato 2",bg="DarkOrange1",font=("verdana",12))
        labelPlato2.place(x=250,y=210)

        EntradaPlato2 = Entry(Ventana_ModificarPlatos)
        EntradaPlato2.place(x=220,y=230)

        labelPrecio2 = Label(Ventana_ModificarPlatos,text="Precio 2: ",bg="DarkOrange1",font=("verdana",12))
        labelPrecio2.place(x=248,y=250)

        EntradaPrecio2 = Entry(Ventana_ModificarPlatos)
        EntradaPrecio2.place(x=220,y=270)

        labelPlato3 = Label(Ventana_ModificarPlatos,text="Plato 3",bg="DarkOrange1",font=("verdana",12))
        labelPlato3.place(x=420,y=210)

        EntradaPlato3 = Entry(Ventana_ModificarPlatos)
        EntradaPlato3.place(x=400,y=230)

        labelPrecio3 = Label(Ventana_ModificarPlatos,text="Precio 3",bg="DarkOrange1",font=("verdana",12))
        labelPrecio3.place(x=420,y=250)

        EntradaPrecio3 = Entry(Ventana_ModificarPlatos)
        EntradaPrecio3.place(x=400,y=270)

        labelPlato4 = Label(Ventana_ModificarPlatos,text="Plato 4",bg="DarkOrange1",font=("verdana",12))
        labelPlato4.place(x=600,y=210)

        EntradaPlato4 = Entry(Ventana_ModificarPlatos)
        EntradaPlato4.place(x=570,y=230)

        labelPrecio4 = Label(Ventana_ModificarPlatos,text="Precio 4",bg="DarkOrange1",font=("verdana",12))
        labelPrecio4.place(x=600,y=250)

        EntradaPrecio4 = Entry(Ventana_ModificarPlatos)
        EntradaPrecio4.place(x=570,y=270)

        boton_Modificar = Button(Ventana_ModificarPlatos,text="Modificar",width=25,height=2,command=lambda: Modificar(EntradaPlato.get(),EntradaPrecio.get(),EntradaPlato2.get(),EntradaPrecio2.get(),EntradaPlato3.get(),EntradaPrecio3.get(),EntradaPlato4.get(),EntradaPrecio4.get()))
        boton_Modificar.place(x=285,y=320)

        def Modificar(plato,precio,plato2,precio2,plato3,precio3,plato4,precio4):
            if '' in [plato,precio,plato2,precio2,plato3,precio3,plato4,precio4]:
                messagebox.showerror("Error","Error por favor complete todos los campos")
            else:
                ArchivoPlatos = open("Platos.txt","w")
                ArchivoPrecios = open("Precios.txt","w")

                platos = [plato,plato2,plato3,plato4]
                precios = [precio,precio2,precio3,precio4]

                i = 0
                while i < len(platos):
                    ArchivoPlatos.write(platos[i] + '\n')
                    ArchivoPrecios.write(precios [i] + '\n')
                    i = i + 1

                ArchivoPlatos.close()
                ArchivoPrecios.close()
                messagebox.showinfo("Informacion","Platos Modificados Correctamente")
                Ventana_ModificarPlatos.destroy()
                MenuGerente()
    #Ventana Que permitira al gerente restablecer las contraseñas
    def RestablecerContraseñas():
        
        # def Verificar_Usuario():
        #     ArchivoLogin = open("Login.txt","r")
        #     ArchivoContraseñas = open("Contraseñas.txt","r")

        #     ListaLogin = ArchivoLogin.readlines()
        #     ListaContraseña = ArchivoContraseñas.readlines()

        #     Nombre = EntradaNombre.get()
        #     Apellido = EntradaApellido.get()
        #     Rol = EntradaRol.get()

        #     Login = Nombre + Apellido

        #     if Login + '\n' in ListaLogin:
        #        indice = ListaLogin.index(Login + '\n')
        #        respuesta = messagebox.askyesno("Confirmar","¿Esta seguro que desea restablecer la contraseña de este usuario?")
        #        if respuesta:
        #            nueva_contraseña = GenerarContraseña(Rol)
        #            ListaContraseña[indice] = nueva_contraseña

        #            ArchivoContraseñas = open("Contraseñas.txt","w")
        #            ArchivoContraseñas.write(nueva_contraseña)
        #            ArchivoContraseñas.close()
                   
        #            messagebox.showinfo("Informacion",f"La nueva contraseña es {nueva_contraseña}")
        #     else:
        #         print("Usuario inexistente")
        global Ventana_Restablecer_Contraseñas
        Ventana_Restablecer_Contraseñas = Toplevel()
        Ventana_Restablecer_Contraseñas.title("Restablecer Contraseñas")
        Ventana_Restablecer_Contraseñas.geometry("600x500")
        Ventana_Restablecer_Contraseñas.config(bg="cadet blue")

        Titulo = Label(Ventana_Restablecer_Contraseñas,text="Restablecer Contraseñas",bg="cadet blue",font=("verdana",15))
        Titulo.place(x=200,y=10)

        imagen = PhotoImage(file="candadito.png")
        imagen_modi = imagen.subsample(4,4)

        LabelImagen = Label(Ventana_Restablecer_Contraseñas,image=imagen_modi,bg="cadet blue")
        LabelImagen.image = imagen_modi

        LabelImagen.place(x=200,y=50)
        
        LabelNombre = Label(Ventana_Restablecer_Contraseñas,text="Nombre: ",bg="cadet blue",font=("verdana",12))
        LabelNombre.place(x=220,y=300)

        LabelApellido = Label(Ventana_Restablecer_Contraseñas,text="Apellido: ",bg="cadet blue",font=("verdana",12))
        LabelApellido.place(x=220,y=330)

        EntradaNombre = Entry(Ventana_Restablecer_Contraseñas)
        EntradaNombre.place(x=300,y=300)

        EntradaApellido = Entry(Ventana_Restablecer_Contraseñas)
        EntradaApellido.place(x=300,y=330)

        LabelRol = Label(Ventana_Restablecer_Contraseñas,text="Rol: ",bg="cadet blue",font=("verdana",12))
        LabelRol.place(x=250,y=355)

        EntradaRol = Entry(Ventana_Restablecer_Contraseñas)
        EntradaRol.place(x=300,y=360)

        Boton = Button(Ventana_Restablecer_Contraseñas,text="Restablecer",width=20,height=2,command=Verificar_Usuario)
        Boton.place(x=260,y=400)

    def MontoRecaudado():
        ArchivoRecaudacion = open("Recaudacion.txt","r")
        ListaRecaudacion = ArchivoRecaudacion.readlines()
        ArchivoRecaudacion.close()

        total_recaudado = 0

        for linea in ListaRecaudacion:
            total_recaudado += int(linea + '\n')
        return total_recaudado
    
    def GraficoRecaudacion():
        ArchivoRecaudacion = open("Recaudacion.txt","r")
        ListaRecaudacion = ArchivoRecaudacion.readlines()
        ArchivoRecaudacion.close()

        Montos_Recaudados = [int(linea.strip()) for linea in ListaRecaudacion]
        Montos_Recaudados.sort(reverse=True)

        plt.figure(figsize=(8, 5))
        plt.bar(range(1, len(Montos_Recaudados) + 1), Montos_Recaudados, color='blue')
        plt.xlabel('Ventas')
        plt.ylabel('Monto Recaudado ($)')
        plt.title('Monto Recaudado por Venta (Ordenado de Mayor a Menor)')
        plt.grid(True)
        plt.tight_layout()

        plt.show()
    def Baja_Caja():
        total = MontoRecaudado()
        messagebox.showinfo("Informacion",f"El total recaudado fue ${total}")
        GraficoRecaudacion()
    


    #Diseño de la interfaz Principal del menu del Gerente
    global Ventana_MenuGerente
    Ventana_MenuGerente = Toplevel()
    Ventana_MenuGerente.title("Menu Gerente")
    Ventana_MenuGerente.geometry("600x400")
    Ventana_MenuGerente.resizable(0,0)

    labelTitulo = Label(Ventana_MenuGerente,text="Menu Gerente",font=("verdana",16))
    labelTitulo.place(x=235,y=20)

    boton_registrarEmpleados = Button(Ventana_MenuGerente,text="Registrar Empleado",width=25,height=2,command=RegistrarEmpleado)
    boton_registrarEmpleados.place(x=210,y=80)

    boton_ModificarPlatos = Button(Ventana_MenuGerente,text="Modificar Platos",width=25,height=2,command=ModificarPlatos)
    boton_ModificarPlatos.place(x=210,y=140)

    boton_RestablecerContraseñas = Button(Ventana_MenuGerente,text="Restablecer Contraseñas",width=25,height=2,command=RestablecerContraseñas)
    boton_RestablecerContraseñas.place(x=210,y=200)

    boton_BajaCaja = Button(Ventana_MenuGerente,text="Baja Caja",width=25,height=2,command=Baja_Caja)
    boton_BajaCaja.place(x=210,y=265)




    
#Esta funcion validara los datos para dar acceso al usuario, al sistema dependiendo del rol
def ValidarDatos():
    global Ventana_MenuGerente
    global root
    #Tomamos los valores de las cajas de texto
    Nombre = EntradaUsuario.get()
    Contraseña = EntradaContraseña.get()

    if Nombre == '' or Contraseña == '':
        messagebox.showwarning("Advertencia","Error campos incompletos")
        return
    #Abrimos los archivos en modo lectura para leer la informacion de ellos
    FileNombre = open("Login.txt","r")
    FileContraseñas = open("Contraseñas.txt","r")

    #Convertimos los archivos en listas
    ListasNombres = FileNombre.readlines()
    ListasContraseñas = FileContraseñas.readlines()

    #Ciframos la contraseña ingresada por el usuario llamando a la funcion 'cifrar_contraseña'
    contraseña_cifrada = cifrar_contraseña(Contraseña)

    #Verificamos si el usuario ingresado existe en el archivo (que fue convertido a lista)
    if Nombre + '\n' in ListasNombres:
        indice = ListasNombres.index(Nombre + '\n') #Una vez verificamos que existe obtenemos su indice
        #Resultados Esperados
        # print(f"Contraseña cifrada esperada: {contraseña_cifrada.strip()}")
        # print(f"Contraseña cifrada almacenada: {ListasContraseñas[indice].strip()}")
        # contraseña_Descrifrada = descifrar_contraseña(ListasContraseñas[indice].strip())

        #Verificamos si la contraseña ingresada sea igual a la contraseña almacenada
        if ListasContraseñas[indice] == contraseña_cifrada + '\n':
            messagebox.showinfo("Informacion","Usuario encontrado, acceso concedido")
            if len(Contraseña) == 8:
                MenuGerente()
            elif len(Contraseña) == 6:
                Menu_Empleados()
            elif len(Contraseña) == 4:
                Ventana_MenuComidas() #De ser asi se otorga el acceso al usuario
            
            #Limpiar cajas de texto
            EntradaUsuario.delete(0,END)
            EntradaContraseña.delete(0,END)
        else:
            messagebox.showerror("Error","Error,usuario o contraseña incorrectos")
    else:
        messagebox.showerror("Error","Usuario Inexistente")

#Esta funcion mostrara la ventana de registro
def Ventana_Registro():

    root.withdraw()
    global VentanaRegistro
    VentanaRegistro = Toplevel()
    VentanaRegistro.title("Registro Usuarios")
    VentanaRegistro.geometry("400x500")
    VentanaRegistro.resizable(0,0)
    VentanaRegistro.config(bg="green yellow")

    TituloRegistro = Label(VentanaRegistro,text="Registro",font=("Verdana",18),bg="green yellow")
    TituloRegistro.place(x=140,y=20)

    imagenn = PhotoImage(file="registro.png")
    imagenn_modi = imagenn.subsample(3,3)


    myLabel = Label(VentanaRegistro,image=imagenn_modi,bg="green yellow")

    myLabel.image = imagenn_modi
    myLabel.place(x=100,y=70)

    LabelNombre = Label(VentanaRegistro,text="Nombre: ",bg="green yellow")
    LabelNombre.place(x=100,y=280)

    LabelApellido = Label(VentanaRegistro,text="Apellido: ",bg="green yellow")
    LabelApellido.place(x=100,y=310)

    LabelRol = Label(VentanaRegistro,text="Rol: ",bg="green yellow")
    LabelRol.place(x=120,y=340)

    EntradaNombre = Entry(VentanaRegistro)
    EntradaNombre.place(x=160,y=280)

    EntradaApellido = Entry(VentanaRegistro)
    EntradaApellido.place(x=160,y=310)

    EntradaRol = Entry(VentanaRegistro)
    EntradaRol.place(x=160,y=340)

    BotonRegistrar = Button(VentanaRegistro,text="Registrarse",font=("verdana",10),command=lambda: RegistrarUsuario(EntradaNombre.get,EntradaApellido.get,EntradaRol.get))
    BotonRegistrar.place(x=150,y=380)

    #Limpiar Campos
    EntradaNombre.delete(0, END)
    EntradaApellido.delete(0, END)
    EntradaRol.delete(0, END)


#Esta funcion guardara los datos ingresados en los archivos correspondientes
def ObtenerLogin(nombre,apellido,contraseña): #Se recibe por parametro los valores de las cajas de texto
    login = nombre + apellido
    contraseña_Cifrada = cifrar_contraseña(contraseña)
    #Guardamos lo ingresado en las cajas de texto en los archivos
    FileLogin = open("Login.txt","a")
    FileLogin.write(login + '\n')
    FileContraseña = open("Contraseñas.txt","a")
    FileContraseña.write(contraseña_Cifrada + '\n')
    messagebox.showinfo("Informacion","Login generado correctamente")

#Funcion que generara la contraseña aleatoria dependiendo del rol
def GenerarContraseña(rol):
    Caracteres = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
    ListaCaracteres = list(Caracteres)
    Clave = ''

    if rol == 'Gerente':
        Longitud = 8
    elif rol == 'Empleado':
        Longitud = 6
    elif rol == 'Cliente':
        Longitud = 4
    else:
        print("Error al generar longitud rol invalido, intentelo nuevamente")
    
    i = 0
    while i < Longitud:
        Clave = Clave + random.choice(ListaCaracteres)
        i = i + 1
    return Clave

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

#Variables locales y demas
global cantidad_pedidos
cantidad_pedidos = 0

global Total_Precio
Total_Precio = 0

#Se crea la ventana principal Tkinter que mostrara el menu de inicio de sesion
global root
root = Tk()
root.title("Inicio Sesion")
root.geometry("400x500")
root.resizable(0,0)
root.config(bg="lightskyblue2")

def CrearArchivos():
    ArchivoVentas = open("Ventas.txt","w")
    ArchivoPrecios = open("Precios.txt")
    ArchivoLogin = open("Login.txt","w")
    ArchivoContraseñas = open("Contraseñas.txt","w")
    ArchivoPlatos = open("Platos.txt","w")
    ArchivoIDPedidos = open("IDPedidos.txt")
    ArchivoDirecciones = open("Direcciones.txt")
    ArchivoRecaudacion = open("Recaudacion.txt","w")

    ArchivoVentas.close()
    ArchivoPrecios.close()
    ArchivoLogin.close()
    ArchivoContraseñas.close()
    ArchivoPlatos.close()
    ArchivoIDPedidos.close()
    ArchivoDirecciones.close()
    ArchivoRecaudacion.close()


labelTitulo = Label(root,text="Inicio Sesion",font=("Verdana",16),bg="lightskyblue2")
labelTitulo.place(x=140,y=20)

imagen = PhotoImage(file="logocomida.png")
imagen_reducida = imagen.subsample(3,3)

myLabelImagen = Label(root,image=imagen_reducida,bg="lightskyblue2")
myLabelImagen.place(x=100,y=50)

labelNombre = Label(root,text="Usuario: ",font=("Verdana",12),bg="lightskyblue2")
labelNombre.place(x=80,y=250)

labelContraseña = Label(root,text="Contraseña: ",font=("Verdana",12),bg="lightskyblue2")
labelContraseña.place(x=50,y=280)

EntradaUsuario = Entry(root)
EntradaUsuario.place(x=160,y=250)

EntradaContraseña = Entry(root)
EntradaContraseña.place(x=160,y=282)

BotonIniciarSesion = Button(root,text="Iniciar Sesion",font=("Verdana",10),width=15,command=ValidarDatos)
BotonIniciarSesion.place(x=125,y=340)

Registratelabel = Label(root,text="¿No tienes cuenta? Registrate",bg="lightskyblue2",fg="black",cursor="hand2",font=("Helvetica",10,"underline"))
Registratelabel.place(x=95,y=380)
Registratelabel.bind("<Button-1>",lambda e: Ventana_Registro())

def IniciarSistema():
    if path.exists("Ventas.txt"):
        messagebox.showinfo("Informacion","Archivos encontrados abriendo sistema")
    else:
        messagebox.showwarning("Informacion","Archivos no encontrados,creando archivos...")
        CrearArchivos()

IniciarSistema()

root.mainloop()