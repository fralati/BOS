# cliCHair · pagina "Chi siamo" (About us) v2 · 14.10.2026

Riscrittura completa della pagina `about-us` (`gid://shopify/Page/686209073533`) nelle 4 lingue.
Stato: **pronta, non ancora pubblicata**. La pagina live è invariata finché Francesco non approva il testo italiano.

## File

| Percorso | Cosa contiene |
|---|---|
| `build.py` | Generatore: un solo markup, CSS con prefisso `cca-`, testi EN/IT/DE/FR, link con prefisso lingua, controlli automatici (niente trattini lunghi, niente parole vietate, niente `ß`, grafia `cliCHair`/`clichAIr`). |
| `dist/about-us.en.html` | `body_html` da caricare con `pageUpdate` (lingua primaria). |
| `dist/about-us.{it,de,fr}.html` | Traduzioni da registrare con `translationsRegister` (chiave `body_html`). |
| `preview/*.html` | Anteprima locale con una cornice simile al tema (titolo pagina, divisore, footer). Non è il tema reale. |
| `shot.mjs` | Screenshot Playwright desktop 1280 e mobile 390, con controlli numerici (scroll orizzontale, errori JS). |
| `shots/*.png` | Screenshot a pagina intera delle 4 lingue. |
| `backup-2026-10-14/` | Corpo live EN e IT prima della modifica (DE e FR restano leggibili su Shopify finché la pagina non viene sovrascritta: salvarli prima di pubblicare). |

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

## Pubblicazione (dopo l'ok di Francesco)

1. Salvare i backup DE e FR (`translatableResource.translations(locale:)`).
2. `pageUpdate(id, page: {body: $body})` con il contenuto di `dist/about-us.en.html` nella variabile `$body`.
3. Rileggere `translatableResource` per il digest fresco di `body_html`.
4. `translationsRegister` per IT, DE, FR, una lingua per chiamata, corpo nella variabile, `translatableContentDigest` = digest appena letto; controllare `outdated: false`.
5. Verificare `/pages/about-us`, `/it/pages/about-us`, `/de/pages/about-us`, `/fr/pages/about-us` nel browser (desktop e iPhone), Zipchat badge in basso a sinistra non coperto.
6. Mai risalvare la pagina dall'editor visuale: toglie il blocco `<style>`.

Meta title e meta description (metafield `global.title_tag` / `global.description_tag` e traduzioni) non sono stati toccati.
