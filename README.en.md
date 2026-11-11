# Artificial Intelligence / Inteligjenca Artificiale (CIS525)

[Shqip](README.md) · English

Seminar exercises for CIS525 at UET, implemented as Jupyter notebooks in `notebooks/`, with datasets in `data/`. Each lesson contains its own Python implementation, explanations, inline figures, controls and result checks.

## Seminars

| Notebook | Contents | Status |
|---|---|---|
| [Seminar 2](notebooks/seminar2.ipynb) | Dijkstra, road quality, BFS, maze, traces and inline visualizations | Existing exercises |
| [Seminar 3](notebooks/seminar3.ipynb) | A* starter, zero heuristic and comparisons with Dijkstra/BFS | Assignment in progress |
| [Seminar 4](notebooks/seminar4.ipynb) | Production systems, forward chaining and a five-question car symptom form in Albanian | Interactive exercise; assignment in progress |

## Running it

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/). From the repository root:

```text
uv sync --locked
uv run jupyter lab
```

Open a lesson and choose **Restart Kernel and Run All Cells**. In PyCharm, use the root `.venv` interpreter. Launch from the repository root or `notebooks/`; the lessons locate `data/` automatically. Each lesson runs without importing another notebook or a seminar Python package. When copying a lesson elsewhere, include its required data folders and preserve the relative layout.

In Seminar 4, answer the five questions in **Çfarë problemi ka makina juaj?**, then click **Vlerëso përgjigjet**. Each question includes **Nuk e di**. The form shows possible problems, recommendations and the rules supporting them; unmatched answers produce an explicit unknown-condition result. **Fillo nga e para** resets the form. Run All finishes without waiting for keyboard input.

## Layout

The three lesson notebooks are in `notebooks/`. This guide, `pyproject.toml` and `uv.lock` stay at the root. Algorithms are editable in notebook cells; course datasets are editable in these files:

| Folder | Contents | Used by |
|---|---|---|
| `data/shared/` | `cities.csv`, `maze_doors.csv`, `maze_config.json` | Seminars 2 and 3 |
| `data/seminar3/` | `starter_roads.csv` (12 cities, 15 roads; FR–TP = 83) | Seminar 3 |
| `data/seminar4/` | `facts.json`, `rules.json`, `questions.json` (Albanian knowledge and questionnaire) | Seminar 4 |
| `models/` | Reserved for future trained models and fitted preprocessing objects | Currently empty |

Each undirected road or door appears once in its CSV; loaders add both directions and validate inputs. Seminar 4's JSON rules use `kushtet` and `perfundimet`, with a rule ID, type and explanation. Its facts file is a vocabulary of observations; actual starting facts come only from questionnaire answers. Manually written rules are input data, not trained models. Small illustrative examples and expected-result assertions remain in the notebooks. Notebook controls and inline views replace the former terminal UI, MCP server and separate web viewer.

## Checking the lessons

Each lesson includes assertions that check its results. Run all cells in a lesson, or check all three from the terminal:

```text
uv run jupyter nbconvert --execute --to notebook --ExecutePreprocessor.timeout=180 --output-dir .notebook-checks notebooks/seminar2.ipynb notebooks/seminar3.ipynb notebooks/seminar4.ipynb
uvx ruff@0.17.3 check .
```

This executes each lesson in a fresh kernel and writes generated copies to the ignored `.notebook-checks/` directory, keeping the saved lesson outputs unchanged. There is no separate verification notebook. CI runs the same checks on Windows and Ubuntu.

## Development

Use feature branches and PRs into `development`; promote `development` to `main` through a release PR. Keep the Albanian and English guides in step.

License: [MIT](LICENSE).
