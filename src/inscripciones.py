import random
import time

from datetime import datetime, timedelta

from osbrain import run_agent
from osbrain import run_nameserver

from src.colors import bcolors
from src.helpers import siguiente_semestre, convertir, malla_curricular

cantidad_aleatoria_materias_semestre = random.randint(30, 55)
materiasHabilitadasArr = random.sample(malla_curricular, cantidad_aleatoria_materias_semestre)


def log_message(agent, message):
    agent.log_info('Recibido: %s' % message)


hora_actual = datetime.strptime("08:30", "%H:%M")


def aumentar_tiempo(minutos):
    # Obtener la hora actual

    # Añadir la cantidad de minutos a la hora actual
    hora_nueva = hora_actual + timedelta(minutes=minutos)
    # Devolver la hora en formato "HH:MM"
    return hora_nueva.strftime("%H:%M")


nombre_cajero = "Cajero1"
nombre_director = "Director1"
semestre = "1/2022"
estudiante_arr = []
nombre_estudiante = "Estudiante1"
nombre_estudiante = nombre_estudiante.replace(nombre_estudiante[len(nombre_estudiante) - 1:],
                                              str(random.randint(1, 10)))
cantidad_aleatoria_materias = abs(random.randint(1, 6))
materias_deseadas = random.sample(materiasHabilitadasArr, cantidad_aleatoria_materias)

cod_sys = "2018" + str(random.randint(10000, 99999))
# Cajero
nombre_cajero = nombre_cajero.replace(nombre_cajero[len(nombre_cajero) - 1:], str(random.randint(1, 10)))
# Director
nombre_director = nombre_director.replace(nombre_director[len(nombre_director) - 1:], str(random.randint(1, 10)))
semestre = siguiente_semestre(semestre)
tiempo_habilitacion_materias = random.randint(60, 120)
billeteraRand = random.randint(10, 100)
tiempo_compra = 0
tiempo_inscripcion = 0

if __name__ == '__main__':

    # Inicializacion de agentes con sus atributos
    ns = run_nameserver()

    estudiante = run_agent(bcolors.OKCYAN + nombre_estudiante + bcolors.ENDC, attributes={
        "materiasDeseadas": materias_deseadas,
        "codSys": cod_sys,
        "boleta": False,
        "billetera": billeteraRand,
    })
    cajero = run_agent(bcolors.WARNING + nombre_cajero + bcolors.ENDC, attributes={
        "monto": 14
    })
    director = run_agent(bcolors.FAIL + nombre_director + bcolors.ENDC, attributes={
        "materiasRecibidas": materiasHabilitadasArr,
        "semestre": semestre,
        "estudiantes": estudiante_arr
    })
    responsable = run_agent(bcolors.HEADER + 'ResponsableA' + bcolors.ENDC)

    # Configuracion de direcciones de los agentes
    dirEst = estudiante.bind('PUSH', alias='main')
    dirCaj = cajero.bind('PUSH', alias='main')
    dirDir = director.bind('PUSH', alias='main')
    dirRes = responsable.bind('PUSH', alias='main')

    # El cajero y el estudiante realizan una conexion para el paso de mensajes
    cajero.connect(dirEst, handler=log_message)
    estudiante.connect(dirCaj, handler=log_message)

    # Compra de boleta

    print(bcolors.HEADER + "  (ESTUDIANTE)  Hola cajero! quiero comprar una boleta de inscripcion" + bcolors.ENDC)
    time.sleep(1)
    print(bcolors.OKCYAN + '  (CAJERO)  Hola estudiante, son ' + str(cajero.get_attr("monto")) + bcolors.ENDC)
    tiempo_compra = random.randint(10, 15)
    if cajero.get_attr("monto") <= estudiante.get_attr("billetera"):
        monto_restante = abs(estudiante.get_attr("billetera") - cajero.get_attr("monto"))
        estudiante.set_attr(billetera=monto_restante, boleta=True)
        print(bcolors.OKBLUE + "   ----SISTEMA----   El cajero cobro al estudiante y ahora tiene en la billetera: " + str(
            estudiante.get_attr("billetera")) + bcolors.ENDC)
        time.sleep(1)

        # El director y el estudiante realizan una conexion para el paso de mensajes

        director.connect(dirEst, handler=log_message)
        estudiante.connect(dirDir, handler=log_message)

        # Inscripcion de materias

        print(bcolors.HEADER + '  (ESTUDIANTE)  Hola Director, deseo inscribirme a las siguientes materias: ' + str(
            estudiante.get_attr("materiasDeseadas")) + bcolors.ENDC)
        time.sleep(1)
        print(bcolors.WARNING + '  (DIRECTOR)  Hola estudiante necesito tu codigo Sis y tu boleta' + bcolors.ENDC)
        time.sleep(1)
        tiempo_inscripcion = random.randint(5, 15)
        aumentar_tiempo(tiempo_inscripcion)
        if estudiante.get_attr("boleta"):
            print(bcolors.HEADER + '  (ESTUDIANTE)  Mi codigo Sys es: ' + str(
                estudiante.get_attr("codSys")) + ' y tengo el recibo de mi boleta aqui' + bcolors.ENDC)
            materiasTomadas = [x for x in director.get_attr("materiasRecibidas") if
                               x in estudiante.get_attr("materiasDeseadas")]
            if len(materiasTomadas) >= 1:
                # El director inscribe a los estudiantes
                time.sleep(1)
                estudiante_data = director.get_attr("estudiantes")
                estudiante_data.append({
                    "codSys": estudiante.get_attr("codSys"),
                    "boleta": estudiante.get_attr("boleta"),
                    "materiasInscritas": materiasTomadas

                }, )
                director.set_attr(estudiantes=estudiante_data)
                print(bcolors.WARNING + '  (DIRECTOR)  Te inscribi con exito en tus materias!!' + bcolors.ENDC)
                estudiante_inscrito = estudiante_data[len(estudiante_data) - 1]
                print(bcolors.OKBLUE + "(------SISTEMA------)  El director inscribio al estudiante en las siguientes "
                                       "materias: " + bcolors.ENDC
                      , *estudiante_inscrito["materiasInscritas"], sep='      \n- ')
                materias_no_tomadas = difference = set(estudiante.get_attr("materiasDeseadas")).difference(
                    set(estudiante_inscrito["materiasInscritas"]))
                if len(materias_no_tomadas) != 0:
                    print(
                        bcolors.OKBLUE + "(------SISTEMA------)  El director no pudo inscribir al estudiante en estas materias: "
                                         "materias: " + bcolors.ENDC
                        , *materias_no_tomadas, sep='      \n- ')

            else:
                time.sleep(1)
                print(
                    bcolors.WARNING + '  (DIRECTOR)  No existen materias habilitadas suficientes para que puedas continuar.' + bcolors.ENDC)
        else:
            time.sleep(1)
            print(bcolors.WARNING + '  (DIRECTOR)  Debes pasar por caja y comprar una boleta.' + bcolors.ENDC)

        print(bcolors.OKBLUE + '(------SISTEMA------) Fin Iteracion.' + bcolors.ENDC)
    else:
        print(
            bcolors.OKCYAN + '  (CAJERO)  No puedes inscribirte por que no tienes el dinero suficiente' + bcolors.ENDC)


    aumentar_tiempo(tiempo_compra)
    tiempo_acumulado = tiempo_compra + tiempo_inscripcion + tiempo_habilitacion_materias
    tiempo_con_formato = convertir(tiempo_acumulado)
    print(bcolors.OKBLUE + '(------SISTEMA------) El proceso de inscripcion duro un total de: ' + str(
        tiempo_con_formato) + bcolors.ENDC)
    print(" - " + str(convertir(tiempo_habilitacion_materias)) + " Durante el la habililtacion de materias")
    print(" - " + str(convertir(tiempo_compra)) + " Durante el tiempo de compra")
    print(" - " + str(convertir(tiempo_inscripcion)) + " Durante el tiempo de inscripcion")

    # ns.shutdown()
