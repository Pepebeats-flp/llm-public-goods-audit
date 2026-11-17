# Etapa 4 — revisión simulada, ronda 1 (con resultados)

Fecha: 17-11-2026. Borrador revisado: `latex_writeup/paper.tex` completo, 12 páginas. La revisión la hizo un agente independiente, sin acceso al razonamiento del autor, con la instrucción de cotejar cada número contra `raw_materials/experimental_log.md` y los CSV.

## Resultado de la verificación numérica

Las tablas 2, 3 y 4 coinciden celda a celda con el log y los CSV. Los recuentos del texto ("dos de seis", "3 a 21 veces", "cinco de seis fallan Q2", porcentajes de varianza, conteos de llamadas) coinciden, con las excepciones corregidas abajo. Las ocho variantes de prompt descritas en la sección 4 coinciden con `pgg/prompts.py`. Las 29 claves citadas existen en la bibliografía.

## Hallazgos y qué se hizo

| # | Severidad | Hallazgo | Acción |
|---|---|---|---|
| 1 | Bloqueante | El texto decía que Claude Haiku deja "94 % a 100 %" en el marco de retirar "en cada valor de m"; por valor es 100, 100, 76, 100, 100, 100 | Corregido: 94 % en promedio dentro del dilema y 100 % en ambos controles |
| 2 | Bloqueante | La razón señal/ruido "indefinida" es una desviación del prerregistro y no se declaraba | Declarada en Limitaciones |
| 3 | Bloqueante | Solo se declaraba H6 como decisión posterior al piloto; faltaban la reclasificación de P3, la escritura de P4 y el análisis casi binario | Declaradas en la sección 4 y en Limitaciones |
| 4 | Bloqueante | "We found no study…" convivía con Kořínek y Štekerová sin citarlo | Citado y frase suavizada a "We are not aware of…" |
| 5 | Importante | H2 "se sostiene salvo para un modelo": también falla para Claude Haiku, sin variación entre paráfrasis | Corregido: cuatro de seis |
| 6 | Importante | "Bajo uno para todos los modelos": indefinida para Claude Haiku | Corregido: los cinco donde está definida |
| 7 | Importante | "Tres de cinco pasan a contribución total": Qwen llega a 84 % | Corregido: dos llegan a 98–100 % y uno a 84 % |
| 8 | Importante | Nombrar el juego "lleva a 4 % en cuatro modelos": uno ya estaba en cero; además F3 cambia el vocabulario, no solo el nombre | Corregido en resumen y sección 5.2; se declara que nombre y vocabulario no se separan |
| 9 | Importante | Lenguaje causal o mentalista ("recall", "reverted", "not a calculation error") | Reescrito en términos de conducta observada; la fuga de datos queda como explicación compatible, no demostrada |
| 10 | Importante | El resumen unía contribución cero y vocabulario del razonamiento, sugiriendo mecanismo | Quitado del resumen; en 5.3 se aclara que es un conteo de palabras |
| 11 | Importante | Generalización a "LLM" y a "simulaciones" | Acotado a "fast-tier" y a "in this audit"; conclusión corregida a cinco de seis |
| 12 | Importante | Faltaban Spearman, la regresión logística de robustez, el detalle de H5 y la explicación del salto de H2 a H5 | Agregados en 5.1, 5.3 y sección 4 |
| 13 | Importante | Los agregados de la sección 1 del log no los generaba ningún script | Nuevo `pgg/extra_aggregates.py` |
| 14 | Importante | Citas apoyadas en trabajos leídos solo como abstract (Edmonds; Li y Wu; Kitadai et al.) y rango humano tomado de working papers | **Pendiente de los autores**: las frases usadas están en los abstracts, pero hay que leer los textos completos y cotejar las cifras humanas |
| 15 | Importante | 12 páginas justas con autor ficticio y tres marcadores | **Pendiente**: al poner autoría y declaraciones puede pasarse; ver recortes abajo |
| 16 | Menor | "17.940 llamadas": son celdas; hubo 17.945 llamadas y un fallo de transporte | Corregido en resumen y sección 4 |
| 17 | Menor | Pie de la Tabla 3 impreciso; el 9,8 agrupado no estaba en el log | Pie corregido; dato agregado al log |
| 18 | Menor | Descripción de P2 con cita no literal | Corregido |
| 19 | Menor | No se nombraba el proveedor ni la instantánea de DeepSeek | Agregados |
| 20 | Menor | Umbrales de H1b ambiguos | Corregido con "respectively" |
| 21 | Menor | Editor de la sexta edición de *Moral Sentiments* dudoso; cita de Smith truncada | Se cita la primera edición (1759, A. Millar) y la frase completa. **Verificar** la referencia antes de enviar |
| 22 | Menor | Un `Overfull \hbox` de 3,9 pt | Sin corregir |

## Criterios SSC tras la ronda 1

| # | Criterio | Estado |
|---|---|---|
| 1 | Propósito declarado | Cumple |
| 2 | Replicable (ODD) | Parcial: falta el ODD completo y el repositorio público |
| 3 | Anclaje externo | Parcial: rango humano sin cotejar; prerregistro no público |
| 4 | Robustez | Parcial: un día, una temperatura, 50 decisiones por celda |
| 5 | Memorización | Cumple, con la limitación declarada de F3 |
| 6 | El prompt no predetermina | Cumple: es el objeto del estudio |
| 7 | Versiones y fechas | Cumple en lo que el proveedor informa |
| 8 | Agente frente a colectivo | Cumple tras acotar el resumen; no hay interacción |
| 9 | Línea base de reglas | Parcial: solo la acción dominante como referencia |
| 10 | Implicaciones | Cumple |
| 11 | Formato | Parcial: 12 páginas justas |

## Recortes disponibles si hay que ganar espacio

- Quitar el párrafo sobre recursos comunes y el de Lorè y Heydari en Trabajo relacionado (unas 6 líneas y 3 referencias).
- Pasar la Tabla 1 a una frase (un tercio de página).
- Reducir la Figura 2 al 80 % del ancho.
- Si las referencias no cuentan en el límite de 2027, sobra una página y media.

## Para una ronda 2

- Hacerla después de que los autores lean Edmonds, Li y Wu, y Kořínek y Štekerová, y cotejen las cifras humanas.
- Revisar el PDF renderizado: posición de tablas y figuras, y legibilidad en escala de grises.
- El brazo de razonamiento con todas las variantes queda como trabajo futuro por decisión del autor (17-11-2026); el paper lo declara en Limitaciones.

## Revisión de formato sobre el PDF renderizado (17-11-2026)

Equivale al paso de revisión de formato de PaperOrchestra. Se renderizaron las páginas con PyMuPDF y se miraron una por una.

| Hallazgo | Acción |
|---|---|
| Tabla 1: los textos de columnas vecinas se tocaban | Columnas con texto alineado a la izquierda, anchos ajustados y separación entre filas |
| Tablas 2 y 4: encabezados de grupo que no quedaban sobre sus columnas y números pegados | Reglas parciales bajo cada grupo y más separación entre columnas |
| Tabla 3: columnas apretadas | Reglas parciales por grupo; encabezado "F2 Teamw." abreviado |
| Al corregir las tablas el paper subió a 13 páginas | Se quitó la frase sobre recursos comunes (y sus dos referencias) y la Figura 2 se redujo al 80 % del ancho; vuelve a 12 páginas con 27 referencias |
| Párrafo de modelos con una línea que se salía 13 pt del margen | Corregido |
| Figuras 1 y 2 | Sin problemas: leyendas legibles, sin solapamientos |

Queda un `Overfull \hbox` de 3,9 pt en el párrafo de variantes de prompt, imperceptible a simple vista.

## Verificación de dos citas contra el texto completo (17-11-2026)

- **Kořínek y Štekerová (2026):** leído completo. Dilema del prisionero iterado de 25 rondas, 50 partidas por emparejamiento, cuatro modelos locales, temperatura 0,7, tres prompts (neutro, con sesgo positivo, de hambre), pagos constantes. No varían incentivos ni usan paráfrasis de igual contenido, y reconocen que el prompt de hambre introduce un contexto narrativo que actúa como confusor. La frase del paper es fiel y la afirmación de novedad se mantiene.
- **Kitadai et al. (2025):** leído completo. Juego del ultimátum; "capacidad de razonamiento" operacionalizada como modelo (gpt-3.5 frente a gpt-4) y método de prompting. A mayor capacidad, resultados más cerca de la solución teórica y no de los datos experimentales. La Discusión lo citaba junto a Li y Shirado como evidencia de que razonar "baja la cooperación", lo que no corresponde a un juego de ultimátum; se corrigió para que diga que acerca la conducta a la solución teórica.
- Siguen sin leerse completos: Edmonds (2026) y Li y Wu (2025).

**Decisión del autor (17-11-2026):** las citas de Edmonds (2026) y de Li y Wu (2025) se dan por aceptadas con base en sus abstracts. El hallazgo 14 queda cerrado para esos dos trabajos; sigue abierto el cotejo de las cifras humanas con las versiones publicadas.
