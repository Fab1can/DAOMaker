# Modulo `type.py`

## Descrizione

Il modulo `type.py` definisce la classe `Type`, che incapsula la rappresentazione di un tipo di dato nelle tre dimensioni necessarie a DAOMaker: Java, SQL DB2 e JDBC (`PreparedStatement`).

## Classe `Type`

### Costruttore

```python
Type(java_name, sql_name, prepared_name, array_list=False, foreign=False)
```

### Parametri

| Parametro | Tipo | Obbligatorio | Descrizione |
|-----------|------|--------------|-------------|
| `java_name` | `str` | Sì | Nome del tipo in Java (es. `"String"`, `"int"`, `"Date"`) |
| `sql_name` | `str` | Sì | Nome del tipo in SQL DB2 (es. `"VARCHAR(50)"`, `"INT"`) o `None` per tipi lista |
| `prepared_name` | `str` | Sì | Suffisso del metodo JDBC (es. `"String"` per `setString`, `"Int"` per `setInt`) |
| `array_list` | `bool` | No (default `False`) | `True` se il tipo rappresenta una lista di oggetti collegati (relazione molti-a-molti) |
| `foreign` | `bool` | No (default `False`) | `True` se il tipo rappresenta una chiave esterna verso un'altra entità |

### Attributi

| Attributo | Descrizione |
|-----------|-------------|
| `self.java_name` | Nome del tipo Java |
| `self.sql_name` | Definizione SQL del tipo (es. `"INT NOT NULL REFERENCES tabelle(id)"`) |
| `self.prepared_name` | Suffisso JDBC per `PreparedStatement` (es. `"String"` → `setString()`) |
| `self.array_list` | Flag: l'attributo è una lista (Set o List) di oggetti correlati |
| `self.foreign` | Flag: l'attributo è una chiave esterna |

### Metodo `static_name()`

```python
def static_name(self) -> str
```

Restituisce il nome del tipo Java da usare in un contesto statico (es. dichiarazione costante). Per le chiavi esterne restituisce `"int"` (l'ID numerico), per gli altri tipi restituisce `self.java_name`.

## Tabella di Mappatura dei Tipi

| Stringa nel file | `java_name` | `sql_name` | `prepared_name` | `foreign` | `array_list` |
|------------------|-------------|------------|-----------------|-----------|--------------|
| `string` | `String` | `VARCHAR(50)` | `String` | `False` | `False` |
| `int` | `int` | `INT` | `Int` | `False` | `False` |
| `float` | `float` | `FLOAT` | `Float` | `False` | `False` |
| `boolean` | `boolean` | `BOOL` | `Boolean` | `False` | `False` |
| `date` | `Date` | `DATE` | `Date` | `False` | `False` |
| Nome di entità | PascalCase del nome | `INT NOT NULL REFERENCES plurale(id)` | `Int` | `True` | `False` |
| Lista (mapping) | PascalCase del nome | `None` | `True` | `False` | `True` |

## Note Implementative

- Quando `array_list=True`, il tipo rappresenta una collezione di oggetti correlati tramite una tabella di mapping molti-a-molti. In questo caso `sql_name` è `None` perché non esiste una colonna diretta.
- Quando `foreign=True`, la colonna SQL memorizza un intero (`INT`) che è la chiave esterna verso un'altra tabella. Il tipo Java sarà `NomeEntitàDTO` (o `NomeEntità` in modalità `nodao`), ma il valore persistito è sempre un `int`.
- Il parametro `prepared_name` viene usato dalla classe `Attribute` per costruire le chiamate `prep_stmt.set<PreparedName>(index, value)` nelle query JDBC.
