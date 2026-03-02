---
id: DOC-SIS-001
titulo: Arquitectura del Sistema de Informacion Hospitalario (HIS)
proyecto: G_Hospital_Organizador
institucion: Hospital Provincial del Limari
ultima_actualizacion: 2026-03-01
estado: borrador
depends_on:
  - config/folder_structure.yaml
impacts:
  - docs/knowledge_vault/README.md
  - docs/knowledge_vault/sistemas/README.md
---

# Arquitectura del Sistema de Informacion Hospitalario (HIS)

## 1. Vision General

El Hospital Provincial del Limari opera con un ecosistema de sistemas de
informacion en salud interconectados, bajo la gobernanza del Servicio de
Salud Coquimbo y el Ministerio de Salud de Chile (MINSAL). Este documento
describe la arquitectura de alto nivel, los componentes principales y las
integraciones entre sistemas.

```text
+------------------------------------------------------------------+
|                    MINSAL / Servicio de Salud                     |
|   SIDRA    SIGFE    SINAISO    REM    DEIS    ChileCompra        |
+------+-------+--------+--------+-------+--------+---------------+
       |       |        |        |       |        |
       v       v        v        v       v        v
+------------------------------------------------------------------+
|              Hospital Provincial del Limari                       |
|                                                                  |
|  +------------------+    +------------------+                    |
|  |    TrakCare      |    |      ALMA        |                    |
|  |  (HIS Principal) |<-->|  (Gestion Hosp.) |                    |
|  +--------+---------+    +--------+---------+                    |
|           |                       |                              |
|     +-----+-----+          +-----+-----+                        |
|     |           |          |           |                         |
|  +--v---+  +----v----+  +-v------+  +-v------+                  |
|  | RIS/ |  |   LIS   |  |Farmacia|  |  RRHH  |                  |
|  | PACS |  |         |  |        |  |        |                  |
|  +------+  +---------+  +--------+  +--------+                  |
|                                                                  |
|  +------------------+    +------------------+                    |
|  | Red de Datos     |    | Seguridad TI     |                    |
|  | (LAN/WAN/VPN)    |    | (Firewall/AD)    |                    |
|  +------------------+    +------------------+                    |
+------------------------------------------------------------------+
```

## 2. Sistemas Principales

### 2.1 TrakCare (InterSystems IRIS)

**Funcion**: Sistema HIS (Hospital Information System) principal.
Registro clinico electronico, agendamiento, admision y gestion de camas.

| Atributo | Valor |
|----------|-------|
| Proveedor | InterSystems |
| Plataforma | IRIS for Health |
| Despliegue | Servidor central SSCoquimbo |
| Protocolo de integracion | HL7 v2.5, REST/JSON |
| Modulos activos | ADT, ORM, ORU, Agendamiento, Farmacia clinica |

**Modulos en uso**:

- **ADT** (Admision, Descarga, Transferencia): Gestion de episodios
  clinicos, admision de urgencia y hospitalizacion.
- **Agendamiento**: Citas de consulta externa y procedimientos.
- **Farmacia clinica**: Prescripcion electronica y dispensacion.
- **Solicitudes (ORM)**: Ordenes de laboratorio e imagenologia.
- **Resultados (ORU)**: Recepcion de resultados de laboratorio.

**Datos que maneja**: Registros clinicos, fichas de pacientes,
epicrisis, indicaciones medicas, interconsultas.

> **Nota SAIA**: TrakCare NO es parte del alcance del sistema de
> organizacion documental. SAIA solo organiza documentos administrativos.

### 2.2 SIDRA (Sistema de Informacion de la Red Asistencial)

**Funcion**: Plataforma MINSAL para gestion de listas de espera,
derivaciones y regulacion de camas a nivel de red.

| Atributo | Valor |
|----------|-------|
| Proveedor | MINSAL / DTIC |
| Plataforma | Web (navegador) |
| Despliegue | Nube MINSAL |
| Integracion | Manual + HL7 via motor de integracion |

**Modulos relevantes**:

- **Listas de espera**: LEQ (quirurgica), LEN (nueva especialidad),
  LEIC (imagenes y procedimientos).
- **Regulacion de camas**: Solicitudes de traslado entre establecimientos.
- **GES/AUGE**: Seguimiento de garantias explicitas en salud.

### 2.3 ALMA (Sistema de Gestion Hospitalaria)

**Funcion**: ERP hospitalario para gestion administrativa: bodega,
abastecimiento, activo fijo, farmacia (stock).

| Atributo | Valor |
|----------|-------|
| Proveedor | MINSAL / empresa adjudicada |
| Plataforma | Web |
| Despliegue | Servidor local + enlace MINSAL |
| Integracion | Webservices SOAP / CSV |

**Modulos relevantes**:

- **Bodega central**: Control de stock y despacho a centros de costo.
- **Farmacia (stock)**: Inventario de medicamentos e insumos.
- **Activo fijo**: Registro de equipamiento biomedico.
- **Abastecimiento**: Ordenes de compra y recepcion de mercaderia.

### 2.4 RIS/PACS (Imagenologia)

**Funcion**: Gestion de solicitudes y almacenamiento de imagenes
diagnosticas (radiologia, ecografia, TAC).

| Atributo | Valor |
|----------|-------|
| Componente | RIS (Radiology Information System) + PACS (Picture Archiving) |
| Estandar | DICOM 3.0, HL7 ORM/ORU |
| Almacenamiento | Servidor PACS local + respaldo en nube SSCoquimbo |
| Visor | Visor web integrado con TrakCare |

**Flujo**:

1. Medico genera solicitud en TrakCare (HL7 ORM)
2. RIS recibe la solicitud y agenda el estudio
3. Tecnologo realiza el examen, imagen se almacena en PACS
4. Radiologo informa via RIS
5. Informe retorna a TrakCare (HL7 ORU)

### 2.5 LIS (Sistema de Informacion de Laboratorio)

**Funcion**: Gestion del flujo de trabajo del laboratorio clinico,
desde la solicitud hasta la entrega de resultados.

| Atributo | Valor |
|----------|-------|
| Integracion | HL7 v2.5 (ORM/ORU) con TrakCare |
| Analizadores | Interfaz bidireccional con equipos automatizados |
| Banco de Sangre | Modulo de hemoterapia y trazabilidad de hemocomponentes |

**Flujo**:

1. Medico genera solicitud en TrakCare (HL7 ORM)
2. LIS recibe y asigna codigo de barras a muestra
3. Muestra procesada por analizador automatizado
4. Tecnologo valida resultados
5. Resultados validados retornan a TrakCare (HL7 ORU)

## 3. Integraciones

### 3.1 HL7 v2.x

El protocolo principal de integracion entre sistemas clinicos es HL7
version 2.5. Los mensajes se transportan via TCP/IP (MLLP).

| Mensaje | Origen | Destino | Contenido |
|---------|--------|---------|-----------|
| ADT^A01 | TrakCare | SIDRA, LIS, RIS | Admision de paciente |
| ADT^A03 | TrakCare | SIDRA, LIS, RIS | Alta de paciente |
| ORM^O01 | TrakCare | LIS, RIS | Solicitud de examen |
| ORU^R01 | LIS, RIS | TrakCare | Resultado de examen |
| SIU^S12 | TrakCare | SIDRA | Agendamiento de cita |

### 3.2 Motor de Integracion

El Servicio de Salud Coquimbo opera un motor de integracion (Integration
Engine) basado en InterSystems HealthShare que enruta los mensajes HL7
entre los establecimientos de la red.

```text
TrakCare <--HL7/MLLP--> HealthShare <--HL7/MLLP--> LIS
                              |
                              +----HL7/MLLP--> RIS/PACS
                              |
                              +----REST/JSON--> SIDRA (MINSAL)
                              |
                              +----SOAP/XML---> ALMA
```

### 3.3 Integraciones Administrativas

| Sistema externo | Protocolo | Datos intercambiados |
|-----------------|-----------|----------------------|
| SIGFE (Finanzas) | CSV / Webservice | Presupuesto, ejecucion |
| ChileCompra (Mercado Publico) | API REST | Ordenes de compra, licitaciones |
| SINAISO (Indicadores) | Web manual | Indicadores hospitalarios |
| REM (Estadistica) | CSV upload | Registros estadisticos mensuales |
| DEIS (Demografico) | CSV upload | Egresos hospitalarios |

## 4. Infraestructura de Red

### 4.1 Red Local (LAN)

- Cableado estructurado Cat 6A
- Switches core: Cisco / HP ProCurve
- VLANs segmentadas: Clinica, Administrativa, Invitados, Servidores
- WiFi: Red corporativa (802.1X) + red invitados

### 4.2 Conectividad WAN

- Enlace dedicado al Servicio de Salud Coquimbo (fibra optica)
- VPN site-to-site para acceso a sistemas MINSAL
- Internet dedicado para servicios en nube

### 4.3 Seguridad

- Firewall perimetral (Fortinet / Sophos)
- Active Directory para autenticacion centralizada
- Antivirus corporativo (endpoints)
- Backup automatizado diario (NAS local + nube)
- Politica de acceso basada en roles (RBAC)

## 5. Diagrama de Flujo de Datos

```text
Paciente llega
      |
      v
[Admision] --ADT^A01--> TrakCare --ADT--> SIDRA
      |
      v
[Atencion Clinica]
      |
      +-- Solicita Lab ---ORM^O01---> LIS
      |                                |
      |                          ORU^R01 (resultado)
      |                                |
      +-- Solicita Imagen -ORM^O01-> RIS/PACS
      |                                |
      |                          ORU^R01 (informe)
      |                                |
      +-- Prescribe --------> Farmacia clinica (TrakCare)
      |                                |
      |                          Dispensacion (ALMA stock)
      |
      v
[Alta] --ADT^A03--> TrakCare --ADT--> SIDRA
      |
      v
[Epicrisis + Estadistica] --> REM / DEIS
```

## 6. Relacion con SAIA

El sistema SAIA (Sistema de Apoyo Integral de Archivos) NO interactua
directamente con los sistemas clinicos descritos arriba. SAIA organiza
exclusivamente la **documentacion administrativa** que estos sistemas
generan como salida indirecta:

- **Informes de gestion** exportados desde SIDRA/ALMA
- **Resoluciones** de la direccion del hospital
- **Actas de comite** donde se revisan indicadores de los sistemas
- **Protocolos** que documentan los flujos de trabajo con cada sistema
- **Planillas** de seguimiento manual complementario

La relacion es de lectura y archivo, nunca de escritura hacia los
sistemas clinicos.

## 7. Referencias

- InterSystems TrakCare Documentation
- HL7 v2.5 Implementation Guide (hl7.org)
- MINSAL - Departamento de Tecnologias de Informacion y Comunicaciones
- Servicio de Salud Coquimbo - Unidad de Informatica
- IHE (Integrating the Healthcare Enterprise) - Perfiles de integracion
