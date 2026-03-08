# Modulo `attribute.py`

## Descrizione

Il modulo `attribute.py` definisce la classe `Attribute`, che rappresenta una singola colonna/attributo di una tabella del database. Ogni `Attribute` ha un nome e un tipo (`Type`), e fornisce metodi per generare il codice Java corrispondente (getter, setter, dichiarazioni di campo).

## Classe `Attribute`

### Costruttore

```python
Attribute(name: str, type: Type)
```

### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `name` | `str` | Nome dell'attributo in formato `snake_case` (come scritto nel file di input) |
| `type` | `Type` | Oggetto `Type` che descrive il tipo di dato dell'attributo |

### Attributi

| Attributo | Descrizione |
|-----------|-------------|
| `self.name` | Nome originale in `snake_case` |
| `self.type` | Oggetto `Type` associato |

---

## Metodi

### `java_name()`

```python
def java_name(self) -> str
```

Restituisce il nome dell'attributo in formato **camelCase**, adatto per i campi e le variabili Java.

**Esempio:** `birth_date` → `birthDate`

---

### `java_signature()`

```python
def java_signature(self) -> str
```

Restituisce il nome dell'attributo in formato **PascalCase**, usato come suffisso nei nomi dei metodi getter e setter Java.

**Esempio:** `birth_date` → `BirthDate` (usato in `getBirthDate()`, `setBirthDate()`)

---

### `static_name()`

```python
def static_name(self) -> str
```

Restituisce il nome della colonna SQL da usare nelle costanti statiche del DAO. Per le chiavi esterne aggiunge il suffisso `_id`.

| Tipo di attributo | Risultato |
|-------------------|-----------|
| Tipo normale | `self.name` |
| Chiave esterna (`foreign=True`) | `self.name + "_id"` |

**Esempio:** `owner` (chiave esterna) → `"owner_id"`

---

### `get_getter_method(variable)`

```python
def get_getter_method(self, variable: str) -> str
```

Genera il codice Java per leggere il valore dell'attributo da un oggetto DTO, da usare nei metodi di persistenza (es. `setInt(index, dto.getOwner().getId())`).

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `variable` | `str` | Nome della variabile Java che contiene il DTO |

#### Logica

| Condizione | Codice generato |
|------------|-----------------|
| Tipo `Date` | `new java.sql.Date(variable.getBirthDate().getTime())` |
| Tipo `boolean` | `variable.isNome()` |
| Chiave esterna | `variable.getNome().getId()` |
| Altro | `variable.getNome()` |

---

### `get_setter_method()`

```python
def get_setter_method(self) -> str
```

Genera il codice Java per impostare il valore dell'attributo su un DTO leggendolo da un `ResultSet` JDBC.

#### Logica

| Condizione | Codice generato |
|------------|-----------------|
| Tipo `Date` | `entry.setBirthDate(new java.sql.Date(rs.getDate(BIRTH_DATE).getTime()))` |
| Tipo `boolean` | `entry.isNome(rs.getBoolean(NOME))` |
| Chiave esterna | `//TODO: INSERISCI IL GETTER PER NOME` (commento reminder) |
| Altro | `entry.setNome(rs.getNomeTipo(NOME))` |

> **Nota:** Per le chiavi esterne, il recupero dell'oggetto collegato richiede una query aggiuntiva che va implementata manualmente dallo sviluppatore. DAOMaker inserisce un commento `//TODO` come promemoria.

---

### `get_getter(nodao)`

```python
def get_getter(self, nodao: bool) -> str
```

Genera il metodo getter Java completo per il campo dell'attributo nel DTO.

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `nodao` | `bool` | Se `True`, usa il tipo senza il suffisso `DTO` |

#### Comportamento

- Per attributi lista (`array_list=True`):
  - `nodao=True`: `Set<NomeTipo>`
  - `nodao=False`: `List<NomeTipoDTO>`
- Per chiavi esterne (`foreign=True`):
  - `nodao=True`: `NomeTipo`
  - `nodao=False`: `NomeTipoDTO`
- Per tipi booleani: usa il prefisso `is` invece di `get`
- Per tutti gli altri: usa il prefisso `get`

---

### `get_setter(nodao)`

```python
def get_setter(self, nodao: bool) -> str
```

Genera il metodo setter Java completo per il campo dell'attributo nel DTO.

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `nodao` | `bool` | Se `True`, usa il tipo senza il suffisso `DTO` |

#### Comportamento

Speculare a `get_getter()`. Per i booleani usa il prefisso `is` nel nome del setter.

## Esempio

Per un attributo `birth_date:date`:

```python
attr = Attribute("birth_date", Type("Date", "DATE", "Date"))
attr.java_name()         # → "birthDate"
attr.java_signature()    # → "BirthDate"
attr.static_name()       # → "birth_date"
attr.get_getter_method("farmer")  # → "new java.sql.Date(farmer.getBirthDate().getTime())"
```
