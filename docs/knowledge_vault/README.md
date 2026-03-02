---
id: IDX-ROOT-001
titulo: Knowledge Vault Index
proyecto: G_Hospital_Organizador
institucion: Hospital Provincial del Limari
ultima_actualizacion: 2026-03-01
depends_on: []
impacts:
  - docs/protocolos_urgencias.md
  - docs/arquitectura_his.md
---

# Knowledge Vault - Hospital Provincial del Limari

> Boveda de Conocimiento Estructurada para Documentacion de Alta Densidad.
> Sistema SAIA (Sistema de Apoyo Integral de Archivos).

Este directorio sigue el patron **Knowledge Vault**: descomponer la complejidad
del Hospital en atomos de informacion navegables. Cada archivo documenta un tema
unico con frontmatter YAML para trazabilidad.

## Mapa de Navegacion

### [Infraestructura](./infraestructura/README.md)

Planos, redes, equipamiento fisico y mantenimiento edilicio del hospital.

- Planos arquitectonicos y de instalaciones
- Inventario de redes y cableado estructurado
- Equipamiento biomedico

### [Procesos Medicos](./procesos_medicos/README.md)

Protocolos clinicos, guias de practica, flujos de urgencias y hospitalizacion.

- Protocolos de urgencias (Triage, Codigo Azul, Codigo Rojo)
- Guias de practica clinica por servicio
- Flujos de hospitalizacion y alta

### [Administracion](./administracion/README.md)

Recursos humanos, legal, facturacion y gestion administrativa.

- Estructura organizacional y dotacion
- Procesos de abastecimiento y compras publicas
- Normativa interna y reglamentos

### [Sistemas](./sistemas/README.md)

Documentacion tecnica del HIS, integraciones, redes y software.

- Arquitectura HIS (TrakCare, SIDRA, ALMA)
- Integraciones HL7/FHIR
- Infraestructura TI y seguridad informatica

### [Normativa](./normativa/README.md)

Marco regulatorio aplicable al establecimiento.

- Normativa MINSAL y Servicio de Salud Coquimbo
- Leyes de transparencia y datos personales
- Estandares de acreditacion

### [Calidad](./calidad/README.md)

Gestion de calidad, seguridad del paciente e IAAS.

- Indicadores de calidad asistencial
- Eventos adversos y gestion de riesgos
- Comites de calidad y acreditacion

## Estructura de Archivos

```text
knowledge_vault/
  README.md                    # Este indice
  infraestructura/
    README.md                  # Indice de infraestructura
    planos/
    inventario_redes/
  procesos_medicos/
    README.md                  # Indice de procesos medicos
    urgencias/
    hospitalizacion/
  administracion/
    README.md                  # Indice de administracion
  sistemas/
    README.md                  # Indice de sistemas TI
  normativa/
    README.md                  # Indice de normativa
  calidad/
    README.md                  # Indice de calidad
```

## Reglas de Contribucion

1. **Atomicidad**: Un archivo = Un tema.
2. **Frontmatter**: Todo archivo debe tener metadatos YAML (id, titulo, fecha).
3. **Indices**: Actualizar este mapa al crear nuevas carpetas principales.
4. **Idioma**: Contenido clinico y administrativo en espanol.
5. **No RCE**: Este vault NO contiene registros clinicos electronicos
   ni datos de pacientes. Solo documentacion administrativa y de procesos.
