**SM Educamos - Savia digital** ofrece a los profesores unos recursos que solo están
disponibles de manera online (tras autenticación) y que son de difícil
descarga.

El objetivo de este script es automatizar la generación de `html` estático
y accesible de manera offline con el contenido de esos recursos.

De esta manera los profesores no dependerán de la, en ocasiones,
precaria conexión a internet de los centros educativos, y podrán impartir
clase de manera más cómoda y segura.

Por el momento este script solo se ha usado para la asignatura de
matemáticas y por ello incluye la librería `MathJax.js` que probablemente
sobrara para otras asignaturas.

Para ejecutar el script primero ha de escribirse un fichero `config.yml`
como el siguiente ejemplo:

```yaml
url: https://login.educamos.sm/
form: user-login-form
login_user: ************
login_pass: ************
```

La `url` es la dirección donde se encuentra el formulario de logeo
para entrar en *SM Educamos - Savia digital*. `form` es el `id` del formulario `html`
a rellenar para entrar en el portal.

El resto de campos son los valores del formulario que queremos
sobreescribir para hacer `login`.

Como la web de *SM Educamos - Savia digital* cambia de vez en cuando, si el script no
funciona hay que mirar con un inspector de códgio html (por [ejemplo](firefox.png) en
`firefox`) cual es el `id` actual del formulario de logeo y cual es el
`name` de los campos para usuario y contraseña, a fin de rescribir
`config.yml` con los nuevos valores.

La salida del script sera generada en el directorio `out`.

Ejemplo de ejecución:

```console
$ python3 sm.py 
1 BACH Matemáticas aplicadas a las Ciencias Sociales I
   1 - Números reales
   2 - Matemática financiera
   3 - Expresiones algebraicas
   4 - Ecuaciones y sistemas
   5 - Inecuaciones y sistemas
   6 - Funciones
   7 - Límites y continuidad
   8 - Derivadas
   9 - Funciones elementales
  10 - Estadística unidimensional
  11 - Estadística bidimensional
  12 - Combinatoria y probabilidad
  13 - Distribución binomial
  14 - Distribución normal
1º ESO Matemáticas
   1 - Números naturales. Divisibilidad
   2 - Números enteros
   3 - Potencias y raíz cuadrada
   4 - Fracciones
   5 - Números decimales
   6 - Magnitudes proporcionales. Porcentajes
   7 - Ecuaciones
   8 - Tablas y gráficas
   9 - Estadística y probabilidad
  10 - Medida de magnitudes
  11 - Elementos geométricos
  12 - Figuras geométricas
  13 - Longitudes y áreas
  14 - Cuerpos geométricos. Volúmenes
2º ESO Matemáticas
   1 - Divisibilidad. Números enteros
   2 - Fracciones y decimales
   3 - Potencias y raíces
   4 - Proporcionalidad
   5 - Expresiones algebraicas
   6 - Ecuaciones
   7 - Sistemas de ecuaciones
   8 - Funciones
   9 - Medidas. Teorema de Pitágoras
  10 - Semejanza
  11 - Cuerpos geométricos
  12 - Estadística
  13 - Probabilidad
3º ESO Matemáticas orientadas a las enseñanzas académicas
   1 - Conjuntos numéricos
   2 - Potencias y raíces
   3 - Polinomios
   4 - División y factorización de polinomios
   5 - Ecuaciones y sistemas
   6 - Proporcionalidad
   7 - Figuras planas
   8 - Movimientos en el plano
   9 - Cuerpos geométricos
  10 - Sucesiones
  11 - Funciones
  12 - Funciones lineales y cuadráticas
  13 - Estadística unidimensional
  14 - Probabilidad
4º ESO Matemáticas orientadas a las enseñanzas académicas
   1 - Números reales
   2 - Expresiones algebraicas
   3 - Ecuaciones y sistemas
   4 - Inecuaciones y sistemas
   5 - Semejanza y trigonometría
   6 - Aplicaciones de la trigonometría
   7 - Geometría analítica
   8 - Funciones
   9 - Funciones elementales
  10 - Introducción al concepto de límite
  11 - Introducción al concepto de derivada
  12 - Combinatoria
  13 - Probabilidad
  14 - Estadística
$ ls out/
ESO_1.01_-_Números_naturales._Divisibilidad.html        ESO_2.06_-_Ecuaciones.html                              ESO_3.12_-_Funciones_lineales_y_cuadráticas.html
ESO_1.02_-_Números_enteros.html                         ESO_2.07_-_Sistemas_de_ecuaciones.html                  ESO_3.13_-_Estadística_unidimensional.html
ESO_1.03_-_Potencias_y_raíz_cuadrada.html               ESO_2.08_-_Funciones.html                               ESO_3.14_-_Probabilidad.html
ESO_1.04_-_Fracciones.html                              ESO_2.09_-_Medidas._Teorema_de_Pitágoras.html           ESO_4.01_-_Números_reales.html
ESO_1.05_-_Números_decimales.html                       ESO_2.10_-_Semejanza.html                               ESO_4.02_-_Expresiones_algebraicas.html
ESO_1.06_-_Magnitudes_proporcionales._Porcentajes.html  ESO_2.11_-_Cuerpos_geométricos.html                     ESO_4.03_-_Ecuaciones_y_sistemas.html
ESO_1.07_-_Ecuaciones.html                              ESO_2.12_-_Estadística.html                             ESO_4.04_-_Inecuaciones_y_sistemas.html
ESO_1.08_-_Tablas_y_gráficas.html                       ESO_2.13_-_Probabilidad.html                            ESO_4.05_-_Semejanza_y_trigonometría.html
ESO_1.09_-_Estadística_y_probabilidad.html              ESO_3.01_-_Conjuntos_numéricos.html                     ESO_4.06_-_Aplicaciones_de_la_trigonometría.html
ESO_1.10_-_Medida_de_magnitudes.html                    ESO_3.02_-_Potencias_y_raíces.html                      ESO_4.07_-_Geometría_analítica.html
ESO_1.11_-_Elementos_geométricos.html                   ESO_3.03_-_Polinomios.html                              ESO_4.08_-_Funciones.html
ESO_1.12_-_Figuras_geométricas.html                     ESO_3.04_-_División_y_factorización_de_polinomios.html  ESO_4.09_-_Funciones_elementales.html
ESO_1.13_-_Longitudes_y_áreas.html                      ESO_3.05_-_Ecuaciones_y_sistemas.html                   ESO_4.10_-_Introducción_al_concepto_de_límite.html
ESO_1.14_-_Cuerpos_geométricos._Volúmenes.html          ESO_3.06_-_Proporcionalidad.html                        ESO_4.11_-_Introducción_al_concepto_de_derivada.html
ESO_2.01_-_Divisibilidad._Números_enteros.html          ESO_3.07_-_Figuras_planas.html                          ESO_4.12_-_Combinatoria.html
ESO_2.02_-_Fracciones_y_decimales.html                  ESO_3.08_-_Movimientos_en_el_plano.html                 ESO_4.13_-_Probabilidad.html
ESO_2.03_-_Potencias_y_raíces.html                      ESO_3.09_-_Cuerpos_geométricos.html                     ESO_4.14_-_Estadística.html
ESO_2.04_-_Proporcionalidad.html                        ESO_3.10_-_Sucesiones.html                              m
ESO_2.05_-_Expresiones_algebraicas.html                 ESO_3.11_-_Funciones.html
```
