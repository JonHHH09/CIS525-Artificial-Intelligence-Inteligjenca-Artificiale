# Artificial Intelligence / Inteligjenca Artificiale (CIS525)

The course repository keeps its executable implementations in notebooks. The three lessons live in `notebooks/`, with result checks in their own cells. Each lesson contains Python implementations, explanations, inline figures and notebook controls, and loads its datasets from the root `data/` directory. `models/` is reserved for future trained model artifacts; its placeholder retains the empty directory in Git. Environment configuration and guides also stay at the root. Do not restore separate seminar packages, CLI scripts, external servers or a nested notebook project unless explicitly requested.

## Notebooks

- `notebooks/seminar2.ipynb`: Dijkstra and BFS with step events, validated city/maze data, road-quality cost, inline graph/search views and optional animation. The old MCP queries, web viewer and terminal menu are replaced by notebook controls.
- `notebooks/seminar3.ipynb`: the provided `Node` and `a_star_search` implementation with `h = 0`, the 12-city state space, graph adaptation, independent reference searches and inline route controls. This remains a starter demonstration; the full assignment is in progress.
- `notebooks/seminar4.ipynb`: the starter `ProductionSystem` engine with an Albanian five-question car symptom form, 13 observable facts, 14 rules, forward chaining, explanations and an explicit unknown-condition result. The full assignment remains in progress.

## Environment and commands

Python >=3.14, managed by the root `pyproject.toml` and `uv.lock`, with `package = false`.

```text
uv sync --locked
uv run jupyter lab
uvx ruff@0.17.3 check .
uv run jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=180 --output-dir .notebook-checks notebooks/seminar2.ipynb notebooks/seminar3.ipynb notebooks/seminar4.ipynb
```

Use the project interpreter as the notebook kernel and choose **Restart Kernel and Run All Cells**. CI runs lint and executes each lesson in a fresh kernel on Ubuntu and Windows. Generated outputs go into the ignored `.notebook-checks/` directory. No separate verification notebook, formatter or type checker is configured.

## Conventions

- Keep every lesson runnable with its required data folders, without importing other notebooks or deleted project modules. Resolve data paths from either the project root or `notebooks/`. No source-file inspection, hard-coded machine paths or source generation.
- Put executable implementations directly in code cells. Keep setup, data, algorithms, presentation, controls and checks in focused cells. Use the Jupyter IDE tools to edit notebooks.
- Store course datasets in `data/`: shared city roads, maze doors and maze JSON configuration in `data/shared/`; the A* starter roads in `data/seminar3/`; facts, production rules and questions in `data/seminar4/`. Seminars 2 and 3 read the same shared files. Keep algorithms, illustrative examples and expected-result assertions in cells. City adjacency is `{city: {neighbour: km}}`; maze adjacency is `{room: [neighbours]}`; A* input is `{node: [(neighbour, cost)]}`. Store each undirected edge once in CSV and add both directions when loading.
- Seminar 4 knowledge and questionnaire text are Albanian. `facts.json` is a vocabulary, not automatically asserted symptoms; `questions.json` maps one alternative per question to a fact, with `null` for "Nuk e di". Rules use `kushtet` and `perfundimet` plus `id`, `lloji` and `shpjegimi`. Require all five answers before evaluation. Unknown answers add no fact, and no matching rule means unknown condition, not a healthy car. Keep the questionnaire nonblocking for Run All and use a fresh production system for each evaluation.
- Reserve `models/` for saved trained models, learned weights and fitted preprocessing objects. Classes, graph inputs and manually written production rules are not trained model artifacts.
- CSV loaders validate before returning data, preserving line-aware errors. Preserve accents in city names. City lookup is case/accent insensitive.
- Sort unweighted neighbours so equal-length BFS paths remain deterministic.
- Step messages and plot/animation captions are English. The course narration is primarily Albanian; keep root `README.md` and `README.en.md` aligned.
- Keep algorithm results, traces, figures and controls consistent. Animation should be user-triggered; Run All must finish without opening windows, launching services or leaving background processes.
- Keep assertions for normal inputs, invalid inputs, boundaries and trace/animation consistency in notebook cells. Verification must exercise actual fresh kernels, without relying on prior notebook state.
- Reference results: 8 cities/9 roads, 25 rooms/31 doors, Shkodër → Korçë 267 km, quality cost 476.1, maze 1 → 25 in 12 doors. Starter A*: TR → EL → LU → FR → TP → GJ, cost 278, with FR–TP = 83 as the documented assumption.
- Branches: feature branch → PR into `development`; `development` → `main` through a release PR.
