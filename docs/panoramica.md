# Panoramica del Progetto

## Cos'è DAOMaker

DAOMaker è uno strumento da riga di comando scritto in Python che genera automaticamente il codice Java necessario per implementare il **pattern DAO (Data Access Object)** con DB2 come DBMS.

A partire da un file di testo che descrive la struttura delle tabelle del database (entità, attributi e relazioni), DAOMaker produce i file Java pronti all'uso, riducendo il lavoro ripetitivo di scrittura del codice boilerplate.

## Obiettivi

- Automatizzare la generazione del codice di accesso al database in Java
- Supportare il pattern DAO completo con DB2
- Supportare la generazione di soli DTO (Data Transfer Object) senza dipendenze DAO
- Supportare la generazione di file Repository per architetture basate su repository
- Generare script SQL per la creazione e l'eliminazione delle tabelle

## Modalità di Funzionamento

DAOMaker supporta tre modalità operative, selezionabili tramite argomenti da riga di comando:

### Modalità DAO (predefinita)

Genera il pattern DAO completo:

- `<Nome>DTO.java` — Data Transfer Object per ogni entità
- `<Nome>DAO.java` — Interfaccia DAO per ogni entità
- `Db2<Nome>DAO.java` — Implementazione DB2 dell'interfaccia DAO
- `DAOFactory.java` — Factory astratta per i DAO
- `Db2DAOFactory.java` — Implementazione DB2 della factory

### Modalità `nodao`

Genera solo i DTO e i file SQL, senza riferimenti al pattern DAO:

- `<Nome>.java` — Classe Java (DTO) per ogni entità
- `<Nome>.sql` — File SQL con le istruzioni `CREATE TABLE` e `DROP TABLE`

### Modalità `repo`

Genera i DTO e le classi Repository (stile Spring/JPA semplificato):

- `<Nome>.java` — Classe Java (DTO) per ogni entità
- `<Nome>Repository.java` — Classe Repository per ogni entità

## Architettura del Codice

Il progetto è composto da sette moduli Python, ognuno con una responsabilità precisa:

```
DAOMaker/
├── main.py          # Punto di ingresso: parsing e orchestrazione
├── attribute.py     # Classe Attribute (colonna di tabella)
├── factories.py     # Generatori di DAOFactory e Db2DAOFactory
├── mapping.py       # Classe Mapping (relazioni molti-a-molti)
├── relation.py      # Classe Relation (entità/tabella)
├── type.py          # Classe Type (tipi di dato)
└── utils.py         # Funzioni di utilità
```

## Flusso di Esecuzione

1. `main.py` legge il file di input
2. Il parser estrae entità, attributi e relazioni molti-a-molti usando espressioni regolari
3. Per ogni entità viene creata un'istanza di `Relation` con i suoi `Attribute` (ciascuno con il proprio `Type`)
4. Per ogni relazione molti-a-molti viene creata un'istanza di `Mapping`
5. In base alla modalità selezionata, ogni oggetto genera il codice Java corrispondente tramite i propri metodi
6. I file generati vengono scritti nella cartella `out/`

## Dipendenze

DAOMaker non richiede librerie Python esterne. Utilizza solo moduli della libreria standard:

- `sys` — Lettura degli argomenti da riga di comando
- `re` — Espressioni regolari per il parsing del file di input
- `os` — Operazioni sul filesystem
- `shutil` — Rimozione ricorsiva della cartella di output
