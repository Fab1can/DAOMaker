# Modulo `relation.py`

## Descrizione

Il modulo `relation.py` definisce la classe `Relation`, che rappresenta un'entità (tabella) del database. È la classe principale per la generazione del codice Java: fornisce metodi per produrre il DTO, l'interfaccia DAO, l'implementazione DB2 DAO, la classe Repository e gli script SQL.

## Classe `Relation`

### Costruttore

```python
Relation(name: str, plural: str, attributes: list[Attribute], nodao: bool)
```

### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `name` | `str` | Nome dell'entità in `snake_case` (es. `"birth_date"`) |
| `plural` | `str` | Forma plurale del nome, usata come nome della tabella SQL |
| `attributes` | `list[Attribute]` | Lista degli attributi dell'entità |
| `nodao` | `bool` | Se `True`, la generazione è in modalità senza DAO |

### Attributi

| Attributo | Descrizione |
|-----------|-------------|
| `self.name` | Nome in `snake_case` |
| `self.plural` | Nome plurale (nome della tabella SQL) |
| `self.attributes` | Lista di oggetti `Attribute` |
| `self.nodao` | Flag modalità `nodao` |

---

## Metodi

### `java_name()`

```python
def java_name(self) -> str
```

Restituisce il nome dell'entità in **PascalCase**, usato come nome delle classi Java.

**Esempio:** `"birth_date"` → `"BirthDate"`

---

### `non_list_attributes()`

```python
def non_list_attributes(self) -> list[Attribute]
```

Restituisce solo gli attributi che **non** sono liste (esclude gli attributi `array_list=True`, cioè le relazioni molti-a-molti). Questi sono gli attributi che corrispondono a colonne reali della tabella SQL.

---

### `getDAO()`

```python
def getDAO(self) -> str
```

Genera il contenuto del file `<NomeEntità>DAO.java`: l'**interfaccia DAO** Java con i metodi CRUD standard.

#### Metodi generati nell'interfaccia

| Metodo | Descrizione |
|--------|-------------|
| `create(NomeEntitàDTO entità)` | Inserisce un record |
| `read(int id)` | Legge un record per ID |
| `update(NomeEntitàDTO entità)` | Aggiorna un record |
| `delete(int id)` | Elimina un record per ID |
| `createTable()` | Crea la tabella nel database |
| `dropTable()` | Elimina la tabella dal database |

---

### `getDb2DAO()`

```python
def getDb2DAO(self) -> str
```

Genera il contenuto del file `Db2<NomeEntità>DAO.java`: l'**implementazione DB2** dell'interfaccia DAO.

#### Struttura del file generato

1. **Costanti letterali** — Nomi delle colonne come costanti `String` statiche (es. `public static final String NAME = "name"`)
2. **Statement SQL** — Query precostruite come costanti statiche:
   - `insert` — Inserimento
   - `read_by_id` — Lettura per ID
   - `delete` — Cancellazione per ID
   - `update` — Aggiornamento
   - `query` — Lettura di tutti i record
   - `create` — Creazione della tabella
   - `drop` — Eliminazione della tabella
3. **Implementazione dei metodi CRUD** — Ogni metodo usa `Db2DAOFactory.createConnection()` e `Db2DAOFactory.closeConnection()`, con gestione delle eccezioni tramite try-catch-finally

#### Note sul codice generato

- I commenti `//TODO: GESTIRE ASSOCIAZIONI` indicano i punti in cui lo sviluppatore deve aggiungere il codice per gestire le relazioni molti-a-molti
- Le chiavi esterne generano commenti `//TODO: INSERISCI IL GETTER PER NOME` nei metodi `read()`

---

### `getRepository()`

```python
def getRepository(self) -> str
```

Genera il contenuto del file `<NomeEntità>Repository.java`: una **classe Repository** che si connette al database tramite un oggetto `DataSource`.

#### Differenze rispetto all'implementazione DB2 DAO

- Non implementa un'interfaccia
- Il costruttore accetta un `int databaseType` e crea un `DataSource`
- I metodi lanciano `PersistenceException` invece di gestire le eccezioni internamente
- Il metodo di persistenza si chiama `persist()` invece di `create()`
- I metodi `read()` e `update()` usano la stessa query `update` per entrambe le operazioni di aggiornamento

---

### `getDTO()`

```python
def getDTO(self) -> str
```

Genera il contenuto del file DTO Java (`<NomeEntità>DTO.java` o `<NomeEntità>.java` in modalità `nodao`).

#### Struttura del file generato

1. **Dichiarazione della classe** — `public class NomeEntitàDTO implements java.io.Serializable`
2. **serialVersionUID** — `private static final long serialVersionUID = 1L`
3. **Campo ID** — `private int id`
4. **Campi degli attributi** — Uno per ciascun attributo:
   - Tipi normali: `private TipoJava nomeAttributo`
   - Chiavi esterne: `private NomeTipoDTO nomeAttributo` (o senza `DTO` in modalità `nodao`)
   - Liste: `private List<NomeTipoDTO> nomeAttributo` (o `Set<NomeTipo>` in modalità `nodao`)
5. **Costruttore** — Inizializza le liste vuote (`new ArrayList<>()` o `new HashSet<>()`)
6. **Getter e setter per ID**
7. **Getter e setter per ogni attributo**

#### Modalità `nodao`

In modalità `nodao`:
- Il nome della classe non ha il suffisso `DTO`
- Le chiavi esterne usano il tipo senza suffisso `DTO`
- Le liste usano `Set<NomeTipo>` invece di `List<NomeTipoDTO>`
- Il costruttore usa `new HashSet<>()` invece di `new ArrayList<>()`

---

### `getCreateDrop()`

```python
def getCreateDrop(self) -> str
```

Genera il contenuto del file `<NomeEntità>.sql` con le istruzioni SQL per creare e eliminare la tabella.

#### Formato del file generato

```sql
CREATE TABLE nomi_plurali ( id INT NOT NULL PRIMARY KEY, COL1 TIPO1, COL2 TIPO2, ... )
            
DROP TABLE nomi_plurali
```

---

### `DTOconstructor()` (metodo privato)

```python
def DTOconstructor(self) -> str
```

Genera il codice del costruttore della classe DTO. Inizializza le liste vuote:
- In modalità `nodao`: `new HashSet<NomeTipo>()`
- In modalità DAO: `new ArrayList<NomeTipoDTO>()`

Questo metodo è usato internamente da `getDTO()`.

## Schema delle Dipendenze

```
Relation
 ├── usa: Attribute (per ogni colonna)
 │    └── usa: Type (tipo del dato)
 └── usa: snake2pascal (da utils.py)
```
