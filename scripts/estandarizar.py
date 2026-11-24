"""Agrega las columnas del estándar de comparación a data/soluciones.csv.

Uso:  python3 scripts/estandarizar.py ruta/al/portafolio_aster_soluciones.csv
Lee el CSV original (o el .xlsx, hoja Soluciones), clasifica cada solución con reglas
de palabras clave y escribe data/soluciones.csv. Si una fila ya trae un valor en una
columna estándar, se respeta (permite corregir a mano).
"""
import csv, re, sys, unicodedata, pathlib

def norm(s):
    s = unicodedata.normalize('NFD', str(s or '')).encode('ascii', 'ignore').decode().lower()
    return s

AREAS = [  # (nombre estándar, patrones sobre "Área que aplica")
    ('Mina y extracción', r'\bmina\b|minas|minera|minero|rajo|subterran|tunel|exploraci|movimiento de mineral|despacho|caex|\bcoi\b|\bcas\b|movimientos? de tierra|faena|terreno|^mineria$'),
    ('Planta y procesos', r'planta|concentrador|catodo|chancado|molienda|molino|\bsag\b|hidrocicl|clasificacion|espesador|filtro|area humeda|^seca$|separacion|fundicion|laminado|naves de proceso|pulpa|canaleta|bombeo|impulsion|calidad operacional|control de procesos'),
    ('Mantenimiento y activos', r'mantenimiento|mantencion|asset|taller|infraestructura|correa|cinta|ducto|montaje|construccion'),
    ('Logística y abastecimiento', r'logistic|transporte(?! gravitacional)|supply|bodega|procurement|combustible|abastecimiento|flota'),
    ('Seguridad y salud', r'seguridad|salud|\bsso\b|garita|proteccion de activos|alto riesgo'),
    ('Personas y gestión', r'personas|rrhh|recursos humanos|reclutamiento|capacitacion|entrenamiento|educacion|contrat|compliance|relaciones laborales|gestion mina|excelencia operacional|planificacion|gerencia|reportabilidad'),
    ('Medio ambiente, agua y energía', r'ambient|relave|hidric|agua|energia|\besg\b|sustentab|lixiviad|salmuera'),
]
KPIS = [  # sobre Tipo de KPI + Variable de Mejora + Métrica
    ('Seguridad', r'segur|accident|incident|fatalidad|exposicion|riesgo|siniestral|lesion|\bepp\b|\bctp\b|colision|intrusion|peligro|fatiga'),
    ('Disponibilidad y continuidad', r'disponib|continuidad|detencion|parada|mtbf|confiab|horas efectivas|falla|indisponib|utilizacion'),
    ('Productividad y producción', r'productiv|produccion|\btph\b|throughput|tonelad|\boee\b|ciclo|rendimiento|eficiencia|\bcolas?\b|demora'),
    ('Costos y valor económico', r'costo|ahorro|financier|opex|economic|utilidad|margen|retorno|valoriz|usd|ingreso|perdida'),
    ('Calidad y recuperación', r'recuperacion|calidad|defecto|reproceso|precision|pureza|clasificacion|fpy|merma|estandar|error'),
    ('Energía y emisiones', r'energ|kwh|co2|co₂|emision|diesel|combustible|carbono|huella'),
    ('Agua y residuos', r'agua|hidric|residuo|reuso|relave|ambiental|patio'),
    ('Gestión, tiempo y cumplimiento', r'tiempo|trazabilidad|cumplimiento|normativ|compliance|auditoria|planificacion|reclutamiento|gestion|coordinacion|respuesta'),
    ('Personas y bienestar', r'ausentismo|rotacion|aprendizaje|capacitacion|entrenamiento|bienestar|licencias|personal|mano de obra'),
]
TECH = [  # sobre Descripción Técnica / Solución
    ('Inteligencia artificial y analítica', r'\bia\b|inteligencia artificial|machine learning|aprendizaje automatico|modelo[s]? predictiv|algoritm|\bnlp\b|analitica|predictiv|big data|deep learning|redes neuronales'),
    ('Visión computacional e imágenes', r'vision (artificial|computacional)|camara|imagen|video|fotogra|escaneo|lidar|3d|termograf'),
    ('Sensores e IoT', r'sensor|iot|telemetr|tiempo real|monitoreo|dispositivo|gps|wearable|radar|rfid|medicion|instrument|uwb|triangulacion|supervision|anomalia'),
    ('Software y plataformas', r'plataforma|software|saas|\bapp\b|aplicacion|dashboard|digital|web|nube|sistema de gestion|gemelo|online|tablero|sistema unico'),
    ('Realidad virtual y simulación', r'realidad virtual|\bvr\b|realidad aumentada|simulador|simulacion|inmersiv'),
    ('Drones y robótica', r'dron|robot|autonom'),
    ('Ingeniería, materiales y química', r'material|recubrimiento|quimic|reactivo|polimer|mecanic|hidraulic|equipo|dispositivo fisico|revestimiento|aditivo|filtro|biolog|tratamiento|filtracion'),
]
STD_COLS = ['Área estándar', 'KPI estándar', 'Tecnología', 'Evidencia de impacto']

def classify(text, rules, fallback):
    t = norm(text)
    out = [name for name, pat in rules if re.search(pat, t)]
    return out or [fallback]

def evidence(r):
    m = (r.get('Métrica de Impacto Cuantitativa') or '').strip()
    b = (r.get('Línea Base') or '').strip()
    pts = 0
    if m: pts += 2 if re.search(r'\d', m) else 1
    if b and not re.match(r'(?i)(no aplica|sin |n/?a$|-$)', b): pts += 1
    return 'Alta' if pts >= 3 else 'Media' if pts == 2 else 'Baja'

def load(path):
    p = pathlib.Path(path)
    if p.suffix.lower() in ('.xlsx', '.xls'):
        import pandas as pd
        return pd.read_excel(p, 'Soluciones').fillna('').astype(str).to_dict('records')
    with open(p, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def main(src, dst):
    rows = load(src)
    for r in rows:
        auto = {
            'Área estándar': classify(r.get('Área que aplica'), AREAS, 'Transversal'),
            'KPI estándar': classify(' '.join(r.get(k, '') for k in ('Tipo de KPI Impactado', 'Variable de Mejora', 'Métrica de Impacto Cuantitativa')), KPIS, 'Otro'),
            'Tecnología': classify(r.get('Descripción Técnica / Solución'), TECH, 'No especificada'),
            'Evidencia de impacto': [evidence(r)],
        }
        for c in STD_COLS:
            if not (r.get(c) or '').strip():
                r[c] = '; '.join(auto[c])
    cols = list(rows[0].keys())
    for c in STD_COLS:
        if c not in cols: cols.append(c)
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} soluciones -> {dst}')

if __name__ == '__main__':
    here = pathlib.Path(__file__).resolve().parent.parent
    main(sys.argv[1] if len(sys.argv) > 1 else here / 'data' / 'soluciones.csv', here / 'data' / 'soluciones.csv')
