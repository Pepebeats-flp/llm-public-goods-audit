# Guía de trabajo para el paper SSC 2027

## Agentes LLM en juegos de bienes públicos: sensibilidad a incentivos, consistencia ante el prompt y efectos colectivos

**Versión:** 2.1 (reemplaza la propuesta 1.0 orientada a AAMAS; la 2.1 incorpora la lectura a texto completo de los papers y el encuadre Smith–Nash)\
**Fecha:** 17 de noviembre de 2026\
**Conferencia objetivo:** Social Simulation Conference 2027 (SSC 2027, ESSA), Malmö, 16–20 de agosto de 2027\
**Tipo de envío objetivo:** full paper para proceedings (6–12 páginas, plantilla Springer LNCS, según el formato de SSC 2026)\
**Fuentes de la revisión:** Scopus (búsquedas del 17-11-2026, consultas en el Apéndice A), abstracts vía OpenAlex y lectura a texto completo de 22 trabajos (estado de acceso en el Apéndice C)

---

## Estado al 17-11-2026: experimento corrido y paper redactado

Esta guía describe el plan. Lo que se ejecutó es más acotado:

- **Alcance:** solo el juego de una ronda (E0, E1, E2 y un brazo con razonamiento). Poblaciones mixtas, juego repetido y método de estrategia quedan como trabajo futuro.
- **Modelos:** seis, vía OpenCode Go: gpt-5.6-luna, claude-haiku-5-5, qwen3.8-flash, glm-5.3-flash, deepseek-v4.1-flash y hy3. Cinco se corrieron también con razonamiento.
- **Tamaño:** 17.940 llamadas prerregistradas, 50 decisiones por celda, 1,85 USD de cuota.
- **Resultado principal:** sin razonamiento, la redacción explica entre 3 y 21 veces más varianza que el incentivo en cinco modelos, y ninguno elige la acción dominante en los dos controles. Con razonamiento, cuatro de cinco aportan cero en todo el dilema.
- **Dónde está todo:** paper en `paper_ssc2027/latex_writeup/paper.pdf`; resultados en `paper_ssc2027/raw_materials/experimental_log.md`; código y datos en `llm-public-goods-study/`; pendientes en `paper_ssc2027/README.md`.

---

## 0. Qué cambió respecto de la versión 1.0

1. **El estado del arte creció de 5 a unos 45 trabajos**, organizados por bloque (§4). Varios compiten directamente con la idea original y obligan a afinar la contribución (§5).
2. **Corrección bibliográfica:** Liang et al. ("Everyone Contributes!") ya no es solo un workshop de NeurIPS 2025. Scopus lo indexa en los proceedings de **AAMAS 2026** (DOI 10.65109/SJPO2377). La versión 1.0 decía lo contrario.
3. **Reencuadre para SSC:** el paper se presenta como una *auditoría conductual de agentes LLM como módulos de decisión para ABM*, enlazada con el debate de validación de los ABM generativos, que es el tema que la comunidad ESSA está discutiendo (§3 y §4.6).
4. **Tres añadidos al diseño** que salen de la literatura: condiciones de control fuera del dilema, método de estrategia para medir cooperación condicional y comparación con hechos estilizados de experimentos humanos (§9).
5. **Una métrica de la v1.0 no aporta información:** en el PGG lineal de una ronda el regret unilateral es una transformación lineal de la contribución (§10.2).
6. Se corrigió la numeración de secciones y las fórmulas, que estaban rotas por la conversión de formato.

**Novedades de la versión 2.1, tras leer los papers completos:**

7. **GAMA-Bench (ICLR 2025) es el antecedente más cercano**, no Li y Shirado. Incluye un juego de bienes públicos, barre el multiplicador, prueba cinco redacciones y mete un free-rider fijo, todo con GPT-3.5 y pocas corridas (§4.1). La diferenciación pasa a ser de profundidad y rigor.
8. **Parámetros anclados en la literatura:** $N=4$, dotación 20 y valores de $r/N$ que coinciden con los experimentos humanos y con los estudios de LLM previos (§9.1).
9. **Encuadre Smith–Nash**, con citas de fuente primaria (§3.1).
10. **Referencias humanas con cifras** para la comparación (§4.8) y fórmulas exactas de GovSim (§10.1).
11. Sabato et al. baja de categoría: es un juego en redes y los LLM predicen, no juegan.

---

## 1. Resumen ejecutivo

Se estudia cómo deciden los agentes basados en LLM en un juego de bienes públicos lineal (PGG) y qué consecuencias colectivas tienen esas decisiones. Se comparan con políticas de referencia transparentes (egoísta, cooperativa, recíproca, adaptativa) y con los hechos estilizados de los experimentos con humanos.

La pregunta para la comunidad de simulación social es concreta: **antes de poner un LLM como regla de decisión dentro de un ABM, ¿qué sabemos de cómo responde a los incentivos del modelo y cuánto de su conducta depende de la redacción del prompt?** El paper responde con un protocolo reproducible y tres mediciones:

- **Sensibilidad a incentivos:** cómo cambia la contribución al variar el retorno marginal per cápita ($r/N$), incluyendo condiciones donde el dilema desaparece.
- **Consistencia ante el prompt:** dispersión de las decisiones entre descripciones equivalentes del mismo juego.
- **Efectos colectivos:** bienestar, eficiencia y desigualdad en poblaciones homogéneas y mixtas.

**Alcance recomendado:** PGG lineal, dos o tres familias de LLM, cuatro políticas de referencia, una ronda más juego repetido. Sin negociación libre, sin instituciones, sin memoria ilimitada y sin entrenamiento de los LLM.

---

## 2. SSC 2027: lo que se sabe hoy

Datos tomados del sitio oficial (https://essa.eu.org/ssc/2027/) el 17-11-2026. El sitio advierte que las fechas exactas se confirman al publicar cada convocatoria.

| Hito | Fecha |
|---|---|
| Convocatoria de workshops y tracks | Noviembre de 2026 |
| Cierre de propuestas de workshops y tracks | Principios de enero de 2027 |
| Publicación del Call for Papers | Febrero de 2027 |
| **Cierre de envío de papers** | **Principios de abril de 2027** |
| Conferencia | 16–20 de agosto de 2027, Malmö University, Suecia |

- **Lema de la conferencia:** "Social Simulation in Action: Catalysing Public Decision-Making?!". Conviene que la introducción y la discusión hablen de qué implica el resultado para quien usa simulaciones en decisiones públicas (§3.1).
- **Grupo de interés afín:** ESSA tiene un SIG sobre LLM para modelos basados en agentes (SIG-LLM4ABM, organizado por Peer-Olaf Siebers), del que salió el paper de Vanhée et al. Es el candidato natural a proponer el track de IA generativa.
- **Organización:** Fabian Lorig (Malmö), Harko Verhagen y Nanda Wijermans (Stockholm), Melania Borit (UiT). Contacto: ssc2027@essa.eu.org. Las novedades se anuncian en la lista SIMSOC.
- **Aún sin publicar para 2027:** tipos de envío, límites de páginas, plantilla, editorial de proceedings, lista de tracks y criterios de revisión.

### Referencia: formato de SSC 2026 (Durham)

Mientras no salga el CFP 2027, conviene trabajar con el formato de la edición anterior:

| Tipo | Extensión | Va a proceedings |
|---|---|---|
| Póster | Resumen de 300–500 palabras | No |
| Extended abstract | 3–4 páginas, puede ser trabajo en curso | No |
| Full paper solo presentación | 6–12 páginas | No |
| Full paper para proceedings | 6–12 páginas, con diseño del modelo, resultados y conclusiones | Sí, con posible revisión adicional |

- Plantilla: Springer LNCS (LaTeX o Word).
- Trabajo original, no publicado ni en revisión en otro lugar.
- En 2026 hubo un track **"Generative AI meets Agent-Based Modelling"**, que sería el destino natural. Otros dos tracks cercanos fueron "Sense & Sensibility: Modelling Human Deliberation and Decision-making" y "NISE: Norms and Institutions in the Social Environment". No hubo track de teoría de juegos. Los tracks de 2027 se definen entre noviembre y enero.

### Indexación

Scopus indexa los proceedings de SSC 2025 ("20th Annual Social Simulation Conference, SSC 2025") en la serie **Springer Proceedings in Complexity**, y también ediciones anteriores. Para 2027 la editorial no está anunciada, así que la indexación es probable por precedente pero no está confirmada.

---

## 3. Qué espera la comunidad SSC y cómo encajar

De los proceedings de SSC 2025 y de JASSS se desprende qué valora esta comunidad, que es distinto de lo que valora AAMAS:

- **Un modelo descrito de forma explícita y replicable.** El estándar es el protocolo ODD (Grimm et al., 2020, JASSS). Conviene describir el entorno con ODD aunque el modelo sea pequeño.
- **Validación y justificación de supuestos.** Importa más por qué se cree en la regla de decisión del agente que el rendimiento en un benchmark.
- **Una postura crítica frente a los LLM.** En SSC 2025, Vanhée et al. revisaron los usos de LLM a lo largo del ciclo de modelado "holding a critical stance" y Edmonds presentó "When Can You Use AI for ABM?". Un paper que promete sociedades artificiales realistas va a encontrar resistencia; uno que mide límites va a encontrar audiencia.
- **Efectos colectivos emergentes**, con análisis de sensibilidad.

**Encaje propuesto:** el trabajo es un test de micro-validez de un LLM como regla de decisión. Usa el PGG porque tiene equilibrio, óptimo social y una literatura experimental humana muy establecida contra la cual contrastar. Aporta a la discusión abierta por Larooij y Törnberg (2026), según la cual la validación es el problema central de la simulación social generativa.

AAMAS queda como literatura complementaria para los aspectos de sistemas multiagente y teoría de juegos computacional.

**Calibración de rigor.** De los papers de SSC 2025 leídos, Vanhée et al. solo reporta conteos y Malleson y Manley no reporta estadística ni réplicas; ninguno de los dos usa ODD. Las extensiones publicadas van de 11 a 19 páginas, con 28 a 52 referencias. Un full paper con ODD, réplicas, intervalos y línea base de reglas queda en la parte alta de lo habitual.

**Tres requisitos de validación** que se pueden usar como estructura del argumento (Larooij y Törnberg, §2.2): alineación con el propósito del modelo, anclaje externo en datos humanos o en benchmarks prerregistrados, y robustez mediante múltiples corridas y análisis de sensibilidad.

**Nivel de afirmación.** En la escala de plausibilidad de Zhao et al. (nivel 0, simulación sin fenómeno objetivo; nivel 1, modelo fenomenal reproducible; nivel 2, hipótesis falsable y mapeo a mecanismos reales; nivel 3, evidencia capaz de desconfirmarla), este trabajo se declara en el nivel 1, con elementos del 2. Según esos autores, un modelo de nivel 1 no sirve para contrafactuales, así que el paper no debe sacar conclusiones de política a partir de los agentes LLM.

### 3.1 Encuadre conceptual: Nash y los dos Smith

**¿Se puede guiar el paper con Nash y Adam Smith? Sí, pero no como "Nash contra Smith".** Ese choque es el de la película *A Beautiful Mind* ("Adam Smith… he was wrong") y falla por dos lados: la solución que muestra la película no es un equilibrio de Nash, y Smith nunca sostuvo que el interés propio baste siempre.

Lo que dicen las fuentes primarias:

- **La mano invisible es una afirmación acotada.** *Wealth of Nations* IV.ii: "By pursuing his own interest he *frequently* promotes that of the society more effectually than when he really intends to promote it." Dice "frequently", no "always", y el contexto es la preferencia por la industria doméstica.
- **Smith reconoce el problema de los bienes públicos.** *Wealth of Nations* V.i, Parte III, sobre el tercer deber del soberano: obras e instituciones públicas "which, though they may be in the highest degree advantageous to a great society, are, however, of such a nature that the profit could never repay the expence to any individual or small number of individuals, and which it therefore cannot be expected that any individual or small number of individuals should erect or maintain."
- **Smith no supone agentes puramente egoístas.** Primera frase de *The Theory of Moral Sentiments*: "How selfish soever man may be supposed, there are evidently some principles in his nature, which interest him in the fortune of others, and render their happiness necessary to him, though he derives nothing from it except the pleasure of seeing it."

De ahí sale un encuadre correcto y más interesante:

| Referente | Predicción en el juego de bienes públicos |
|---|---|
| Nash (equilibrio de una ronda) | Nadie contribuye |
| Smith, *Wealth of Nations* V.i | Los individuos no proveerán el bien; hace falta el soberano. Coincide con Nash |
| Smith, *Theory of Moral Sentiments* | Las personas se interesan por la suerte de los demás; cabe esperar contribuciones positivas |
| Humanos en el laboratorio | Contribuyen entre 40 % y 60 % al inicio y la contribución decae con la repetición |

En este juego Nash formaliza lo que Smith ya había dicho en el Libro V. La tensión real está entre los dos libros de Smith, y los humanos caen en el medio. La pregunta del paper queda así: **¿los agentes LLM se comportan como los jugadores de Nash o como los agentes morales de Smith, y eso depende de los incentivos o de la redacción?**

**Enlace con el lema de SSC 2027.** Si los agentes LLM contribuyen por defecto mucho más que los humanos, una simulación poblada con ellos hará que el bien público parezca proveerse solo, y la intervención pública, el "tercer deber del soberano", parecerá innecesaria. Es un sesgo relevante para quien use estas simulaciones en decisiones públicas. Los datos lo sugieren: los modelos sin razonamiento explícito cooperan entre 96 % y 100 % en Li y Shirado, y GPT-4 nunca aporta cero en Mei et al.

**Cuidados al usar este encuadre:**

- La asignación de *Theory of Moral Sentiments* a contribuciones positivas en bienes públicos es una interpretación nuestra. Ashraf, Camerer y Loewenstein (2005) conectan ese libro con los juegos del dictador, ultimátum y confianza, pero no mencionan bienes públicos.
- Vernon Smith (1998) sostiene que los dos libros no se contradicen: interés propio en el intercambio impersonal y reciprocidad en el personal. Conviene presentarlo como dos predicciones que conviven, no como una contradicción.
- Identificar el primer teorema del bienestar con la mano invisible también es discutible (Blaug, 2007, según fuentes secundarias). Basta con decir que ese teorema no cubre bienes públicos (Samuelson, 1954).
- Usarlo como marco de la introducción y de la discusión, en dos o tres párrafos. El aporte sigue siendo empírico; un revisor de SSC no va a aceptar historia del pensamiento económico en lugar de resultados.
- No se encontró ningún paper de agentes LLM en dilemas sociales con este encuadre. Lo más parecido es "Artificial Leviathan" (arXiv:2406.14373), de corte hobbesiano. La búsqueda fue limitada, así que la ausencia es provisional.

---

## 4. Estado del arte

Todos los trabajos de las tablas aparecen en Scopus. Las descripciones salen del abstract, salvo donde se indica "sin abstract", que significa que solo se confirmaron título, autores y fuente.

### 4.1 LLM en juegos de bienes públicos (competencia directa)

Leídos a texto completo, salvo Sabato et al. y Hintze y Adami.

| Trabajo | Diseño | Resultado | Qué deja abierto |
|---|---|---|---|
| **Huang et al. (ICLR 2025)**, GAMA(γ)-Bench | $N=10$ agentes del mismo modelo, 20 rondas con horizonte conocido, 20 fichas, multiplicador 2 ($r/N=0{,}2$), contribución entera. 13 modelos, temperatura 1, 5 corridas. El prompt no nombra el juego pero dice "public pot". La puntuación premia aportar cero. | Con GPT-3.5: al barrer el multiplicador (0; 0,5; 1; 2; 4) la puntuación va de 25,9 a 52,5 sin patrón, y concluyen que el modelo contribuye parecido incluso con retorno nulo. Cinco redacciones del prompt dan entre 24,2 y 50,2. Un free-rider fijo entre nueve GPT-3.5 hace que estos aporten más. | **Antecedente más cercano.** El barrido y las redacciones se hacen con un solo modelo antiguo y una corrida por variante. No llega a $r/N>1$, no descompone la varianza, no mezcla modelos distintos y no compara con humanos. |
| **Li y Shirado (EMNLP 2025)** | $N=4$, 100 puntos, multiplicador 2 ($r/N=0{,}5$), acción binaria (aportar todo o nada). Una ronda y juego iterado de 10 rondas. Diez modelos en cinco familias, con y sin razonamiento; 100 ensayos por condición. Un solo prompt, que describe un "group project". | Cooperación sin y con razonamiento: OpenAI 96 y 20 de 100; Gemini 100 y 2; DeepSeek 23 y 0; Qwen 64 y 0; Claude 99 y 93. Pago grupal tras 10 rondas: 3932 con GPT-4o frente a 740 con o1. | No varía $r/N$, la acción no es continua, no hay paráfrasis ni agentes de reglas. Reconocen que no aleatorizan el orden de las opciones. |
| **Sreedhar et al. (IUI 2025)** | 3 o 4 jugadores más un moderador, con memoria y planes. Dotación de 20 dólares, multiplicador 1,6. Contribución continua. Solo gpt-4o-mini; 5 partidas por condición. La biografía del agente dice que juega "a PGG-like game". | El nombre del juego cambia todo: "Teamwork" más de 60 % frente a "Taxation" menos de 40 %. Transparencia 60 % frente a 35 %. Primado "unity" 65 % frente a "proportionality" 30 %. | Reconocen como limitación que el resultado depende del multiplicador y que no lo variaron. Muestras muy pequeñas, un solo modelo. |
| **Mei et al. (PNAS 2024)** | $N=4$, 20 dólares, $r/N=0{,}5$, 3 rondas. Los otros jugadores son guiones, no LLM. 30 sesiones. El prompt nombra el juego y lo presenta como un proyecto de limpieza de agua. | Ambos modelos aportan más que los humanos y nunca cero; lo más común es la mitad de la dotación. GPT-4 aporta 10 o 12 dólares en la primera ronda en las 30 sesiones. | No hay interacción real entre LLM ni variación de pagos. Los autores califican su análisis de framing como "far from systematic". |
| **Liang et al. (AAMAS 2026)** | Marco de coordinación para tres LLM pequeños que resuelven benchmarks, con una recompensa rediseñada. No hay dotación ni retorno marginal clásico. | Mejora la exactitud en tareas frente a un solo agente. | No es un experimento conductual. Compite solo de nombre. |
| **Hintze y Adami (npj Complexity 2026)** | Modelo evolutivo con agentes artificiales, sin LLM. | Solo los agentes que imitan a los jugadores reducen el umbral de sinergia para cooperar. | Referencia para poblaciones mixtas. Solo abstract. |
| **Sabato, Hazon y Azaria (ICTAI 2025)** | Bienes públicos en redes, no lineal. 96 personas y dos LLM predicen el resultado; no juegan. | Los humanos tienden a predecir equilibrios de Nash y los LLM casi nunca. | Cita secundaria. Solo abstract; el texto está tras paywall de IEEE. |

Tres patrones que salen de estas lecturas:

- **El nivel de cooperación por defecto es muy alto y depende más del modelo y del modo de razonamiento que de cualquier otra cosa medida hasta ahora.**
- **Casi todos los prompts llevan contexto cargado:** "group project", "water cleaning project", "Teamwork". Ninguno usa un marco realmente neutro.
- **Nadie ha comprobado si los modelos actuales distinguen un multiplicador de otro.** El único barrido es el de GAMA-Bench con GPT-3.5.

### 4.2 LLM en otros dilemas sociales y juegos repetidos

| Trabajo | Qué hace |
|---|---|
| **Akata et al. (Nature Human Behaviour 2025)** | LLM en juegos 2×2 repetidos entre sí, contra estrategias tipo humano y contra humanos. Rinden bien en la familia del dilema del prisionero y mal en coordinación. Proponen una "teoría de juegos conductual para máquinas". |
| **Pal et al. (PNAS Nexus 2026)** | Cinco modelos en el dilema del prisionero repetido. Miden cooperación en un marco neutral, sin el lenguaje habitual del juego, y luego cómo adaptan sus estrategias al cambiar probabilidad de término, pagos y conocimiento del horizonte, además del efecto de distintos framings. Ningún modelo es consistente en todas las tareas. |
| **Piatti et al. (NeurIPS 2024)**, GovSim | Plataforma de recursos comunes. Salvo los modelos más potentes, los agentes no alcanzan un equilibrio sostenible, con tasa de supervivencia máxima bajo 54 %. La comunicación resulta crítica. |
| **Gupta et al. (AAMAS 2026)** | Juego de recursos comunes sin recompensa explícita, con aprendizaje social y castigo basado en normas. Validan reproduciendo hallazgos humanos y comparan sociedades de distintos LLM. |
| **Vallinder y Hughes (AAMAS 2025, extended abstract)** | Evolución cultural de la reciprocidad indirecta en un Donor Game. Grandes diferencias entre modelos base y entre semillas. |
| **Han et al. (PLOS ONE 2025)** | Dilema del prisionero en redes. Los humanos cooperan más en redes fijas, los LLM más en poblaciones bien mezcladas, y casi no ajustan su conducta a la estructura. |
| **Suzuki y Arita (Sci. Rep. 2024)**; **Sakai et al. (Sci. Rep. 2026)** | Rasgos de personalidad como genes en un modelo evolutivo, y efecto de inducir personalidad en el dilema repetido. La amabilidad es el factor dominante. |
| **Smith et al. (NeurIPS 2025)**, Concordia Contest | Evaluación de cooperación en escenarios de motivos mixtos con socios diversos. Brechas grandes en persuasión y aplicación de normas. |
| **Willis, Du y Leibo (AAMAS 2025, extended abstract)** | Estrategias completas en lenguaje natural para el dilema del prisionero iterado. |
| **Yılmaz y Kılıç (IISEC 2026)** | Dilema del prisionero y Snowdrift con seis contextos añadidos. El contexto aumenta la cooperación pero no siempre los pagos. |
| Warnakulasuriya et al. (LNCS 2026); Xie et al. (Chaos, Solitons & Fractals 2026); Mu et al. (Neurocomputing 2024) | Castigo en sociedades de agentes LLM; panorama de juegos evolutivos con agentes LLM; survey de cooperación en dilemas sociales. Sin abstract. |

Detalles metodológicos de los textos completos que conviene reutilizar o evitar:

- **Pal et al.** Su marco neutral usa acciones "L" y "R", "points" y "another agent"; no nombra el juego ni usa "cooperate" o "defect". Pide la respuesta así: "Give only the character as output. Give no explanation." Varían la probabilidad de término (0,01; 0,1; 0,2; 0,5) y los pagos con un parámetro de 0 a 10. Usan 50 llamadas por escenario a temperatura 0. Su "consistencia" es un juicio cualitativo, sin tests ni intervalos. Claude y Llama no reaccionan a la probabilidad de término. Reconocen que no contrabalancearon las etiquetas y que falta un estudio controlado de la redacción.
- **Akata et al.** Sus pruebas de robustez son el modelo a seguir para las paráfrasis: orden aleatorio de las opciones, reetiquetado con otras letras, utilidades en puntos, dólares o monedas, y dos historias de cobertura con los mismos pagos. No las analizan estadísticamente. Proponen los juegos de bienes públicos con más de dos agentes como trabajo futuro.
- **Han et al.** La comparación con humanos es visual, superponiendo curvas publicadas, sin test estadístico. Usan 5 corridas por condición.
- **Vallinder y Hughes.** Con 5 corridas por modelo, dos de las cinco de Claude no generan cooperación; la diferencia arranca en la donación inicial (44 % y 47 % frente a 50 % o más). Es un argumento para usar muchas repeticiones.
- **Gupta et al.** La validación con hallazgos humanos se hace con agentes de reglas y es cualitativa; luego ven si los LLM reproducen el patrón de esos agentes. Con los LLM usan ANOVA de dos vías con Tukey y 10 ensayos por condición. Advierten que los benchmarks con recompensas visibles pueden provocar conductas que el modelo recupera del preentrenamiento.

### 4.3 Framing y sensibilidad al prompt

| Trabajo | Qué hace |
|---|---|
| **Lorè y Heydari (Sci. Rep. 2024)** | Separa el efecto de la estructura del juego del efecto del contexto narrativo en GPT-3.5, GPT-4 y LLaMa-2. GPT-3.5 depende mucho del contexto; GPT-4 prioriza la estructura pero distingue poco entre juegos. |
| **Kořínek y Štekerová (J. Cases on IT 2026)** | Dilema iterado de 25 rondas con prompt neutral, positivo y de supervivencia, con pagos constantes. ANOVA con efecto significativo en 13 de 16 emparejamientos. El marco de supervivencia sube la cooperación hasta 80 puntos porcentuales. |
| **Li y Wu (System Dynamics Review 2025)** | Revisión de 22 estudios de ABM generativos. Identifica "sobre-control": el diseño del prompt puede predeterminar el resultado que luego se presenta como emergente. |
| Powell et al. (LNCS 2027) | Cambio de conducta estratégica al usar lenguas con pocos recursos. Sin abstract. |

Estos trabajos varían el *contenido* del marco (contexto, tono, supervivencia). La v1.0 proponía variar solo la *redacción* manteniendo la información. Conviene hacer las dos cosas y separarlas (§9.2, E2).

**Método de Lorè y Heydari para separar estructura y contexto**, reutilizable para nuestra descomposición de varianza: 300 inicializaciones por cada combinación de contexto y juego, a temperatura 0,8; regresión logit por modelo con variables indicadoras de juego y de contexto; análisis de dominancia, que promedia la contribución incremental de cada grupo de variables al $R^2$ sobre todos los subconjuntos de regresores; y tests de diferencia de proporciones. No indican corrección por comparaciones múltiples. El texto de sus contextos está en el material suplementario.

El texto de Kořínek y Štekerová no se pudo descargar (el sitio de IGI Global bloquea el acceso automático) y el de Li y Wu está cerrado en Wiley; de ambos solo se usó el abstract.

### 4.4 Benchmarks de razonamiento estratégico

| Trabajo | Qué mide |
|---|---|
| **Fan et al. (AAAI 2024)** | Racionalidad en tres componentes: formar un deseo claro, refinar creencias y elegir la acción óptima. GPT-4 muestra brechas importantes en los tres. |
| **Jia et al. (NeurIPS 2025)** | 22 modelos con un marco de teoría de juegos conductual que separa capacidad de razonamiento de efectos de contexto. Critica evaluar solo por aproximación al equilibrio de Nash. |
| **Huang et al. (ICLR 2025)**, GAMA(γ)-Bench | Ocho juegos clásicos multijugador con puntuación dinámica según los parámetros del juego. Evalúa robustez y generalización en 13 modelos. Incluye un juego de bienes públicos; detalle en §4.1. |
| **Duan et al. (NeurIPS 2024)**, GTBench; **Xu et al. (EMNLP 2024)**, MAgIC | Suites de evaluación con juegos de teoría de juegos y métricas de racionalidad, cooperación y coordinación. |
| **Kempinski et al. (AAMAS 2025)**, "Game of Thoughts" | La elección directa de acciones produce estrategias explotables; el refinamiento iterativo las mejora. |
| **Sun et al. (IJCAI 2025)** | Survey de la intersección entre teoría de juegos y LLM. Buen punto de entrada para citar. |
| Guo et al. (Neurocomputing 2026); Kader y Lee (J. Behav. Exp. Econ. 2026) | Evaluación de razonamiento estratégico. Sin abstract. |

### 4.5 LLM como sustitutos de humanos: cautelas

| Trabajo | Hallazgo |
|---|---|
| **Gao et al. (PNAS 2025)**, "Take caution in using LLMs as human surrogates" | En el juego 11–20, casi todos los enfoques fallan en reproducir la distribución humana. Las causas son diversas e impredecibles. |
| **Capraro et al. (Sci. Rep. 2025)** | Benchmark público con 106 instrucciones de juegos del dictador de 12 países. GPT-4 subestima el interés propio y sobreestima el altruismo ("sesgo optimista"). |
| **Kitadai et al. (Group Decision and Negotiation 2025)** | En el juego del ultimátum, a mayor capacidad de razonamiento, más cerca de la solución teórica y más lejos del resultado humano. |
| **Filippas, Horton y Manning (EC 2024)**, "Homo Silicus" | Propone usar LLM como los economistas usan al *homo economicus*. Replica cuatro experimentos con resultados cualitativamente similares. |
| Aher et al. (ICML 2023); Park et al. (UIST 2023) | Simulación de múltiples humanos y agentes generativos. Referencias fundacionales. |

Li y Shirado y Kitadai et al. coinciden en un patrón: más razonamiento lleva a más conducta de equilibrio y menos cooperación. Es una hipótesis que este paper puede contrastar en el PGG variando $r/N$.

### 4.6 Validación de ABM generativos (el debate de la comunidad SSC)

| Trabajo | Aporte |
|---|---|
| **Larooij y Törnberg (Artificial Intelligence Review 2026)** | Revisión crítica. Los LLM pueden agravar el problema de validación de los ABM por su carácter de caja negra, sesgos culturales y salidas estocásticas. Muchos estudios se apoyan en validez aparente. |
| **Adornetto et al. (IEEE Trans. AI 2025)** | Panorama de agentes generativos en ABM y métodos de validación. Propone enfoques híbridos. |
| **Lu et al. (Physics of Life Reviews 2024)** | Revisión de LLM en redes, juegos evolutivos y dinámica social. Señala inconsistencias ligadas a la sensibilidad al prompt. |
| **Zhao, Pham y Vincent (FAccT 2026)** | Escala de plausibilidad de mecanismos en cuatro niveles. Separa suficiencia generativa de plausibilidad mecanística. |
| **Hirashima, Hu y Cheong (IEEE TNSE 2026)** | Survey sobre "hiper-racionalidad": convergencia de decisiones y compresión de la varianza conductual en agentes LLM. |
| **Chopra et al. (AAMAS 2025)** | Arquetipos LLM para escalar ABM a millones de agentes. Compara desde heurísticas hasta agentes LLM completos. |
| **Shi et al. (AAMAS 2026)** | ABM con LLM y análisis empírico de teoría de juegos en gobernanza socioecológica. Distintas formas de modelar al agente producen patrones colectivos distintos. |
| Tang y Törnberg (LNCS 2026); Morge (LNCS 2025) | ABM generativos explicables y validables; preparación de la IA generativa para la ciencia social computacional. Sin abstract. |

Citas textuales útiles para la introducción y la discusión:

- **Edmonds (SSC 2025, abstract):** "one cannot assume that an AI entity that is good at one AI goal will be suitable for your ABM purpose"; "one needs to check that it behaves in a reliable manner"; "Neither the sheer plausibility of LLM output, nor clever training, prompting or calibration of LLMs are sufficient".
- **Larooij y Törnberg:** "15 out of 35 studies rely solely on subjective assessments" (§5); "most reviewed studies rely on a single simulation run—akin to drawing general conclusions from a single-case study"; sobre fuga de datos, "what may appear as emergent dynamic can instead stem from a form of 'data leakage', as the models are simply reproducing phenomena identified in previous studies" (§2.1). Reconocen la réplica de experimentos conductuales como validación objetiva.
- **Vanhée et al. (SSC 2025):** en su revisión, el 91 % de los estudios usa el LLM como motor de decisión o comunicación del agente; los LLM carecen de "consistent internal logic or goals". Recomiendan documentar su uso con ODD.
- **Zhao et al.:** los LLM en juegos suelen responder preguntas de "generative sufficiency, rather than related to why a behavior was produced"; validar la arquitectura del agente "is not sufficient as evidence" para el mapeo al fenómeno colectivo.
- **Shi et al.:** "inducing behaviour through system prompts in LLMs is less effective than shaping behaviour through parameterized payoffs". Usan ODD+D como interfaz común a sus cuatro modelos.

### 4.7 Trabajos en SSC y JASSS

| Trabajo | Sede |
|---|---|
| Vanhée, Borit, Siebers et al., "Large Language Models for Agent-Based Modelling: Current and Possible Uses Across the Modelling Cycle" | SSC 2025 |
| Edmonds, "When Can You Use AI for ABM?" | SSC 2025 |
| Malleson y Manley, "Towards the Use of Foundation Models and Embeddings for Nuanced Perception and Decision-Making in Agents" | SSC 2025 |
| Feng et al., "Exploratory Generative Agent-Based Modeling Framework for Flood Resilience Governance" | SSC 2025 |
| Cohen et al., "Introducing Threat-Perceiving Actors in Group-Selective Public Goods Games" | SSC 2025 |
| Zhang, Peng y Ren, "GPLab: A Generative Agent-Based Framework for Policy Simulation and Evaluation" | JASSS 2026 |
| Qu et al., "How Group Cohesion Promotes the Emergence of Cooperation in Public Goods Game Under Conditional Dissociation" | JASSS 2019 |
| Grimm et al., protocolo ODD, segunda actualización | JASSS 2020 |

Melania Borit, coautora del primer trabajo, es una de las presidentas de SSC 2027. Ese paper es de cita obligada. Se leyeron completos Vanhée et al. y Malleson y Manley. De Edmonds y de Cohen et al. solo se obtuvo el abstract, porque Springer los tiene cerrados y no hay preprint; conviene conseguirlos por acceso institucional, sobre todo el de Cohen et al., para ver qué parámetros de juego usa un paper de bienes públicos aceptado en SSC. El de Feng et al. no se intentó.

No apareció en Scopus ningún trabajo de SSC que evalúe agentes LLM en un PGG. Es un indicio de espacio disponible, no una prueba: Scopus no cubre los extended abstracts ni los pósters de la conferencia.

### 4.8 Referentes humanos del PGG

| Trabajo | Uso |
|---|---|
| **Zelmer (Experimental Economics 2003)**, meta-análisis de PGG lineales | La contribución aumenta con el retorno marginal per cápita: coeficiente de 39,5 puntos porcentuales por unidad, sobre 711 grupos. El framing positivo suma 19,3 puntos y la comunicación 40,5. El tamaño de grupo y el número de periodos no son significativos. |
| **Isaac y Walker (QJE 1988)** | Con retorno 0,3 la contribución en el periodo 10 es 3,65 % de las fichas; con 0,75 es 26,35 %. No hay efecto puro del tamaño de grupo (14,5 % con $N=4$ y 15,5 % con $N=10$). Sujetos experimentados. |
| **Fischbacher y Gächter (AER 2010)** | $N=4$, 20 fichas, retorno 0,4, 10 rondas. Tipos según el método de estrategia: 55 % cooperadores condicionales, 23 % free-riders, 12 % en forma de triángulo, 10 % sin clasificar. La contribución inicial es 8 de 20 fichas y cae 0,64 fichas por ronda. |
| **Gächter y Marino Fages (JEBO 2026)** | Una ronda en línea, 2.136 participantes, dotación 10. Con retorno 0,4 la contribución media es cercana a 4; con 0,8, cercana a 5. El efecto del retorno es significativo y el del tamaño de grupo no. |
| **Ledyard (1995)**, survey | Contribuciones de 40 % a 60 % del óptimo en una ronda o al inicio, que decaen con la repetición y suben con la comunicación. |
| **Fischbacher, Gächter y Fehr (Economics Letters 2001)** | Origen del método de estrategia: una contribución incondicional más una tabla de contribuciones condicionales a la media de los demás. |
| **Andreoni (QJE 1995)** | Se coopera más cuando el juego se presenta como externalidad positiva que como negativa, con pagos idénticos. Es el precedente humano para el framing de dar frente a tomar. |
| **Fehr y Gächter (AER 2000)** | El castigo costoso sostiene la cooperación. Fuera del alcance de este paper; citar solo como trabajo futuro. |

Advertencias sobre estas cifras: las de Zelmer y las de Fischbacher y Gächter vienen de los working papers, no de la versión publicada. Las de Gächter y Marino Fages se calcularon a partir de los coeficientes de regresión del working paper de IZA. Hay que cotejarlas con las versiones finales antes de citarlas con decimales.

La pendiente humana no es única: el meta-análisis da unos 40 puntos por unidad de retorno, Isaac y Walker unos 50 con sujetos experimentados y Gächter y Marino Fages unos 25 en una ronda. Para comparar con los LLM basta con la dirección y el orden de magnitud.

---

## 5. Brecha y contribución revisada

### Lo que ya está hecho

1. PGG con LLM, incluido el efecto del razonamiento (Li y Shirado).
2. Réplica de tratamientos humanos en PGG (Sreedhar et al.).
3. Adaptación a parámetros y a framings en el dilema del prisionero repetido (Pal et al.).
4. Efecto del contexto narrativo y del tono del prompt en juegos de dos jugadores (Lorè y Heydari; Kořínek y Štekerová).
5. Recursos comunes con comunicación, normas y castigo (GovSim; Gupta et al.).
6. Benchmarks amplios de razonamiento estratégico.
7. Un primer barrido del multiplicador, cinco redacciones del prompt y un free-rider fijo en un juego de bienes públicos, todo con GPT-3.5 y pocas corridas (GAMA-Bench).

Afirmar que "se evalúa si los LLM cooperan en un dilema social" o que "el prompt afecta la cooperación" no es novedoso.

### Lo que sigue abierto

- **Curva de respuesta a incentivos en un juego de N jugadores, con modelos actuales.** Pal et al. lo hacen en un juego de dos jugadores y GAMA-Bench solo con GPT-3.5, donde no encuentra respuesta. Falta barrer $r/N$ con varias familias de modelos, cruzar los límites del dilema y comparar la curva con la de humanos y con la predicción de equilibrio. Sreedhar et al. reconocen esta carencia como limitación propia y Akata et al. piden juegos de bienes públicos como trabajo futuro.
- **Separar comprensión de preferencia.** Si un LLM contribuye 50 % con $r/N = 0{,}4$, no se sabe si coopera o si no entendió los pagos. Las condiciones de control fuera del dilema lo distinguen.
- **Paráfrasis frente a framing.** La literatura cambia el contenido del marco. Falta medir cuánta varianza produce la sola redacción, que es el ruido de fondo que cualquier modelador de ABM va a heredar. Ninguno de los trece trabajos leídos a texto completo separa ambas cosas con un diseño factorial ni aplica un test formal de monotonicidad o de consistencia.
- **Poblaciones mixtas de LLM y reglas clásicas**, con métricas de bienestar y desigualdad.
- **Traducción al lenguaje de ABM:** ODD, análisis de sensibilidad y recomendaciones para quien quiera usar un LLM como regla de decisión.

### Contribuciones

1. **Protocolo de auditoría reproducible** para agentes LLM en PGG lineal, descrito con ODD, con instancias de parámetros conocidos y variantes de prompt.
2. **Curvas de respuesta a incentivos** por modelo, con controles fuera del dilema y comparación con hechos estilizados humanos.
3. **Descomposición de la varianza** de las contribuciones entre incentivo, paráfrasis, framing, modelo y semilla.
4. **Efectos colectivos** en poblaciones homogéneas y mixtas: bienestar, eficiencia y desigualdad.
5. **Artefactos abiertos:** código, prompts, configuraciones, versiones de modelos, semillas y datos crudos.

La contribución 3 es la más diferenciadora y la que más le sirve a la audiencia de SSC.

---

## 6. Preguntas de investigación e hipótesis

**RQ principal**

> ¿En qué medida las decisiones de agentes LLM en un juego de bienes públicos responden a los incentivos del juego y no a la redacción con que se presenta, y cómo se trasladan esas decisiones al resultado colectivo?

**Preguntas secundarias**

- **RQ1, incentivos:** ¿Cambian las contribuciones de forma monótona con $r/N$? ¿Se comportan correctamente fuera del dilema?
- **RQ2, prompt:** ¿Qué parte de la varianza de las contribuciones se debe a paráfrasis equivalentes y qué parte a cambios de framing?
- **RQ3, composición:** ¿Cómo cambian bienestar y desigualdad al mezclar LLM de distintas familias o LLM con políticas clásicas?
- **RQ4, repetición:** ¿Muestran cooperación condicional y caída de las contribuciones como los humanos?

**Hipótesis** (se registran antes del experimento final y se ajustan solo tras un piloto separado)

- **H1a:** la contribución media aumenta con $r/N$ dentro del rango del dilema. La dirección viene de la evidencia humana (Zelmer, 2003), no del equilibrio, que predice cero para todo $r/N < 1$.
- **H1b:** en las condiciones de control, los LLM contribuyen cerca de $E$ cuando $r/N > 1$ y cerca de cero cuando $r < 1$. Las desviaciones indican falta de comprensión, no cooperación.
- **H2:** la dispersión entre paráfrasis es mayor que cero y menor que la dispersión entre framings.
- **H3:** las sociedades mixtas difieren de las homogéneas en bienestar y desigualdad. En particular, los agentes más cooperativos obtienen pagos menores cuando conviven con agentes egoístas.
- **H4:** en el juego repetido las contribuciones dependen positivamente de la contribución media observada de los demás.
- **H5, exploratoria:** los modelos con razonamiento explícito contribuyen menos que sus contrapartes sin él (réplica de Li y Shirado al variar $r/N$).

No se formula una hipótesis general sobre si los LLM cooperan más que los humanos, ni se asume que más cooperación implica más bienestar.

---

## 7. Modelo formal

### 7.1 Juego de bienes públicos lineal

Hay $N$ agentes. Cada agente $i$ recibe una dotación $E$ y elige una contribución $c_i \in [0, E]$. El fondo común se multiplica por $r$ y se reparte en partes iguales:

$$u_i(c_i, c_{-i}) = E - c_i + \frac{r}{N}\sum_{j=1}^{N} c_j$$

El retorno marginal per cápita es $m = r/N$. El dilema social estándar requiere $1 < r < N$, es decir, $1/N < m < 1$. En ese rango, con utilidad monetaria y una sola ronda, contribuir cero es estrategia dominante y el perfil de contribución cero es el equilibrio de Nash.

### 7.2 Equilibrio y óptimo social

$$W(c) = \sum_{i=1}^{N} u_i(c) = NE + (r-1)\sum_{i=1}^{N} c_i$$

- Equilibrio de Nash de una ronda: $c_i = 0$ para todos.
- Óptimo social: $c_i = E$ para todos.

La comparación ilustra el dilema. No demuestra una contradicción entre Adam Smith y Nash: Nash define estabilidad estratégica y la eficiencia social es otro criterio.

### 7.3 Condiciones fuera del dilema (nuevo)

| Condición | Rango | Predicción |
|---|---|---|
| Contribuir es ineficiente | $r < 1$ | Cero es dominante y también socialmente óptimo |
| Dilema social | $1 < r < N$ | Cero es dominante; $E$ es socialmente óptimo |
| Contribuir es dominante | $r > N$ | $E$ es dominante y socialmente óptimo |

En la primera y la tercera, interés propio y bienestar colectivo coinciden, de modo que cualquier agente que entienda los pagos debería elegir lo mismo. Funcionan como prueba de comprensión.

### 7.4 Ejemplo numérico

Con $N = 10$, $E = 100$ y $r = 5$ ($m = 0{,}5$): si todos contribuyen cero, cada agente obtiene 100 y el bienestar es 1.000. Si todos contribuyen 100, cada uno obtiene 500 y el bienestar es 5.000. Con la convención de maximización, $\text{PoA} = W_{\text{óptimo}} / W_{\text{equilibrio}} = 5$. La convención debe declararse.

### 7.5 Juego repetido

El mismo grupo juega $T$ rondas. La contribución cero no es necesariamente el único equilibrio del juego repetido, así que el equilibrio de una ronda se usa solo como referencia estática. Hay que especificar qué observa cada agente (contribuciones propias, promedio del grupo, contribuciones individuales, pagos) y si conoce $T$. Pal et al. muestran que conocer o no el horizonte cambia la conducta, por lo que debe fijarse o tratarse como factor.

---

## 8. Diseño de agentes

| Agente | Política | Propósito |
|---|---|---|
| Egoísta | $c_i = 0$ | Control de equilibrio de Nash |
| Cooperativo | $c_i = E$ | Referencia de óptimo social |
| Recíproco | Iguala la contribución media observada en la ronda anterior | Control de cooperación condicional |
| Adaptativo | Actualiza su acción según recompensas observadas (por ejemplo, promedio móvil exponencial o bandido simple) | Control de aprendizaje no lingüístico |
| LLM | Recibe el estado y devuelve una contribución válida | Agente evaluado |

### 8.1 Qué se le pide al LLM

Recibe reglas, dotación, número de participantes, factor de multiplicación, información permitida sobre los demás e historial. Devuelve una acción estructurada:

```json
{ "contribution": 35 }
```

El entorno valida el formato. Las respuestas no parseables se registran como error y se tratan según una política definida de antemano, sin corregirlas en silencio. La explicación textual del LLM no se usa como evidencia de su razonamiento.

### 8.2 Modelos

- Dos o tres familias distintas, con nombre exacto, proveedor, identificador de versión y fecha de consulta.
- Al menos un modelo open-weight ejecutable localmente, para que la réplica no dependa de una API.
- Parámetros de generación constantes y registrados.
- **Modo de razonamiento declarado.** Dado el resultado de Li y Shirado, hay que fijarlo o variarlo como factor (H5).

---

## 9. Diseño experimental

### 9.1 Factores

**Parámetros base, elegidos para coincidir con la literatura:**

| Parámetro | Valor | Coincide con |
|---|---|---|
| Jugadores | $N = 4$ | Fischbacher y Gächter; Isaac y Walker; Li y Shirado; Mei et al. |
| Dotación | $E = 20$ | Fischbacher y Gächter; Mei et al.; Sreedhar et al. |
| Acción | Entero de 0 a 20 | Fischbacher y Gächter; GAMA-Bench |
| Retorno dentro del dilema | $m$ = 0,3; 0,4; 0,5; 0,75 | 0,3 y 0,75 de Isaac y Walker; 0,4 de Fischbacher y Gächter y de Sreedhar et al.; 0,5 de Li y Shirado y de Mei et al. |
| Control ineficiente | $m = 0{,}2$ ($r = 0{,}8$) | Fuera del dilema: aportar destruye valor |
| Control dominante | $m = 1{,}25$ ($r = 5$) | Fuera del dilema: aportar conviene a cada uno |
| Condición secundaria | $N = 10$, $m = 0{,}2$ | Réplica de la configuración de GAMA-Bench |

Con $N = 4$ el dilema ocupa el rango $0{,}25 < m < 1$.

**Prompt base.** Marco neutro al estilo de Pal et al.: sin nombrar el juego, sin las palabras "public", "cooperate" ni "contribute", con "points" y "other participants". Los prompts de los trabajos anteriores ("group project", "water cleaning project", "Teamwork") pasan a ser condiciones de framing.

**Repeticiones.** Los trabajos leídos usan desde 5 corridas (GAMA-Bench, Han et al., Vallinder y Hughes) hasta 100 ensayos (Li y Shirado) o 300 (Lorè y Heydari). Con 5 corridas la varianza entre semillas domina. Se propone un mínimo de 50 decisiones independientes por celda en una ronda.

| Factor | Niveles iniciales |
|---|---|
| Incentivo $m = r/N$ | 4 valores dentro del dilema y 2 controles fuera |
| Prompt | Neutral, 2–3 paráfrasis, 2 framings |
| Modelo | 2–3 familias |
| Razonamiento | Con y sin, en al menos una familia |
| Juego | Una ronda; repetido |
| Composición | Homogénea; mixta de LLM; mixta de LLM y políticas clásicas |

No conviene cruzar todo. Se propone un diseño factorial completo solo para incentivo × prompt × modelo en una ronda, y diseños reducidos para el resto.

### 9.2 Experimentos

**E0. Validación del entorno.** Políticas deterministas, verificación de pagos, equilibrio, óptimo y reproducibilidad con semillas. No prueba hipótesis.

**E1. Curva de respuesta a incentivos (RQ1).** Barrido de $m$ en una ronda, con los dos controles fuera del dilema. Antes de decidir, el agente responde dos o tres preguntas de cálculo de pagos; la tasa de acierto se reporta por separado.

**E2. Paráfrasis y framing (RQ2).** Dos manipulaciones distintas:

- *Paráfrasis:* misma información, mismos números, distinta redacción y orden. Siguiendo las pruebas de robustez de Akata et al.: orden de las oraciones, unidad de pago (puntos, monedas, fichas), etiquetas de los participantes y forma de expresar el retorno (multiplicador, porcentaje o ejemplo numérico).
- *Framing:* cambio de marco manteniendo los pagos. Tres candidatos con respaldo en la literatura: dar frente a tomar (Andreoni, 1995); "Teamwork" frente a "Taxation" (Sreedhar et al.); y nombrar o no el juego como "public goods game" (Mei et al.), que además mide el efecto de memorización.

Los pagos deben ser idénticos en ambas y hay que verificarlo de forma automática.

**E3. Composición (RQ3).** Población de políticas clásicas, homogénea de un LLM, mixta de LLM y mixta de LLM con políticas clásicas en distintas proporciones.

**E4. Juego repetido y cooperación condicional (RQ4).** Dos partes:

- *Método de estrategia:* el agente indica cuánto contribuiría para cada nivel posible de contribución media de los demás. Permite clasificarlo como free-rider, cooperador condicional u otro, como en Fischbacher y Gächter. Es barato y muy informativo.
- *Juego repetido:* $T$ rondas con historial, para observar la trayectoria y el efecto de fin de juego.

**E5. Robustez.** Semillas, orden de los agentes, temperatura y, si es posible, una segunda versión del mismo modelo.

### 9.3 Tamaño del piloto

$N = 5$ o $N = 10$; $T = 10$ a 20; 20–30 repeticiones por condición; dos modelos. Son números operativos, no un tamaño muestral justificado. El estudio final debe apoyarse en la varianza del piloto. Hay que calcular el número de llamadas antes de empezar: el factorial de E1 y E2 con 6 niveles de incentivo, 6 prompts, 3 modelos y 50 decisiones por celda son 5.400 decisiones en una ronda. Como referencia, Pal et al. hicieron unas 40.000 llamadas en total.

---

## 10. Métricas

### 10.1 Resultado económico y social

| Métrica | Definición | Usada en |
|---|---|---|
| Contribución media normalizada | $\bar{c} = \frac{1}{N}\sum_i c_i / E$ | Li y Shirado; Sreedhar et al. |
| Bienestar | $W = \sum_i u_i$, total y por agente | Estándar |
| Eficiencia normalizada | $(W - W_{\text{Nash}}) / (W_{\text{óptimo}} - W_{\text{Nash}})$ | Estándar. En el PGG lineal coincide con $\bar{c}$; reportar una sola |
| Desigualdad | Gini sobre pagos acumulados | GovSim usa igualdad $e = 1 - \frac{\sum_i \sum_j \lvert R_i - R_j \rvert}{2 \lvert I \rvert \sum_i R_i}$, que es uno menos el Gini |
| Ganancia colectiva en poblaciones mixtas | Pago medio por tipo de agente | Li y Shirado |

### 10.2 Respuesta a incentivos

| Métrica | Definición |
|---|---|
| Pendiente de respuesta | Coeficiente de $m$ en una regresión de $c_i/E$ dentro del dilema |
| Monotonicidad | Correlación de Spearman entre $m$ y contribución |
| Error en controles | Distancia a la acción dominante cuando $r < 1$ y cuando $r > N$ |
| Tasa de comprensión | Proporción de respuestas correctas en las preguntas de cálculo |
| Distancia a humanos | Diferencia entre la pendiente del LLM y la reportada en la literatura humana (entre 25 y 50 puntos porcentuales por unidad de $m$, §4.8) |

**Sobre el regret.** En el PGG lineal de una ronda, la mejor respuesta es siempre cero, así que

$$\text{Regret}_i = c_i\left(1 - \frac{r}{N}\right)$$

Es la contribución reescalada y no agrega información. Se puede mencionar para conectar con la literatura de teoría de juegos, pero no presentarlo como una métrica independiente. Lo mismo ocurre con la "distancia al equilibrio". Tiene sentido como métrica propia solo en el juego repetido, donde requiere estimar una mejor respuesta frente a las estrategias observadas.

### 10.3 Consistencia ante el prompt

| Métrica | Definición |
|---|---|
| Dispersión por paráfrasis | Desviación estándar de la contribución media entre paráfrasis, con incentivo y modelo fijos |
| Efecto de framing | Diferencia de medias entre marcos, con tamaño de efecto |
| Descomposición de varianza | Proporción de varianza atribuible a incentivo, paráfrasis, framing, modelo y semilla. Dos vías: modelo mixto con componentes de varianza, o regresión con análisis de dominancia como en Lorè y Heydari |
| Razón señal/ruido | Varianza explicada por el incentivo dividida por la explicada por la paráfrasis |

La razón señal/ruido resume el paper en un número por modelo: si es menor que uno, la redacción pesa más que los incentivos.

### 10.4 Conducta en el juego repetido

| Métrica | Definición | Referencia |
|---|---|---|
| Pendiente de cooperación condicional | Coeficiente de la contribución media de los demás sobre la propia, en el método de estrategia | Fischbacher y Gächter |
| Tipología | Proporción de free-riders, cooperadores condicionales y otros | Fischbacher y Gächter |
| Caída | Pendiente de la contribución por ronda | Fischbacher y Gächter |
| Efecto de fin de juego | Diferencia entre la última ronda y el promedio previo | Kořínek y Štekerová lo observan |

### 10.5 Heterogeneidad y operación

- **Compresión de varianza:** desviación estándar entre agentes del mismo modelo en una misma condición. Hirashima et al. señalan que los agentes LLM tienden a converger; para un ABM eso significa perder heterogeneidad.
- **Varianza entre semillas**, que Vallinder y Hughes encuentran grande.
- **Tasa de acciones inválidas.**
- **Costo en tokens** por decisión y por experimento.

---

## 11. Análisis estadístico

Las decisiones de agentes en una misma partida no son independientes.

1. Medias, medianas, desviaciones estándar e intervalos de confianza por condición.
2. Bootstrap por partida o modelos jerárquicos. No remuestrear agentes como si fueran independientes.
3. Modelos mixtos con efectos aleatorios por partida y por agente en el juego repetido.
4. Corrección por comparaciones múltiples.
5. Tamaños de efecto e intervalos, no solo valores $p$.
6. Prerregistro de hipótesis, métricas principales y exclusiones.

Las contribuciones de los LLM suelen concentrarse en pocos valores (0, 50 % o 100 %). Hay que mirar la distribución antes de aplicar modelos que suponen normalidad; una regresión ordinal o fraccional puede ajustar mejor.

---

## 12. Amenazas a la validez

| Amenaza | Riesgo | Mitigación |
|---|---|---|
| Contaminación de entrenamiento | El PGG es un juego muy conocido y el modelo puede recitar la respuesta "de libro". Es la objeción más probable de un revisor: la plantean Larooij y Törnberg (fuga de datos) y Gupta et al. (recuperar del preentrenamiento en vez de razonar) | Marco neutral sin el nombre del juego (como Pal et al.); condición que sí lo nombra, para medir la diferencia; controles fuera del dilema, donde la respuesta "de libro" es incorrecta; reportar si el modelo nombra el juego |
| Sesgo de posición y de etiqueta | El orden de las opciones o las letras usadas cambian la respuesta (limitación reconocida por Li y Shirado y por Pal et al.) | Acción numérica en vez de opciones; aleatorizar el orden de la información |
| Confusión entre comprensión y preferencia | Una contribución alta puede ser un error de cálculo | Controles fuera del dilema y preguntas de comprensión |
| Sobre-control por prompt | El diseño del prompt determina el resultado (Li y Wu) | Publicar todos los prompts; medir la varianza por paráfrasis |
| Antropomorfismo | Leer el texto del LLM como preferencias | Inferir solo desde acciones |
| Variabilidad del LLM | Misma entrada, distintas salidas | Repeticiones y registro de parámetros |
| Dependencia entre agentes | Observaciones correlacionadas | Análisis por partida |
| Deriva de API | El proveedor cambia el modelo | Snapshots con fecha; un modelo open-weight local |
| Modo de razonamiento | Cambia el nivel de cooperación (Li y Shirado) | Fijarlo o tratarlo como factor |
| Validez externa | Un PGG abstracto no es una sociedad | Limitar las conclusiones al entorno estudiado |
| Comparación con humanos | Los datos humanos vienen de otros diseños | Comparar solo direcciones y hechos estilizados, no niveles |

---

## 13. Implementación

El motor del juego y el módulo de decisión del agente van separados.

```text
llm-public-goods-study/
├── configs/        baseline.yaml, prompt_variants.yaml, model_registry.yaml
├── game/           public_goods.py, payoff.py, validation.py
├── agents/         base_agent.py, selfish.py, cooperative.py,
│                   reciprocal.py, adaptive.py, llm_agent.py
├── prompts/        neutral.md, paraphrase_*.md, framing_*.md, comprehension.md
├── experiments/    incentive_curve.py, prompt_robustness.py,
│                   population_mixture.py, strategy_method.py, repeated_game.py
├── metrics/        welfare.py, incentives.py, consistency.py, inequality.py
├── analysis/       statistics.py, plots.py
├── data/           raw/, processed/
├── docs/           ODD.md
└── README.md
```

Reglas:

- El motor calcula todos los pagos. El LLM solo devuelve una acción estructurada.
- Se guardan prompt, respuesta, acción parseada, estado, pagos, modelo y metadatos.
- Los reintentos se registran y no ocultan fallos.
- Las llamadas a modelos pasan por una interfaz común.
- Pruebas unitarias para pagos, restricciones y casos límite, incluida la igualdad de pagos entre variantes de prompt.

Python con NumPy, pandas, SciPy y Matplotlib basta. Mesa es opcional; usarlo acerca el trabajo a las herramientas de la comunidad ABM pero no es necesario para un PGG pequeño.

**ODD.** El archivo `docs/ODD.md` describe propósito, entidades y variables, proceso y calendario, conceptos de diseño, inicialización, datos de entrada y submodelos. En el paper va una versión resumida y la completa queda en el repositorio.

---

## 14. Estructura del paper (12 páginas LNCS)

| Sección | Páginas | Contenido |
|---|---|---|
| 1. Introducción | 1,5 | El problema de validación de reglas de decisión basadas en LLM en ABM; pregunta y contribuciones |
| 2. Trabajo relacionado | 1,5 | LLM en dilemas sociales; framing; validación de ABM generativos; evidencia humana |
| 3. Modelo | 1,5 | PGG lineal, condiciones fuera del dilema, resumen ODD |
| 4. Agentes y diseño experimental | 2 | Agentes, factores, experimentos, métricas |
| 5. Resultados | 3,5 | Curvas de incentivos; descomposición de varianza; poblaciones mixtas; cooperación condicional |
| 6. Discusión | 1 | Implicaciones para modeladores; límites |
| 7. Conclusión | 0,5 | |
| Referencias | 0,5–1 | Unas 30 |

Figuras previstas, cuatro como máximo: curva de contribución frente a $m$ por modelo con referencia humana y de equilibrio; descomposición de varianza por modelo; bienestar y pago por tipo en poblaciones mixtas; perfiles de cooperación condicional.

Si el tiempo no alcanza, el paper mínimo viable es E0, E1 y E2 con dos modelos. E3 y E4 pueden pasar a un extended abstract o a trabajo futuro.

---

## 15. Cronograma hacia abril de 2027

Supone cierre a principios de abril, con la fecha exacta por confirmar en febrero.

| Semanas | Fechas aproximadas | Actividad | Resultado |
|---|---|---|---|
| 1–2 | 17–30 nov | Leer completos los trabajos de §4.1, §4.3 y §4.7; cerrar diseño | Diseño y ODD en borrador |
| 3–4 | 1–14 dic | Implementar juego, políticas clásicas y pruebas (E0) | Simulador validado |
| 5–6 | 15 dic–4 ene | Integrar dos LLM; redactar prompts y controles | Módulo LLM con registro |
| 7–8 | 5–18 ene | Piloto de E1 y E2; revisar los tracks publicados de SSC 2027 | Varianza, costos, track elegido |
| 9 | 19–25 ene | Ajustar hipótesis y tamaño muestral; prerregistro | Diseño final congelado |
| 10–14 | 26 ene–28 feb | Ejecutar E1 a E5 | Datos crudos |
| 15–16 | 1–14 mar | Análisis y figuras; leer el CFP y ajustar formato | Resultados |
| 17–19 | 15 mar–4 abr | Redacción, revisión interna, repositorio | Manuscrito enviado |

Hitos externos a vigilar: publicación de tracks (noviembre–enero) y CFP (febrero). Conviene suscribirse a la lista SIMSOC.

### Criterios para detener o ampliar

- Si los LLM no responden a los incentivos, revisar primero prompt, formato de acción y comprensión de reglas.
- Si la varianza por paráfrasis domina, ese pasa a ser el resultado central del paper.
- Si los LLM fallan los controles fuera del dilema, reportarlo como hallazgo principal: invalida la lectura de sus contribuciones como cooperación.
- Si el costo impide escalar, reducir modelos o condiciones antes que repeticiones.

---

## 16. Título y abstract de trabajo

### Títulos

Recomendado para SSC:

**Incentives or Wording? Auditing LLM Agents as Decision Rules in Public Goods Games**

Si se adopta el encuadre de §3.1:

**Nash's Players or Smith's Moral Agents? Auditing LLM Decision Rules in Public Goods Games**

Alternativas:

- **How Much Do LLM Agents Respond to Incentives? A Public Goods Game Audit for Agent-Based Modellers**
- **Strategic Consistency and Collective Outcomes of LLM-Based Agents in Linear Public Goods Games**

El título de la v1.0 decía "An Empirical Game-Theoretic Study". Conviene evitarlo: EGTA es un método específico (el que usan Shi et al.) y este trabajo no lo aplica.

### Abstract de trabajo (no final)

Large language models are increasingly proposed as decision rules for agents in social simulations, yet it remains unclear whether their choices track the incentives encoded in a model or the wording used to describe it. We present a controlled audit of LLM-based agents in linear public goods games. We vary the marginal per capita return within and beyond the social-dilemma range, present each game under payoff-equivalent paraphrases and alternative framings, and compare LLM agents with transparent selfish, cooperative, reciprocal and adaptive baselines in homogeneous and mixed populations. We report incentive-response curves, a decomposition of contribution variance into incentive, wording, model and seed components, conditional-cooperation profiles elicited with the strategy method, and collective outcomes in terms of welfare and inequality. Results are contrasted with the Nash prediction and with stylised facts from human public goods experiments. The game engine computes all payoffs independently of the language models, and the environment is documented following the ODD protocol. The resulting protocol and open artefacts are intended to help modellers decide when an LLM is a defensible decision rule in an agent-based model.

---

## 17. Bibliografía

### 17.1 Verificada en Scopus (17-11-2026)

**LLM y bienes públicos**

1. Li, Y., & Shirado, H. (2025). Spontaneous Giving and Calculated Greed in Language Models. *EMNLP 2025*. doi:10.18653/v1/2025.emnlp-main.267
2. Sreedhar, K., Cai, A., Ma, J., Nickerson, J. V., & Chilton, L. B. (2025). Simulating Cooperative Prosocial Behavior with Multi-Agent LLMs. *IUI 2025*. doi:10.1145/3708359.3712149
3. Liang, Y., Qu, Y., Yang, J., Lin, S., & Shen, Z.-J. M. (2026). Everyone Contributes! Incentivizing Strategic Cooperation in Multi-LLM Systems via Sequential Public Goods Games. *AAMAS 2026*. doi:10.65109/SJPO2377. Páginas por confirmar.
4. Sabato, Y., Hazon, N., & Azaria, A. (2025). Humans Predict the Nash Equilibrium as an Outcome of a Multi-Agent Public Goods Game. *ICTAI 2025*. doi:10.1109/ICTAI66417.2025.00195
5. Hintze, A., & Adami, C. (2026). Promoting cooperation in the public goods game using artificial intelligent agents. *npj Complexity*. doi:10.1038/s44260-025-00065-9
6. Mei, Q., Xie, Y., Yuan, W., & Jackson, M. O. (2024). A Turing test of whether AI chatbots are behaviorally similar to humans. *PNAS*. doi:10.1073/pnas.2313925121

**LLM en dilemas sociales**

7. Akata, E., Schulz, L., Coda-Forno, J., Oh, S. J., Bethge, M., & Schulz, E. (2025). Playing repeated games with large language models. *Nature Human Behaviour*. doi:10.1038/s41562-025-02172-y
8. Pal, S., Mallela, A., Pracher, L., Wei, C., Fu, F., Schnell, S. D., & Nowak, M. A. (2026). Large language models instantiate evolutionarily robust strategies of cooperation. *PNAS Nexus*. doi:10.1093/pnasnexus/pgag210
9. Piatti, G., Jin, Z., Kleiman-Weiner, M., Schölkopf, B., Sachan, M., & Mihalcea, R. (2024). Cooperate or Collapse: Emergence of Sustainable Cooperation in a Society of LLM Agents. *NeurIPS 2024*.
10. Gupta, P., Zhong, Q., Yakura, H., Eisenmann, T., & Rahwan, I. (2026). The Role of Social Learning and Collective Norm Formation in Fostering Cooperation in LLM Multi-Agent Systems. *AAMAS 2026*, 1238–1246. doi:10.65109/CZDC3237
11. Vallinder, A., & Hughes, E. (2025). Cultural Evolution of Cooperation among LLM Agents. *AAMAS 2025*. Extended abstract.
12. Willis, R., Du, Y., & Leibo, J. Z. (2025). Will Systems of LLM Agents Lead to Cooperation: An Investigation into a Social Dilemma. *AAMAS 2025*, 2786–2788. Extended abstract.
13. Han, J., Battu, B., Romić, I., Rahwan, T., & Holme, P. (2025). Static network structure cannot stabilize cooperation among large language model agents. *PLOS ONE*. doi:10.1371/journal.pone.0320094
14. Suzuki, R., & Arita, T. (2024). An evolutionary model of personality traits related to cooperative behavior using a large language model. *Scientific Reports*. doi:10.1038/s41598-024-55903-y
15. Sakai, M., Yokoyama, M., Tateishi, W., & Ichinose, G. (2026). Effects of personality steering on cooperative behavior in large language model agents. *Scientific Reports*. doi:10.1038/s41598-026-56163-8
16. Smith, C., et al. (2025). Evaluating Generalization Capabilities of LLM-Based Agents in Mixed-Motive Scenarios Using Concordia. *NeurIPS 2025*.
17. Yılmaz, H., & Kılıç, H. (2026). About Cooperative Behavior of LLM Agents in Different Repeated Social Dilemma Game Contexts. *IISEC 2026*. doi:10.1109/IISEC69317.2026.11418487
18. Warnakulasuriya, K., et al. (2026). Evolution of Cooperation in LLM-Agent Societies: A Preliminary Study Using Different Punishment Strategies. *LNCS*. doi:10.1007/978-3-032-17542-7_7
19. Xie, K., Liu, Y., Lan, Z., & Szolnoki, A. (2026). Evolutionary games in LLM-agent societies: Early milestones and perspectives. *Chaos, Solitons & Fractals*. doi:10.1016/j.chaos.2026.119158
20. Mu, C., et al. (2024). Multi-agent, human–agent and beyond: A survey on cooperation in social dilemmas. *Neurocomputing*. doi:10.1016/j.neucom.2024.128514
21. Meylahn, B. V. (2025). Multi-agent Reinforcement Learning in the All-or-Nothing Public Goods Game on Networks. *AAMAS 2025*, 1492–1500. Heredada de la v1.0; no apareció en las búsquedas de hoy.

**Framing y prompt**

22. Lorè, N., & Heydari, B. (2024). Strategic behavior of large language models and the role of game structure versus contextual framing. *Scientific Reports*. doi:10.1038/s41598-024-69032-z
23. Kořínek, M., & Štekerová, K. (2026). Words Matter: How Prompt Framing Shapes Strategic Behaviour in Large Language Models. *Journal of Cases on Information Technology*. doi:10.4018/JCIT.398628
24. Li, Z., & Wu, Q. (2025). Let It Go or Control It All? The Dilemma of Prompt Engineering in Generative Agent-Based Models. *System Dynamics Review*. doi:10.1002/sdr.70008
25. Powell, A., et al. (2027). Lost in Translation? Large Language Models Alter Strategic Behaviour When Prompted in Low-Resource Languages. *LNCS*. doi:10.1007/978-3-032-39028-8_19

**Benchmarks y racionalidad**

26. Fan, C., Chen, J., Jin, Y., & He, H. (2024). Can Large Language Models Serve as Rational Players in Game Theory? A Systematic Analysis. *AAAI 2024*. doi:10.1609/aaai.v38i16.29751
27. Jia, J., Yuan, Z., Pan, J., McNamara, P. E., & Chen, D. (2025). LLM Strategic Reasoning: Agentic Study through Behavioral Game Theory. *NeurIPS 2025*.
28. Duan, J., et al. (2024). GTBench: Uncovering the Strategic Reasoning Limitations of LLMs via Game-Theoretic Evaluations. *NeurIPS 2024*. Autores por confirmar.
29. Xu, L., et al. (2024). MAgIC: Investigation of Large Language Model Powered Multi-Agent in Cognition, Adaptability, Rationality and Collaboration. *EMNLP 2024*. doi:10.18653/v1/2024.emnlp-main.416
30. Kempinski, B., et al. (2025). Game of Thoughts: Iterative Reasoning in Game-Theoretic Domains with Large Language Models. *AAMAS 2025*.
31. Sun, H., Wu, Y., Cheng, Y., & Chu, X. (2025). Game Theory Meets Large Language Models: A Systematic Survey. *IJCAI 2025*. doi:10.24963/ijcai.2025/1184
32. Guo, Y., Wang, H., & Feng, X. (2026). Game-theoretic evaluation of strategic reasoning in large language models. *Neurocomputing*. doi:10.1016/j.neucom.2026.133006
33. Kader, G., & Lee, D. (2026). The emergence of strategic reasoning of large language models. *Journal of Behavioral and Experimental Economics*. doi:10.1016/j.socec.2026.102643

**LLM como sustitutos humanos**

34. Gao, Y., Lee, D., Burtch, G., & Fazelpour, S. (2025). Take caution in using LLMs as human surrogates. *PNAS*. doi:10.1073/pnas.2501660122
35. Capraro, V., Di Paolo, R., & Pizziol, V. (2025). A publicly available benchmark for assessing large language models' ability to predict how humans balance self-interest and the interest of others. *Scientific Reports*. doi:10.1038/s41598-025-01715-7
36. Kitadai, A., et al. (2025). Can AI with High Reasoning Ability Replicate Human-like Decision Making in Economic Experiments? *Group Decision and Negotiation*. doi:10.1007/s10726-025-09946-9
37. Filippas, A., Horton, J. J., & Manning, B. S. (2024). Large Language Models as Simulated Economic Agents: What Can We Learn from Homo Silicus? *EC 2024*. doi:10.1145/3670865.3673513
38. Aher, G., Arriaga, R. I., & Kalai, A. T. (2023). Using Large Language Models to Simulate Multiple Humans and Replicate Human Subject Studies. *ICML 2023 (PMLR)*. Autores por confirmar.
39. Park, J. S., et al. (2023). Generative Agents: Interactive Simulacra of Human Behavior. *UIST 2023*. doi:10.1145/3586183.3606763

**Validación de ABM generativos**

40. Larooij, M., & Törnberg, P. (2026). Validation is the central challenge for generative social simulation: a critical review of LLMs in agent-based modeling. *Artificial Intelligence Review*. doi:10.1007/s10462-025-11412-6
41. Adornetto, C., et al. (2025). Generative Agents in Agent-Based Modeling: Overview, Validation, and Emerging Challenges. *IEEE Transactions on Artificial Intelligence*. doi:10.1109/TAI.2025.3566362
42. Lu, Y., Aleta, A., Du, C., Shi, L., & Moreno, Y. (2024). LLMs and generative agent-based models for complex systems research. *Physics of Life Reviews*. doi:10.1016/j.plrev.2024.10.013
43. Zhao, P., Pham, D. H., & Vincent, N. (2026). Mechanism Plausibility in Generative Agent-Based Modeling. *FAccT 2026*. doi:10.1145/3805689.3812388
44. Hirashima, S., Hu, S., & Cheong, K. H. (2026). Beyond Hyper-Rationality: Persona-Driven Heterogeneity in Networked Agent-Based Systems. *IEEE TNSE*. doi:10.1109/TNSE.2026.3742449
45. Chopra, A., et al. (2025). On the Limits of Agency in Agent-based Models. *AAMAS 2025*.
46. Shi, J., Frantz, C. K., Kimmich, C., Siddiki, S., & Sarkar, A. (2026). LLM-augmented Empirical Game Theoretic Simulation for Socio-ecological Systems. *AAMAS 2026*, 1601–1609. doi:10.65109/SEWU4006. Heredada de la v1.0; no apareció en las búsquedas de hoy.
47. Tang, X., & Törnberg, P. (2026). Beyond Black-Box Agents: Explainable and Validatable Generative ABMs. *LNCS*. doi:10.1007/978-3-032-29915-4_39
48. Morge, M. (2025). Is Generative Artificial Intelligence Ready for Computational Social Science? *LNCS*. doi:10.1007/978-3-032-07638-0_19

**SSC y JASSS**

49. Vanhée, L., Borit, M., Siebers, P.-O., et al. (2026). Large Language Models for Agent-Based Modelling: Current and Possible Uses Across the Modelling Cycle. *SSC 2025, Springer Proceedings in Complexity*. doi:10.1007/978-3-032-31712-4_43
50. Edmonds, B. (2026). When Can You Use AI for ABM? *SSC 2025*. doi:10.1007/978-3-032-31712-4_9
51. Malleson, N., & Manley, E. (2026). Towards the Use of Foundation Models and Embeddings for Nuanced Perception and Decision-Making in Agents. *SSC 2025*. doi:10.1007/978-3-032-31712-4_28
52. Feng, W., et al. (2026). Exploratory Generative Agent-Based Modeling Framework for Flood Resilience Governance. *SSC 2025*. doi:10.1007/978-3-032-31712-4_11
53. Cohen, Y. L., Callahan, J., Left, S. C., & Rothman, D. S. (2026). Introducing Threat-Perceiving Actors in Group-Selective Public Goods Games. *SSC 2025*. doi:10.1007/978-3-032-31712-4_6
54. Zhang, S., Peng, Z., & Ren, Y. (2026). GPLab: A Generative Agent-Based Framework for Policy Simulation and Evaluation. *JASSS*. doi:10.18564/jasss.5933
55. Qu, X., Cao, Z., Yang, X., & Han, T. A. (2019). How Group Cohesion Promotes the Emergence of Cooperation in Public Goods Game Under Conditional Dissociation. *JASSS*. doi:10.18564/jasss.4070
56. Grimm, V., et al. (2020). The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism. *JASSS*. doi:10.18564/jasss.4259

**Evidencia humana en PGG**

57. Zelmer, J. (2003). Linear Public Goods Experiments: A Meta-Analysis. *Experimental Economics*. doi:10.1023/A:1026277420119
58. Fischbacher, U., & Gächter, S. (2010). Social Preferences, Beliefs, and the Dynamics of Free Riding in Public Goods Experiments. *American Economic Review*. doi:10.1257/aer.100.1.541
59. Gächter, S., & Marino Fages, D. (2026). The behavioral structure of one-shot cooperation in small and large groups. *Journal of Economic Behavior & Organization*. doi:10.1016/j.jebo.2026.107828

### 17.2 Añadidas en la versión 2.1 (metadatos verificados en Crossref o en la fuente)

60. Huang, J.-t., Li, E. J., Lam, M. H., Liang, T., Wang, W., Yuan, Y., et al. (2025). How Far Are We on the Decision-Making of LLMs? Evaluating LLMs' Gaming Ability in Multi-Agent Environments. *ICLR 2025*. arXiv:2403.11807.
61. Isaac, R. M., & Walker, J. M. (1988). Group Size Effects in Public Goods Provision: The Voluntary Contributions Mechanism. *Quarterly Journal of Economics*, 103(1), 179–199. doi:10.2307/1882648
62. Ledyard, J. O. (1995). Public Goods: A Survey of Experimental Research. En Kagel y Roth (eds.), *The Handbook of Experimental Economics*, Princeton University Press, 111–194.
63. Fehr, E., & Gächter, S. (2000). Cooperation and Punishment in Public Goods Experiments. *American Economic Review*, 90(4), 980–994. doi:10.1257/aer.90.4.980
64. Fischbacher, U., Gächter, S., & Fehr, E. (2001). Are people conditionally cooperative? Evidence from a public goods experiment. *Economics Letters*, 71(3), 397–404. doi:10.1016/S0165-1765(01)00394-9
65. Andreoni, J. (1995). Warm-Glow versus Cold-Prickle: The Effects of Positive and Negative Framing on Cooperation in Experiments. *Quarterly Journal of Economics*, 110(1), 1–21. doi:10.2307/2118508
66. Smith, A. (1776). *An Inquiry into the Nature and Causes of the Wealth of Nations*. Ed. Cannan. Libro IV, cap. ii (párr. IV.2.9) y Libro V, cap. i, parte III (párr. V.1.69).
67. Smith, A. (1759). *The Theory of Moral Sentiments*. Parte I, sec. i, cap. 1 (párr. I.I.1) y Parte IV, cap. 1 (párr. IV.I.10).
68. Ashraf, N., Camerer, C. F., & Loewenstein, G. (2005). Adam Smith, Behavioral Economist. *Journal of Economic Perspectives*, 19(3), 131–145. doi:10.1257/089533005774357897
69. Smith, V. L. (1998). The Two Faces of Adam Smith. *Southern Economic Journal*, 65(1), 1–19. doi:10.2307/1061349. Solo resumen leído.
70. Smith, V. L., & Wilson, B. J. (2019). *Humanomics: Moral Sentiments and the Wealth of Nations for the Twenty-First Century*. Cambridge University Press. doi:10.1017/9781108185561. Solo índice revisado.
71. Samuelson, P. A. (1954). The Pure Theory of Public Expenditure. *Review of Economics and Statistics*, 36(4), 387–389. doi:10.2307/1925895
72. Blaug, M. (2007). The Fundamental Theorems of Modern Welfare Economics, Historically Contemplated. *History of Political Economy*, 39(2), 185–207. doi:10.1215/00182702-2007-001. No leído; tesis tomada de fuentes secundarias.

Datos de publicación confirmados para entradas anteriores: Li y Shirado, pp. 5271–5286, arXiv:2502.17720; Sreedhar et al., pp. 1272–1286, arXiv:2502.12504; Liang et al., pp. 772–781, arXiv:2508.02076; Pal et al., arXiv:2601.09849; Gupta et al., arXiv:2510.14401; Zhao et al., arXiv:2605.12824; Vanhée et al., pp. 601–619, arXiv:2507.05723; Edmonds, pp. 124–136; Cohen et al., pp. 80–94; Malleson y Manley, pp. 377–387; Sabato et al., pp. 1344–1349; Zelmer, 6(3), 299–310; Fischbacher y Gächter, 100(1), 541–556; Gächter y Marino Fages, vol. 252, 107828.

### 17.3 Por verificar antes de citar

- Cifras de Zelmer, de Fischbacher y Gächter y de Gächter y Marino Fages: provienen de working papers y hay que cotejarlas con las versiones publicadas.
- Arrow (1951) y Debreu (1959), si se menciona el primer teorema del bienestar: solo se confirmaron los metadatos.
- La escena de *A Beautiful Mind*: la cita viene de una transcripción no oficial. No se encontró una fuente académica que critique la escena de forma explícita; hay un artículo de divulgación de S. Ikeda (FEE, 2002). Si se menciona la película, hacerlo en una nota al pie.
- De Curtò y de Zarzà (2026), "Theory-Grounded LLM Societies for Emergent Coordination", *IEEE Access*, doi:10.1109/ACCESS.2026.3706338. Parece relevante para cooperación en redes, pero el resumen que obtuve no era el abstract original.
- Páginas de los trabajos de AAMAS 2026 y nombres completos de autores donde figura "et al.".

---

## Apéndice A. Consultas de Scopus

Ejecutadas el 17-11-2026, ordenadas por relevancia, 25 resultados cada una.

```text
TITLE-ABS-KEY(("large language model*" OR LLM* OR "generative agent*") AND "public good*")

TITLE-ABS-KEY("public goods game*" AND ("language model*" OR GPT* OR chatbot*
  OR "generative AI" OR "AI agent*")) AND PUBYEAR > 2022

TITLE-ABS-KEY(("large language model*" OR LLM*) AND ("social dilemma*"
  OR "prisoner's dilemma" OR "common pool resource*") AND cooperat*) AND PUBYEAR > 2022

TITLE-ABS-KEY(("large language model*" OR LLM*) AND "game theor*"
  AND (benchmark* OR "strategic reasoning" OR rationality)) AND PUBYEAR > 2022

TITLE-ABS-KEY(("large language model*" OR LLM*) AND (game* OR "social dilemma*" OR cooperat*)
  AND ("prompt sensitivity" OR "framing effect*" OR "prompt framing" OR paraphras*
  OR "prompt robustness" OR "contextual framing")) AND PUBYEAR > 2022

TITLE-ABS-KEY(("large language model*" OR GPT OR LLM*) AND ("behavioral game*"
  OR "dictator game" OR "ultimatum game" OR "trust game" OR "homo silicus"
  OR "economic experiment*" OR "behavioral economics")) AND PUBYEAR > 2022

TITLE-ABS-KEY(("large language model*" OR LLM* OR "generative agent*")
  AND ("agent-based model*" OR "social simulation" OR "agent-based simulation")
  AND (validat* OR calibrat* OR review OR methodolog*)) AND PUBYEAR > 2022

CONFNAME("Social Simulation Conference") AND PUBYEAR > 2022 AND TITLE-ABS-KEY(
  "language model*" OR LLM* OR generative OR "public good*" OR "social dilemma*"
  OR "game theor*" OR cooperat* OR "reinforcement learning")

SRCTITLE("Springer Proceedings in Complexity") AND TITLE-ABS-KEY("social simulation"
  OR "agent-based") AND TITLE-ABS-KEY("public good*" OR "social dilemma*" OR cooperation
  OR "game theor*" OR "common pool" OR "collective action") AND PUBYEAR > 2018

ISSN(1460-7425) AND TITLE-ABS-KEY("language model*" OR LLM* OR "generative agent*"
  OR "public good*" OR "social dilemma*") AND PUBYEAR > 2018
```

Notas prácticas:

- Los proceedings de SSC se encuentran con `CONFNAME("Social Simulation Conference")` o con `SRCTITLE("Springer Proceedings in Complexity")`. La búsqueda `SRCTITLE("Advances in Social Simulation")` solo devuelve workshops brasileños antiguos.
- JASSS se filtra mejor por ISSN (1460-7425) que por título de fuente.
- La herramienta de Scopus usada aquí devuelve metadatos pero no el texto del abstract ni la lista de autores, y la búsqueda de citas entrantes falla con error 400. Los abstracts se obtuvieron por DOI desde OpenAlex (`https://api.openalex.org/works/doi:<DOI>`). Unos 13 trabajos no tienen abstract allí y hay que leerlos en la fuente.

---

## Apéndice C. Estado de acceso a los textos (17-11-2026)

| Trabajo | Acceso | Dónde |
|---|---|---|
| Li y Shirado | Texto completo | arxiv.org/abs/2502.17720; aclanthology.org/2025.emnlp-main.267 |
| Sreedhar et al. | Texto completo | arxiv.org/abs/2502.12504 |
| Huang et al., GAMA-Bench | Texto completo con apéndices | arxiv.org/abs/2403.11807 |
| Liang et al. | Texto completo | arxiv.org/abs/2508.02076; ifaamas.org/Proceedings/aamas2026/pdfs/SJPO2377.pdf |
| Mei et al. | Texto completo, material suplementario y prompts | PMC10907317; github.com/yutxie/ChatGPT-Behavioral |
| Pal et al. | Texto completo | PMC13298648; arxiv.org/abs/2601.09849 |
| Lorè y Heydari | Texto completo, sin material suplementario | nature.com/articles/s41598-024-69032-z |
| Akata et al. | Texto completo, sin material suplementario | nature.com/articles/s41562-025-02172-y |
| Han et al. | Texto completo | journals.plos.org, doi 10.1371/journal.pone.0320094 |
| Piatti et al., GovSim | Texto completo | arxiv.org/abs/2404.16698 |
| Vallinder y Hughes | Texto completo | arxiv.org/abs/2412.10270 |
| Vanhée et al. | Texto completo (preprint) | arxiv.org/abs/2507.05723 |
| Malleson y Manley | Texto completo (preprint de los autores) | urban-analytics.github.io/INTEGRATE |
| Larooij y Törnberg | Texto completo; §4.1 y tablas sin leer en detalle | link.springer.com, doi 10.1007/s10462-025-11412-6 |
| Zhao, Pham y Vincent | Texto completo salvo apéndice | arxiv.org/abs/2605.12824 |
| Gupta et al. | Cuerpo completo; apéndice sin revisar | arxiv.org/abs/2510.14401 |
| Shi et al. | Texto completo, sin material suplementario | arxiv.org/abs/2510.21965 |
| Zelmer | Working paper SEDAP 46, no la versión publicada | web.archive.org (socserv.mcmaster.ca/sedap/p/sedap46.pdf) |
| Fischbacher y Gächter | Working paper CeDEx 2009-04 | nottingham.ac.uk/cedex/documents/papers/2009-04.pdf |
| Gächter y Marino Fages | Working paper IZA DP 16605 | docs.iza.org/dp16605.pdf |
| Isaac y Walker | Texto completo escaneado | econweb.ucsd.edu/~jandreon/Econ264/papers |
| Ashraf, Camerer y Loewenstein | Texto completo | andrew.cmu.edu/user/gl20 |
| Adam Smith, ambas obras | Texto completo | econlib.org/library/Smith |
| **Edmonds (SSC 2025)** | Solo abstract y referencias; cerrado en Springer | Conseguir por acceso institucional |
| **Cohen et al. (SSC 2025)** | Solo abstract y referencias; cerrado en Springer | Conseguir por acceso institucional |
| **Li y Wu** | Solo abstract; cerrado en Wiley | Conseguir por acceso institucional |
| **Sabato et al.** | Solo abstract; cerrado en IEEE | Prioridad baja |
| **Kořínek y Štekerová** | Solo abstract; el sitio bloquea descargas automáticas aunque figura como abierto | Abrir en el navegador: doi.org/10.4018/JCIT.398628 |

No se intentó el texto completo de los demás trabajos de §17.1.

---

## Apéndice B. Resumen de decisiones

| Elemento | Decisión |
|---|---|
| Sede | SSC 2027, full paper para proceedings; track de IA generativa y ABM si se repite |
| Encuadre | Auditoría de LLM como regla de decisión para ABM |
| Juego | PGG lineal, una ronda y repetido |
| Comparadores | Egoísta, cooperativo, recíproco, adaptativo, y hechos estilizados humanos |
| Factores centrales | Incentivo ($r/N$) y prompt (paráfrasis y framing) |
| Añadidos | Controles fuera del dilema, preguntas de comprensión, método de estrategia |
| Métrica central | Razón entre varianza explicada por incentivos y por redacción |
| Documentación | ODD, prerregistro, repositorio abierto |
| Parámetros base | $N=4$, dotación 20, $r/N$ en 0,3; 0,4; 0,5; 0,75, más controles en 0,2 y 1,25 |
| Encuadre conceptual | Nash y los dos Smith, en introducción y discusión (§3.1) |
| Riesgo principal | Solaparse con GAMA-Bench, Li y Shirado, Sreedhar et al. y Pal et al. |
| Diferenciación | Modelos actuales de varias familias, barrido de incentivos con controles fuera del dilema, separación de paráfrasis y framing, descomposición formal de varianza, comparación con datos humanos, lenguaje ABM |
| Paper mínimo viable | E0, E1 y E2 con dos modelos |
