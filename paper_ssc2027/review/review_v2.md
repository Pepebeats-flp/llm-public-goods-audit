# Etapa 4 — ronda 2 (paper con los dos estudios)

Fecha: 18-11-2026. Borrador revisado: `latex_writeup/paper.tex` tras incorporar el Estudio 2. Revisión hecha por un agente independiente, con la instrucción de cotejar cada número contra `raw_materials/experimental_log.md` y los CSV de `llm-public-goods-study/data/processed/`.

## Verificado sin cambios

Conteos de diseño (14.400, 1.500, 2.040, 17.940, 576, 12.000, 410 juegos, 15.503 llamadas); las tres tablas celda por celda; todos los números del Estudio 1; A1 (cuatro de cinco) y A2 (cinco de cinco); D1 con sus intervalos ajustados; D2; D3; los porcentajes de la inestabilidad entre tandas; el brazo exploratorio de `glm-5.3-flash`; la descripción del juego repetido frente al código; las 22 citas. Sin punto y coma ni rayas largas en la prosa.

## Hallazgos y qué se hizo

| # | Severidad | Hallazgo | Acción |
|---|---|---|---|
| 1 | Bloqueante | "Three of five models contribute nothing under every wording" era falso: solo dos dan cero en las ocho variantes; el tercero da 20,8 % bajo "Teamwork". Aparecía en resumen, discusión, implicaciones y conclusión | Corregido en los cuatro lugares: tres bajo toda paráfrasis, dos bajo toda redacción |
| 2 | Importante | "Only weakly by the modelled incentives" no vale con razonamiento, donde los incentivos deciden en el borde del dilema | Frase del resumen reemplazada |
| 3 | Importante | No se declaraba que dos corridas se repartieron en procesos paralelos | Declarado en el diseño |
| 4 | Importante | No quedaba claro qué análisis del Estudio 2 son confirmatorios | Frase en el diseño: A1, A2 y D1 confirmatorios; D2 y D3 de dirección; el resto descriptivo o exploratorio. El párrafo del agente fijo se etiqueta como exploratorio |
| 5 | Importante | "Persists" describía mal D1: en los tres modelos la brecha crece entre la ronda 1 y la 10 | Se reportan las brechas de la ronda 1 junto a las de la 10 y se quitó la generalización |
| 6 | Importante | La caída en grupos humanos no tenía cita | Citado Fischbacher y Gächter (2010) |
| 7 | Importante | H5 definida y no reportada en los resultados del Estudio 1 | Frase con datos agregada en 5.1 |
| 8–9 | Menor | Dos redondeos: [0,46; 0,65] debía ser [0,45; 0,65]; "20 a 34" debía ser "20 a 33" | Corregidos |
| 10 | Menor | D3 sin acotar a la redacción base ni informar grupos excluidos | Acotado; se informan 13 a 15 grupos por modelo y 5 para `hy3` |
| 11 | Menor | "An hour later" y "within the hour" frente a 22 minutos; generalización desde un modelo | Unificado en "22 minutes"; la implicación habla de "one hosted model" |
| 12 | Menor | "Contributed nothing in the one-shot game" solo vale para la redacción base | Acotado |
| 13 | Menor | Fecha de acceso decía solo 17 de noviembre | Corregido a 17 y 18 |
| 14 | Menor | "Apply the payoff rule" es lenguaje mentalista | Cambiado a "behave consistently with" |
| 15 | Menor | La introducción rozaba una conclusión de política | Frase eliminada |
| 16 | Menor | "Did not differ" demasiado fuerte para el chequeo de estabilidad | "No detectable difference" |
| 17 | Menor | No se decía que los grupos con agente fijo usan solo la redacción base | Agregado |
| 19 | Menor | "Preregistration" en disponibilidad de datos chocaba con "no registry" | Cambiado a "analysis plans" |

No verificables por el revisor: "20 of 22" y "15 of 35" de la introducción, que vienen de Vanhée et al. y de Larooij y Törnberg y fueron cotejados contra esos textos el 17-11-2026.

## Revisión de formato

Páginas renderizadas con PyMuPDF y revisadas en imagen. Tablas y figuras sin solapes. Para caber en 12 páginas las dos figuras quedaron al 72 % del ancho; siguen legibles por ser vectoriales, pero conviene mirarlas impresas.

## Recortes hechos para caber en 12 páginas

Se quitaron la figura de descomposición de varianza (sus números están en la Tabla 1 y en el texto), la tabla de estudios previos (pasó a texto), la fila "All models" de la Tabla 2 y cinco referencias. Se condensaron trabajo relacionado, el resumen ODD, el diseño y la discusión. La versión de un solo estudio está en `latex_writeup/paper_v1_study1_only.tex`.

## Pendiente

- Lectura completa por los autores.
- Si el CFP de 2027 no cuenta las referencias en el límite, hay espacio para devolver la figura de varianza y agrandar las otras dos.
- Edmonds (2026), Li y Wu (2025) citados desde el abstract por decisión de los autores.
