# Modulo `main.py`

## Descrizione

`main.py` è il punto di ingresso di DAOMaker. Si occupa di:

1. Leggere e validare gli argomenti da riga di comando
2. Fare il parsing del file di input per costruire la struttura dati interna
3. Orchestrare la generazione dei file di output in base alla modalità selezionata

## Argomenti da Riga di Comando

```sh
python main.py <nomefile> [nodao|repo]
```

| Variabile | Valore |
|-----------|--------|
| `FILENAME` | `sys.argv[1]` — percorso del file di input |
| `NODAO` | `True` se è presente un secondo argomento (qualsiasi) |
| `REPO` | `True` se il secondo argomento è `"repo"` (case-insensitive) |

## Espressioni Regolari

Il parser usa quattro pattern regex per riconoscere i tipi di riga:

| Variabile | Pattern | Descrizione |
|-----------|---------|-------------|
| `CARATETRI_INIZIALI` | `[a-zàèìòùé]` | Caratteri validi come primo carattere di un nome |
| `ALTRI_CARATTERI` | `[a-z_0-9àèìòùé]` | Caratteri validi nei caratteri successivi di un nome |
| `PAROLA` | `CARATETRI_INIZIALI + ALTRI_CARATTERI + "*"` | Pattern completo per un nome valido |

I pattern completi usati nel parsing di ogni riga:

| Nome | Pattern | Tipo di riga riconosciuta |
|------|---------|--------------------------|
| `res_relation` | `^(PAROLA)(/(PAROLA)){0,1}$` | Dichiarazione di entità (con o senza plurale esplicito) |
| `res_attribute` | `^(PAROLA):(PAROLA)$` | Dichiarazione di attributo |
| `res_mappings` | `^(PAROLA)\*(PAROLA)$` | Relazione molti-a-molti |
| `res_empty` | `^$` | Riga vuota (ignorata) |

## Funzione `from_file(filename)`

### Scopo

Legge e fa il parsing del file di input, restituendo una lista di oggetti `Relation` e `Mapping` pronti per la generazione del codice.

### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `filename` | `str` | Percorso del file di input |

### Valore di Ritorno

`list` — Lista di oggetti `Relation` e `Mapping` nell'ordine in cui sono stati definiti nel file (le entità prima, le relazioni molti-a-molti in fondo).

### Logica di Parsing

Il parsing avviene riga per riga. Lo stato corrente è mantenuto dalla variabile `_relation` (nome dell'ultima entità incontrata):

1. **Riga entità** (`res_relation`): aggiunge l'entità al dizionario `_relations`, registra il plurale in `plurals`, aggiorna `_relation`
2. **Riga attributo** (`res_attribute`): aggiunge l'attributo all'entità corrente (`_relation`)
3. **Riga mapping** (`res_mappings`): registra la relazione molti-a-molti in `mappings` (bidirezionale) e `clean_mappings` (solo una direzione, usato per evitare duplicati)
4. **Riga vuota** (`res_empty`): ignorata
5. **Altro**: chiama `syntax_error()` e termina

### Costruzione degli Oggetti

Dopo il parsing, la funzione costruisce gli oggetti del modello:

**Per ogni entità in `_relations`:**

- Per ogni attributo, risolve il tipo stringa in un oggetto `Type`:
  - `"string"` → `Type("String", "VARCHAR(50)", "String")`
  - `"int"` → `Type("int", "INT", "Int")`
  - `"float"` → `Type("float", "FLOAT", "Float")`
  - `"boolean"` → `Type("boolean", "BOOL", "Boolean")`
  - `"date"` → `Type("Date", "DATE", "Date")`
  - Nome di un'altra entità → `Type(PascalCase, "INT NOT NULL REFERENCES tabella(id)", "Int", foreign=True)`
  - Altro → `Type(valore, VALORE, Valore[0].upper()+valore[1:])`
- Se l'entità ha relazioni molti-a-molti, aggiunge un attributo lista per ciascuna
- Crea l'oggetto `Relation(nome, plurale, attributi, NODAO)`

**Per ogni coppia in `clean_mappings`:**

- Crea un oggetto `Mapping(entità1, entità2, plurale1, plurale2)`

## Generazione dei File

I file vengono scritti nella cartella `out/`. Se esiste già, viene eliminata con `shutil.rmtree()` e ricreata con `os.mkdir()`.

### Modalità DAO (predefinita, `NODAO = False`)

```python
for relation in relations:
    if type(relation) is Relation:
        # <NomeEntità>DTO.java
    # <NomeEntità>DAO.java (anche per Mapping)
    # Db2<NomeEntità>DAO.java (anche per Mapping)
# DAOFactory.java
# Db2DAOFactory.java
```

### Modalità `nodao` (`NODAO = True`, `REPO = False`)

```python
for relation in relations:
    if type(relation) is Relation:
        # <NomeEntità>.java
        # <NomeEntità>.sql
```

### Modalità `repo` (`NODAO = True`, `REPO = True`)

```python
for relation in relations:
    if type(relation) is Relation:
        # <NomeEntità>.java
        # <NomeEntità>Repository.java
```

> **Nota:** In modalità `nodao` e `repo`, i file sono scritti con separatore di percorso `\\` (Windows). Su sistemi Unix potrebbe essere necessario adattare il codice.
