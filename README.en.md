# Artificial Intelligence / Inteligjenca Artificiale (CIS525)

[![CI](https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale/actions/workflows/ci.yml/badge.svg)](https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale/actions/workflows/ci.yml)

[Shqip](README.md) · English

Seminar exercises for the Artificial Intelligence course (CIS525, UET). Each seminar has its own folder with a README, code, tests and the written report.

## Seminars

| Seminar | Topic | Report | Status |
|---|---|---|---|
| [Seminar 2](seminar2/README.en.md) | Graph search: shortest route between cities (Dijkstra) and the way out of a maze (BFS) | [U1: cities](seminar2/cities/arsyetimi.md), [U2: maze](seminar2/maze/arsyetimi.md) (Albanian) | Done |
| [Seminar 3](seminar3/README.en.md) | A* search | – | In progress |

## How to read it

1. **The seminar README**: task, result and figures on one page.
2. **The report** (`arsyetimi.md`): why the algorithm was chosen and how the result is reached, step by step.
3. **Code and tests**: the seminar README says where each part is.

Everything reads directly on GitHub, without running anything.

## Running it

Requires Python 3.14+ and [uv](https://docs.astral.sh/uv/). Run commands from the repo root.

```
git clone https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale.git
cd CIS525-Artificial-Intelligence-Inteligjenca-Artificiale
uv sync
uv run python -m unittest discover -s seminar2/tests -t .   # tests confirm the results in the reports
uv run python -m seminar2.tui                               # menu with every feature
```

Each seminar's README has its own commands.

## Layout

```
seminar2/        Graph search (U1 cities, U2 maze)
  cities/        U1: graph loader, quality route, figures, report
  maze/          U2: maze loader, figures, report
  dataset/       CSV data
  images/        generated figures and animations
  tests/         tests (unittest)
seminar3/        A* search (starter code, graph image)
pyproject.toml   dependencies (uv)
```

## Development

- Lint: `uvx ruff@0.17.3 check .` (config in `pyproject.toml`).
- CI (GitHub Actions) runs ruff and the tests on Ubuntu and Windows.
- Work happens on feature branches with PRs into `development`; `development` reaches `main` through a release PR.

License: [MIT](LICENSE).
