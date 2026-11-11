"""Spanish LA renter checklist (/la-renters-es). Mirrors LA_HOME, LA_DRILL and LA_ASK in build.py; keep them in step."""

TITLE = "Lista de emergencia para inquilinos de Los Ángeles (gratis para imprimir)"
META = ("Una lista gratuita de una página para quienes rentan en Los Ángeles: alertas de NotifyLA y Alert LA County, qué tener en casa, "
        "un simulacro de 10 minutos y qué preguntarle al dueño.")
H1 = "Lista de emergencia para inquilinos de Los Ángeles"
DEK = ("Una lista gratuita de una página para quienes rentan en Los Ángeles: las alertas oficiales, qué tener en casa, "
       "un simulacro de 10 minutos en su edificio y qué preguntarle al dueño o administrador.")
NOTE = ("Esta página no tiene enlaces a productos ni de afiliados. Los consejos vecinales, grupos de inquilinos, bibliotecas y "
        "administradores de edificios pueden imprimirla y compartirla. Traducida del inglés; si ve un error, avísenos.")
CHECKED = "Enlaces revisados en octubre de 2026."

# (label, url, how): same sign-ups as the English page
SIGNUPS = [
    ("Regístrese en NotifyLA", "https://emergency.lacity.gov/notifyla",
     "Mensajes de texto, llamadas y correos gratis de la Ciudad de Los Ángeles sobre emergencias cerca de las direcciones que usted elija."),
    ("Regístrese en Alert LA County", "https://lacounty.gov/emergency/",
     "El sistema del condado. Úselo también, sobre todo si vive fuera de los límites de la ciudad o en un área no incorporada."),
    ("Descargue MyShake", "https://myshake.berkeley.edu/",
     "Alerta temprana de terremotos gratuita del sistema ShakeAlert. Puede darle unos segundos para agacharse, cubrirse y sujetarse antes de que llegue el temblor."),
    ("Busque su zona de evacuación", "https://protect.genasys.com/",
     "El Condado de Los Ángeles emite advertencias y órdenes de evacuación por zona. Busque su dirección, anote su zona y guárdela en su mochila de emergencia."),
]

HOME = [
    ("Agua", "Para empezar, al menos 3 galones por persona; luego llegue a dos semanas: unos 14 galones por persona. Un terremoto fuerte puede romper las tuberías de agua por semanas."),
    ("Comida", "Comida para dos semanas que se pueda comer sin cocinar, y un abrelatas manual."),
    ("Junto a cada cama", "Zapatos resistentes y una linterna o lámpara de cabeza. Los vidrios rotos son la lesión más común en un terremoto."),
    ("Baño de emergencia", "Una cubeta, bolsas de basura gruesas y arena para gatos. Después de un terremoto, no descargue el inodoro hasta saber que el drenaje está bien."),
    ("Humo", "Mascarillas N95 para todos, para el humo de los incendios y el polvo de un terremoto."),
    ("Medicinas y documentos", "Una semana o más de sus medicinas recetadas, lentes de repuesto y copias de identificaciones, su contrato de renta y su seguro."),
    ("Energía y efectivo", "Una batería portátil cargada para cada teléfono y algo de efectivo en billetes chicos."),
    ("Mochila de emergencia", "Una mochila lista junto a la puerta por si tiene que salir rápido por un incendio."),
]

DRILL = [
    "De noche, con las luces apagadas, camine con una linterna desde su cama hasta la escalera más cercana. Cuente las puertas. Los elevadores no funcionan después de un terremoto ni durante un incendio.",
    "Practique agacharse, cubrirse y sujetarse junto a su cama, su escritorio y su sofá.",
    "Ubique la llave de paso del agua de su unidad y pregunte dónde están la llave del gas del edificio y la herramienta para cerrarla. Cierre el gas solo si huele a gas o escucha un silbido.",
    "Elija un punto de encuentro afuera de su edificio y otro fuera del vecindario.",
    "Intercambie números con dos vecinos y fíjese quién podría necesitar ayuda: personas mayores, personas con discapacidad, familias con bebés.",
]

ASK = [
    "¿Está nuestro edificio en la lista de la ciudad de edificios de planta débil (soft-story) o de concreto que necesitan refuerzo sísmico, y ya se hizo el trabajo? También puede buscar la dirección en el sitio del Departamento de Construcción y Seguridad de Los Ángeles (LADBS).",
    "¿Está sujeto con correas el calentador de agua? Si se cae, puede causar un incendio o inundar la unidad.",
    "¿Dónde están las llaves de paso del gas y del agua, y quién tiene las herramientas?",
    "¿Tiene cada unidad alarmas de humo que funcionen, y alarmas de monóxido de carbono donde hay aparatos de gas?",
]

INSURANCE = ("El seguro estándar para inquilinos por lo general no cubre daños por terremoto. La California Earthquake Authority vende "
             "pólizas de terremoto para inquilinos a través de aseguradoras participantes; pregúntele a su agente.")

LINES = ["Nuestra zona de evacuación", "Punto de encuentro cerca de casa", "Contacto fuera del área", "Teléfono de un vecino"]

FOOT = ("De PrepScore, un sitio gratuito de preparación para emergencias · prepscore.org/la-renters-es · Información general, no asesoría "
        "profesional. En una emergencia, siga las indicaciones de las autoridades locales y llame al 911 si hay peligro de muerte.")
