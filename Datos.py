#https://github.com/sferreyr/PythonPLCController


from Constantes import *
import Telegram


class SEPAM:
    """
         NroBomba = Numero de Bomba
         IA = Corriente de Fase A
         IB = Corriente de Fase B
         IC = Corriente de Fase C
         Vab = Tension de Fase A
         Vbc = Tension de Fase B
         Vca = Tension de Fase C
         frec = Frecuencia de Red
         pot = Potencia
         Q = Caudal
         FP = Factor de Potencia.
         Preactiva = Potencia Reactiva

    """

    def __init__(self, NroBomba, IA, IB, IC, Vab, Vbc, Vca, frec, pot, Q, S, FP):
        self.NroBomba = NroBomba
        self.IA = IA / 10  # Dividimo por 10, para obtener Amperaje real.
        self.IB = IB / 10  # Dividimo por 10, para obtener Amperaje real.
        self.IC = IC / 10  # Dividimo por 10, para obtener Amperaje real.
        self.Vab = Vab
        self.Vbc = Vbc
        self.Vca = Vca
        self.frec = frec / 10  # Dividimo por 10, para obtener HZ.
        self.pot = pot
        self.Q = Q
        self.S = S * -1  # Convertimos similar a magelis.
        self.FP = FP

    def sepam_valores(self):
        return print(f"Nro de Bomba:  {self.NroBomba}\n"
                     f"Corriente de Fase A:  {self.IA}\n"
                     f"Corriente de Fase B:  {self.IB}\n"
                     f"Corriente de Fase C:  {self.IC}\n"

                     f"Tension de Fase A:  {self.Vab}\n"
                     f"Tension de Fase B:  {self.Vbc}\n"
                     f"Tension de Fase C:  {self.Vca}\n"

                     f"Frecuencia de Red: {self.frec}\n"
                     f"Potencia : {self.pot}\n"
                     f"Potencia REACTIVA: {self.Q}\n"
                     f"Potencia APARENTE:  {self.S}KW \n"
                     f"Factor de Potencia: {float(self.FP)}\n"
                     #    f"Potencia Reactiva: {self.Preactiva}\n"
                     )

    def promedios_tensiones(self):
        return (self.Vab + self.Vbc + self.Vca) / 3

    # return print(f"{((self.Vca + self.Vbc + self.Vca) / 3)} KW")

    def promedios_intensidades(self):
        # return print(f"{(self.IA + self.IB + self.IC) / 3} A")
        return (self.IA + self.IB + self.IC) / 3

    def check_tension(self):
        # Vpromedio = (self.Vab or self.Vbc or self.Vca)/3
            if self.promedios_tensiones() < LOW_KV:
                print(f"TENSION B{self.NroBomba} MUY BAJA")
                Telegram.enviar_mensaje(f"Tension B{self.NroBomba} MUY BAJA")
            elif self.promedios_tensiones() > HIGH_KV:
                print(f"TENSION {self.NroBomba} MUY ALTA")
                Telegram.enviar_mensaje(f"Tension B{self.NroBomba} MUY ALTA")
            else:
                print(f"TENSION B{self.NroBomba} NORMAL")

    def check_intensidad_aeg(self):
        # Ipromedio = (self.IA + self.IB + self.IC)/3
            if self.promedios_intensidades() < LOW_AEG_I:
                    print(f"INTENSIDAD B{self.NroBomba} MUY BAJA")
                    Telegram.enviar_mensaje(f"Intesidad B{self.NroBomba} MUY BAJA")
            elif self.promedios_intensidades() > HIGH_AEG_I:
                print(f"INTENSIDAD B{self.NroBomba} MUY ALTA")
                Telegram.enviar_mensaje(f"Intesidad B{self.NroBomba} MUY ALTA")
            else:
                print(f"INTENSIDAD B{self.NroBomba}  NORMAL")

    def check_intensidad_siemens(self):
        # Ipromedio = (self.IA + self.IB + self.IC)/3
            if self.promedios_intensidades() < LOW_SIEMENS_I:
                print(f"INTENSIDAD B{self.NroBomba} MUY BAJA")
            elif self.promedios_intensidades() > HIGH_SIEMENS_I:
                print(f"INTENSIDAD B{self.NroBomba} MUY ALTA")
            else:
                print(f"INTENSIDAD B{self.NroBomba}  NORMAL")


class General:

    def __init__(self, ncamara, pdorrego, cloro, flushing, turbiedad, ph, Qb1, Qb2, Qb3, Qb4, Qb5, Qb6, Qtotal):
        self.ncamara = ncamara / 100
        self.pPunto = pdorrego / 100
        self.cloro = cloro / 1000  # Lo dividimos para que las unidades sean exactas.
        self.flushing = flushing / 100
        self.turbiedad = turbiedad / 1000
        self.ph = ph / 1000
        # Caudales Bomba * y total.
        self.Qb1 = Qb1
        self.Qb2 = Qb2
        self.Qb3 = Qb3
        self.Qb4 = Qb4
        self.Qb5 = Qb5
        self.Qb5 = Qb6
        self.Qtotal = Qtotal

    def general_valores(self):
        return print(f"Nivel de Camara:  {self.ncamara}\n"
                     f"Presion -:  {self.pPunto} mCa\n"
                     f"Nivel de Cloro:  {self.cloro} mgL\n"
                     f"Presion de Flushing:  {self.flushing}\n"
                     f"Turbiedad:  {self.turbiedad} unt\n"
                     f"PH:  {self.ph} pH\n"
                     f"Q de Bomba N°1:  {self.Qb1} m3/h\n"
                     f"Q de Bomba N°2: {self.Qb2} m3/h\n"
                     f"Q de Bomba N°3: {self.Qb3} m3/h\n"
                     f"Q de Bomba N°4: {self.Qb4} m3/h\n"
                     f"Q de Bomba N°5:  {self.Qb5} m3/h \n"
                     f"Q de Bomba N°6:  {self.Qb6} m3/h \n"
                     f"Q Total:  {self.Qb1 + self.Qb2 + self.Qb3 + self.Qb4 + self.Qb5 + self.Qb6} \n"
                     )

    # Chequeos Generales
    def check_nivel(self):
        if self.ncamara >= HIGH_NCAMARA:
            print("Nivel de Camara MUY ALTO")
            Telegram.enviar_mensaje("Nivel de Camara MUY ALTO")
        elif self.ncamara <= LOW_NCAMARA:
            print("Nivel de Camara MUY BAJO")
            Telegram.enviar_mensaje("Nivel de Camara MUY BAJO")
        else:
            print("Nivel de Camara NORMAL")

    def check_cloro(self):
        if self.cloro >= HIGH_CLORO:
            print("Cloro MUY ALTO")
            Telegram.enviar_mensaje("Cloro MUY ALTO")
        elif self.cloro <= LOW_CLORO:
            print("Cloro MUY BAJO")
            Telegram.enviar_mensaje("Cloro MUY BAJO")
        else:
            print("Cloro Normal")

    def check_flushing(self):
        if self.flushing >= HIGH_FLUSH:
            print("Flushing MUY ALTO")
            Telegram.enviar_mensaje("Flushing MUY ALTO")
        elif self.flushing <= LOW_FLUSH:
            print("Flushing MUY BAJO")
            Telegram.enviar_mensaje("Flushing MUY BAJO")
        else:
            print("Flushing NORMAL")

    def check_Qbombas(self):
        if self.Qb1 <= LOW_Q1:
            print("Caudal de B1 BAJO")
            Telegram.enviar_mensaje("Caudal de Bx BAJO")
        if self.Qb2 <= LOW_Q2:
            print("Caudal de B2 BAJO")
            Telegram.enviar_mensaje("Caudal de Bx BAJO")
        if self.Qb3 <= LOW_Q3:
            print("Caudal de B3 BAJO")
            Telegram.enviar_mensaje("Caudal de Bx BAJO")
        if self.Qb4 <= LOW_Q4:
            print("Caudal de B4 BAJO")
            Telegram.enviar_mensaje("Caudal de Bx BAJO")
        if self.Qb5 <= LOW_Q5:
            print("Caudal de B5 BAJO")
            # Telegram.enviar_mensaje("Caudal de Bx BAJO")
        if self.Qb5 <= LOW_Q6:
            print("Caudal de B6 BAJO")
            # Telegram.enviar_mensaje("Caudal de Bx BAJO")
        else:
            print("Caudales OK!")
