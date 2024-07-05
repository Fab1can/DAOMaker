# DAOMaker

## Come lanciarlo

```sh
cd DAOMaker
python main.py nomefile [nodao]
```

## Come funziona

Questo script prenderà come argomento un file contenente la stuttura delle tabelle del database e creerà nella cartella `out` i file necessari all'implementazione di base del pattern DAO in Java usando DB2 come DBMS, specificando il parametro `nodao` verrano generati esclusivamente i file DTO senza riferimenti al pattern DAO e dei file SQl contenenti le istruzioni necessarie a creare ed eliminare le tabelle, specificando il parametro `repo` verrano generati i file DTO senza riferimenti al pattern DAO e i file di repository necessari alla forza bruta

## Sintassi del file

I caratteri supportati per la scrittura dei nomi all'interno del file sono numeri, lettere minuscole dell'alfabeto latino, `à`, `è`, `ì`, `ò`, `ù` e `_`, gli `_` verranno trattati come separatori di parole nella costruzione dei nomi, un nome non può inizare per numero o per `_`. Altri caratteri di sintassi sono `/` per indicare il plurale del nome di un entità (il nome della tabella), `:` per separare il nome di un attributo e il suo tipo, `*` per separare i due nomi di due tabelle in relazione molti a molti e si va a capo per separare le righe. Le righe vuote verranno ignorate.
Qualunque altro carattere presente nel file causerà un errore di sintassi.

### Strutture possibili delle righe

`nome` per indicare il nome di un'entità il cui plurale sarà il nome con aggiunta la s finale
`nome/plurale` per indicare il nome di un'entità esplicitando il plurale
`nome:tipo` per indicare un attributo di un'entità
Tutti gli attributi dovranno essere inseriti nelle righe dopo il nome dell'entità
`nome_entità1*nome_entità2` per indicare il nome delle due entità in relazione molti a molti fra loro (la posizione di queste righe all'interno del file è indifferente)

### Tipi supportati

-   Tipo stringa, indicato nel file come `string`
-   Tipo intero, indicato nel file come `int`
-   Tipo float, indicato nel file come `float`
-   Tipo data, indicato nel file come `date`
-   Un'altra entità (un DTO), indicato nel file con il nome di un'altra tabella già esistente
-   Qualunque altra cosa che rispetti le regole di sintassi (non è garantito il supporto in Java o DB2)

### Esempio

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

cow*field
```
