# Artificial Intelligence / Inteligjenca Artificiale (CIS525)

[![CI](https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale/actions/workflows/ci.yml/badge.svg)](https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale/actions/workflows/ci.yml)

Shqip · [English](README.en.md)

Ushtrimet e seminareve për lëndën Inteligjenca Artificiale (CIS525, UET). Çdo seminar ka dosjen e vet, me README, kod, teste dhe raportin me arsyetimin.

## Seminaret

| Seminari | Tema | Raporti | Gjendja |
|---|---|---|---|
| [Seminari 2](seminar2/README.md) | Kërkimi në graf: rruga më e shkurtër mes qyteteve (Dijkstra) dhe dalja nga labirinti (BFS) | [U1: qytetet](seminar2/cities/arsyetimi.md), [U2: labirinti](seminar2/maze/arsyetimi.md) | E përfunduar |
| [Seminari 3](seminar3/README.md) | Kërkimi A* | – | Në punë |

## Si të lexohet

1. **README e seminarit**: detyra, rezultati dhe figurat, në një faqe.
2. **Raporti** (`arsyetimi.md`): pse u zgjodh algoritmi dhe si arrihet rezultati, hap pas hapi.
3. **Kodi dhe testet**: README e seminarit tregon ku ndodhet secila pjesë.

Gjithçka lexohet direkt në GitHub, pa ekzekutuar asgjë.

## Si të ekzekutohet

Kërkon Python 3.14+ dhe [uv](https://docs.astral.sh/uv/). Komandat ekzekutohen nga rrënja e repos.

```
git clone https://github.com/JonHHH09/CIS525-Artificial-Intelligence-Inteligjenca-Artificiale.git
cd CIS525-Artificial-Intelligence-Inteligjenca-Artificiale
uv sync
uv run python -m unittest discover -s seminar2/tests -t .   # testet konfirmojnë rezultatet e raporteve
uv run python -m seminar2.tui                               # menyja me të gjitha funksionet
```

Komandat e secilit seminar janë në README-në e tij.

## Struktura

```
seminar2/        Kërkimi në graf (U1 qytetet, U2 labirinti)
  cities/        U1: ngarkimi i grafit, rruga sipas cilësisë, figurat, raporti
  maze/          U2: ngarkimi i labirintit, figurat, raporti
  dataset/       të dhënat CSV
  images/        figurat dhe animacionet e gjeneruara
  tests/         testet (unittest)
seminar3/        Kërkimi A* (kodi fillestar)
pyproject.toml   varësitë (uv)
```

## Zhvillimi

- Lint: `uvx ruff@0.17.3 check .` (konfigurimi në `pyproject.toml`).
- CI (GitHub Actions) ekzekuton ruff dhe testet në Ubuntu dhe Windows.
- Puna bëhet në degë të veçanta me PR drejt `development`; `development` kalon në `main` me një PR publikimi.

Licenca: [MIT](LICENSE).
