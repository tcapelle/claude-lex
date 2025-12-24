---
name: leychile
description: Queries Chilean legislation from the Biblioteca del Congreso Nacional using SPARQL. Use when searching for Chilean laws, decrees, regulations, congressional information, or when user mentions specific Chilean legal codes.
---

# Ley Chile API Skill

Use this skill to query Chilean legislation from the Biblioteca del Congreso Nacional (BCN).

## Overview

This is a **free, public API** - no authentication required. It provides access to Chilean laws, decrees, regulations, legal norms, and congressional information.

## Primary API: SPARQL Endpoint

The main data access method is via the SPARQL endpoint at `https://datos.bcn.cl/sparql`.

### Basic Query Structure

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=YOUR_SPARQL_QUERY" \
  -H "Accept: application/json"
```

### Example 1: Search for Law Projects

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bcn: <http://datos.bcn.cl/ontologies/bcn-resources#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?proyecto ?label
WHERE {
  ?proyecto a bcn:ProyectoDeLey .
  OPTIONAL { ?proyecto rdfs:label ?label }
}
LIMIT 10" \
  -H "Accept: application/json"
```

### Example 2: Search Law Projects by Keyword

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bcn: <http://datos.bcn.cl/ontologies/bcn-resources#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?proyecto ?label
WHERE {
  ?proyecto a bcn:ProyectoDeLey .
  ?proyecto rdfs:label ?label .
  FILTER(CONTAINS(LCASE(?label), 'trabajo'))
}
LIMIT 10" \
  -H "Accept: application/json"
```

### Example 3: Get Parliamentary Sessions

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX congress: <http://datos.bcn.cl/ontologies/bcn-congress#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sesion ?label
WHERE {
  ?sesion a congress:SesionParlamentaria .
  OPTIONAL { ?sesion rdfs:label ?label }
}
LIMIT 10" \
  -H "Accept: application/json"
```

### Example 4: Get Senators and Deputies

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bio: <http://datos.bcn.cl/ontologies/bcn-biographies#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?persona ?nombre
WHERE {
  { ?persona a bio:Senador } UNION { ?persona a bio:Diputado }
  OPTIONAL { ?persona rdfs:label ?nombre }
}
LIMIT 20" \
  -H "Accept: application/json"
```

### Example 5: List All Available Entity Types

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=SELECT DISTINCT ?type WHERE { ?s a ?type . FILTER(CONTAINS(STR(?type), 'bcn')) } LIMIT 100" \
  -H "Accept: application/json"
```

## Available Ontologies/Namespaces

| Prefix | Namespace | Description |
|--------|-----------|-------------|
| bcn-resources | `http://datos.bcn.cl/ontologies/bcn-resources#` | Legislative resources (ProyectoDeLey, Articulo) |
| bcn-congress | `http://datos.bcn.cl/ontologies/bcn-congress#` | Congressional entities (sessions, commissions) |
| bcn-biographies | `http://datos.bcn.cl/ontologies/bcn-biographies#` | Biographies (Senador, Diputado, Alcalde) |
| bcn-norms | `http://datos.bcn.cl/ontologies/bcn-norms#` | Norms and governmental organizations |

## Key Entity Types

### Legislative Resources (bcn-resources)
- `ProyectoDeLey` - Law projects/bills
- `Articulo` - Articles
- `MocionParlamentaria` - Parliamentary motions
- `InformeDeComision` - Commission reports
- `VotacionProyectoDeLey` - Bill votes

### Congressional (bcn-congress)
- `SesionParlamentaria` - Parliamentary sessions
- `ComisionParlamentaria` - Parliamentary commissions
- `Legislatura` - Legislature terms

### Biographies (bcn-biographies)
- `Senador` - Senator
- `Diputado` - Deputy
- `Presidente` - President

## Web Navigation

For browsing individual laws by ID:
```
https://www.leychile.cl/Navegar?idNorma={ID_NORMA}
```

Historical version:
```
https://www.leychile.cl/Navegar?idNorma={ID_NORMA}&idVersion={YYYY-MM-DD}
```

## Common Law IDs (idNorma)

| Law | idNorma | Description |
|-----|---------|-------------|
| Constitucion | 242302 | Constitution of Chile |
| Codigo Civil | 172986 | Civil Code |
| Codigo Penal | 1984 | Penal Code |
| Codigo del Trabajo | 207436 | Labor Code |
| Ley de Proteccion de Datos | 141599 | Data Protection Law (19.628) |

## Response Format

SPARQL returns JSON with structure:
```json
{
  "head": { "vars": ["var1", "var2"] },
  "results": {
    "bindings": [
      { "var1": { "type": "uri", "value": "..." } }
    ]
  }
}
```

## Reference

- Main Portal: https://www.bcn.cl/leychile/
- Open Data: https://datos.bcn.cl/es/
- SPARQL Endpoint: https://datos.bcn.cl/sparql
