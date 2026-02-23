# [METHOD] [PATH]

**Fecha de creación:** YYYY-MM-DD  
**Última actualización:** YYYY-MM-DD

## Descripción

Breve descripción de qué hace este endpoint.

## Autenticación

- [ ] Requiere autenticación
- [ ] Requiere rol: [role_name]

## Request

### Headers
```
Authorization: Bearer {token}
Content-Type: application/json
```

### Body
```json
{
  "field1": "string",
  "field2": "number",
  "field3": "boolean"
}
```

### Query Parameters
| Parámetro | Tipo | Requerido | Descripción |
|-----------|------|-----------|-------------|
| `page` | number | No | Número de página (default: 1) |
| `limit` | number | No | Items por página (default: 10) |

## Response

### Success (200)
```json
{
  "id": "uuid",
  "field1": "string",
  "created_at": "2026-02-02T12:00:00Z"
}
```

### Error (400)
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Ejemplo

### cURL
```bash
curl -X POST http://localhost:3000/api/endpoint \\
  -H "Authorization: Bearer token" \\
  -H "Content-Type: application/json" \\
  -d '{
    "field1": "value"
  }'
```

### JavaScript
```javascript
const response = await fetch('/api/endpoint', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ field1: 'value' })
});
```

## Notas

- Nota importante 1
- Consideración especial 2
