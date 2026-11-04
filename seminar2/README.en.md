# Seminar 2: graph search

[Shqip](README.md) · English · [Course index](../README.en.md)

Two graph problems, a shortest route between Albanian cities and a way out of a maze, solved with one small search module. The results are available as a terminal UI, command-line scripts, an MCP server and a live web viewer that animates each search.

## Reports

- [U1: cities](cities/arsyetimi.md) (Albanian)
- [U2: maze](maze/arsyetimi.md) (Albanian)

## At a glance

| | U1: cities | U2: maze |
|---|---|---|
| Data | [`dataset/cities.csv`](dataset/cities.csv) | [`maze_doors.csv`](dataset/maze_doors.csv), [`maze_config.csv`](dataset/maze_config.csv) |
| Graph | 8 cities, 9 roads, weighted, undirected (km) | 25 rooms (5x5), 31 doors, unweighted, undirected |
| Question | Shortest route by total km | Path with the fewest doors, room 1 to room 25 |
| Algorithm | Dijkstra | BFS |
| Why | Roads have different lengths, so the nearest unsettled city is expanded first | Every door costs the same, so the first time BFS reaches a room is already the shortest way |
| Result | Shkodër → Lezhë → Tirana → Elbasan → Korçë, **267 km** | 1 → 2 → 3 → 8 → 13 → 18 → 17 → 16 → 21 → 22 → 23 → 24 → 25, **12 doors** |

**Extension (U1): best-quality route.** Each road has a quality (`highway`, `good`, `fair`, `poor`). Dijkstra runs on km × factor (1.0 / 1.3 / 1.8 / 2.5), so a longer but better road can win. For Shkodër → Korçë it gives the same route (cost 476.1, worst road: `poor`). Code: [`cities/quality.py`](cities/quality.py).

| Cities graph | Route animation |
|---|---|
| <img src="images/cities/graph.png" width="360" alt="City graph"> | <img src="images/cities/route.gif" width="360" alt="Route animation"> |

| Maze | Path animation |
|---|---|
| <img src="images/maze/maze.png" width="360" alt="Maze"> | <img src="images/maze/path.gif" width="360" alt="Path animation"> |

## Where things are

| Part | File |
|---|---|
| Search algorithms (Dijkstra, BFS) | [`graph_search.py`](graph_search.py) |
| U1 loader and checks | [`cities/graph.py`](cities/graph.py) |
| U1 best-quality route | [`cities/quality.py`](cities/quality.py) |
| U2 loader and checks | [`maze/maze.py`](maze/maze.py) |
| Figures and animations | `cities/draw.py`, `cities/animate.py`, `maze/draw.py`, `maze/animate.py`, [`animation.py`](animation.py) |
| MCP server | [`mcp_server.py`](mcp_server.py) |
| Live viewer | [`live/`](live/) |
| Terminal UI | [`tui/`](tui/) |
| Tests | [`tests/`](tests/) |

## How it works

- The data lives in CSV files in `dataset/`.
- The loaders (`cities/graph.py`, `maze/maze.py`) validate it and raise `ValueError` with the file and line number. They never return partial data.
- `graph_search.py` holds `Graph` and the search algorithms. `dijkstra_steps` and `bfs_steps` are generators that yield one dict per step (frontier, visited, distances, predecessors). `dijkstra` and `bfs` just consume them, so a trace and a result cannot disagree.
- Dijkstra uses a priority queue ordered by distance. BFS uses a FIFO queue, and neighbours are sorted so the path is the same on every run.
- The consumers all read the same steps: the plain results, the MCP trace tools, the matplotlib animations and the live viewer.

## Running it

Run from the repo root (see the [course index](../README.en.md) for setup):

```
uv run python -m unittest discover -s seminar2/tests -t .   # tests
uv run python -m seminar2.tui                               # terminal UI with every feature
```

### Terminal UI

A [Textual](https://textual.textualize.io/) app that works on Windows, Linux and macOS, mouse included. The left side is the action list with a filter box; the right side is the options form, a Run button and the output. The status bar shows the live viewer URL and any background processes.

- `↑`/`↓` select an action; `Enter` opens its form (or runs it if it has no options); `Enter` in a field runs
- `Tab` / `Shift+Tab` move between fields; `Ctrl+R` runs from anywhere
- `Esc` cancels a running job or goes back to the list
- `/` filters, `Ctrl+L` clears the output, `?` help (`F1` while typing), `Ctrl+P` command palette (themes)
- `q` quits (not while typing), `Ctrl+Q` / `Ctrl+C` quit anywhere

Background processes (the live viewer, for example) are stopped on exit.

### Command line

Modules run with `-m`:

```
uv run python -m seminar2.cities.draw     # writes seminar2/images/cities/graph.png
uv run python -m seminar2.maze.draw       # writes seminar2/images/maze/maze.png
uv run python -m seminar2.cities.animate  # writes seminar2/images/cities/route.gif (--from, --to, --show, --out, --fps)
uv run python -m seminar2.maze.animate    # writes seminar2/images/maze/path.gif (--from, --to, --show, --out, --fps)
uv run python -m seminar2.live            # live viewer at http://127.0.0.1:8765 with demo searches
uv run python seminar2/mcp_server.py      # MCP server over stdio, plus the live viewer
uv run python -m seminar2.cities.graph    # print the city graph and checks
uv run python -m seminar2.maze.maze       # print the maze and validation result
```

`--show` opens a matplotlib window instead of saving a GIF.

## MCP server

Runs over stdio. The data is read once at startup, so restart the server after editing the CSVs.

| Tool | Problem | Purpose |
|---|---|---|
| `list_cities` | cities | Cities and how many roads each has |
| `get_roads(city)` | cities | Direct roads from a city, in km (name matching ignores case and accents) |
| `shortest_route(from_city, to_city)` | cities | Shortest route by total km (Dijkstra) |
| `best_quality_route(from_city, to_city)` | cities | Route with the lowest km × road-quality cost |
| `trace_route(from_city, to_city, detail=False)` | cities | Shortest route plus a step-by-step explanation; `detail=True` returns the raw events |
| `get_maze` | maze | Entrance, exit, doors and each room's neighbours |
| `get_doors(room)` | maze | Rooms reachable through one room's doors |
| `find_path(from_room=1, to_room=25)` | maze | Fewest-doors path (BFS) |
| `trace_maze(from_room=1, to_room=25, detail=False)` | maze | Same path plus a step-by-step explanation; `detail=True` returns the raw events |
| `live_viewer()` | both | URL of the live viewer |

The search tools also play their search in the live viewer at http://127.0.0.1:8765: first the graph is built edge by edge, then the search runs.

- Port: `SEMINAR2_LIVE_PORT` (default 8765). Off: `SEMINAR2_LIVE=0`.
- If the default port is busy, the viewer picks a free one (ask `live_viewer` for the URL). A busy port set through `SEMINAR2_LIVE_PORT` disables the viewer; the server keeps working.

### Connecting a client

Claude Code: the repo ships a project-scoped `.mcp.json`. Start `claude` in the repo root and approve the `seminar2` server; the tools appear as `mcp__seminar2__<tool>`. Check with `claude mcp list` or `/mcp`.

Generic MCP client config:

```json
{
  "mcpServers": {
    "seminar2": {
      "command": "uv",
      "args": ["run", "python", "seminar2/mcp_server.py"],
      "cwd": "/path/to/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale"
    }
  }
}
```

To try the tools by hand: `npx @modelcontextprotocol/inspector uv run python seminar2/mcp_server.py`.
