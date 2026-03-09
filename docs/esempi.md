# Esempi

## File di Input di Esempio

DAOMaker include il file `esempio` nella root del progetto come esempio di input. Descrive un semplice schema con allevatori, mucche, campi e oche con relazioni tra loro.

### Contenuto del file `esempio`

```
farmer
name:string
surname:string
birth_date:date

cow
name:string
race:string
owner:farmer

field
size:float
owner:farmer

goose/geese
name:string
age:int
owner:farmer

cow*field
goose*field
```

### Spiegazione dello schema

| Entità | Tabella SQL | Attributi | Note |
|--------|-------------|-----------|------|
| `farmer` | `farmers` | `name` (VARCHAR), `surname` (VARCHAR), `birth_date` (DATE) | — |
| `cow` | `cows` | `name` (VARCHAR), `race` (VARCHAR), `owner` → FK verso `farmers` | — |
| `field` | `fields` | `size` (FLOAT), `owner` → FK verso `farmers` | — |
| `goose` | `geese` | `name` (VARCHAR), `age` (INT), `owner` → FK verso `farmers` | Plurale irregolare esplicito |

**Relazioni molti-a-molti:**
- `cow*field` → tabella `cows_fields(cow_id, field_id)`
- `goose*field` → tabella `geese_fields(goose_id, field_id)`

---

## Output in Modalità DAO

Eseguendo:
```sh
python main.py esempio
```

Vengono generati nella cartella `out/` i seguenti file:

### File DTO

**`FarmerDTO.java`** (schema semplificato):
```java
public class FarmerDTO implements java.io.Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String name;
    private String surname;
    private Date birthDate;

    public FarmerDTO() {}

    public int getId() { return this.id; }
    public void setId(int id) { this.id = id; }
    public String getName() { return this.name; }
    public void setName(String name) { this.name = name; }
    // ... altri getter/setter ...
}
```

**`CowDTO.java`** (schema semplificato):
```java
public class CowDTO implements java.io.Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String name;
    private String race;
    private FarmerDTO owner;   // chiave esterna

    public CowDTO() {}
    // ... getter/setter ...
}
```

### File DAO

**`FarmerDAO.java`**:
```java
public interface FarmerDAO {
    public void create(FarmerDTO farmer);
    public FarmerDTO read(int id);
    public boolean update(FarmerDTO farmer);
    public boolean delete(int id);
    public boolean createTable();
    public boolean dropTable();
}
```

### File Db2DAO

**`Db2FarmerDAO.java`** (estratto):
```java
public class Db2FarmerDAO implements FarmerDAO {
    public static final String TABLE = "farmers";
    public static final String ID = "id";
    public static final String NAME = "name";
    public static final String SURNAME = "surname";
    public static final String BIRTH_DATE = "birth_date";

    static final String insert = "INSERT INTO " + TABLE + " ( " + ID + ","+NAME+","+SURNAME+","+BIRTH_DATE+" ) VALUES (?,?,?,?) ";
    // ... altre query SQL ...

    @Override
    public void create(FarmerDTO farmer) { ... }

    @Override
    public FarmerDTO read(int id) { ... }
    // ...
}
```

### File Factory

**`DAOFactory.java`**:
```java
public abstract class DAOFactory {
    public static final int DB2 = 0;

    public static DAOFactory getDAOFactory(int whichFactory) {
        switch (whichFactory) {
        case DB2: return new Db2DAOFactory();
        default: return null;
        }
    }

    public abstract FarmerDAO getFarmerDAO();
    public abstract CowDAO getCowDAO();
    public abstract FieldDAO getFieldDAO();
    public abstract GooseDAO getGooseDAO();
    public abstract CowsFieldsMappingDAO getCowsFieldsMappingDAO();
    public abstract GeeseFieldsMappingDAO getGeeseFieldsMappingDAO();
}
```

---

## Output in Modalità `nodao`

Eseguendo:
```sh
python main.py esempio nodao
```

Vengono generati:

**`Farmer.java`**: come il DTO, ma senza il suffisso `DTO` e con `Set<>` invece di `List<>`

**`Farmer.sql`**:
```sql
CREATE TABLE farmers ( id INT NOT NULL PRIMARY KEY, NAME VARCHAR(50), SURNAME VARCHAR(50), BIRTH_DATE DATE )
            
DROP TABLE farmers
```

---

## Esempio di Progetto Java Completo

La cartella `esempioJava/` contiene un progetto Java completo con schema studenti-corsi, che mostra come appare il codice finale dopo la generazione e l'eventuale personalizzazione. Include:

- `CourseDTO.java`, `StudentDTO.java` — I DTO
- `CourseDAO.java`, `StudentDAO.java` — Le interfacce DAO
- `CourseStudentMappingDAO.java` — L'interfaccia DAO del mapping
- `DAOFactory.java` — La factory astratta
- `db2/` — Implementazione DB2
- `hsqldb/` — Implementazione HSQLDB
- `mysql/` — Implementazione MySQL

Questo esempio illustra come il codice generato da DAOMaker può essere esteso con implementazioni per più DBMS e arricchito con logica applicativa aggiuntiva.
