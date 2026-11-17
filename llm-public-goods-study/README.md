# llm-public-goods-study

Código del estudio para el paper de SSC 2027: agentes LLM en un juego de bienes públicos lineal. El diseño está en `../paper_ssc2027/raw_materials/idea.md`.

El motor, los prompts, el ejecutor y el monitor solo usan la biblioteca estándar de Python 3. El análisis y las figuras usan numpy, pandas, scipy, statsmodels y matplotlib.

## Estructura

| Ruta | Contenido |
|---|---|
| `pgg/game.py` | Motor del juego: pagos, bienestar, régimen (dilema o control), eficiencia, Gini |
| `pgg/agents.py` | Agentes de reglas (egoísta, cooperativo, recíproco, adaptativo) y juego repetido |
| `pgg/prompts.py` | Ocho variantes de prompt (P0, P1, P2, P4 paráfrasis; P3 con ejemplos; F1–F3 framings) y preguntas de comprensión |
| `pgg/llm.py` | Cliente de OpenCode Go (API compatible con OpenAI) y análisis de la respuesta |
| `pgg/run_oneshot.py` | Ejecutor de decisiones de una ronda (experimentos E1 y E2), reanudable |
| `pgg/summarize.py` | Resumen descriptivo de una corrida |
| `pgg/launch.py`, `pgg/status.py` | Lanzador con supervisor y monitor de consola |
| `pgg/analyze.py`, `pgg/figures.py` | Análisis prerregistrado y figuras |
| `tests/test_environment.py` | Experimento E0: validación del entorno |
| `configs/` | Configuraciones de corrida e instantánea de metadatos de modelos |
| `data/raw/` | Una fila JSON por llamada, con prompt, respuesta, uso y costo |

## Uso

```bash
python3 -m unittest discover -s tests -v          # E0: validación del entorno
python3 -m pgg.launch                             # arranca lo pendiente de configs/final_*.json y muestra el estado
python3 -m pgg.status --watch                     # solo el monitor
python3 -m pgg.launch --stop                      # detiene todo (se puede reanudar)
python3 -m pgg.analyze --glob 'data/raw/final_*.jsonl' --tag final   # análisis prerregistrado
python3 -m pgg.figures --tag final                # figuras del paper
```

`pgg.launch` deja un supervisor en segundo plano que reinicia las corridas caídas; cada corrida retoma donde quedó. `pgg/analyze.py` y `pgg/figures.py` necesitan numpy, pandas, scipy, statsmodels y matplotlib.

Estado: la corrida confirmatoria del 17-11-2026 está completa (17.940 celdas en `data/raw/final_*.jsonl`). El informe está en `data/processed/final_analysis.md`. Los datos del piloto (`pilot_20261117`) nunca se mezclan con los finales.

## Acceso a los modelos

Las llamadas van a OpenCode Go (`https://opencode.ai/inference/go/openai/v1`). La clave se lee al momento de la llamada desde la variable `OPENCODE_API_KEY` o, si no existe, desde el archivo de autenticación de OpenCode. No se escribe en ningún archivo de datos ni de registro.

OpenCode Go está pensado para agentes de programación y su documentación dice que vigila el tráfico. Por eso el cliente:

- se identifica con su propio user agent,
- envía un identificador de sesión estable en `x-opencode-session`,
- hace las llamadas en secuencia, con al menos 1,5 segundos entre una y otra,
- se detiene al llegar a un tope de gasto de la cuota (`max_allowance_usd`).

`configs/opencode_go_models_snapshot.json` guarda los metadatos de los 32 modelos tal como los entregó la API el 17-11-2026: identificador canónico, si es de pesos abiertos, precios y opciones de razonamiento. La lista de modelos de Go cambia con el tiempo, así que esta instantánea es la referencia para el paper.

## Reglas fijadas antes de correr

- El motor calcula todos los pagos. El modelo solo devuelve `{"amount": <entero>}`.
- Una respuesta sin acción válida se registra como inválida y la celda se pregunta una vez más. Se conservan ambas filas. No se repara nada.
- Los fallos de transporte (HTTP 429 o 5xx, tiempo agotado) se reintentan hasta tres veces y no cuentan como respuestas del modelo.
- El orden de las celdas se baraja con semilla, para no confundir condición con momento del día.
- Las preguntas de comprensión van en llamadas separadas, nunca en el mismo contexto que una decisión.
- El texto de razonamiento que devuelve el modelo se guarda para auditoría, pero no se usa como evidencia de cómo decidió.

## Limitaciones conocidas

- Acceso por un intermediario: el campo `served_model` registra lo que el proveedor dice haber servido, pero no hay forma independiente de verificar la versión exacta de cada modelo.
- `gpt-5.6-luna` no generó tokens de razonamiento al pedir esfuerzo alto por esta vía, así que solo se puede usar sin razonamiento.
- La temperatura se fija en 1,0 para todos; si un modelo rechaza el parámetro, se usa el valor por defecto del proveedor y queda registrado en la fila.
