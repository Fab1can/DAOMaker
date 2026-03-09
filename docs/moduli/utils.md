# Modulo `utils.py`

## Descrizione

Il modulo `utils.py` fornisce funzioni di utilità condivise tra i vari moduli di DAOMaker. Contiene le funzioni di conversione dei nomi e la funzione di segnalazione degli errori di sintassi.

## Funzioni

### `snake2camel(string)`

```python
def snake2camel(string: str) -> str
```

Converte una stringa dal formato `snake_case` al formato **camelCase** (prima parola minuscola, parole successive con iniziale maiuscola).

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `string` | `str` | Stringa in formato `snake_case` |

#### Valore di Ritorno

`str` — La stringa convertita in **camelCase**.

#### Esempi

| Input | Output |
|-------|--------|
| `"name"` | `"name"` |
| `"birth_date"` | `"birthDate"` |
| `"first_name_of_person"` | `"firstNameOfPerson"` |

#### Logica

Divide la stringa sui caratteri `_`. Se ci sono più parole, la prima rimane minuscola e le successive vengono capitalizzate (prima lettera maiuscola + resto invariato). Con una sola parola, restituisce la stringa originale.

---

### `snake2pascal(string)`

```python
def snake2pascal(string: str) -> str
```

Converte una stringa dal formato `snake_case` al formato **PascalCase** (tutte le parole con iniziale maiuscola).

#### Parametri

| Parametro | Tipo | Descrizione |
|-----------|------|-------------|
| `string` | `str` | Stringa in formato `snake_case` |

#### Valore di Ritorno

`str` — La stringa convertita in **PascalCase**.

#### Esempi

| Input | Output |
|-------|--------|
| `"name"` | `"Name"` |
| `"birth_date"` | `"BirthDate"` |
| `"cow_field"` | `"CowField"` |
| `"first_name_of_person"` | `"FirstNameOfPerson"` |

#### Logica

Divide la stringa sui caratteri `_` e capitalizza la prima lettera di ogni parola, concatenando il risultato.

---

### `syntax_error()`

```python
def syntax_error()
```

Stampa il messaggio `"Syntax error"` sullo standard output e termina il programma con codice di uscita `1`.

Viene chiamata da `main.py` ogni volta che una riga del file di input non corrisponde ad alcun pattern valido.

#### Effetti

- Stampa: `Syntax error`
- Termina il processo con `exit(1)`

## Utilizzo nei Moduli

| Funzione | Usata in | Scopo |
|----------|----------|-------|
| `snake2camel` | `attribute.py` | Genera il nome Java dell'attributo (camelCase) |
| `snake2pascal` | `attribute.py`, `mapping.py`, `relation.py` | Genera nomi di classi e metodi Java (PascalCase) |
| `syntax_error` | `main.py` | Segnala errori nel file di input |
