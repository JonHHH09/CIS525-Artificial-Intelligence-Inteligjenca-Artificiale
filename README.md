# Artificial Intelligence / Inteligjenca Artificiale (CIS525)

Shqip · [English](README.en.md)

Ushtrimet e CIS525 në UET janë realizuar si Jupyter notebooks në dosjen `notebooks/`, me të dhënat në `data/`. Çdo seminar përmban implementimin Python, shpjegimet, figurat, kontrollet ndërvepruese dhe verifikimin e rezultateve.

## Seminaret

| Notebook | Përmbajtja | Gjendja |
|---|---|---|
| [Seminari 2](notebooks/seminar2.ipynb) | Dijkstra, cilësia e rrugës, BFS, labirinti, gjurmët dhe figurat | Ushtrimet ekzistuese |
| [Seminari 3](notebooks/seminar3.ipynb) | Starter-i A*, heuristika zero dhe krahasimi me Dijkstra/BFS | Detyra në punë |
| [Seminari 4](notebooks/seminar4.ipynb) | Sistemet e prodhimit, inferenca përpara dhe pyetësori me pesë pyetje për makinën | Ushtrim ndërveprues; detyra në punë |

## Ekzekutimi

Kërkon Python 3.14+ dhe [uv](https://docs.astral.sh/uv/). Nga rrënja e repos:

```text
uv sync --locked
uv run jupyter lab
```

Hap një seminar dhe zgjidh **Restart Kernel and Run All Cells**. Në PyCharm përdor interpretuesin e `.venv` në rrënjë. Nise nga rrënja e repos ose nga `notebooks/`; seminaret e gjejnë automatikisht dosjen `data/`. Çdo seminar ekzekutohet pa importuar notebook tjetër apo paketë Python të seminareve. Kur kopjon një seminar diku tjetër, përfshi edhe dosjet përkatëse të të dhënave duke ruajtur strukturën relative.

Në Seminarin 4 plotëso pesë pyetjet te **Çfarë problemi ka makina juaj?**, pastaj shtyp **Vlerëso përgjigjet**. Çdo pyetje përfshin **Nuk e di**. Formulari shfaq problemet e mundshme, këshillat dhe rregullat që i mbështesin; kur përgjigjet nuk përputhen me rregullat, shfaqet qartë se nuk u gjet gjendje e njohur. **Fillo nga e para** pastron formularin. Run All përfundon pa pritur hyrje nga tastiera.

## Struktura

Tre notebook-et e seminareve ndodhen në dosjen `notebooks/`. Ky udhëzues, `pyproject.toml` dhe `uv.lock` mbeten në rrënjë. Algoritmet ndryshohen brenda qelizave; të dhënat ndryshohen në këta skedarë:

| Dosja | Përmbajtja | Përdoret nga |
|---|---|---|
| `data/shared/` | `cities.csv`, `maze_doors.csv`, `maze_config.json` | Seminaret 2 dhe 3 |
| `data/seminar3/` | `starter_roads.csv` (12 qytete, 15 rrugë; FR–TP = 83) | Seminari 3 |
| `data/seminar4/` | `facts.json`, `rules.json`, `questions.json` (njohuritë dhe pyetësori në shqip) | Seminari 4 |
| `models/` | Për modele të trajnuara dhe objekte të përshtatura të parapërpunimit në të ardhmen | Aktualisht bosh |

Çdo rrugë ose derë e padrejtuar ruhet vetëm një herë në CSV; funksionet e leximit shtojnë të dy drejtimet dhe validojnë hyrjet. Rregullat JSON të Seminarit 4 përdorin `kushtet` dhe `perfundimet`, bashkë me identifikuesin, llojin dhe shpjegimin. Skedari i fakteve është fjalor vëzhgimesh; faktet fillestare mblidhen vetëm nga përgjigjet e pyetësorit. Rregullat e shkruara manualisht janë të dhëna hyrëse, jo modele të trajnuara. Shembujt e vegjël dhe kontrollet e rezultateve mbeten në notebook-e. Kontrollet dhe pamjet brenda notebook-ut zëvendësojnë TUI-në, serverin MCP dhe shikuesin e veçantë në web.

## Kontrolli i seminareve

Çdo seminar përmban kontrolle `assert` për rezultatet. Ekzekuto të gjitha qelizat e një seminari, ose kontrollo të tre nga terminali:

```text
uv run jupyter nbconvert --execute --to notebook --ExecutePreprocessor.timeout=180 --output-dir .notebook-checks notebooks/seminar2.ipynb notebooks/seminar3.ipynb notebooks/seminar4.ipynb
uvx ruff@0.17.3 check .
```

Komanda ekzekuton secilin seminar me kernel të ri dhe ruan kopjet e gjeneruara në dosjen `.notebook-checks/`, të përjashtuar nga Git. Rezultatet e ruajtura në notebook-et origjinale nuk ndryshohen. Nuk ka notebook të veçantë verifikimi. CI kryen të njëjtat kontrolle në Windows dhe Ubuntu.

## Zhvillimi

Puna bëhet në degë të veçanta me PR drejt `development`; kalimi nga `development` në `main` bëhet me PR publikimi. Mbaji udhëzuesit shqip dhe anglisht në përputhje.

Licenca: [MIT](LICENSE).
