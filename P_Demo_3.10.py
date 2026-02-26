import tkinter as tk
import threading
import random
from tkinter import PhotoImage


class Jugador:
    def __init__(self, nombre, canvas, x, y):
        self.nombre = nombre
        self.equipo = "A"
        self.hp = 100
        self.energia = 100
        self.canvas = canvas
        self.x = x                                                                          #Creacion de rectangulo (Personaje), barra de vida y energia
        self.y = y
        
        self.imagen_jugador = PhotoImage(file="jugador.png")
        self.IJ = canvas.create_image(x+40, y+15, image=self.imagen_jugador)
        self.label = canvas.create_text(x+40, y+43, text=nombre, fill="black")
        self.imagen_daño = PhotoImage(file="jugador_daño.png")

        self.hp_bar_bg = canvas.create_rectangle(x, y-30, x+80, y-17, fill="gray")
        self.hp_bar = canvas.create_rectangle(x, y-30, x+80, y-17, fill="green")#
        self.hp_text = canvas.create_text(x+40, y-23, text="HP: 100", fill="black", font=("Arial", 8))
        self.energy_bar_bg = canvas.create_rectangle(x, y-15, x+80, y-2, fill="lightgray")
        self.energy_bar = canvas.create_rectangle(x, y-15, x+80, y-2, fill="yellow")
        self.energy_text = canvas.create_text(x+40, y-8, text="EN: 100", fill="black", font=("Arial", 8))

        #self.rect = canvas.create_rectangle(x, y, x+80, y+30, fill="blue")
        #self.label = canvas.create_text(x+40, y+15, text=f"{nombre}\n100 HP", fill="white")

    def ejecutar_accion(self, accion):                                                      #Funcion para las acciones
        tipo = accion["tipo"]
        if tipo == "atacar" and self.energia >= 10:                                          #Condicion para atacar
            objetivo = accion["objetivo"]
            daño = random.randint(30, 40)
            self.energia -= 10
            objetivo.recibir_daño(daño)
        elif tipo == "curar" and self.energia >= 20:                                                #Condicion para curar
            curación = random.randint(1, 100)
            self.hp = min(100, self.hp + curación)
            self.energia -= 20
        elif tipo == "esperar":
            self.energia = min(100, self.energia + 30)                                        #Condicion para esperar
        self.actualizar_barras()
        '''
        elif tipo == "escudo":
            self.proteccion = min(100, self.escudo + 30)                                        #Condicion para cubrir
        self.actualizar_barras()
        '''
    def recibir_daño(self, cantidad):
        self.hp = max(0, self.hp - cantidad)                                                  #Condicion para disminuir la vida
        self.actualizar_barras()
        self.animacion_daño()

    def animacion_daño(self):
        impacto = self.canvas.create_image(self.x + 40, self.y + 15, image=self.imagen_daño)
        self.canvas.after(200, lambda: self.canvas.delete(impacto))
        

    def actualizar_barras(self):
        ancho_hp = int((self.hp / 100) * 80)
        color_hp = "green" if self.hp > 30 else "orange" if self.hp > 0 else "darkred"
        self.canvas.coords(self.hp_bar, self.x, self.y-30, self.x + ancho_hp, self.y-17)            #Calculo de la vida
        self.canvas.itemconfig(self.hp_bar, fill=color_hp)
        self.canvas.itemconfig(self.hp_text, text=f"HP: {self.hp}")

        ancho_en = int((self.energia / 100) * 80)
        color_en = "yellow" if self.energia > 0 else "gray"
        self.canvas.coords(self.energy_bar, self.x, self.y-15, self.x + ancho_en, self.y-2)     #Calculo de la energia
        self.canvas.itemconfig(self.energy_bar, fill=color_en)
        self.canvas.itemconfig(self.energy_text, text=f"EN: {self.energia}")
        
        color = "gray" if self.hp == 0 else "blue"
        self.canvas.itemconfig(self.label, text=self.nombre)                 #Condicion de muerte
        #self.canvas.itemconfig(self.rect, fill=color)

class Enemigo:
    def __init__(self, nombre, canvas, x, y):
        self.nombre = nombre
        self.equipo = "B"
        self.hp = 100
        self.energia = 100
        self.canvas = canvas
        self.x = x
        self.y = y

        self.imagen_enemigo = PhotoImage(file="enemigo.png")
        self.IE = canvas.create_image(x+40, y+15, image=self.imagen_enemigo)
        self.label = canvas.create_text(x+40, y+43, text=nombre, fill="black")
        self.imagen_daño = PhotoImage(file="enemigo_daño.png")

        self.hp_bar_bg = canvas.create_rectangle(x, y-30, x+80, y-17, fill="gray")
        self.hp_bar = canvas.create_rectangle(x, y-30, x+80, y-17, fill="green")
        self.hp_text = canvas.create_text(x+40, y-23, text="HP: 100", fill="black", font=("Arial", 8))
        self.energy_bar_bg = canvas.create_rectangle(x, y-15, x+80, y-2, fill="lightgray")
        self.energy_bar = canvas.create_rectangle(x, y-15, x+80, y-2, fill="yellow")
        self.energy_text = canvas.create_text(x+40, y-8, text="EN: 100", fill="black", font=("Arial", 8))
        
        #self.rect = canvas.create_rectangle(x, y, x+80, y+30, fill="red")
        #self.label = canvas.create_text(x+40, y+15, text=f"{nombre}\n100 HP", fill="white")

    def decidir_accion(self, enemigos):                                                                #Condiciones para las decisiones del enemigo 
        vivos = [e for e in enemigos if e.hp > 0]
        if not vivos:
            return {"tipo": "esperar"}
        objetivo = random.choice(vivos)

        if self.hp <= 30:                                                                               #Si está muy herido, intenta curarse
            return {"tipo": "curar"}
        elif objetivo.hp <= 20:                                                                         #Si el jugador está débil, lo remata
            return {"tipo": "atacar", "objetivo": objetivo}
        else:                                                                                           #Si ambos están bien, aleatoriza
            tipo = random.choice(["atacar", "esperar"])
            return {"tipo": tipo, "objetivo": objetivo} if tipo == "atacar" else {"tipo": "esperar"}

    def ejecutar_accion(self, accion):
        tipo = accion["tipo"]
        if tipo == "atacar" and self.energia >= 10:
            objetivo = accion["objetivo"]
            daño = random.randint(10, 25)
            self.energia -= 10
            objetivo.recibir_daño(daño)
        elif tipo == "curar" and self.energia >= 20:
            curación = random.randint(10, 20)
            self.hp = min(100, self.hp + curación)
            self.energia -= 20
        elif tipo == "esperar":
            self.energia = min(100, self.hp + 30)
        self.actualizar_barras()

    def recibir_daño(self, cantidad):
        self.hp = max(0, self.hp - cantidad)
        self.actualizar_barras()
        self.animacion_daño()

    def animacion_daño(self):
        impacto = self.canvas.create_image(self.x + 40, self.y + 15, image=self.imagen_daño)
        self.canvas.after(200, lambda: self.canvas.delete(impacto))

    def actualizar_barras(self):
        ancho_hp = int((self.hp / 100) * 80)
        color_hp = "green" if self.hp > 30 else "orange" if self.hp > 0 else "darkred"
        self.canvas.coords(self.hp_bar, self.x, self.y-30, self.x + ancho_hp, self.y-17)
        self.canvas.itemconfig(self.hp_bar, fill=color_hp)
        self.canvas.itemconfig(self.hp_text, text=f"HP: {self.hp}")

        ancho_en = int((self.energia / 100) * 80)
        color_en = "yellow" if self.energia > 0 else "gray"
        self.canvas.coords(self.energy_bar, self.x, self.y-15, self.x + ancho_en, self.y-2)
        self.canvas.itemconfig(self.energy_bar, fill=color_en)
        self.canvas.itemconfig(self.energy_text, text=f"EN: {self.energia}")

        color = "gray" if self.hp == 0 else "red"
        self.canvas.itemconfig(self.label, text=self.nombre)
        #self.canvas.itemconfig(self.rect, fill=color)


class Simulador_De_Batalla:
    def __init__(self, jugador, enemigos, IU):
        self.jugador = jugador
        self.enemigos = enemigos
        self.IU = IU

    def turno_enemigos(self):
        self.IU.borrar_indicador()
        for enemigo in self.enemigos:
            if enemigo.hp > 0 and self.jugador.hp > 0:
                accion = enemigo.decidir_accion([self.jugador])
                enemigo.ejecutar_accion(accion)
                self.IU.indicador(enemigo, accion["tipo"])


class IU_Batalla:
    def __init__(self, root, atributos, nivel, finalizar_callback):
        self.root = root
        self.root.title("Simulador de Batalla por Turnos")
        self.canvas = tk.Canvas(root, width=700, height=350, bg="white")
        self.canvas.pack()#place_configure(x=700,y=250, anchor="center")#pack()

        self.I_A = PhotoImage(file="ataque.png")                                                #Cargar imagenes
        self.I_C = PhotoImage(file="curacion.png")   
        self.I_E = PhotoImage(file="esperar.png")   
        self.frame_botones = tk.Frame(root)                                                                                  #Creacion de los botones de accion
        self.frame_botones.pack() #place_configure(x=900, y=500)#pack()

        self.I_indicadores = {}

        self.objetivo_var = tk.StringVar()
        self.boton_atacar = tk.Button(self.frame_botones, text="Atacar", image=self.I_A, command=lambda: self.turno_jugador("atacar"))
        self.boton_curar = tk.Button(self.frame_botones, text="Curar", image=self.I_C, command=lambda: self.turno_jugador("curar"))
        self.boton_esperar = tk.Button(self.frame_botones, text="Esperar", image=self.I_E, command=lambda: self.turno_jugador("esperar"))

        self.menu_objetivo = tk.OptionMenu(self.frame_botones, self.objetivo_var, "...")
        self.menu_objetivo.config(width=10)
        self.boton_atacar.pack(side=tk.LEFT, padx=5)
        self.boton_curar.pack(side=tk.LEFT, padx=5)
        self.boton_esperar.pack(side=tk.LEFT, padx=5)
        self.menu_objetivo.pack(side=tk.LEFT, padx=5)                                                                         #Colocacion de los botones

        self.jugador = Jugador("Jugador", self.canvas, 50, 150)                                                              #Crear personajes
        self.jugador.hp = atributos["vida"]
        self.jugador.energia = atributos["energia"]

        self.enemigos = [Enemigo(f"Enemigo{i+1}", self.canvas, 550, 100 + i*80) for i in range(1 + nivel)]
        '''
        self.enemigo1 = Enemigo("Enemigo1", self.canvas, 550, 100)
        self.enemigo2 = Enemigo("Enemigo2", self.canvas, 550, 200)
        self.enemigos = [self.enemigo1, self.enemigo2]
        '''
        self.engine = Simulador_De_Batalla(self.jugador, self.enemigos, self)
        self.root.after(1000, self.turno_enemigos_en_thread)
        
        self.turno = 1
        self.actualizar_menu_objetivos()
        self.desactivar_botones()
        self.root.after(1000, self.turno_enemigos_en_thread)

        self.finalizar_callback = finalizar_callback

    def mostrar_turno_jugador(self):
        if self.jugador.hp == 0 or all(e.hp == 0 for e in self.enemigos):
            return

        self.turno += 1
        self.actualizar_menu_objetivos()
        self.activar_botones()

    def turno_jugador(self, accion_tipo):
        self.desactivar_botones()

        if accion_tipo == "atacar":
            nombre = self.objetivo_var.get()
            objetivo = next((e for e in self.enemigos if e.nombre == nombre and e.hp > 0), None)
            if objetivo:
                accion = {"tipo": "atacar", "objetivo": objetivo}
            else:
                return
        else:
            accion = {"tipo": accion_tipo}

        self.jugador.ejecutar_accion(accion)
        self.root.after(1000, self.turno_enemigos_en_thread)

    def turno_enemigos_en_thread(self):
        threading.Thread(target=self.turno_enemigos).start()

    def turno_enemigos(self):
        self.engine.turno_enemigos()
        if self.jugador.hp > 0 and any(e.hp > 0 for e in self.enemigos):
            self.root.after(1000, self.mostrar_turno_jugador)
        else:
            self.finalizar_callback(ganado=self.jugador.hp > 0)
            self.canvas.pack_forget()
            self.frame_botones.pack_forget()

    def indicador(self, enemigo, tipo):
        imagenes = {"atacar": self.I_A, "curar": self.I_C, "esperar": self.I_E}.get(tipo)
        if imagenes:
            x = enemigo.x + 100
            y = enemigo.y - 40
            indicador = self.canvas.create_image(x, y, image=imagenes)
            self.I_indicadores[enemigo.nombre] = indicador

    def borrar_indicador(self):
        for indicador in self.I_indicadores.values():
            self.canvas.delete(indicador)
        self.I_indicadores.clear()

    def actualizar_menu_objetivos(self):
        vivos = [e.nombre for e in self.enemigos if e.hp > 0]
        menu = self.menu_objetivo["menu"]
        menu.delete(0, "end")
        for nombre in vivos:
            menu.add_command(label=nombre, command=lambda n=nombre: self.objetivo_var.set(n))
        if vivos:
            self.objetivo_var.set(vivos[0])
        else:
            self.objetivo_var.set("...")

    def activar_botones(self):
        for b in (self.boton_atacar, self.boton_curar, self.boton_esperar):
            b.config(state=tk.NORMAL)
        self.menu_objetivo.config(state=tk.NORMAL)

    def desactivar_botones(self):
        for b in (self.boton_atacar, self.boton_curar, self.boton_esperar):
            b.config(state=tk.DISABLED)
        self.menu_objetivo.config(state=tk.DISABLED)


class Menu_Inicio:
    def __init__(self, root):
        self.root = root
        self.root.geometry("700x450")
        self.root.attributes("-fullscreen", True)
        self.frame = tk.Frame(root, width=700, height=450, bg="white")
        self.frame.pack(fill="both", expand=True)

        titulo = tk.Label(self.frame, text="Simulador de Batalla", font=("Arial", 24), bg="white")
        titulo.pack(pady=40)

        boton_jugar = tk.Button(self.frame, text="Jugar", width=15, height=2, command=self.iniciar_juego)
        boton_jugar.pack(pady=10)

        boton_salir = tk.Button(self.frame, text="Salir", width=15, height=2, command=root.destroy)
        boton_salir.pack(pady=10)

    def iniciar_juego(self):
        self.frame.destroy()
        Juego(self.root)


class MapaNiveles:
    def __init__(self, root, iniciar_batalla_callback):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack()
        self.iniciar_batalla_callback = iniciar_batalla_callback

        # === NUEVO: Instrucción visual ===
        self.label_indicacion = tk.Label(root, text="Selecciona el nivel desbloqueado para jugar, el cual se indica con color verde", font=("Arial", 12), fg="green")
        self.label_indicacion.pack()

        self.niveles = []
        self.crear_niveles()

    def crear_niveles(self):
        for i in range(5):
            x = 100 + i * 90
            y = 200
            color = "gray" if i > 0 else "green"
            ovalo = self.canvas.create_oval(x, y, x+50, y+50, fill=color, tags=f"nivel_{i}")
            self.canvas.tag_bind(f"nivel_{i}", "<Button-1>", lambda e, n=i: self.seleccionar_nivel(n))
            self.niveles.append(ovalo)

    def desbloquear_nivel(self, nivel):
        if nivel < len(self.niveles):
            self.canvas.itemconfig(self.niveles[nivel], fill="green")

    def seleccionar_nivel(self, nivel):
        if self.canvas.itemcget(self.niveles[nivel], "fill") == "green":
            self.label_indicacion.pack_forget()  # Oculta la indicación al avanzar
            self.canvas.pack_forget()
            self.iniciar_batalla_callback(nivel)


class PantallaMejoras:
    def __init__(self, root, atributos, continuar_callback):
        self.root = root
        self.frame = tk.Frame(root, bg="white")
        self.frame.pack(fill="both", expand=True)

        self.atributos = atributos
        self.continuar_callback = continuar_callback

        tk.Label(self.frame, text="Mejora tus habilidades", font=("Arial", 16), bg="white").pack(pady=10)

        self.puntos_disponibles = 5
        self.puntos_var = tk.IntVar(value=self.puntos_disponibles)
        tk.Label(self.frame, textvariable=self.puntos_var, bg="white").pack()

        self.valores = {}
        for key in atributos:
            f = tk.Frame(self.frame, bg="white")
            f.pack(pady=5)
            tk.Label(f, text=key.capitalize(), width=10, bg="white").pack(side="left")
            self.valores[key] = tk.IntVar(value=atributos[key])
            tk.Label(f, textvariable=self.valores[key], width=5, bg="white").pack(side="left")
            tk.Button(f, text="+", command=lambda k=key: self.incrementar(k)).pack(side="left")

        tk.Button(self.frame, text="Continuar", command=self.continuar).pack(pady=20)

    def incrementar(self, key):
        if self.puntos_disponibles > 0:
            self.valores[key].set(self.valores[key].get() + 1)
            self.puntos_disponibles -= 1
            self.puntos_var.set(self.puntos_disponibles)

    def continuar(self):
        for key in self.atributos:
            self.atributos[key] = self.valores[key].get()
        self.frame.destroy()
        self.continuar_callback()



class Juego:
    def __init__(self, root):
        self.root = root
        self.atributos = {"vida": 100, "energia": 100, "ataque": 20}
        self.nivel_actual = 0
        self.mapa = MapaNiveles(root, self.iniciar_nivel)

    def iniciar_nivel(self, nivel):
        self.nivel_actual = nivel
        PantallaMejoras(self.root, self.atributos, self.iniciar_combate)

    def iniciar_combate(self):
        IU_Batalla(self.root, atributos=self.atributos, nivel=self.nivel_actual, finalizar_callback=self.finalizar_combate)

    def finalizar_combate(self, ganado):
        if ganado:
            if self.nivel_actual + 1 < 5:
                self.mapa.desbloquear_nivel(self.nivel_actual + 1)
                self.mapa.canvas.pack()
            else:
                self.mostrar_mensaje_final("¡Has completado todos los niveles!")
        else:
            self.mostrar_mensaje_final("¡Fuiste derrotado! Intenta de nuevo.")

    def mostrar_mensaje_final(self, mensaje):
        for widget in self.root.winfo_children():
            widget.destroy()

        mensaje_final = tk.Label(self.root, text=mensaje, font=("Arial", 16), bg="white")
        mensaje_final.pack(pady=20)

        if "derrotado" in mensaje.lower():
            tk.Button(self.root, text="Volver a intentar", font=("Arial", 12),
                      command=self.reiniciar_juego).pack(pady=10)

    def reiniciar_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.__init__(self.root)
        
if __name__ == "__main__":
    root = tk.Tk()
    Menu_Inicio(root)
    root.mainloop()
