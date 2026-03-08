# Modulo `mapping.py`

## Descrizione

Il modulo `mapping.py` definisce la classe `Mapping`, che rappresenta una relazione **molti-a-molti** tra due entità. Genera il codice Java per le tabelle di mapping (tabelle di associazione), sia come interfaccia DAO che come implementazione DB2, Repository o script SQL.

## Classe `Mapping`

### Costruttore

```python
Mapping(relation1, relation2, plural_relation1, plural_relation2)
```

### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `relation1` | `str` | Nome della prima entità in `snake_case` |
| `relation2` | `str` | Nome della seconda entità in `snake_case` |
| `plural_relation1` | `str` | Forma plurale del nome della prima entità (nome della tabella SQL) |
| `plural_relation2` | `str` | Forma plurale del nome della seconda entità (nome della tabella SQL) |

### Attributi

| Attributo | Descrizione |
|-----------|-------------|
| `self.relation1` | Nome della prima entità |
| `self.relation2` | Nome della seconda entità |
| `self.plural_relation1` | Plurale della prima entità |
| `self.plural_relation2` | Plurale della seconda entità |

---

## Metodi

### `java_name(extra="Mapping")`

```python
def java_name(self, extra: str = "Mapping") -> str
```

Restituisce il nome Java base del mapping, ottenuto concatenando i nomi plurali in **PascalCase** con il suffisso `extra`.

#### Parametri

| Parametro | Tipo | Default | Descrizione |
|-----------|------|---------|-------------|
| `extra` | `str` | `"Mapping"` | Suffisso da aggiungere al nome |

#### Esempio

Per `Mapping("cow", "field", "cows", "fields")`:
- `java_name()` → `"CowsFieldsMapping"`
- `java_name("DAO")` → `"CowsFieldsMappingDAO"`

---

### `getDAO()`

```python
def getDAO(self) -> str
```

Genera il contenuto del file `<Nome>MappingDAO.java`: l'**interfaccia DAO** per la tabella di mapping.

#### Metodi nell'interfaccia

| Metodo | Descrizione |
|--------|-------------|
| `create(int idEntità1, int idEntità2)` | Inserisce una associazione |
| `delete(int idEntità1, int idEntità2)` | Elimina un'associazione |
| `createTable()` | Crea la tabella di mapping |
| `dropTable()` | Elimina la tabella di mapping |

> **Nota:** Le operazioni di lettura non sono incluse nell'interfaccia di base; sono implementate nella classe DB2 come query statiche.

---

### `getDb2DAO()`

```python
def getDb2DAO(self) -> str
```

Genera il contenuto del file `Db2<Nome>MappingDAO.java`: l'**implementazione DB2** del mapping DAO.

#### Struttura del file generato

1. **Costanti** — Nomi delle tabelle e delle colonne:
   - `TABLE` — Nome della tabella di mapping (es. `"cows_fields"`)
   - `TABLE_1` — Nome della prima tabella (es. `"cows"`)
   - `TABLE_2` — Nome della seconda tabella (es. `"fields"`)
   - `ID_1` — Nome della prima colonna chiave esterna (es. `"cow_id"`)
   - `ID_2` — Nome della seconda colonna chiave esterna (es. `"field_id"`)

2. **Statement SQL**:
   - `insert` — Inserimento di un'associazione
   - `read_by_ids` — Lettura per entrambe le chiavi
   - `read_by_<id1>` — Lettura di tutti i record associati alla prima entità (con JOIN sulla seconda tabella)
   - `read_by_<id2>` — Lettura di tutti i record associati alla seconda entità (con JOIN sulla prima tabella)
   - `read_all` — Lettura di tutti i record
   - `delete` — Cancellazione per entrambe le chiavi
   - `create` — Creazione della tabella con chiavi primarie composite e vincoli di integrità referenziale con `ON DELETE CASCADE`
   - `drop` — Eliminazione della tabella

3. **Implementazione dei metodi**:
   - `create(int id1, int id2)` — Inserisce l'associazione usando `PreparedStatement`
   - `delete(int id1, int id2)` — Elimina l'associazione
   - `createTable()` — Esegue la query `create`
   - `dropTable()` — Esegue la query `drop`

#### Schema della tabella generata

```sql
CREATE TABLE plurale1_plurale2 (
    entità1_id INT NOT NULL,
    entità2_id INT NOT NULL,
    PRIMARY KEY (entità1_id, entità2_id),
    FOREIGN KEY (entità1_id) REFERENCES plurale1(id) ON DELETE CASCADE,
    FOREIGN KEY (entità2_id) REFERENCES plurale2(id) ON DELETE CASCADE
)
```

---

### `getRepo()`

```python
def getRepo(self) -> str
```

Genera il contenuto del file `<Nome>MappingRepository.java`: la **classe Repository** per la tabella di mapping (alternativa alla modalità DAO).

La struttura è analoga a `getDb2DAO()`, ma:
- Usa `DataSource` invece di `Db2DAOFactory`
- I metodi lanciano `PersistenceException`
- Il metodo di inserimento si chiama `persist()` invece di `create()`
- Riferisce le classi Repository delle entità collegate invece dei DAO DB2

---

### `getCreateDrop()`

```python
def getCreateDrop(self) -> str
```

Genera il contenuto del file SQL con le istruzioni `CREATE TABLE` e `DROP TABLE` per la tabella di mapping.

#### Formato

```sql
CREATE TABLE plurale1_plurale2 ( entità1_id INT NOT NULL, entità2_id INT NOT NULL, PRIMARY KEY ( entità1_id, entità2_id ), FOREIGN KEY ( entità1_id ) REFERENCES plurale1(id) ON DELETE CASCADE, FOREIGN KEY ( entità2_id ) REFERENCES plurale2(id) ON DELETE CASCADE)

DROP TABLE plurale1_plurale2
```

## Schema della Tabella di Mapping

Una relazione `cow*field` genera una tabella `cows_fields` con questa struttura:

| Colonna | Tipo | Vincoli |
|---------|------|---------|
| `cow_id` | `INT NOT NULL` | FOREIGN KEY → `cows(id)` ON DELETE CASCADE |
| `field_id` | `INT NOT NULL` | FOREIGN KEY → `fields(id)` ON DELETE CASCADE |
| _(chiave primaria)_ | — | `PRIMARY KEY (cow_id, field_id)` |
