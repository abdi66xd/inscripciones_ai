import random
import time

from osbrain import run_agent
from osbrain import run_nameserver

from src.colors import bcolors
from src.helpers import siguiente_semestre


materiasRecibidas = [
    "Algebra I", "Calculo I", "Introduccion a la programacion", "Metodologia de la investigacion", "Fisica General",
    "Ingles", "Algebra II",
    "Calculo II", "Matematica discreta", "Elementos de programacion y estrucutura de datos",
    "Arquitectura de computadoras", "Estadistica I",
    "Ecuaciones diferenciales", "Calculo numerico", "Metodos  tecnicas de programacion", "Base de datos I",
    "Circuitos electronicos",
    "Estadistica II", "Investigacion operativa I", "Contabilidad Basica", "Sistemas de Informacion I",
    "Base de datos II",
    "Taller de sistemas operativos", "Mercadotecnia", "Investigacion operativa II"
]


def log_message(agent, message):
    agent.log_info('Recibido: %s' % message)


nombre_cajero = "Cajero1"
nombre_director = "Director1"
semestre = "1/2022"
estudiantes = []
nombre_estudiante = "Estudiante1"
nombre_estudiante = nombre_estudiante.replace(nombre_estudiante[len(nombre_estudiante) - 1:], str(random.randint(1, 10)))
cantidad_aleatoria = random.randint(1, 6)
materias_deseadas = random.sample(materiasRecibidas, cantidad_aleatoria)
cod_sys = "2018" + str(random.randint(10000, 99999))
# Cajero
nombre_cajero = nombre_cajero.replace(nombre_cajero[len(nombre_cajero) - 1:], str(random.randint(1, 10)))
# Director
nombre_director = nombre_director.replace(nombre_director[len(nombre_director) - 1:], str(random.randint(1, 10)))
semestre = siguiente_semestre(semestre)

materiasHabilitadasArr = [
    "Algebra I", "Calculo I", "Introduccion a la programacion", "Metodologia de la investigacion", "Fisica General",
    "Ingles", "Algebra II",
    "Calculo II", "Matematica discreta", "Elementos de programacion y estrucutura de datos",
    "Arquitectura de computadoras", "Estadistica I",
    "Ecuaciones diferenciales", "Calculo numerico", "Metodos  tecnicas de programacion", "Base de datos I",
    "Circuitos electronicos",
    "Estadistica II", "Investigacion operativa I", "Contabilidad Basica", "Sistemas de Informacion I",
    "Base de datos II",
    "Taller de sistemas operativos", "Mercadotecnia", "Investigacion operativa II"
]

if __name__ == '__main__':

    # Inicializacion de agentes con sus atributos
    ns = run_nameserver()

    estudiante = run_agent(bcolors.OKCYAN + nombre_estudiante + bcolors.ENDC, attributes={
        "materiasDeseadas": materias_deseadas,
        "codSys": cod_sys,
        "boleta": False,
        "billetera": 250,
    })
    cajero = run_agent(bcolors.WARNING + nombre_cajero + bcolors.ENDC, attributes={
        "monto": 14
    })
    director = run_agent(bcolors.FAIL + nombre_director + bcolors.ENDC, attributes={
        "materiasRecibidas": materiasRecibidas,
        "semestre": semestre,
        "estudiantes": estudiantes
    })
    responsable = run_agent(bcolors.HEADER + 'ResponsableA' + bcolors.ENDC, attributes={
        "materiasHabilitadas": materiasHabilitadasArr
    })

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
    if cajero.get_attr("monto") <= estudiante.get_attr("billetera"):
        monto_restante = abs(estudiante.get_attr("billetera") - cajero.get_attr("monto"))
        estudiante.set_attr(billetera=monto_restante, boleta=True)
    else:
        print(bcolors.OKBLUE + "  ----SISTEMA----   el estudiante no tiene dinero:" + bcolors.ENDC)
    print(bcolors.OKBLUE + "   ----SISTEMA----   el estudiante tiene en la billetera: " + str(
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
    if estudiante.get_attr("boleta"):
        print(bcolors.HEADER + '  (ESTUDIANTE)  Mi codigo Sys es: ' + str(
            estudiante.get_attr("codSys")) + ' y tengo el recibo de mi boleta aqui' + bcolors.ENDC)
        materiasTomadas = [x for x in director.get_attr("materiasRecibidas") if
                           x in estudiante.get_attr("materiasDeseadas")]
        if len(materiasTomadas) >= 1:
            # El director inscribe a los estudiantes
            time.sleep(1)
            todos_los_estudiantes = director.get_attr("estudiantes")
            todos_los_estudiantes.append({
                "codSys": estudiante.get_attr("codSys"),
                "boleta": estudiante.get_attr("boleta"),
                "materiasInscritas": materiasTomadas

            }, )
            director.set_attr(estudiantes=todos_los_estudiantes)
            print(bcolors.WARNING + '  (DIRECTOR)  Te inscribi con exito en tus materias!!' + bcolors.ENDC)
            materiasUltimoEstudiante = todos_los_estudiantes[len(todos_los_estudiantes) - 1]
            print(bcolors.OKBLUE + "(------SISTEMA------)  El director inscribio al estudiante en las siguientes "
                                   "materias: " + bcolors.ENDC
                  , *materiasUltimoEstudiante["materiasInscritas"], sep='      \n- ')
        else:
            time.sleep(1)
            print(
                bcolors.WARNING + '  (DIRECTOR)  No existen materias habilitadas suficientes para que puedas continuar.' + bcolors.ENDC)
    else:
        time.sleep(1)
        print(bcolors.WARNING + '  (DIRECTOR)  Debes pasar por caja y comprar una boleta.' + bcolors.ENDC)

    print(bcolors.OKBLUE + '(------SISTEMA------) Fin Iteracion.' + bcolors.ENDC)
    # ns.shutdown()
