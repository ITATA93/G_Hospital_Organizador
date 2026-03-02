---
id: DOC-URG-001
titulo: Estructura de Protocolos de Urgencias
proyecto: G_Hospital_Organizador
institucion: Hospital Provincial del Limari
servicio: Servicio de Urgencia
ultima_actualizacion: 2026-03-01
estado: borrador
depends_on:
  - config/folder_structure.yaml
impacts:
  - docs/knowledge_vault/README.md
  - docs/knowledge_vault/procesos_medicos/README.md
---

# Protocolos del Servicio de Urgencia

## Descripcion General

Este documento define la estructura organizativa de los protocolos del
Servicio de Urgencia del Hospital Provincial del Limari (Ovalle, Region de
Coquimbo). Los protocolos estan organizados segun la clasificacion de
emergencias y procesos criticos del servicio.

> **Nota**: Este archivo NO contiene los protocolos clinicos en si mismos,
> sino la estructura de organizacion documental para el sistema SAIA.
> Los protocolos originales residen en formato PDF/DOCX en la estructura
> de carpetas de la unidad.

## 1. Protocolo de Triage

### 1.1 Clasificacion

- **Nombre**: Protocolo de Triage Estructurado
- **Codigo**: PROT-URG-001
- **Sistema de referencia**: ESI (Emergency Severity Index) adaptado
- **Carpeta SAIA**: `Urgencia/2026/Protocolos/`

### 1.2 Categorias de Triage

| Nivel | Color | Descripcion | Tiempo maximo de atencion |
|-------|-------|-------------|---------------------------|
| C1 | Rojo | Riesgo vital inmediato | Inmediato (0 min) |
| C2 | Naranja | Emergencia | 15 minutos |
| C3 | Amarillo | Urgencia | 30 minutos |
| C4 | Verde | Urgencia menor | 60 minutos |
| C5 | Azul | No urgente | 120 minutos |

### 1.3 Documentos asociados

- Flujograma de triage (formato PDF)
- Planilla de registro de triage diario (formato XLSX)
- Manual de criterios de clasificacion (formato DOCX)

## 2. Codigo Azul (Paro Cardiorrespiratorio)

### 2.1 Clasificacion

- **Nombre**: Protocolo de Activacion Codigo Azul
- **Codigo**: PROT-URG-002
- **Referencia**: Guias AHA/ILCOR vigentes
- **Carpeta SAIA**: `Urgencia/2026/Protocolos/`

### 2.2 Componentes del protocolo

1. **Activacion**: Criterios de activacion del codigo azul
   - Paciente inconsciente sin respuesta
   - Ausencia de pulso carotideo
   - Apnea o respiracion agonica
2. **Respuesta**: Conformacion del equipo de reanimacion
   - Medico lider (Urgencia o UCI)
   - Enfermera de reanimacion
   - Tecnico paramedico (via aerea)
   - Tecnico paramedico (acceso vascular)
3. **Algoritmo**: Secuencia RCP segun ritmo
   - Ritmos desfibrilables (FV/TV sin pulso)
   - Ritmos no desfibrilables (Asistolia/AESP)
4. **Post-reanimacion**: Cuidados post-paro
5. **Registro**: Formulario Utstein de paro cardiaco

### 2.3 Documentos asociados

- Algoritmo de RCP imprimible (formato PDF)
- Checklist de carro de paro (formato XLSX)
- Formulario de registro Utstein (formato DOCX)

## 3. Codigo Rojo (Hemorragia Obstetrica / Trauma Mayor)

### 3.1 Clasificacion

- **Nombre**: Protocolo de Activacion Codigo Rojo
- **Codigo**: PROT-URG-003
- **Referencia**: Guia Perinatal MINSAL / ATLS
- **Carpeta SAIA**: `Urgencia/2026/Protocolos/`

### 3.2 Variantes

#### 3.2.1 Codigo Rojo Obstetrico

Activacion ante hemorragia obstetrica masiva (perdida estimada > 1000 mL
o inestabilidad hemodinamica).

- **Etapa 1**: Reanimacion inicial (cristaloides, acido tranexamico)
- **Etapa 2**: Transfusion masiva (protocolo con Banco de Sangre)
- **Etapa 3**: Intervencion quirurgica si no responde
- **Etapa 4**: Estabilizacion y derivacion a UCI si corresponde

#### 3.2.2 Codigo Rojo Trauma

Activacion ante trauma mayor con hemorragia activa.

- Evaluacion primaria ABCDE
- Control de hemorragia externa (torniquete, presion directa)
- Reanimacion con hemocomponentes (ratio 1:1:1)
- Evaluacion secundaria y estudios imagenologicos

### 3.3 Documentos asociados

- Flujograma Codigo Rojo Obstetrico (formato PDF)
- Flujograma Codigo Rojo Trauma (formato PDF)
- Checklist de activacion (formato DOCX)

## 4. Atencion al Politraumatizado

### 4.1 Clasificacion

- **Nombre**: Protocolo de Atencion al Paciente Politraumatizado
- **Codigo**: PROT-URG-004
- **Referencia**: ATLS (Advanced Trauma Life Support)
- **Carpeta SAIA**: `Urgencia/2026/Protocolos/`

### 4.2 Fases de atencion

1. **Evaluacion primaria (ABCDE)**
   - A: Via aerea con control cervical
   - B: Ventilacion y oxigenacion
   - C: Circulacion con control de hemorragia
   - D: Deficit neurologico (Glasgow, pupilas)
   - E: Exposicion y control de hipotermia
2. **Reanimacion simultanea**
   - Accesos vasculares (2 vias gruesas)
   - Fluidos y hemocomponentes
   - Monitoreo continuo
3. **Evaluacion secundaria**
   - Examen fisico completo cabeza a pies
   - Estudios complementarios (FAST, Rx, TAC)
4. **Tratamiento definitivo**
   - Manejo en sala o derivacion a centro de mayor complejidad
   - Contacto con SAMU / regulacion SSCoquimbo

### 4.3 Documentos asociados

- Hoja de registro de trauma (formato PDF)
- Escala de Glasgow imprimible (formato PDF)
- Checklist de evaluacion primaria (formato DOCX)

## 5. Protocolo de Intoxicaciones

### 5.1 Clasificacion

- **Nombre**: Protocolo de Manejo de Intoxicaciones Agudas
- **Codigo**: PROT-URG-005
- **Referencia**: CITUC (Centro de Informacion Toxicologica UC)
- **Carpeta SAIA**: `Urgencia/2026/Protocolos/`

### 5.2 Tipos de intoxicacion

| Tipo | Agentes frecuentes | Antidoto especifico |
|------|-------------------|---------------------|
| Medicamentosa | Paracetamol, benzodiazepinas, ISRS | N-acetilcisteina, flumazenil |
| Plaguicidas | Organofosforados, rodenticidas | Atropina, pralidoxima |
| Alcoholica | Etanol, metanol | Fomepizol / etanol IV |
| Corrosivos | Acidos, alcalis (limpiadores) | Sin neutralizacion, dilusion |
| Monoxido de carbono | CO (calefaccion, incendios) | Oxigeno al 100% |

### 5.3 Flujo de atencion

1. **Estabilizacion inicial**: ABCDE, monitorizacion
2. **Identificacion del toxico**: Anamnesis, envases, testigos
3. **Descontaminacion**: Lavado gastrico (si indicado), carbon activado
4. **Antidoto especifico**: Segun agente identificado
5. **Tratamiento de soporte**: UCI si Glasgow < 8 o falla organica
6. **Notificacion**: CITUC (fono 600 360 7777), SEREMI de Salud

### 5.4 Documentos asociados

- Tabla de antidotos disponibles en farmacia (formato XLSX)
- Flujograma de intoxicaciones (formato PDF)
- Formulario de notificacion SEREMI (formato DOCX)

## Estructura de Carpetas SAIA para Urgencia

```text
Urgencia/
  2026/
    Protocolos/
      PROT-URG-001_Triage.pdf
      PROT-URG-002_Codigo_Azul.pdf
      PROT-URG-003_Codigo_Rojo.pdf
      PROT-URG-004_Politraumatizado.pdf
      PROT-URG-005_Intoxicaciones.pdf
    Manuales/
      Manual_Servicio_Urgencia.docx
    Informes/
      Informe_Gestion_Mensual_URG.xlsx
    Actas/
      Acta_Comite_Urgencia_2026-01.docx
    Planillas/
      Registro_Triage_Diario.xlsx
      Dotacion_Turno_Urgencia.xlsx
```

## Referencias

- Guias Clinicas MINSAL (Ministerio de Salud de Chile)
- ATLS - American College of Surgeons, 10a edicion
- AHA Guidelines for CPR and ECC (2020, actualizado 2025)
- CITUC - Centro de Informacion Toxicologica, Universidad Catolica de Chile
- Norma Tecnica de Urgencia MINSAL (Decreto 2295/1995)
