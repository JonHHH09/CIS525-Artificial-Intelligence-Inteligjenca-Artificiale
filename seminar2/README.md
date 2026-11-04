# Seminari 2: kërkimi në graf

Shqip · [English](README.en.md) · [Përmbajtja e lëndës](../README.md)

Dy probleme grafi, rruga më e shkurtër mes qyteteve të Shqipërisë dhe dalja nga një labirint, të zgjidhura me një modul të vetëm kërkimi. Rezultatet mund të shihen në një ndërfaqe terminali, me skripte nga rreshti i komandave, përmes një serveri MCP dhe në një shikues web që animon çdo kërkim.

## Raportet

- [U1: grafi ndërqytetas](cities/arsyetimi.md)
- [U2: labirinti me 25 dhoma](maze/arsyetimi.md)

## Përmbledhje

| | U1: qytetet | U2: labirinti |
|---|---|---|
| Të dhënat | [`dataset/cities.csv`](dataset/cities.csv) | [`maze_doors.csv`](dataset/maze_doors.csv), [`maze_config.csv`](dataset/maze_config.csv) |
| Grafi | 8 qytete, 9 rrugë, me pesha, i padrejtuar (km) | 25 dhoma (5x5), 31 dyer, pa pesha, i padrejtuar |
| Pyetja | Rruga më e shkurtër sipas km gjithsej | Rruga me më pak dyer, nga dhoma 1 te dhoma 25 |
| Algoritmi | Dijkstra | BFS |
| Pse | Rrugët kanë gjatësi të ndryshme, prandaj zgjerohet gjithmonë qyteti më i afërt i pazgjidhur | Çdo derë kushton njësoj, prandaj herën e parë që BFS arrin një dhomë, ajo është tashmë rruga më e shkurtër |
| Rezultati | Shkodër → Lezhë → Tirana → Elbasan → Korçë, **267 km** | 1 → 2 → 3 → 8 → 13 → 18 → 17 → 16 → 21 → 22 → 23 → 24 → 25, **12 dyer** |

**Zgjerim (U1): rruga me cilësinë më të mirë.** Çdo rrugë ka një cilësi (`highway`, `good`, `fair`, `poor`). Dijkstra ekzekutohet mbi km × faktor (1.0 / 1.3 / 1.8 / 2.5), kështu që një rrugë më e gjatë, por më e mirë, mund të fitojë. Për Shkodër → Korçë del e njëjta rrugë (kosto 476.1, rruga më e keqe: `poor`). Kodi: [`cities/quality.py`](cities/quality.py).

| Grafi i qyteteve | Animacioni i rrugës |
|---|---|
| <img src="images/cities/graph.png" width="360" alt="Grafi i qyteteve"> | <img src="images/cities/route.gif" width="360" alt="Animacioni i rrugës"> |

| Labirinti | Animacioni i rrugës |
|---|---|
| <img src="images/maze/maze.png" width="360" alt="Labirinti"> | <img src="images/maze/path.gif" width="360" alt="Animacioni i rrugës në labirint"> |

## Ku ndodhet secila pjesë

| Pjesa | Skedari |
|---|---|
| Algoritmet e kërkimit (Dijkstra, BFS) | [`graph_search.py`](graph_search.py) |
| U1: ngarkimi dhe kontrollet | [`cities/graph.py`](cities/graph.py) |
| U1: rruga me cilësinë më të mirë | [`cities/quality.py`](cities/quality.py) |
| U2: ngarkimi dhe kontrollet | [`maze/maze.py`](maze/maze.py) |
| Figurat dhe animacionet | `cities/draw.py`, `cities/animate.py`, `maze/draw.py`, `maze/animate.py`, [`animation.py`](animation.py) |
| Serveri MCP | [`mcp_server.py`](mcp_server.py) |
| Shikuesi live | [`live/`](live/) |
| Ndërfaqja e terminalit | [`tui/`](tui/) |
| Testet | [`tests/`](tests/) |

## Si funksionon

- Të dhënat janë në skedarë CSV në `dataset/`.
- Ngarkuesit (`cities/graph.py`, `maze/maze.py`) i validojnë dhe ngrenë `ValueError` me emrin e skedarit dhe numrin e rreshtit. Nuk kthejnë kurrë të dhëna të paplota.
- `graph_search.py` përmban `Graph` dhe algoritmet e kërkimit. `dijkstra_steps` dhe `bfs_steps` janë gjeneratorë që japin një fjalor për çdo hap (kufiri, të vizituarit, distancat, paraardhësit). `dijkstra` dhe `bfs` thjesht i konsumojnë, kështu që gjurma dhe rezultati nuk mund të ndryshojnë nga njëri-tjetri.
- Dijkstra përdor një radhë me prioritet sipas distancës. BFS përdor një radhë FIFO, dhe fqinjët renditen, që rruga të jetë e njëjtë në çdo ekzekutim.
- Të gjithë përdoruesit lexojnë të njëjtat hapa: rezultatet, mjetet e gjurmimit MCP, animacionet matplotlib dhe shikuesi live.

## Si të ekzekutohet

Nga rrënja e repos (përgatitja është te [përmbajtja e lëndës](../README.md)):

```
uv run python -m unittest discover -s seminar2/tests -t .   # testet
uv run python -m seminar2.tui                               # ndërfaqja e terminalit me të gjitha funksionet
```

### Ndërfaqja e terminalit

Një aplikacion [Textual](https://textual.textualize.io/) që punon në Windows, Linux dhe macOS, edhe me maus. Majtas është lista e veprimeve me kutinë e filtrit; djathtas formulari i opsioneve, butoni Run dhe rezultati. Shiriti i gjendjes tregon adresën e shikuesit live dhe proceset në sfond.

- `↑`/`↓` zgjedhin veprimin; `Enter` hap formularin (ose e ekzekuton nëse s'ka opsione); `Enter` në një fushë e ekzekuton
- `Tab` / `Shift+Tab` lëvizin mes fushave; `Ctrl+R` ekzekuton nga kudo
- `Esc` anulon punën që po ekzekutohet ose kthehet te lista
- `/` filtron, `Ctrl+L` pastron rezultatin, `?` ndihmë (`F1` gjatë shkrimit), `Ctrl+P` paleta e komandave (temat)
- `q` mbyll (jo gjatë shkrimit), `Ctrl+Q` / `Ctrl+C` mbyllin nga kudo

Proceset në sfond (p.sh. shikuesi live) ndalen kur mbyllet aplikacioni.

### Rreshti i komandave

Modulet ekzekutohen me `-m`:

```
uv run python -m seminar2.cities.draw     # shkruan seminar2/images/cities/graph.png
uv run python -m seminar2.maze.draw       # shkruan seminar2/images/maze/maze.png
uv run python -m seminar2.cities.animate  # shkruan seminar2/images/cities/route.gif (--from, --to, --show, --out, --fps)
uv run python -m seminar2.maze.animate    # shkruan seminar2/images/maze/path.gif (--from, --to, --show, --out, --fps)
uv run python -m seminar2.live            # shikuesi live në http://127.0.0.1:8765 me kërkime demo
uv run python seminar2/mcp_server.py      # serveri MCP mbi stdio, bashkë me shikuesin live
uv run python -m seminar2.cities.graph    # printon grafin e qyteteve dhe kontrollet
uv run python -m seminar2.maze.maze       # printon labirintin dhe rezultatin e validimit
```

`--show` hap një dritare matplotlib në vend që të ruajë GIF-in.

## Serveri MCP

Punon mbi stdio. Të dhënat lexohen një herë në nisje, prandaj serveri duhet rinisur pas ndryshimit të CSV-ve.

| Mjeti | Problemi | Qëllimi |
|---|---|---|
| `list_cities` | qytetet | Qytetet dhe sa rrugë ka secili |
| `get_roads(city)` | qytetet | Rrugët direkte nga një qytet, në km (emri nuk varet nga shkronjat e mëdha apo ë/ç) |
| `shortest_route(from_city, to_city)` | qytetet | Rruga më e shkurtër sipas km (Dijkstra) |
| `best_quality_route(from_city, to_city)` | qytetet | Rruga me koston më të ulët km × cilësia e rrugës |
| `trace_route(from_city, to_city, detail=False)` | qytetet | Rruga më e shkurtër me shpjegim hap pas hapi; `detail=True` kthen ngjarjet e plota |
| `get_maze` | labirinti | Hyrja, dalja, dyert dhe fqinjët e çdo dhome |
| `get_doors(room)` | labirinti | Dhomat ku të çojnë dyert e një dhome |
| `find_path(from_room=1, to_room=25)` | labirinti | Rruga me më pak dyer (BFS) |
| `trace_maze(from_room=1, to_room=25, detail=False)` | labirinti | E njëjta rrugë me shpjegim hap pas hapi; `detail=True` kthen ngjarjet e plota |
| `live_viewer()` | të dyja | Adresa e shikuesit live |

Mjetet e kërkimit e luajnë kërkimin edhe në shikuesin live në http://127.0.0.1:8765: fillimisht grafi ndërtohet brinjë pas brinje, pastaj ekzekutohet kërkimi.

- Porta: `SEMINAR2_LIVE_PORT` (parazgjedhja 8765). Çaktivizimi: `SEMINAR2_LIVE=0`.
- Nëse porta e parazgjedhur është e zënë, shikuesi zgjedh një portë të lirë (adresën e jep `live_viewer`). Nëse porta e caktuar me `SEMINAR2_LIVE_PORT` është e zënë, shikuesi çaktivizohet; serveri vazhdon të punojë.

### Lidhja e një klienti

Claude Code: repoja ka një `.mcp.json` për projektin. Nisni `claude` në rrënjën e repos dhe miratoni serverin `seminar2`; mjetet shfaqen si `mcp__seminar2__<tool>`. Kontrolli: `claude mcp list` ose `/mcp`.

Konfigurimi për një klient MCP të përgjithshëm:

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

Për t'i provuar mjetet me dorë: `npx @modelcontextprotocol/inspector uv run python seminar2/mcp_server.py`.
