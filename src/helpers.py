malla_curricular = [
    "Algebra I", "Calculo I", "Introduccion a la programacion", "Metodologia de la investigacion", "Fisica General",
    "Ingles I", "Algebra II",
    "Calculo II", "Matematica discreta", "Elementos de programacion y estrucutura de datos",
    "Arquitectura de computadoras", "Estadistica I",
    "Ecuaciones diferenciales", "Calculo numerico", "Metodos  tecnicas de programacion", "Base de datos I",
    "Circuitos electronicos",
    "Estadistica II", "Investigacion operativa I", "Contabilidad Basica", "Sistemas de Informacion I",
    "Base de datos II",
    "Taller de sistemas operativos", "Mercadotecnia", "Investigacion operativa II", "Sistemas I",
    "Sistems de informacion II", "Taller de base de datos", "Aplicacion de sistemas operativos",
    "Sistemas economicos", "Simulacion de sistemas", "Sistemas II", "Ingenieria de software", "Inteligencia artificial",
    "Redes de computadoras", "Planificacion y evaluacion de proyectos", "Dinamica de sistemas", "Topicos selectos I",
    "Taller de ingenieria de software", "Gestion de calidad de software", "Redes avanzadas de computadoras",
    "Gestion estrategica de empresas", "Taller de modelacion y simulacion de sistemas", "Topicos selectos II",
    "Metodologia y planificacion de proyecto de grado", "Evaluacion y auditoria de sistemas", "Seguridad de sistemas",
    "Topicos selectos III", "Topicos selectos IV", "Practica empresarial", "Proyecto final", "Topicos selectos V",
    "Topicos selectos VI"
    "Ingles II", "Ingles III"
]


def siguiente_semestre(semestre):
    mes, anio = semestre.split("/")
    mes = int(mes)
    anio = int(anio)

    mes += 1

    if mes == 3:
        mes = 1
        anio += 1
    semestre = f"{mes}/{anio}"




