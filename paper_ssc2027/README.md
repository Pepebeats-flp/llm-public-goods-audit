# Paper SSC 2027 — flujo de trabajo estilo PaperOrchestra

Este directorio aplica la metodología de [PaperOrchestra](https://github.com/google-research/paper-orchestra) (Song et al., arXiv:2604.05018) al paper para la Social Simulation Conference 2027, con plantilla Springer LNCS.

No se ejecuta el código de Google. Ese código está escrito para papers de conferencias de IA, llama a Gemini u OpenAI y a Semantic Scholar con claves propias, y sus prompts piden el tono de "top-tier ML conference". Aquí se sigue la misma secuencia de etapas y los mismos archivos de entrada y salida, con las reglas de SSC en lugar de las de ICLR o CVPR.

## Etapas y estado (17-11-2026, tras la corrida confirmatoria)

| Etapa de PaperOrchestra | Archivo aquí | Estado |
|---|---|---|
| Entrada: idea | `raw_materials/idea.md` | Lista (con nota del alcance realmente ejecutado) |
| Entrada: log experimental | `raw_materials/experimental_log.md` | **Completo**: 17.940 celdas, análisis prerregistrado |
| Entrada: plantilla y reglas de la sede | `templates/ssc2027_lncs/` | Lista; reglas basadas en SSC 2026, a confirmar con el CFP 2027 |
| Entrada: figuras | `latex_writeup/figures/`, registro en `raw_materials/figures/info.json` | Tres generadas; el paper usa dos |
| Prerregistro | `preregistration.md`, `preregistration_manifest.txt` | Escrito y con huellas antes de la corrida; **no subido a un registro público** |
| 1. Esquema | `outline.json` | Hecho (plan original; ver nota de alcance) |
| 2. Revisión de literatura | `literature/references.bib` | 38 entradas verificadas; el paper cita 27 |
| 3. Redacción de secciones | `latex_writeup/paper.tex` → `paper.pdf` | **Completa**, 12 páginas |
| 4. Refinamiento | `review/review_v0.md`, `review/review_v1.md` | Primera ronda con resultados hecha |

## Regla central

Ningún número entra al paper si no está antes en `experimental_log.md`. Lo que aún depende de una decisión de los autores está marcado en rojo con `\pending{...}`:

```bash
grep -n "pending{" latex_writeup/paper.tex
```

## Cómo regenerar todo

```bash
cd ../llm-public-goods-study
python3 -m pgg.analyze --glob 'data/raw/final_*.jsonl' --tag final   # tablas e informe
python3 -m pgg.figures --tag final                                   # figuras al paper
cd ../paper_ssc2027/latex_writeup
cp ../literature/references.bib .
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

## Qué falta para enviar

1. **Autoría, correos, enlace al repositorio y declaraciones: completos (17-11-2026).** No quedan marcadores pendientes en el paper.
2. **Repositorio público:** https://github.com/Pepebeats-flp/llm-public-goods-audit
3. **Citas de Edmonds (SSC 2025) y de Li y Wu (2025):** por decisión del autor (17-11-2026) se mantienen apoyadas en sus abstracts, sin leer el texto completo. Las frases del paper reproducen lo que dicen esos abstracts. Kořínek y Štekerová (2026) y Kitadai et al. (2025) sí se leyeron completos y se verificaron.
4. **Cifras humanas: cotejadas el 17-11-2026.** El paper cita dos valores verificados en la fuente leída (unos 50 puntos por unidad en Isaac y Walker, versión publicada; unos 25 en Gächter y Marino Fages, documento de trabajo IZA 16605, que es la versión que se cita) y usa a Zelmer solo para la dirección del efecto. No se pudo obtener la versión publicada de Zelmer (cerrada) ni la de JEBO (el servidor rechaza descargas automáticas). Detalle en la sección 0b del log.
5. **Confirmar con el CFP de febrero de 2027:** límite de páginas, si las referencias cuentan, anonimato, track y política de uso de IA.
6. **Dar una última mirada al PDF**: las 12 páginas se revisaron renderizadas en la ronda de formato, pero conviene una lectura humana.
7. Trabajo futuro, fuera de este paper por decisión del autor: el brazo de razonamiento con todas las variantes de prompt, y los experimentos de interacción (juego repetido, poblaciones mixtas).

## Relación con la guía

La guía `../guia_paper_ssc2027_llm_public_goods.md` contiene la revisión de literatura completa, el diseño y el cronograma. `idea.md` es su versión condensada en inglés, en el formato que espera la etapa de esquema.
