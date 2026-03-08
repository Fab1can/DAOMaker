# DAOMaker - Indice della Documentazione

## Documentazione Generale

- [Panoramica del Progetto](panoramica.md) — Cos'è DAOMaker, obiettivi e architettura generale
- [Guida all'Utilizzo](utilizzo.md) — Come installare e usare DAOMaker
- [Sintassi del File di Input](sintassi.md) — Come scrivere il file di definizione delle tabelle
- [Esempi](esempi.md) — Esempi completi di input e output generato

## Documentazione dei Moduli

| Modulo | File | Descrizione |
|--------|------|-------------|
| [main](moduli/main.md) | `main.py` | Punto di ingresso, parsing del file e generazione dei file di output |
| [attribute](moduli/attribute.md) | `attribute.py` | Classe `Attribute` che rappresenta una colonna/attributo di tabella |
| [factories](moduli/factories.md) | `factories.py` | Funzioni per generare `DAOFactory.java` e `Db2DAOFactory.java` |
| [mapping](moduli/mapping.md) | `mapping.py` | Classe `Mapping` per le relazioni molti-a-molti |
| [relation](moduli/relation.md) | `relation.py` | Classe `Relation` che rappresenta un'entità/tabella del database |
| [type](moduli/type.md) | `type.py` | Classe `Type` per la mappatura dei tipi di dato |
| [utils](moduli/utils.md) | `utils.py` | Funzioni di utilità condivise tra i moduli |
