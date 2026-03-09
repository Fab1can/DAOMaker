# Guida all'Utilizzo

## Requisiti

- Python 3.9 o superiore (la sintassi `list[Attribute]` richiede Python 3.9+)
- Nessuna dipendenza esterna

## Installazione

Non è richiesta alcuna installazione. È sufficiente clonare il repository:

```sh
git clone https://github.com/Fab1can/DAOMaker.git
cd DAOMaker
```

## Utilizzo

```sh
python main.py <nomefile> [nodao|repo]
```

### Parametri

| Parametro | Obbligatorio | Descrizione |
|-----------|--------------|-------------|
| `<nomefile>` | Sì | Percorso del file di input che descrive le tabelle |
| `nodao` | No | Genera solo DTO e file SQL, senza pattern DAO |
| `repo` | No | Genera DTO e classi Repository (implica `nodao`) |

> **Nota:** `nodao` e `repo` si escludono a vicenda. Se si specifica `repo`, il comportamento è quello di `nodao` ma con Repository al posto dei file SQL.

### Esempi di utilizzo

**Generazione del pattern DAO completo:**
```sh
python main.py esempio
```

**Generazione di soli DTO e SQL:**
```sh
python main.py esempio nodao
```

**Generazione di DTO e Repository:**
```sh
python main.py esempio repo
```

## Output

I file generati vengono salvati nella cartella `out/` nella directory corrente. Se la cartella esiste già, viene eliminata e ricreata ad ogni esecuzione.

### File generati in modalità DAO

Per ogni entità definita nel file di input:
- `<NomeEntità>DTO.java` — Il Data Transfer Object
- `<NomeEntità>DAO.java` — L'interfaccia DAO
- `Db2<NomeEntità>DAO.java` — L'implementazione DB2

Per ogni relazione molti-a-molti:
- `<NomePluraleEntità1><NomePluraleEntità2>MappingDAO.java` — Interfaccia DAO per la tabella di mapping
- `Db2<NomePluraleEntità1><NomePluraleEntità2>MappingDAO.java` — Implementazione DB2

File globali:
- `DAOFactory.java` — Factory astratta
- `Db2DAOFactory.java` — Implementazione DB2 della factory

### File generati in modalità `nodao`

Per ogni entità:
- `<NomeEntità>.java` — La classe Java (DTO)
- `<NomeEntità>.sql` — Script SQL (CREATE e DROP TABLE)

Per ogni relazione molti-a-molti:
- `<NomePluraleEntità1><NomePluraleEntità2>Mapping.sql` — Script SQL per la tabella di mapping

### File generati in modalità `repo`

Per ogni entità:
- `<NomeEntità>.java` — La classe Java (DTO)
- `<NomeEntità>Repository.java` — La classe Repository

Per ogni relazione molti-a-molti:
- `<NomePluraleEntità1><NomePluraleEntità2>MappingRepository.java` — Repository per la tabella di mapping

## Convenzioni sui Nomi

DAOMaker converte automaticamente i nomi scritti in `snake_case` nel formato Java corretto:

| Nome nel file | Java (camelCase) | Java (PascalCase) |
|---------------|-----------------|-------------------|
| `birth_date`  | `birthDate`     | `BirthDate`       |
| `owner`       | `owner`         | `Owner`           |
| `first_name`  | `firstName`     | `FirstName`       |

- I nomi degli attributi Java usano il formato **camelCase**
- I nomi delle classi e dei metodi usano il formato **PascalCase**
- I nomi delle colonne SQL usano il formato originale **snake_case** (o con `_id` per le chiavi esterne)
