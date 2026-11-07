# Språk MN/KZ – mongolsk og kasakhisk

Leksjoner, øvelser og flashcards i mongolsk og kasakhisk. Appen er én HTML-fil som virker uten nett etter første åpning og kan installeres på mobilen som en app.

## Filene

| Fil | Hva den gjør |
|---|---|
| `index.html` | Hele appen (innhold, øvelser, fremgang) |
| `manifest.webmanifest` | Navn, farger og ikon når appen installeres |
| `sw.js` | Gjør at appen virker uten nett og henter nye versjoner |
| `icon-*.png`, `apple-touch-icon.png` | App-ikonene |
| `.nojekyll` | Sier til GitHub at filene skal vises som de er |

## Legge appen ut på GitHub Pages (første gang)

1. Logg inn på github.com og trykk **New repository** (grønn knapp).
2. Gi den et navn, f.eks. `sprak`. Velg **Public**. Trykk **Create repository**.
3. Trykk **uploading an existing file**, og dra inn **alle filene i denne mappa** (også `.nojekyll`). Trykk **Commit changes**.
4. Gå til **Settings → Pages**. Under *Build and deployment* velger du **Deploy from a branch**, branch **main** og mappe **/ (root)**. Trykk **Save**.
5. Etter 1–2 minutter står adressen øverst på siden, f.eks. `https://brukernavn.github.io/sprak/`.

Lenker direkte til ett språk:
- Mongolsk: `https://brukernavn.github.io/sprak/#lang=mn`
- Kasakhisk: `https://brukernavn.github.io/sprak/#lang=kz`

## Installere på mobilen

- **Android (Chrome):** åpne lenken → meny ⋮ → **Installer app** / **Legg til på startskjermen**.
- **iPhone (Safari):** åpne lenken → Del-knappen → **Legg til på Hjem-skjerm**.

## Oppdatere appen

1. Åpne repoet på GitHub og trykk **Add file → Upload files**.
2. Dra inn den nye `index.html` (og `sw.js` hvis den er med). Trykk **Commit changes**.
3. Brukerne får den nye versjonen automatisk neste gang de åpner appen med nett. Fremgangen deres blir liggende.
