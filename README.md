# Portafolio Open Aster

Vista dinámica de las soluciones de las empresas del portafolio de Aster Aceleradora (1era a 8va expedición).

**Ver el sitio:** se publica con GitHub Pages desde la rama `main`.

## Qué tiene

- **Soluciones**: tarjetas con filtros por expedición, empresa, área, KPI, tecnología, categoría y nivel de evidencia.
- **Comparar por categorías**: matriz que cruza dos dimensiones del estándar (por ejemplo KPI × Categoría) y cuenta soluciones o empresas; al hacer clic en una celda se ven cuáles son.
- **Empresas**: tabla ordenable con una ficha estándar por empresa.
- **Comparación lado a lado** de 2 a 4 soluciones o empresas, marcando lo que tienen en común.

## El estándar de comparación

Cada solución se clasifica en listas cerradas para poder compararlas:

| Columna | Qué es |
|---|---|
| Área estándar | 7 áreas de la operación (Mina y extracción, Planta y procesos, Mantenimiento y activos, Logística y abastecimiento, Seguridad y salud, Personas y gestión, Medio ambiente/agua/energía), a partir de "Área que aplica". |
| KPI estándar | 9 familias de indicador (Seguridad, Disponibilidad y continuidad, Productividad y producción, Costos y valor económico, Calidad y recuperación, Energía y emisiones, Agua y residuos, Gestión/tiempo/cumplimiento, Personas y bienestar), a partir de "Tipo de KPI", "Variable de Mejora" y la métrica. |
| Tecnología | Base tecnológica leída de la "Descripción Técnica". |
| Evidencia de impacto | Alta: métrica con cifras y línea base. Media: métrica con cifras sin línea base. Baja: sin métrica cuantitativa. |

Las columnas se generan con `scripts/estandarizar.py` (reglas por palabras clave). Si una clasificación no te convence, corrige la celda a mano en el CSV: el script respeta los valores que ya existen.

- Búsqueda de texto en todos los campos (sin importar tildes ni mayúsculas).
- Ficha de detalle por solución con los 8 campos: Variable de Mejora, Área que aplica, Problema que Resuelve, Descripción Técnica / Solución, Beneficios, Tipo de KPI Impactado, Métrica de Impacto Cuantitativa y Línea Base.
- La URL guarda los filtros y la ficha abierta, así que se puede compartir una vista filtrada.

## Cómo actualizar los datos

El sitio lee `data/soluciones.csv`. Para actualizarlo:

1. Exporta la hoja "Soluciones" del Excel como CSV UTF-8 (mismas columnas).
2. Genera las columnas del estándar: `python3 scripts/estandarizar.py ruta/al/archivo.csv` (escribe `data/soluciones.csv`; también acepta el `.xlsx`).
3. Haz commit. No hay que tocar el HTML.

Columnas esperadas: `Expedición, Empresa, Categoría (sitio), Sitio web, Solución, Variable de Mejora, Área que aplica, Problema que Resuelve, Descripción Técnica / Solución, Beneficios, Tipo de KPI Impactado, Métrica de Impacto Cuantitativa, Línea Base, Ficha en Aster, Nota`, más las 4 del estándar: `Área estándar, KPI estándar, Tecnología, Evidencia de impacto`.

## Verlo en tu computador

Abrir `index.html` directo con doble clic no carga el CSV (el navegador lo bloquea). Usa un servidor local:

```
python3 -m http.server
```

y abre http://localhost:8000.

Fuente: fichas públicas de asteraceleradora.com.
