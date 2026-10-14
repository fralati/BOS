# cliCHair · pagina "Chi siamo" (About us) v2.1 · 14.10.2026

Riscrittura completa della pagina `about-us` (`gid://shopify/Page/686209073533`) nelle 4 lingue.
Stato: **pubblicata il 14.10.2026** (ok di Francesco), poi **corretta sul tema reale e ripubblicata lo stesso giorno (v2.1)**: EN con `pageUpdate`, IT/DE/FR con `translationsRegister`, tutte `outdated: false`. Confronto fatto fra i corpi salvati su Shopify e i file in `dist/`: testi, CSS, 28 link, 30 icone e i 24 spazi unificatori francesi identici (Shopify riformatta solo gli a capo e scrive `viewbox` in minuscolo, che i browser gestiscono).

## Correzioni v2.1 (dagli screenshot live di Francesco)

| Difetto sul sito | Causa nel tema | Correzione in `build.py` |
|---|---|---|
| Pulsanti neri con testo invisibile | `.page-content a{color:currentcolor}` del tema vince sul colore del pulsante | tutte le dichiarazioni del blocco `<style>` escono con `!important` (post-processore `important()`), colori espliciti sui pulsanti |
| Titoli neri su schede e pannelli scuri | `h3{color:var(--color)}` del tema | colore esplicito (`#fff`) su ogni `h3` dentro `.cca-pillar-dark`, `.cca-step-dark`, `.cca-aud`, pannello scuro |
| Elenchi rientrati con striscia grigia | `.rte ul{padding-inline-start}` e reset del tema | reset con `:where()` (specificità zero) più `!important` |
| Spazi grandi dopo le etichette di sezione | `.rte :is(h1..h6){margin-block}` | margini dei titoli in classi proprie (`.cca-t`, `.cca-mt26`, `.cca-mb26`, `.cca-mb28`), niente stili inline |
| Pagina stretta su schermi grandi | sezione `main-page` con classe `page-width-content` (colonna di lettura da 42rem) | il contenitore `.cca` esce dalla colonna con `width:calc(100vw - 24px)` e `margin-left:calc(50% - 50vw + 12px)`, gutter propri (`--cca-g`) e larghezza massima del contenuto 1360 px |
| Testi a sinistra con vuoto a destra sui monitor larghi | colonne a testo singolo | pannello scuro: i due paragrafi introduttivi affiancati su due colonne (`.cca-panel-intro`), terzo paragrafo a 80ch; sezione team in due colonne (titolo a sinistra, ruoli + testo + pulsante a destra) come le altre sezioni |

Sotto 1000 px le due colonne tornano una; sotto 640 px valgono le regole mobile già presenti. Gli screenshot in `shots/` sono a 1280, 1920 e 390 px.

L'anteprima locale (`preview/*.html`) riproduce la colonna stretta del tema (752 px) e le sue regole in conflitto (`.page-content a`, `h3{color}`, `.rte ul`, `.rte :is(h1..h6)`), così un difetto di specificità si vede prima di pubblicare. Non è il tema reale: il controllo finale resta sul sito.

## File

| Percorso | Cosa contiene |
|---|---|
| `build.py` | Generatore: un solo markup, CSS con prefisso `cca-`, testi EN/IT/DE/FR, link con prefisso lingua, controlli automatici (niente trattini lunghi, niente parole vietate, niente `ß`, grafia `cliCHair`/`clichAIr`). |
| `dist/about-us.en.html` | `body_html` da caricare con `pageUpdate` (lingua primaria). |
| `dist/about-us.{it,de,fr}.html` | Traduzioni da registrare con `translationsRegister` (chiave `body_html`). |
| `preview/*.html` | Anteprima locale con una cornice che imita il tema: colonna stretta da 752 px, titolo pagina, divisore, footer e le regole CSS del tema che entrano in conflitto con la pagina. Non è il tema reale. |
| `shot.mjs` | Screenshot Playwright desktop 1280, wide 1920 e mobile 390, con controlli numerici (scroll orizzontale, errori JS, colonne delle griglie, numero di link). |
| `shots/*.png` | Screenshot a pagina intera delle 4 lingue nei tre formati. |
| `backup-2026-10-14/` | Corpo live delle 4 lingue prima della modifica (versione del 25.09.2026). |

Rigenerare: `python3 build.py && node shot.mjs`.

## Struttura della pagina

Hero (tre parole: Intelligente. Innovativa. Imparziale. + 6 fatti verificabili) ·
01 Tre parole (tre pilastri con prove concrete, Imparziale in evidenza) ·
02 Il metodo (ciclo in 4 passi, testi approvati il 25.09) ·
03 L'origine (timeline 2018 → piattaforma → clichAIr → oggi) ·
04 La piattaforma (pannello scuro, schema hub marchi → cliCHair → persone, 6 profili: saloni, privati, scuole, distributori, negozi online, partner) ·
05 Il principio (profondità, marchi NIKA / Code Zero / Edelstein) ·
06 Il motore clichAIr (salone / privato, "L'AI non decide da sola") ·
07 Gli strumenti (8 schede: ordine rapido, calcolatore colore, pannello redditività, costo per utilizzo, account, pagamenti, abbonamenti, aggiornamenti) ·
08 Il valore · 09 La formazione · 10 Protocollo ECO · 11 Il team · 12 Scegli il tuo accesso.

## Fonti dei fatti

Tutti i fatti vengono da pagine già pubblicate: policy Spedizioni e Resi, policy Abbonamenti, footer (pagamenti, 24/7), pagina Professionisti (verifica in 24 ore, nessun minimo), pagina Rivenditori, pagina Collaborazioni, pagina Sostenibilità (DHL GoGreen, Shopify Planet, imballaggi), pagina Aggiornamenti (strumenti PRO live), pagina Chi siamo precedente (origine, metodo, team).

Numeri che dipendono dalla policy di spedizione e dal footer (da aggiornare insieme se cambiano): CHF 99, ore 12:00, 14 giorni per i resi, 24 ore per la verifica PRO.

## Cosa è stato tolto rispetto alla pagina precedente

- "cruelty-free" (parola vietata dalle regole UWG/LCD della Knowledge Base) e "carbon-neutral" (sostituito con "emissioni compensate tramite DHL GoGreen e Shopify Planet", come nella policy).
- "ti passa alla persona giusta" → "passa la mano al nostro team" (modello AI-first del 9.10.2026, nessuna persona nominata).
- Il claim "+20% di margine" resta fuori da questa pagina (appartiene a /pages/professionals).

## Pubblicazione (procedura usata il 14.10.2026, due volte, da ripetere a ogni modifica)

1. Salvare i backup DE e FR (`translatableResource.translations(locale:)`).
2. `pageUpdate(id, page: {body: $body})` con il contenuto di `dist/about-us.en.html` nella variabile `$body`.
3. Rileggere `translatableResource` per il digest fresco di `body_html`.
4. `translationsRegister` per IT, DE, FR, una lingua per chiamata, corpo nella variabile, `translatableContentDigest` = digest appena letto; controllare `outdated: false`.
5. Verificare `/pages/about-us`, `/it/pages/about-us`, `/de/pages/about-us`, `/fr/pages/about-us` nel browser (desktop e iPhone), Zipchat badge in basso a sinistra non coperto.
6. Mai risalvare la pagina dall'editor visuale: toglie il blocco `<style>`.

Meta title e meta description (metafield `global.title_tag` / `global.description_tag` e traduzioni) non sono stati toccati.
