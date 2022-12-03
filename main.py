#https://github.com/sferreyr/PythonPLCController

from pymodbus.client.sync import ModbusTcpClient
from Datos import *
import GenerarExcel
import time
import datetime
import schedule
import numpy as np
import Telegram
import matplotlib.pyplot as plt  #Desactivado en raspberry


import keyboard
from threading import Thread

TIEMPO_FUNCIONAMIENTO = 1  # Cada X MINUTOS hace el chequeo.
TIPO_DE_INFORME_CHEQUEO= 3 # 1: Valores Generales, 2: Electrobombas, 3: Todos los valores.
NOTIFICACIONES_TELEGRAM_FECHA = True #Si esta habilitado envia mensaje luego de hacer el chequeo.
'''
In most cases, the first legal address (0) of each type of memory location are referred to as:
000001 - outputs/coils R/W
100001 - inputs R/O
300001 - input registers R/O
400001 - holding register R/W
'''
'''
One more thing: with pymodbus you don't have to use the 4000x naming convention. 
When you call read_holding_registers the address argument should be 0 if you want to read holding register at address 40001.
'''

def Conexion():

    client = ModbusTcpClient('127.0.0.1')
    connection = client.connect()

    # https://www.rapidtables.com/convert/number/decimal-to-hex.html
    if connection:
        print("CONECTADO")
        requestSepam = (client.read_holding_registers(0x0, 97, unit=0x1)) #Reemplazar en Hex la direccion del registro
        dat = np.array(requestSepam.registers)

        BancoCapacitores = "Banco Capacitores"
        SPAM_Banco = SEPAM(BancoCapacitores, dat[0], dat[1], dat[2], dat[3], dat[4], dat[5], dat[6], dat[7],
                           dat[8], dat[9], dat[10])

        BombaNro = 1
        SPAM_B1 = SEPAM(BombaNro, dat[15], dat[16], dat[17], dat[18], dat[19], dat[20], dat[21], dat[22],
                        dat[23], dat[24],
                        dat[25])
        #print(SPAM_B1.sepam_valores())

        BombaNro = 2
        SPAM_B2 = SEPAM(BombaNro, dat[30], dat[31], dat[32], dat[33], dat[34], dat[35], dat[36], dat[37],
                        dat[38], dat[39],
                        dat[40])
        #print(SPAM_B2.sepam_valores())

        BombaNro = 3
        SPAM_B3 = SEPAM(BombaNro, dat[45], dat[46], dat[47], dat[48], dat[49], dat[50], dat[51], dat[52],
                        dat[53], dat[54],
                        dat[55])
        #print(SPAM_B3.sepam_valores())

        BombaNro = 4
        SPAM_B4 = SEPAM(BombaNro, dat[60], dat[61], dat[62], dat[63], dat[64], dat[65], dat[66], dat[67],
                        dat[68], dat[69],
                        dat[70])
        # print(SPAM_B4.sepam_valores())

        BombaNro = 5
        SPAM_B5 = SEPAM(BombaNro, dat[75], dat[76], dat[77], dat[78], dat[79], dat[80], dat[81], dat[82],
                        dat[83], dat[84],
                        dat[85])
        # print(SPAM_B5.sepam_valores())

        BombaNro = 6
        SPAM_B6 = SEPAM(BombaNro, dat[86], dat[87], dat[88], dat[89], dat[90], dat[91], dat[92], dat[93],
                        dat[94], dat[95],
                        dat[96])
        # print(SPAM_B5.sepam_valores())
        requestGeneral = (client.read_holding_registers(0x0, 21, unit=0x1)) #Reemplazar en Hex la direccion del registro
        dat = requestGeneral.registers

        info_gral = General(dat[14], dat[15], dat[16], dat[17], dat[18], dat[20], dat[3], dat[4], dat[5],
                            dat[6], dat[0], dat[1])

        # Cerramos la conexion con el PLC
        client.close()


        if NOTIFICACIONES_TELEGRAM_FECHA:
            Telegram.enviar_mensaje_chequeo(f" Tipo de Chequeo:{TIPO_DE_INFORME_CHEQUEO}  - Horario de Sensado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        # Generamos en el mismo Excel
        # Generar Datos Generales
        GE = GenerarExcel.GenExcel(0, info_gral)
        print("Generando info_gral")
        GE.Generar()
        # Generar Banco de Capacitores
        GE = GenerarExcel.GenExcel(SPAM_Banco, 0)
        print("Generando SPAM_Banco")
        GE.Generar()

        # Generar Datos SEPAM
        for x in range(1, 6): #6 bombas.
            print("Generando SPAM_B" + str(x))
            SPAM_OBJ = locals()["SPAM_B" + str(x)]
            INFO_OBJ = locals()["info_gral"]
            GE = GenerarExcel.GenExcel(SPAM_OBJ, 0)
            GE.Generar()
            # Hacer chequeo completo:
            if TIPO_DE_INFORME_CHEQUEO == 3: #Todos
                Activar_Chequeos(TIPO_DE_INFORME_CHEQUEO, SPAM_OBJ, INFO_OBJ)
            elif TIPO_DE_INFORME_CHEQUEO == 2: #Solo Electrobombas
                Activar_Chequeos(TIPO_DE_INFORME_CHEQUEO, SPAM_OBJ, 0)
            elif TIPO_DE_INFORME_CHEQUEO == 1:  # Solo General
                 Activar_Chequeos(TIPO_DE_INFORME_CHEQUEO, 0, INFO_OBJ)
            else:
                print("Sin Chequeos.")




schedule.every(TIEMPO_FUNCIONAMIENTO).minutes.do(Conexion)
# Modo Automatico
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)

        def Activar_Chequeos(isActivado, SEPAMM, GENERAL): # 1: Valores Generales, 2: Electrobombas, 3: Todos los valores.

            if isActivado == 1:
                General.check_flushing(GENERAL)
                General.check_Qbombas(GENERAL)
                General.check_cloro(GENERAL)
                General.check_nivel(GENERAL)
                print("Chequeo solo General.")
            elif isActivado == 2:
                SEPAM.check_tension(SEPAMM)
                SEPAM.check_intensidad_aeg(SEPAMM)
                SEPAM.check_intensidad_siemens(SEPAMM)
                print("Chequeo solo Electrobombas.")
            elif isActivado == 3:
                General.check_flushing(GENERAL)
                General.check_Qbombas(GENERAL)
                General.check_cloro(GENERAL)
                General.check_nivel(GENERAL)
                SEPAM.check_tension(SEPAMM)
                SEPAM.check_intensidad_aeg(SEPAMM)
                SEPAM.check_intensidad_siemens(SEPAMM)
                print("Chequeo Completo.")
            else:
                 print("Chequeo Desactivado.")



