# Sintassi del File di Input

## Caratteri Supportati

I nomi nel file di input possono contenere:

- Lettere minuscole dell'alfabeto latino (`a`–`z`)
- Lettere accentate: `à`, `è`, `é`, `ì`, `ò`, `ù`
- Cifre numeriche (`0`–`9`), ma **non** come primo carattere
- Trattino basso `_`, usato come separatore di parole (es. `birth_date`)

> **Attenzione:** Un nome non può iniziare con un numero o con `_`. Qualsiasi altro carattere non supportato causerà un errore di sintassi.

## Struttura del File

Il file è composto da righe di testo. Le righe vuote vengono ignorate. Ogni riga ha uno dei seguenti formati:

### Dichiarazione di entità

```
nome
```

Dichiara un'entità (tabella) il cui nome plurale sarà `nome` + `s`.

```
nome/plurale
```

Dichiara un'entità esplicitando il nome plurale. Utile per plurali irregolari (es. `goose/geese`).

### Dichiarazione di attributo

```
nome:tipo
```

Dichiara un attributo dell'entità corrente (l'ultima entità dichiarata sopra). Gli attributi devono essere inseriti nelle righe immediatamente successive alla dichiarazione dell'entità.

### Dichiarazione di relazione molti-a-molti

```
nome_entità1*nome_entità2
```

Dichiara una relazione molti-a-molti tra due entità. Queste righe possono essere posizionate **in qualsiasi punto** del file.

## Tipi Supportati

| Tipo nel file | Tipo Java     | Tipo SQL DB2         | Metodo PreparedStatement |
|---------------|---------------|----------------------|--------------------------|
| `string`      | `String`      | `VARCHAR(50)`        | `setString`              |
| `int`         | `int`         | `INT`                | `setInt`                 |
| `float`       | `float`       | `FLOAT`              | `setFloat`               |
| `boolean`     | `boolean`     | `BOOL`               | `setBoolean`             |
| `date`        | `Date`        | `DATE`               | `setDate`                |
| `nome_entità` | `NomeEntità`  | `INT NOT NULL REFERENCES plurale(id)` | `setInt` (chiave esterna) |
| Qualsiasi altro valore | Uguale al tipo specificato | Valore in maiuscolo | Prima lettera maiuscola |

> **Nota:** Per i tipi personalizzati (non presenti nella lista), DAOMaker genera comunque il codice Java ma non è garantita la compatibilità con DB2 o Java.

### Tipo chiave esterna (entità collegata)

Quando il tipo di un attributo corrisponde al nome di un'altra entità già dichiarata nel file, DAOMaker genera:

- Nel DTO: un campo del tipo `NomeEntitàDTO` (o `NomeEntità` in modalità `nodao`)
- Nel database: una colonna `nome_attributo_id INT NOT NULL REFERENCES tabella(id)`
- Nel codice di accesso ai dati: un commento `//TODO: INSERISCI IL GETTER PER NOME` che ricorda allo sviluppatore di gestire il recupero dell'oggetto collegato

## Esempio Completo

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

### Spiegazione

- `farmer` — Entità con nome plurale `farmers`
  - `name:string` — Attributo stringa
  - `surname:string` — Attributo stringa
  - `birth_date:date` — Attributo data (generato come `birthDate` in Java)
- `cow` — Entità con nome plurale `cows`
  - `owner:farmer` — Chiave esterna verso `farmer` (colonna `owner_id` in SQL)
- `field` — Entità con nome plurale `fields`
- `goose/geese` — Entità con nome plurale irregolare `geese`
- `cow*field` — Relazione molti-a-molti tra `cow` e `field`
- `goose*field` — Relazione molti-a-molti tra `goose` e `field`

## Errori di Sintassi

Se il file contiene caratteri non supportati o righe con formato non riconosciuto, lo script termina con il messaggio:

```
Syntax error
```

e codice di uscita `1`.
