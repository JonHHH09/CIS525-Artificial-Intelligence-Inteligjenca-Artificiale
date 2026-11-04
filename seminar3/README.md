# Seminari 3: kërkimi A*

Shqip · [English](README.en.md) · [Përmbajtja e lëndës](../README.md)

**Gjendja: në punë.**

## Përmbajtja

| Skedari | Përshkrimi |
|---|---|
| [`seminar_3_initial_code.py`](seminar_3_initial_code.py) | Kodi fillestar i dhënë: `Node`, `a_star_search` dhe grafi shembull `graph_data` (A–G) |
| [`draw.py`](draw.py) | Vizaton `graph_data` me rrugën e A* të theksuar |
| [`graph.py`](graph.py) | Shndërron grafet e Seminarit 2 (qytetet, labirinti) në formën që pret `a_star_search` |
| [`tests/`](tests/) | Testet për `graph.py`: të njëjtat brinjë si në Seminarin 2, të njëjtat rezultate si Dijkstra dhe BFS |
| [`images/`](images/) | Figurat e gjeneruara |

## Grafi

`graph_data` është i orientuar dhe me pesha: çdo nyje ka një listë çiftesh `(fqinji, kostoja)`.

```python
graph_data = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 4)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'F': [],
    'G': []
}
```

![Grafi fillestar me rrugën e A*](images/starter_graph.png)

Nyjet vendosen në kolona sipas largësisë në brinjë nga A. Rruga e A* është me ngjyrë rozë.

## Si funksionon A*

Çdo `Node` mban tri vlera:

| Vlera | Kuptimi |
|---|---|
| `g` | kostoja e rrugës nga fillimi deri te kjo nyje |
| `h` | kostoja e vlerësuar nga kjo nyje deri te qëllimi (heuristika) |
| `f` | `g + h`: kostoja e vlerësuar e gjithë rrugës përmes kësaj nyjeje |

`a_star_search(graph, start, end)`:

1. Vendos nyjen e fillimit në **listën e hapur** (një heap i renditur sipas `f`).
2. Merr nyjen me `f` më të vogël dhe shtoje në **listën e mbyllur** (nyjet e zgjeruara).
3. Nëse është qëllimi, ndiq lidhjet `parent` deri te fillimi dhe kthe rrugën të përmbysur.
4. Përndryshe, për çdo fqinj që nuk është në listën e mbyllur, llogarit `g`, `h` dhe `f` dhe shtoje në listën e hapur, përveç rastit kur është tashmë aty me `f` të barabartë ose më të vogël.
5. Përsërit derisa lista e hapur të boshatiset; atëherë nuk ka rrugë (`None`).

Rezultati mbi `graph_data`: **A → B → D → G, kosto 4** (1 + 2 + 1). Alternativa A → B → E → G kushton 8.

Në kodin fillestar `h = 0`, prandaj `f = g` dhe kërkimi sillet si Dijkstra: i saktë, por pa u drejtuar drejt qëllimit. Një heuristikë e vërtetë nuk duhet ta mbivlerësojë kurrë koston e mbetur (e pranueshme), përndryshe A* mund të kthejë një rrugë më të gjatë.

## Si të ekzekutohet

Nga rrënja e repos:

```
uv run python seminar3/seminar_3_initial_code.py           # shfaq rrugën nga A te G
uv run python -m seminar3.draw                             # shkruan images/starter_graph.png
uv run python -m seminar3.graph                            # A* mbi grafet e qyteteve dhe labirintit nga Seminari 2
uv run python -m unittest discover -s seminar3/tests -t .  # testet
```
