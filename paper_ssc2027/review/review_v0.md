# Etapa 4 — revisión simulada, pasada 0

Fecha: 17-11-2026. Alcance: secciones 1 a 4 de `latex_writeup/paper.tex` (las secciones 5 a 7 no existen todavía). No se asigna puntaje global porque un paper sin resultados no es evaluable; sí se revisa lo ya escrito contra los criterios de la comunidad SSC.

## Criterios de revisión para SSC

Tomados de las reglas de SSC 2026 y de las exigencias que plantean los propios autores de la comunidad. Se aplican completos cuando exista el borrador entero.

| # | Criterio | Fuente | Estado en el borrador |
|---|---|---|---|
| 1 | Propósito del modelo declarado | Edmonds; Zhao et al. | Cumple: "audit", sin afirmaciones contrafactuales |
| 2 | Modelo descrito de forma replicable | ODD, Grimm et al. | Cumple en resumen; falta el ODD completo en repositorio |
| 3 | Anclaje externo en datos humanos o benchmarks prerregistrados | Larooij y Törnberg | Diseñado; depende de resultados y del prerregistro |
| 4 | Robustez: múltiples corridas y sensibilidad | Larooij y Törnberg | Diseñado (al menos 50 decisiones por celda, E5) |
| 5 | Descartar memorización de la literatura | Larooij y Törnberg; Gupta et al. | Diseñado: controles fuera del dilema y condición F3 |
| 6 | Mostrar que el resultado no lo predetermina el prompt | Li y Wu | Diseñado: paráfrasis frente a framing; publicar prompts |
| 7 | Modelos, versiones y fechas exactas | Zhao et al.; Vanhée et al. | Pendiente |
| 8 | Separar validación del agente de la del fenómeno colectivo | Zhao et al. | Parcial: decirlo explícitamente en la Discusión |
| 9 | Línea base de reglas con los mismos parámetros | Gupta et al.; Shi et al. | Cumple |
| 10 | Implicaciones para modeladores y para decisión pública | Lema de SSC 2027 | Planteado en la introducción; desarrollar en la Discusión |
| 11 | Formato: 6 a 12 páginas LNCS | SSC 2026 | **No cumple todavía**, ver abajo |

## Hallazgos de esta pasada

### Bloqueantes

1. **Presupuesto de páginas.** El PDF tiene 11 páginas con Resultados, Discusión y Conclusión vacíos. Las secciones 1 a 4 terminan en la página 7 y las referencias ocupan casi 3. Con 3 páginas de resultados, 1 de discusión y un cuarto de conclusión el total sería de unas 14,5. Hay que recortar unas 2,5 páginas. Plan:
   - Referencias: bajar de 38 a unas 28. Candidatas a salir primero, por haberse leído solo como abstract y no sostener un argumento propio: `fan2024rational`, `jia2025strategic`, `sun2025survey`, `capraro2025benchmark`, `filippas2024homo`, `kitadai2025reasoning`, `gachter2026oneshot`, `han2025static`, `liang2026everyone`, `korinek2026words`. Ahorro aproximado: 0,75 página.
   - Trabajo relacionado: fusionar 2.2 y 2.3 y quitar el párrafo sobre recursos comunes. Ahorro: 0,5 página.
   - Tabla 2 (predicciones de referencia): pasarla a una frase en la introducción o conservarla y quitar el párrafo de Smith de la sección 1. Ahorro: 0,3 página.
   - ODD: convertir el resumen en una tabla compacta o dejar tres líneas y remitir al repositorio. Ahorro: 0,4 página.
   - Sección 4.4: quitar el último párrafo si se detalla en el prerregistro. Ahorro: 0,2 página.
   - Si las referencias no cuentan en el límite de 2027, el recorte necesario baja a una página.
2. **Sin resultados.** Todo lo demás depende de `experimental_log.md`.

### Importantes

3. **Citas de trabajos leídos solo como abstract.** Edmonds (2026) y Li y Wu (2025) sostienen argumentos de la introducción. Antes de enviar hay que leer el texto completo y confirmar que las paráfrasis son fieles. Lo mismo para Kořínek y Štekerová.
4. **Cifras humanas de working papers.** Las pendientes y los porcentajes de tipos provienen de versiones de trabajo de Zelmer, de Fischbacher y Gächter y de Gächter y Marino Fages. En el borrador se usan solo rangos ("40–60 %"), sin decimales; así debe quedar hasta cotejar las versiones publicadas.
5. **Lectura de Smith.** La introducción dice que el vínculo entre *Moral Sentiments* y las contribuciones positivas es una lectura apoyada en Ashraf et al., que no tratan bienes públicos. La Tabla 2 ya lo marca como "our reading". Mantener esa cautela y no añadir más historia del pensamiento.
6. **Afirmación "no study that we could read in full".** Es correcta para los trabajos leídos, pero la búsqueda no fue sistemática. Antes de enviar, repetir la búsqueda en Scopus con fecha de corte de marzo de 2027.
7. **Tabla 1.** La fila de Sreedhar et al. no da el valor del retorno marginal porque depende de si juegan 3 o 4. Correcto, pero conviene una nota.

### Menores

8. Un `Overfull \hbox` de 6 pt en el primer párrafo de la introducción.
9. Título: con el encuadre de Smith queda en 13 palabras. Alternativa más corta en `idea.md`.
10. Autoría, afiliación, agradecimientos y declaración de intereses son marcadores.
11. La palabra "audit" aparece muchas veces en el resumen y la introducción; variar al pulir.

## Qué revisar en la pasada 1 (con resultados)

- Que cada número de la sección 5 esté en `experimental_log.md`.
- Que las figuras se describan según lo que muestran.
- Que la Discusión no extraiga conclusiones de política desde sociedades de LLM.
- Que el resumen tenga las dos frases de resultados y no supere 250 palabras.
- Criterios 3 a 8 de la tabla, uno por uno.
