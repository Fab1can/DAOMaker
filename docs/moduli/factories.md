# Modulo `factories.py`

## Descrizione

Il modulo `factories.py` contiene due funzioni che generano i file di **factory** del pattern DAO: la classe astratta `DAOFactory` e la sua implementazione concreta `Db2DAOFactory`. Questi file sono condivisi tra tutte le entità del progetto e vengono generati una volta sola.

## Funzioni

### `DAOfactory(relations)`

```python
def DAOfactory(relations: list) -> str
```

Genera il contenuto del file `DAOFactory.java`: la **classe astratta** del pattern Abstract Factory per i DAO.

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `relations` | `list` | Lista di oggetti `Relation` e `Mapping` |

#### Valore di Ritorno

`str` — Il codice sorgente Java completo della classe `DAOFactory`.

#### Struttura del file generato

```java
public abstract class DAOFactory {

    // Costanti per i tipi di database supportati
    public static final int DB2 = 0;
    public static final int HSQLDB = 1;
    public static final int MYSQL = 2;

    // Factory method
    public static DAOFactory getDAOFactory(int whichFactory) {
        switch (whichFactory) {
        case DB2:
            return new Db2DAOFactory();
        // ...altri casi commentati...
        default:
            return null;
        }
    }

    // Metodi astratti (uno per ogni entità/mapping)
    public abstract NomeEntità1DAO getNomeEntità1DAO();
    public abstract NomeEntità2DAO getNomeEntità2DAO();
    // ...
}
```

#### Logica di Generazione

Per ogni oggetto nella lista `relations` (sia `Relation` che `Mapping`), viene aggiunto un metodo astratto:

```java
public abstract <NomeJava>DAO get<NomeJava>DAO();
```

Il metodo usa `item.java_name()` per ottenere il nome Java dell'entità o del mapping.

#### Database Supportati

La factory predefinita include tre costanti per i tipi di database:

| Costante | Valore | Stato |
|----------|--------|-------|
| `DB2` | `0` | Implementato (`Db2DAOFactory`) |
| `HSQLDB` | `1` | Commentato (non implementato) |
| `MYSQL` | `2` | Commentato (non implementato) |

---

### `DB2DAOfactory(relations)`

```python
def DB2DAOfactory(relations: list) -> str
```

Genera il contenuto del file `Db2DAOFactory.java`: l'**implementazione DB2** della factory astratta.

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `relations` | `list` | Lista di oggetti `Relation` e `Mapping` |

#### Valore di Ritorno

`str` — Il codice sorgente Java completo della classe `Db2DAOFactory`.

#### Struttura del file generato

```java
import java.sql.Connection;
import java.sql.DriverManager;

public class Db2DAOFactory extends DAOFactory {

    // Configurazione del driver e del database
    public static final String DRIVER = "com.ibm.db2.jcc.DB2Driver";
    public static final String DBURL = "jdbc:db2://diva.deis.unibo.it:50000/tw_stud";
    public static final String USERNAME = "xxx";
    public static final String PASSWORD = "xxx";

    // Blocco statico per il caricamento del driver
    static { ... }

    // Gestione delle connessioni
    public static Connection createConnection() { ... }
    public static void closeConnection(Connection conn) { ... }

    // Implementazione dei metodi factory (uno per ogni entità/mapping)
    @Override
    public NomeEntità1DAO getNomeEntità1DAO() {
        return new Db2NomeEntità1DAO();
    }
    // ...
}
```

#### Logica di Generazione

Per ogni oggetto nella lista `relations`, viene aggiunto un metodo `@Override` che restituisce la corrispondente implementazione DB2:

```java
@Override
public <NomeJava>DAO get<NomeJava>DAO() {
    return new Db2<NomeJava>DAO();
}
```

#### Configurazione della Connessione

La classe generata include le seguenti costanti che devono essere modificate prima dell'uso:

| Costante | Valore predefinito | Descrizione |
|----------|--------------------|-------------|
| `DRIVER` | `"com.ibm.db2.jcc.DB2Driver"` | Classe del driver JDBC per DB2 |
| `DBURL` | `"jdbc:db2://diva.deis.unibo.it:50000/tw_stud"` | URL di connessione al database |
| `USERNAME` | `"xxx"` | Nome utente (da personalizzare) |
| `PASSWORD` | `"xxx"` | Password (da personalizzare) |

> **Sicurezza:** Le credenziali (`USERNAME` e `PASSWORD`) sono lasciate come segnaposto `"xxx"` nel codice generato. È responsabilità dello sviluppatore sostituirle con le credenziali corrette, preferibilmente tramite variabili di ambiente o un file di configurazione esterno.

#### Note sul Connection Pool

Il codice generato include un commento esplicativo sul pool di connessioni. Per semplicità, `createConnection()` crea una nuova connessione ad ogni chiamata. In un ambiente di produzione sarebbe necessario implementare un pool di connessioni.
