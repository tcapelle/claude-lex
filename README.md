# claude-lex

An intelligent legal assistant built with Claude Code that helps draft contracts, legal documents, and provides access to Chilean legislation.

## Overview

This repository contains a set of Claude Skills that transform Claude Code into a specialized legal agent. It integrates with multiple legal databases and maintains a case management system to ensure consistent, professional legal work.

## Features

- **Chilean Legislation Access**: Query laws, decrees, and regulations from the Biblioteca del Congreso Nacional
- **Client Case Management**: Organized database of previous work to maintain consistent style and leverage past documents
- **International Legal Research**: Access to vLex APIs for global legal documents and text analysis
- **Document Drafting**: Generate legal documents based on templates from similar cases

## Available Skills

### 1. `/leychile` - Chilean Legislation Query

Access Chilean laws and regulations via SPARQL queries to the BCN database.

**Use when:**
- Searching for Chilean laws by keyword or topic
- Getting full text of specific laws by ID
- Looking up legal articles and provisions
- Researching regulatory requirements

**Examples:**
```
/leychile Busca leyes sobre protección de datos personales
/leychile Muéstrame el artículo 1545 del Código Civil
/leychile Qué dice el Código del Trabajo sobre vacaciones?
```

**Common Law IDs:**
- Constitución: 242302
- Código Civil: 172986
- Código Penal: 1984
- Código del Trabajo: 207436
- Ley de Protección de Datos (19.628): 141599

### 2. `/mis-documentos` - Case Database Manager

Manages the client/case database in the `mis_documentos/` directory.

**Use when:**
- Starting work on a new legal matter
- Creating documents or proposals
- Finding similar past cases for reference
- Maintaining consistent style across documents

**Workflow:**
1. Search for similar cases in the database
2. Review relevant past documents
3. Use as templates maintaining consistent style
4. Adapt content to new client/case

### 3. `/vlex` - International Legal APIs

Access vLex services for international legal research and document analysis.

**Use when:**
- Searching international legal documents
- Anonymizing documents (removing PII)
- Extracting legal citations from text
- Classifying documents by type/jurisdiction
- Analyzing key legal phrases

**Note:** Requires `VLEX_API_KEY` environment variable.

## Getting Started

### Prerequisites

- Claude Code CLI installed
- For vLex features: Set `VLEX_API_KEY` environment variable

### Usage

1. Navigate to this directory in Claude Code
2. The assistant automatically loads the configuration from `CLAUDE.md`
3. Use skills by typing `/skillname` or just ask questions naturally

### Mandatory Workflow

**IMPORTANT:** When starting any legal work, the assistant will:

1. Ask if you're working on an existing client/case or need a new folder
2. If existing: List available cases in `mis_documentos/` for you to choose
3. If new: Create a new case folder with proper structure
4. Then proceed with the requested work

This ensures all work is properly organized and documented.

## Directory Structure

```
claude-lex/
├── CLAUDE.md                    # Main agent instructions
├── README.md                    # This file
├── .claude/
│   ├── settings.local.json      # Permissions configuration
│   └── skills/
│       ├── leychile/            # Chilean legislation skill
│       ├── mis-documentos/      # Case management skill
│       └── vlex/                # vLex API skill
└── mis_documentos/              # Client/case database
    ├── README.md                # Case index
    └── [client folders]/        # Individual client cases
```

## Configuration

The `.claude/settings.local.json` file pre-approves certain operations for smoother workflow:
- Bash commands for curl, python3, tree, mkdir
- All skill invocations (leychile, mis-documentos, vlex)

## Examples

**Search Chilean labor law:**
```
What does the Código del Trabajo say about severance pay?
```

**Draft a contract:**
```
I need to draft a sales contract. Check if we have similar contracts in mis_documentos.
```

**Anonymize a document:**
```
Remove all personal information from this contract text: [paste text]
```

## Notes

- All Chilean legislation data comes from official BCN sources
- Laws are shown in their current consolidated version
- The assistant maintains your professional style by learning from past documents
- For specific legal advice, always consult with a qualified attorney

## Resources

- [Biblioteca del Congreso Nacional](https://www.bcn.cl/leychile/)
- [BCN Open Data Portal](https://datos.bcn.cl/es/)
- [vLex Developer Portal](https://developer.vlex.com)