# -*- coding: utf-8 -*-
"""México, 3.er grado de preescolar (Fase 2): definición de los 13 temas. gen_mx_matematicas_pre_<slug>.py llama build(slug)."""
import random
import mx_pre as S
from mx_common import src, unit
from mx_12 import BIG, all_le, std_units, s_calendario, s_ayer

ES = 59900


def es(mod, *names, n=10, extra=()):
    return src("gen_es_matematicas_" + mod, ES + sum(map(ord, mod)), *names, lv=1, mx_=BIG, extra=(all_le(n),) + tuple(extra))


def L(f, *k, **kw):
    return lambda: f(*k, **kw)


def spec(slug):
    if slug == "contar-hasta-10":
        return dict(sort=1, cont="P0N", std="Cuenta objetos de su entorno, construye colecciones y representa cantidades hasta el 10 con dibujos, símbolos y numerales",
                    title="Contar hasta el 10", short="Contar hasta el 10",
                    meta="Ejercicios de matemáticas de preescolar: contar objetos hasta el 10 en filas, montones, cajas, platos, dados y marcos de diez, y leer los números. 100 ejercicios con respuestas.",
                    kb="Cada cosa se cuenta una sola vez", ks="El último número que dices es cuántos hay.",
                    think=["Señala cada objeto y di un número: uno, dos, tres… <b>Cada objeto se cuenta una sola vez.</b>",
                           "El último número que dices es <b>cuántos hay</b>.",
                           "Si los objetos están revueltos, ve tachando o moviendo los que ya contaste."],
                    ex=[("¿Cuántas manzanas hay? (7 en fila)", ["uno, dos, tres, cuatro, cinco, seis, siete"], "7")],
                    mist=[["Contar dos veces el mismo objeto", "Toca cada uno una sola vez."], ["Saltarse un número", "Di los números en orden: 1, 2, 3…"], ["Decir el número de un objeto como el total", "El total es el último número."]],
                    faq=[("¿Hasta qué número cuentan en preescolar?", "Cuentan objetos hasta el 10 o más, y recitan la serie hasta el 20 o 30."), ("¿Cómo ayudo en casa?", "Cuenten juntos cosas reales: escalones, cucharas, juguetes.")],
                    sets=[("Contar en fila", [(L(S.contar, "fila"), 20)]), ("Contar revueltos", [(L(S.contar, "disperso"), 20)]), ("Cajas y platos", [(L(S.contar, "caja"), 10), (L(S.contar, "plato"), 10)]),
                          ("Dados y marcos de diez", [(L(S.contar, "dados"), 12), (L(S.contar, "marco"), 8)]), ("Leer los números", [(S.palabra, 18), (L(S.contar, "fila"), 2)])])
    if slug == "numeros-hasta-el-20":
        return dict(sort=2, cont="P0N", std="Recita la serie numérica en orden ascendente y descendente, amplía su rango de conteo hasta el 20 y reconoce el número que va antes y después",
                    title="Los números hasta el 20", short="Números hasta el 20",
                    meta="Ejercicios de matemáticas de preescolar: contar hasta el 20, número antes y después, series de números que faltan y saltos en la recta. 100 ejercicios con respuestas.",
                    kb="Después del 10 viene 11, 12, 13…", ks="Cada número es uno más que el anterior.",
                    think=["Los números van en orden: 1, 2, 3… 10, 11, 12… 20. <b>Cada número es uno más</b> que el anterior.",
                           "«Después» es el número que sigue; «antes» es el que va justo atrás.",
                           "Para contar hacia atrás: 10, 9, 8, 7…"],
                    ex=[("¿Qué número va después del 14?", ["14, 15"], "15"), ("10, 9, __, 7", ["Baja de uno en uno"], "8")],
                    mist=[["Decir «diez y uno» en vez de once", "Después del 10 van once, doce, trece…"], ["Confundir antes y después", "Antes es el de atrás; después, el que sigue."], ["Escribir 51 en vez de 15", "El 1 va primero: quince = 15."]],
                    faq=[("¿Qué es la serie numérica?", "Los números dichos en orden: uno, dos, tres… Es la base para contar."), ("¿Por qué contar hacia atrás?", "Ayuda a entender que quitar es ir hacia números más pequeños.")],
                    sets=[("Contar hasta el 20", [(L(S.contar, "fila", hi=20), 10), (L(S.contar, "disperso", hi=20), 10)]), ("Después de", [(L(S.antes_despues, "despues"), 19), (L(S.contar, "disperso", hi=20), 1)]),
                          ("Antes de y entre", [(L(S.antes_despues, "antes"), 10), (L(S.antes_despues, "entre"), 10)]), ("¿Qué número falta?", [(L(S.serie, "sube"), 14), (L(S.serie, "baja"), 6)]),
                          ("Saltos de la rana", [(S.salta, 20)])])
    if slug == "comparar-colecciones":
        return dict(sort=3, cont="P0N", std="Compara colecciones con distintas estrategias para saber dónde hay más, menos o igual, e iguala colecciones",
                    title="Más, menos o igual", short="Comparar colecciones",
                    meta="Ejercicios de matemáticas de preescolar: comparar colecciones, dónde hay más, menos o igual, comparar números y cuántos faltan para igualar. 100 ejercicios con respuestas.",
                    kb="Cuenta los dos grupos y compara", ks="El número más grande dice dónde hay más.",
                    think=["Para comparar, <b>cuenta cada grupo</b>. Donde el número es mayor, hay <b>más</b>.",
                           "También puedes formar parejas: uno de cada grupo. El grupo al que le sobran tiene más.",
                           "Para <b>igualar</b>, cuenta cuántos le faltan al grupo pequeño."],
                    ex=[("5 flores y 8 pelotas", ["5 es menor que 8"], "hay más pelotas"), ("¿Cuántas flores faltan para tener 8?", ["6, 7, 8: faltan 3"], "3")],
                    mist=[["Fijarse en el tamaño de los objetos", "Lo que importa es cuántos hay."], ["Pensar que lo más extendido es más", "Cuenta: separar los objetos no cambia cuántos son."], ["Olvidar el caso de igual", "Si los números son iguales, hay igual."]],
                    faq=[("¿Qué es una colección?", "Un grupo de objetos que se cuentan juntos, como 5 lápices."), ("¿Cómo se compara sin contar?", "Uniendo cada objeto de un grupo con uno del otro: el que tiene sobrantes tiene más.")],
                    sets=[("¿Dónde hay más?", [(L(S.comparar, "mas"), 20)]), ("¿Dónde hay menos?", [(L(S.comparar, "menos"), 20)]), ("¿Hay igual?", [(L(S.comparar, "igual"), 20)]),
                          ("Número mayor y menor", [(L(S.comparar, "numero"), 20)]), ("¿Cuántos faltan?", [(L(S.comparar, "igualar"), 20)])])
    if slug == "numeros-ordinales":
        return dict(sort=4, cont="P0N", std="Ordena objetos y personas en una fila y usa los números ordinales (primero, segundo, tercero…) para indicar su lugar",
                    title="Primero, segundo, tercero", short="Números ordinales",
                    meta="Ejercicios de matemáticas de preescolar: números ordinales, qué lugar ocupa cada objeto en una fila y en qué lugar llegó cada niño a la meta. 100 ejercicios con respuestas.",
                    kb="Primero, segundo, tercero, cuarto…", ks="Empieza a contar desde donde está la flecha.",
                    think=["Los <b>números ordinales</b> dicen el lugar: primero, segundo, tercero, cuarto, quinto, sexto, séptimo, octavo, noveno, décimo.",
                           "Primero fíjate desde dónde se empieza a contar (la flecha).",
                           "Con palabras de mujer cambian: la primera, la segunda…"],
                    ex=[("Fila: pato, flor, taza. ¿Qué lugar tiene la taza?", ["pato 1.º, flor 2.º, taza 3.º"], "tercera")],
                    mist=[["Empezar a contar por el otro lado", "Mira la flecha."], ["Decir «tres» en vez de «tercero»", "El lugar se dice con ordinales."], ["Saltarse un lugar", "Señala cada objeto en orden."]],
                    faq=[("¿Se dice «primer» o «primero»?", "Antes de un sustantivo se dice «primer lugar»; solo se dice «el primero»."), ("¿Dónde usamos ordinales?", "En filas, carreras, pisos de un edificio y en el orden de los días.")],
                    sets=[("¿En qué lugar está?", [(L(S.ordinal, "lugar"), 20)]), ("¿Qué hay en ese lugar?", [(L(S.ordinal, "que"), 20)]), ("Carreras", [(S.ordinal_carrera, 20)]),
                          ("Más filas", [(L(S.ordinal, "lugar"), 10), (L(S.ordinal, "que"), 10)]), ("Repaso", [(L(S.ordinal, "lugar"), 10), (L(S.ordinal, "que"), 10)])])
    if slug == "agregar-y-quitar":
        jun, qui = es("2_problemas", "s_juntar", "s_quitar")
        return dict(sort=5, cont="P0N", std="Resuelve situaciones de agregar, quitar y juntar con colecciones de hasta 10 elementos, con sus propias estrategias",
                    title="Agregar y quitar", short="Agregar y quitar",
                    meta="Ejercicios de matemáticas de preescolar: problemas de agregar, quitar y juntar con dibujos, hasta el 10. 100 ejercicios con respuestas.",
                    kb="Agregar: hay más. Quitar: hay menos.", ks="Cuenta lo que hay al final.",
                    think=["<b>Agregar</b> es poner más: los objetos aumentan. Cuenta todos al final.",
                           "<b>Quitar</b> es sacar o regalar: tacha los que se van y cuenta los que quedan.",
                           "<b>Juntar</b> dos grupos es contarlos todos juntos."],
                    ex=[("Tengo 4 globos y me dan 3", ["4… 5, 6, 7"], "7 globos"), ("Tengo 6 galletas y me como 2", ["tacho 2", "quedan 4"], "4 galletas")],
                    mist=[["Agregar cuando hay que quitar", "«Regaló», «se comió», «se fueron» quieren decir quitar."], ["Contar también los tachados", "Solo cuentan los que quedan."], ["Contar desde 1 cada vez", "Puedes seguir contando desde el primer número."]],
                    faq=[("¿Hay que usar los signos + y −?", "En preescolar basta resolver con dibujos, dedos u objetos."), ("¿Cómo practicar?", "Con juguetes reales: «tienes 5 carritos, te doy 2, ¿cuántos tienes?».")],
                    sets=[("Agregar", [(L(S.historia, "agregar"), 20)]), ("Quitar", [(L(S.historia, "quitar"), 20)]), ("Juntar", [(L(S.historia, "juntar"), 20)]),
                          ("Problemas con dibujos", [(jun, 10), (qui, 10)]), ("Repaso", [(L(S.historia, "agregar"), 7), (L(S.historia, "quitar"), 7), (L(S.historia, "juntar"), 6)])])
    if slug == "separar-y-repartir":
        return dict(sort=6, cont="P0N", std="Resuelve situaciones de separar una colección en partes y de repartir por partes iguales, y descompone números hasta el 10",
                    title="Separar y repartir", short="Separar y repartir",
                    meta="Ejercicios de matemáticas de preescolar: separar una colección, cuántos están tachados o escondidos, formas de formar un número hasta el 10 y repartir por partes iguales. 100 ejercicios con respuestas.",
                    kb="7 es 3 y 4, o 5 y 2…", ks="Repartir: a todos les toca lo mismo.",
                    think=["Un número se puede <b>separar</b> en dos partes: 7 es 3 y 4, o 5 y 2, o 6 y 1.",
                           "Si sabes el total y una parte, la otra parte es lo que falta.",
                           "<b>Repartir por partes iguales</b>: da uno a cada quien, por turnos, hasta que se acaben."],
                    ex=[("8 son 5 y __", ["5, 6, 7, 8: faltan 3"], "3"), ("Reparte 6 galletas entre 2 niños", ["uno y uno, uno y uno…"], "3 a cada uno")],
                    mist=[["Repartir sin que toque lo mismo", "Todos deben recibir igual."], ["Contar el total como una parte", "Las dos partes juntas forman el total."], ["Olvidar que una parte puede ser 0", "8 es 8 y 0."]],
                    faq=[("¿Por qué separar números?", "Ayuda a sumar y restar después: saber que 10 es 7 y 3 facilita muchas cuentas."), ("¿Qué pasa si sobra?", "Si no alcanza para dar uno más a cada quien, esos objetos sobran.")],
                    sets=[("¿Cuántos están tachados?", [(S.descomponer, 20)]), ("Formar números", [(S.descomponer, 20)]), ("Separar en dos colores", [(L(S.historia, "separar"), 20)]),
                          ("Repartir por partes iguales", [(S.repartir, 20)]), ("Repaso", [(S.repartir, 10), (S.descomponer, 10)])])
    if slug == "monedas-y-billetes":
        return dict(sort=7, cont="P0N", std="Reconoce el valor de monedas y billetes, los usa en situaciones de compra y estima si le alcanza el dinero",
                    title="Monedas y billetes", short="Monedas y billetes",
                    meta="Ejercicios de matemáticas de preescolar: reconocer monedas de $1, $2, $5 y $10 y el billete de $20, contar dinero y saber si alcanza para comprar. 100 ejercicios con respuestas.",
                    kb="Mira el número de la moneda", ks="Una moneda de $5 vale como 5 de $1.",
                    think=["Cada moneda y billete tiene escrito su <b>valor</b>: $1, $2, $5, $10, $20.",
                           "Para saber cuánto dinero hay, suma los valores, no cuentes monedas.",
                           "Te <b>alcanza</b> si tienes igual o más dinero de lo que cuesta."],
                    ex=[("$5 + $2 + $1", ["5, 6, 7, 8"], "$8"), ("Tengo $10 y la paleta cuesta $8", ["10 es más que 8"], "sí me alcanza")],
                    mist=[["Pensar que la moneda más grande vale más", "Mira el número."], ["Contar monedas en vez de sumar valores", "Dos monedas de $5 son $10, no 2."], ["Creer que no alcanza si sobra", "Si sobra, sí alcanza."]],
                    faq=[("¿Qué monedas usamos en México?", "50 centavos, $1, $2, $5, $10 y $20; y billetes de $20, $50, $100, $200, $500 y $1 000."), ("¿Cómo practicar?", "Jugando a la tiendita con monedas de verdad o de papel.")],
                    sets=[("¿Cuánto vale?", [(L(S.dinero, "cual"), 6), (L(S.dinero, "mas"), 12), (L(S.dinero, "contar"), 2)]), ("¿Cuánto dinero hay?", [(L(S.dinero, "contar"), 20)]),
                          ("Pagar con monedas", [(L(S.dinero, "monedas"), 20)]), ("¿Me alcanza?", [(L(S.dinero, "alcanza"), 20)]), ("Repaso", [(L(S.dinero, "alcanza"), 10), (L(S.dinero, "monedas"), 5), (L(S.dinero, "contar"), 5)])])
    if slug == "posiciones-y-recorridos":
        a, b, c, d = es("2_posiciones", "s_mesa", "s_caja", "s_estante", "s_fila")
        return dict(sort=8, cont="P0E", std="Describe la posición de objetos y personas respecto a su cuerpo y a otros objetos (arriba, abajo, dentro, fuera, delante, detrás, al lado) y comunica recorridos",
                    title="¿Dónde está?", short="Posiciones",
                    meta="Ejercicios de matemáticas de preescolar: arriba, abajo, dentro, fuera, delante, detrás, al lado, izquierda y derecha, y lugares en un estante y en una fila. 100 ejercicios con respuestas.",
                    kb="Arriba, abajo, dentro, al lado", ks="Fíjate en qué objeto se usa de referencia.",
                    think=["Para decir dónde está algo, se compara con otro objeto: la pelota está <b>arriba de</b> la mesa, <b>debajo de</b> la silla, <b>dentro de</b> la caja.",
                           "<b>Delante</b> es lo que se ve primero; <b>detrás</b> queda tapado.",
                           "Izquierda y derecha se ven desde quien mira el dibujo."],
                    ex=[("El gato está sobre la caja", ["sobre = arriba"], "arriba de la caja")],
                    mist=[["Confundir dentro y detrás", "Detrás: tapado por el objeto; dentro: adentro del objeto."], ["Mezclar izquierda y derecha", "Levanta la mano con la que comes o escribes y compara."], ["Olvidar el objeto de referencia", "Di siempre «arriba de qué»."]],
                    faq=[("¿Cómo enseñar izquierda y derecha?", "Con juegos como «Simón dice: levanta la mano derecha»."), ("¿Qué es un recorrido?", "Un camino de un lugar a otro, descrito con palabras como «sigue derecho, da vuelta junto al árbol».")],
                    sets=[("La mesa", [(a, 20)]), ("La caja", [(b, 20)]), ("El estante", [(c, 20)]), ("La fila", [(d, 20)]), ("Repaso", [(a, 5), (b, 5), (c, 5), (d, 5)])])
    if slug == "figuras-y-cuerpos":
        fn, fl, fc, fs = es("2_figuras_planas", "s_nombre", "s_lados", "s_contar", "s_saber")
        cn, co, cr, cs = es("2_cuerpos", "s_nombre", "s_objeto", "s_rueda", "s_saber")
        return dict(sort=9, cont="P0E", std="Identifica atributos geométricos de figuras y cuerpos y los describe con términos convencionales: círculo, cuadrado, triángulo, rectángulo, esfera, cubo, cilindro, cono",
                    title="Figuras y cuerpos", short="Figuras y cuerpos",
                    meta="Ejercicios de matemáticas de preescolar: nombres de figuras (círculo, cuadrado, triángulo, rectángulo) y cuerpos (cubo, esfera, cilindro, cono), lados, esquinas y objetos que ruedan. 100 ejercicios con respuestas.",
                    kb="Cuenta lados y esquinas", ks="El círculo no tiene lados rectos.",
                    think=["Las <b>figuras</b> son planas: círculo, triángulo (3 lados), cuadrado (4 lados iguales), rectángulo (4 lados, 2 largos y 2 cortos).",
                           "Los <b>cuerpos</b> tienen volumen: esfera (como una pelota), cubo (como un dado), cilindro (como una lata), cono (como un barquillo).",
                           "Los cuerpos con partes curvas <b>ruedan</b>; los que tienen caras planas se pueden apilar."],
                    ex=[("¿Cuántos lados tiene un triángulo?", ["tri = tres"], "3")],
                    mist=[["Decir que un cuadrado volteado es otra figura", "Girado sigue siendo cuadrado."], ["Confundir cubo y cuadrado", "El cuadrado es plano; el cubo es un cuerpo."], ["Confundir esfera y círculo", "La pelota es esfera; su dibujo es un círculo."]],
                    faq=[("¿Por qué jugar con bloques?", "Construir con bloques y tangram ayuda a reconocer formas y cómo se combinan."), ("¿Qué figura tiene más lados?", "De las básicas, el cuadrado y el rectángulo, con 4.")],
                    sets=[("Nombres de figuras", [(fn, 20)]), ("Lados y esquinas", [(fl, 10), (fc, 10)]), ("Nombres de cuerpos", [(cn, 20)]), ("Cuerpos en la vida diaria", [(co, 12), (cr, 8)]),
                          ("Repaso", [(fs, 10), (cs, 8), (cr, 2)])])
    if slug == "patrones":
        a, b, c = es("2_patrones", "s_siguiente", "s_grupo", "s_serie", n=20)
        return dict(sort=10, cont="P0E", std="Crea y reproduce patrones de repetición y de crecimiento con objetos, figuras, colores y números",
                    title="Patrones", short="Patrones",
                    meta="Ejercicios de matemáticas de preescolar: qué sigue en un patrón de colores, figuras y objetos, cuál es el grupo que se repite y series que crecen. 100 ejercicios con respuestas.",
                    kb="Busca lo que se repite", ks="Dilo en voz alta: rojo, azul, rojo, azul…",
                    think=["Un <b>patrón</b> es algo que se repite siempre igual: rojo, azul, rojo, azul…",
                           "Encuentra el <b>grupo que se repite</b> (el núcleo) y continúa.",
                           "En un patrón que crece, cada paso tiene uno más: 1, 2, 3…"],
                    ex=[("círculo, cuadrado, círculo, cuadrado, …", ["se repite círculo, cuadrado"], "círculo")],
                    mist=[["Mirar solo el último dibujo", "Busca el grupo completo que se repite."], ["Cambiar el orden al continuar", "Sigue exactamente el mismo orden."], ["Pensar que todo se repite de dos en dos", "El grupo puede tener 3 o más elementos."]],
                    faq=[("¿Dónde hay patrones?", "En collares, rayas de la ropa, mosaicos, canciones y aplausos."), ("¿Para qué sirven?", "Ayudan a predecir lo que sigue y son la base del álgebra.")],
                    sets=[("¿Qué sigue?", [(a, 20)]), ("El grupo que se repite", [(b, 20)]), ("Series de números", [(c, 10), (L(S.serie, "sube"), 10)]), ("Más patrones", [(a, 10), (b, 10)]), ("Repaso", [(a, 10), (b, 10)])])
    if slug == "longitud-peso-y-capacidad":
        la, pe, pe2, ca = es("2_medidas", "s_largo", "s_pesa", "s_pesa2", "s_cabe", extra=(std_units,))
        return dict(sort=11, cont="P0M", std="Compara la longitud, el peso y la capacidad de objetos de forma directa, con una balanza o trasvasando, y expresa si son más largos, cortos, pesados o ligeros",
                    title="Largo, pesado y lleno", short="Longitud, peso y capacidad",
                    meta="Ejercicios de matemáticas de preescolar: comparar qué es más largo o más corto, más alto o más bajo, más pesado o más ligero en una balanza y qué tiene más agua. 100 ejercicios con respuestas.",
                    kb="Compara desde el mismo punto", ks="En la balanza, baja lo más pesado.",
                    think=["Para comparar <b>longitudes</b>, pon los objetos uno junto al otro, empezando en el mismo lugar.",
                           "En una <b>balanza</b>, el lado que baja es el más pesado.",
                           "Para saber qué recipiente tiene más, compara el nivel del agua en vasos iguales o pasa el líquido de uno a otro."],
                    ex=[("Lápiz A llega más lejos que B", ["empiezan en el mismo lugar"], "A es más largo")],
                    mist=[["No alinear el inicio", "Empieza a comparar desde el mismo punto."], ["Pensar que lo grande siempre pesa más", "Un globo es grande y ligero."], ["Comparar el agua en vasos distintos", "En vasos de distinto ancho la altura engaña."]],
                    faq=[("¿Se usa la regla en preescolar?", "Primero se compara directo y con unidades no convencionales (manos, pasos, clips)."), ("¿Cómo hacer una balanza en casa?", "Con un gancho de ropa y dos vasos colgados.")],
                    sets=[("Más largo y más corto", [(L(S.medir, "largo"), 10), (L(S.medir, "corto"), 10)]), ("Más alto y más bajo", [(L(S.medir, "alto"), 20)]), ("La balanza", [(L(S.medir, "pesa"), 20)]),
                          ("¿Qué tiene más agua?", [(L(S.medir, "cabe"), 20)]), ("Repaso", [(L(S.medir, "pesa"), 7), (L(S.medir, "largo"), 7), (L(S.medir, "cabe"), 6)])])
    if slug == "el-tiempo":
        R = random.Random(59012)
        cal, ay = s_calendario(R, 1), s_ayer(R)
        return dict(sort=12, cont="P0M", std="Ordena sucesos de su vida diaria, distingue mañana, tarde y noche, ayer, hoy y mañana, y usa el calendario para percibir el paso del tiempo",
                    title="El tiempo", short="El tiempo",
                    meta="Ejercicios de matemáticas de preescolar: mañana, tarde y noche, qué pasa antes y después, días de la semana, ayer y mañana, el calendario y qué dura más. 100 ejercicios con respuestas.",
                    kb="Antes, ahora, después", ks="La semana tiene 7 días.",
                    think=["El día tiene <b>mañana, tarde y noche</b>. Desayunamos en la mañana y dormimos en la noche.",
                           "Las cosas pasan en orden: primero, después, al final.",
                           "La semana tiene <b>7 días</b>: lunes, martes, miércoles, jueves, viernes, sábado y domingo. El calendario los muestra."],
                    ex=[("Hoy es martes", ["ayer: lunes", "mañana: miércoles"], "")],
                    mist=[["Confundir ayer y mañana", "Ayer ya pasó; mañana todavía no llega."], ["Pensar que la semana empieza siempre en domingo", "En el calendario puede empezar en domingo o en lunes."], ["Ordenar al revés", "Primero lo que pasa antes."]],
                    faq=[("¿Se aprende a leer el reloj en preescolar?", "Se empieza a conocer el reloj y el calendario; la hora exacta se aprende en primaria."), ("¿Cómo practicar?", "Hablen de lo que hicieron ayer y lo que harán mañana; marquen fechas en un calendario.")],
                    sets=[("Mañana, tarde y noche", [(L(S.tiempo, "parte"), 13), (L(S.tiempo, "instrumento"), 7)]), ("Antes y después", [(L(S.tiempo, "antes"), 10), (L(S.tiempo, "despues"), 10)]),
                          ("Días de la semana", [(L(S.tiempo, "dia"), 10), (ay, 10)]), ("El calendario", [(cal, 20)]), ("¿Qué dura más?", [(L(S.tiempo, "dura"), 12), (ay, 8)])])
    if slug == "clasificar-y-registrar-datos":
        pic, mar, cla = es("2_graficos", "s_picto", "s_marcas", "s_clasificar", n=20)
        return dict(sort=13, cont="P0C", std="Clasifica objetos de su entorno según sus características y organiza y registra información en tablas, conteos y pictogramas sencillos",
                    title="Clasificar y contar datos", short="Clasificar y registrar datos",
                    meta="Ejercicios de matemáticas de preescolar: encontrar el que no es del grupo, clasificar objetos, leer marcas de conteo y pictogramas. 100 ejercicios con respuestas.",
                    kb="Junta lo que se parece", ks="Después cuenta cuántos hay en cada grupo.",
                    think=["<b>Clasificar</b> es juntar las cosas que se parecen: frutas con frutas, animales con animales, por color o por forma.",
                           "Para registrar, se hace una <b>marca</b> por cada objeto. Cada 5 marcas se juntan con una raya.",
                           "En un <b>pictograma</b> cada dibujo es un objeto; la fila más larga es la que tiene más."],
                    ex=[("manzana, plátano, perro, uva", ["3 son frutas"], "el perro no es del grupo")],
                    mist=[["Clasificar con dos reglas a la vez", "Elige una sola característica."], ["Contar mal las marcas", "Cuenta de 5 en 5 los grupos con raya."], ["Fijarse en el tamaño de los dibujos", "Cuenta cuántos hay en cada fila."]],
                    faq=[("¿Para qué sirve clasificar?", "Para ordenar y comparar: así se ve rápido de qué hay más."), ("¿Qué es un pictograma?", "Una gráfica con dibujos, donde cada dibujo representa un objeto.")],
                    sets=[("¿Cuál no es del grupo?", [(S.clasificar, 20)]), ("Clasificar", [(cla, 20)]), ("Marcas de conteo", [(mar, 20)]), ("Pictogramas", [(pic, 20)]),
                          ("Repaso", [(S.clasificar, 10), (pic, 7), (mar, 3)])])
    raise KeyError(slug)


def build(slug):
    S.setup(random.Random(59000 + sum(map(ord, slug))))
    t = spec(slug)
    unit(slug, t["sort"], t["cont"], t["std"], t["title"], t["short"], t["meta"], t["kb"], t["ks"], t["think"], t["ex"], t["mist"], t["faq"], t["sets"],
         59100 + t["sort"], lv=0)
