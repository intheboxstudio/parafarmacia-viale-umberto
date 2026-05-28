#!/usr/bin/env python3
"""
patch_index_html.py
===================

Applica modifiche idempotenti a index.html della Parafarmacia Viale Umberto 1°.

Patch incluse:
  1. Cache-buster sul fetch di articles.json (blog non si aggiornava perché
     GitHub Pages serve i JSON con cache CDN aggressiva).
  2. Orari mercoledì allineati a lun/mar/ven/sab (15:30–19:30) + footer
     riordinato (Lun, Mar, Mer, Ven, Sab insieme).
  3. Menu mobile ridisegnato (full-screen overlay scrollabile, tipografia
     pulita, blocco scroll del body, anti-overlap con la nav).
  4. Aggiunta sezione "Stanze per consulenze" nella pagina servizi (con
     mini-modulo email che pre-compila l'oggetto).
  5. Aggiunta sezione "Pane Primus" nella home (sotto i brand, prima della
     CTA finale).
  6. Servizi rivisti: Naturopata sostituisce Shiatsu, Farmacista-Cosmetologa
     sostituisce Meditazione dei Chakra.
  7. Marquee, frase contatti e meta description aggiornati di conseguenza.

Lo script è IDEMPOTENTE: se una patch è già stata applicata, la salta.
Fa sempre un backup .bak prima di toccare nulla.

Uso:
    python patch_index_html.py path/to/index.html
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Callable


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 1 — CACHE BUSTER SU articles.json
# ═══════════════════════════════════════════════════════════════════════════════

P1_OLD = """  try{
    const res = await fetch(BLOG_ARTICLES_URL, { cache: 'no-store' });
    if(!res.ok) throw new Error('Fetch failed');"""

P1_NEW = """  try{
    // Cache buster: GitHub Pages e il CDN davanti servono spesso
    // articles.json dalla cache anche dopo che l'agente AI ha pushato
    // la nuova versione. Il timestamp forza una richiesta fresca.
    const cacheBuster = Date.now();
    const res = await fetch(BLOG_ARTICLES_URL + '?_=' + cacheBuster, { cache: 'no-store' });
    if(!res.ok) throw new Error('Fetch failed');"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 2 — ORARI MERCOLEDÌ (allinea a lun/mar/ven/sab)
# ═══════════════════════════════════════════════════════════════════════════════

P2_OLD = """          <div class=\"hours-row\">
            <span>Mercoledì</span>
            <div class=\"time-stack\">9:00 — 13:00<br>15:30 — 19:00</div>
          </div>"""

P2_NEW = """          <div class=\"hours-row\">
            <span>Mercoledì</span>
            <div class=\"time-stack\">9:00 — 13:00<br>15:30 — 19:30</div>
          </div>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 3 — FOOTER ORARI (Mer accorpato a Lun/Mar/Ven/Sab)
# ═══════════════════════════════════════════════════════════════════════════════

P3_OLD = """      <div class=\"footer-col\">
        <h5>Orari</h5>
        <ul>
          <li>Lun, Mar, Ven, Sab<br>9:00 – 13:00 / 15:30 – 19:30</li>
          <li>Mercoledì<br>9:00 – 13:00 / 15:30 – 19:00</li>
          <li>Giovedì<br>9:00 – 13:00 (solo mattina)</li>
          <li>Domenica · chiuso</li>
        </ul>
      </div>"""

P3_NEW = """      <div class=\"footer-col\">
        <h5>Orari</h5>
        <ul>
          <li>Lun, Mar, Mer, Ven, Sab<br>9:00 – 13:00 / 15:30 – 19:30</li>
          <li>Giovedì<br>9:00 – 13:00 (solo mattina)</li>
          <li>Domenica · chiuso</li>
        </ul>
      </div>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 4 — MENU MOBILE (CSS + JS)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Problema attuale: `inset: 70px 0 0 0` lascia 70px scoperti in alto, ma
# l'header in scrolled mode è più alto e il menu finisce sotto la nav,
# tagliando il primo link. `justify-content: center` con 7 voci e font
# da 22px su iPhone SE significa che il testo trabocca o si stira male.
# `gap: 30px` non basta come spacing strutturato.
#
# Nuovo design: overlay full-screen con padding-top per evitare la nav,
# link impilati con bordino di separazione, CTA centrato a fondo lista,
# overflow-y: auto per i telefoni più corti, scroll del body bloccato.

P4_CSS_OLD = """@media (max-width: 980px){
  .menu{
    position: fixed; inset: 70px 0 0 0;
    background: var(--avorio);
    flex-direction: column;
    justify-content: center;
    gap: 30px;
    transform: translateX(100%);
    transition: transform .4s ease;
  }
  .menu.open{ transform: translateX(0); }
  .menu a{ font-size: 22px; font-family: var(--display); }
  .burger{ display: flex; }
}"""

P4_CSS_NEW = """@media (max-width: 980px){
  .menu{
    position: fixed;
    top: 0; right: 0; bottom: 0; left: 0;
    background: var(--azzurro-aria);
    flex-direction: column;
    align-items: stretch;
    justify-content: flex-start;
    gap: 0;
    padding: 96px 28px 40px;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    transform: translateX(100%);
    transition: transform .35s ease;
    z-index: 90;
    box-shadow: -20px 0 60px rgba(31,58,77,.08);
  }
  .menu.open{ transform: translateX(0); }
  .menu a{
    font-size: 22px;
    font-family: var(--display);
    font-weight: 400;
    color: var(--inchiostro);
    padding: 18px 4px;
    border-bottom: 1px solid rgba(31,58,77,.08);
    width: 100%;
    text-align: left;
    letter-spacing: -.01em;
  }
  .menu a::after{ display: none; }
  .menu a.active{ color: var(--azzurro-deep); }
  .menu a.menu-cta{
    margin-top: 28px;
    padding: 14px 26px !important;
    border-bottom: none;
    align-self: center;
    width: auto;
    min-width: 200px;
    text-align: center;
    font-family: var(--body);
    font-size: 14px !important;
  }
  .burger{ display: flex; position: relative; z-index: 100; }
  body.menu-open{ overflow: hidden; }
}

@media (max-width: 420px){
  .menu{ padding: 88px 22px 32px; }
  .menu a{ font-size: 19px; padding: 16px 2px; }
}"""


P4_JS_OLD = """/* ============== BURGER ============== */
document.getElementById('burger').addEventListener('click', () => {
  document.getElementById('menu').classList.toggle('open');
  document.getElementById('burger').classList.toggle('open');
});"""

P4_JS_NEW = """/* ============== BURGER ============== */
document.getElementById('burger').addEventListener('click', () => {
  const menu = document.getElementById('menu');
  const burger = document.getElementById('burger');
  const willOpen = !menu.classList.contains('open');
  menu.classList.toggle('open', willOpen);
  burger.classList.toggle('open', willOpen);
  // Blocca lo scroll del body quando il menu è aperto (mobile).
  document.body.classList.toggle('menu-open', willOpen);
});"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 5 — SEZIONE "STANZE PER CONSULENZE" (pagina servizi)
# ═══════════════════════════════════════════════════════════════════════════════
#
# La inseriamo nella pagina servizi, subito prima della <!-- CTA -->.
# Include un mini-form mailto: che pre-compila oggetto e corpo email
# verso parafarmaciavialeumberto@gmail.com — niente backend richiesto.

P5_ANCHOR = """      </article>

    </div>
  </section>

  <!-- CTA -->
  <section class=\"cta-section\">
    <div class=\"wrap\">
      <h2>Prenota una <em>sessione</em></h2>"""

P5_NEW = """      </article>

    </div>
  </section>

  <!-- =============== STANZE PER CONSULENZE =============== -->
  <section class=\"rooms-section\">
    <div class=\"wrap\">
      <div class=\"rooms-header reveal\">
        <span class=\"eyebrow\">Spazi a disposizione</span>
        <h2>Due stanze per le tue <em>consulenze</em>.</h2>
        <p class=\"lead\">La Parafarmacia Viale Umberto 1° mette a disposizione due stanze attrezzate, affittabili a ore. Pensate per professionisti del benessere — naturopati, nutrizionisti, osteopati, counsellor — che cercano uno spazio luminoso, riservato e in centro a Reggio Emilia.</p>
      </div>

      <div class=\"rooms-grid\">
        <div class=\"room-card reveal\">
          <div class=\"room-num\">STANZA 01</div>
          <h3>La stanza <em>luminosa</em></h3>
          <p>Lettino professionale, scrivania, due poltrone per la consulenza. Luce naturale dalla finestra su viale Umberto, riscaldamento autonomo. Ideale per consulenze nutrizionali, naturopatiche e colloqui.</p>
          <ul>
            <li>Circa 14 m², insonorizzata</li>
            <li>Lettino + scrivania + due poltrone</li>
            <li>Wi-Fi e accesso autonomo</li>
            <li>Sala d'attesa condivisa</li>
          </ul>
        </div>

        <div class=\"room-card reveal\">
          <div class=\"room-num\">STANZA 02</div>
          <h3>La stanza <em>raccolta</em></h3>
          <p>Più piccola e silenziosa, perfetta per sedute one-to-one. Arredata con sobrietà — un tavolo, due sedute, una lampada calda — per chi lavora di parola, di ascolto, di tempo lento.</p>
          <ul>
            <li>Circa 10 m², zona quiet</li>
            <li>Arredo essenziale e luce calda</li>
            <li>Wi-Fi e clima autonomo</li>
            <li>Accesso indipendente dall'esercizio</li>
          </ul>
        </div>
      </div>

      <div class=\"rooms-cta reveal\">
        <h3>Scrivici per <em>disponibilità e tariffe</em>.</h3>
        <p>Affittiamo a ore, mezza giornata o giornata intera. La modalità più semplice è una mail veloce con i tuoi orari: ti rispondiamo entro 24h.</p>

        <form class=\"rooms-form\" id=\"roomsForm\" onsubmit=\"return submitRoomsForm(event)\">
          <div class=\"field\">
            <label for=\"roomsName\">Il tuo nome e attività</label>
            <input type=\"text\" id=\"roomsName\" name=\"name\" placeholder=\"Mario Rossi — Naturopata\" required>
          </div>
          <div class=\"field\">
            <label for=\"roomsContact\">Email o telefono</label>
            <input type=\"text\" id=\"roomsContact\" name=\"contact\" placeholder=\"mario@example.com\" required>
          </div>
          <div class=\"field\">
            <label for=\"roomsMessage\">Quando ti servirebbe?</label>
            <textarea id=\"roomsMessage\" name=\"message\" rows=\"4\" placeholder=\"Indicativamente: giorni della settimana, fasce orarie, una stanza o entrambe...\" required></textarea>
          </div>
          <div class=\"field-action\">
            <button type=\"submit\" class=\"btn btn-primary\">Invia la richiesta <span class=\"arrow\">→</span></button>
            <span class=\"field-hint\">Aprirà la tua app email con tutto pronto.</span>
          </div>
        </form>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class=\"cta-section\">
    <div class=\"wrap\">
      <h2>Prenota una <em>sessione</em></h2>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 6 — SEZIONE "PANE PRIMUS" (home)
# ═══════════════════════════════════════════════════════════════════════════════
#
# La inseriamo nella home dopo i brands, prima della CTA finale.
# Niente foto inline (path da fornire poi): placeholder grafico SVG +
# blocco che riconosce automaticamente assets/primus.jpg se esiste,
# altrimenti mostra il decor SVG di fallback.

P6_ANCHOR = """  <!-- CTA FINALE HOME -->
  <section class=\"cta-section\">
    <div class=\"wrap\">
      <h2>Hai una domanda? <em>Ti aspettiamo.</em></h2>"""

P6_NEW = """  <!-- =============== PUNTO VENDITA PANE PRIMUS =============== -->
  <section class=\"primus-section\">
    <div class=\"wrap\">
      <div class=\"primus-grid\">
        <div class=\"primus-image reveal\">
          <div class=\"primus-img-wrap\">
            <!-- Sostituisci src con assets/primus.jpg quando hai la foto -->
            <img src=\"assets/primus.jpg\" alt=\"Pane Primus — Parafarmacia Viale Umberto 1°\"
                 onerror=\"this.style.display='none'; this.parentElement.classList.add('no-img');\"
                 loading=\"lazy\"/>
            <div class=\"primus-img-placeholder\">
              <svg viewBox=\"0 0 200 200\" fill=\"none\">
                <ellipse cx=\"100\" cy=\"120\" rx=\"72\" ry=\"42\" fill=\"#E8C99B\" opacity=\".6\"/>
                <ellipse cx=\"100\" cy=\"108\" rx=\"68\" ry=\"38\" fill=\"#D4A574\" stroke=\"#8B5E34\" stroke-width=\"1.5\"/>
                <path d=\"M50 100 Q 100 70 150 100\" stroke=\"#8B5E34\" stroke-width=\"1.2\" fill=\"none\" stroke-dasharray=\"3 4\"/>
                <path d=\"M60 112 Q 100 90 140 112\" stroke=\"#8B5E34\" stroke-width=\"1\" fill=\"none\" stroke-dasharray=\"2 3\" opacity=\".7\"/>
                <text x=\"100\" y=\"170\" text-anchor=\"middle\" font-family=\"Fraunces\" font-size=\"12\" font-style=\"italic\" fill=\"#8B5E34\">Primus</text>
              </svg>
            </div>
          </div>
        </div>

        <div class=\"primus-text reveal\">
          <span class=\"eyebrow\">Punto vendita autorizzato</span>
          <h2>Il <em>Pane Primus</em>. Un grano antico, una digestione leggera.</h2>
          <p>Da noi trovi il <strong>Pane Primus</strong>: prodotto con la farina del grano tenero <em>Primus</em>, una varietà a basso indice di glutine e ricca di fibre, lievitata naturalmente a pasta madre per oltre 24 ore.</p>
          <p>Sapore deciso, mollica fitta, crosta croccante. Non è un pane "light" — è un pane <em>vero</em>, fatto come una volta, che resta morbido per giorni e si digerisce con leggerezza anche per chi tende a sentirsi appesantito dopo i pasti.</p>
          <ul class=\"primus-features\">
            <li><strong>Farina di grano Primus</strong> a basso indice glicemico</li>
            <li><strong>Lievito madre</strong> e fermentazione lunga (24h+)</li>
            <li><strong>Senza additivi</strong>, senza zuccheri aggiunti, senza grassi</li>
            <li><strong>Consigliato</strong> a chi cerca digeribilità senza rinunciare al gusto</li>
          </ul>
          <div class=\"primus-cta-row\">
            <a href=\"#contatti\" data-page=\"contatti\" class=\"btn btn-primary\">Vieni a trovarci <span class=\"arrow\">→</span></a>
            <a href=\"tel:0522081652\" class=\"btn btn-secondary\">0522 081652</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA FINALE HOME -->
  <section class=\"cta-section\">
    <div class=\"wrap\">
      <h2>Hai una domanda? <em>Ti aspettiamo.</em></h2>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 7 — SERVIZIO 02: SHIATSU → NATUROPATA
# ═══════════════════════════════════════════════════════════════════════════════

P7_OLD = """      <!-- SERVIZIO 2: SHIATSU -->
      <article class=\"service reveal\">
        <div>
          <div class=\"service-num\">SERVIZIO 02</div>
          <h2>Massaggi <em>Shiatsu</em></h2>
          <p>Lo Shiatsu nasce in Giappone e parla la lingua del corpo. Pressioni profonde, lente, intenzionali — sui meridiani energetici, lì dove la tensione si annida senza che ce ne accorgiamo.</p>
          <p>Non è un massaggio rilassante, è una pratica terapeutica. Esci dalla sessione con la sensazione fisica di esserti rimesso in asse.</p>
          <ul>
            <li>Sessioni individuali da 60 o 90 minuti</li>
            <li>Trattamento mirato su tensioni specifiche</li>
            <li>Riequilibrio energetico secondo MTC</li>
            <li>Indicato per stress cronico, cervicalgie, insonnia</li>
            <li>Operatore qualificato, su appuntamento</li>
          </ul>
        </div>
        <div class=\"service-visual var-2\">
          <svg viewBox=\"0 0 200 200\" fill=\"none\">
            <circle cx=\"100\" cy=\"100\" r=\"65\" stroke=\"#1F3A4D\" stroke-width=\"1.5\"/>
            <circle cx=\"100\" cy=\"100\" r=\"40\" stroke=\"#1F3A4D\" stroke-width=\"1\" stroke-dasharray=\"2 4\"/>
            <path d=\"M100 60 Q 130 100 100 140 Q 70 100 100 60\" fill=\"#1F3A4D\" opacity=\".18\"/>
            <circle cx=\"100\" cy=\"80\" r=\"4\" fill=\"#1F3A4D\"/>
            <circle cx=\"100\" cy=\"120\" r=\"4\" fill=\"#1F3A4D\"/>
            <path d=\"M60 100 L 80 100 M 120 100 L 140 100\" stroke=\"#1F3A4D\" stroke-width=\"2\"/>
            <text x=\"100\" y=\"180\" text-anchor=\"middle\" font-family=\"Fraunces\" font-size=\"11\" font-style=\"italic\" fill=\"#4A7894\">harmony</text>
          </svg>
        </div>
      </article>"""

P7_NEW = """      <!-- SERVIZIO 2: NATUROPATA -->
      <article class=\"service reveal\">
        <div>
          <div class=\"service-num\">SERVIZIO 02</div>
          <h2>Consulenza <em>naturopatica</em></h2>
          <p>La naturopatia guarda alla persona intera — non solo al sintomo. Stress, stanchezza cronica, intestino capriccioso, sonno difficile: ogni squilibrio racconta una storia, e nella maggior parte dei casi la racconta partendo da abitudini che possiamo correggere.</p>
          <p>La nostra naturopata costruisce percorsi su misura: fitoterapia, integrazione mirata, gestione dello stress, alimentazione funzionale. Niente miracoli, solo strumenti naturali usati con metodo.</p>
          <ul>
            <li>Anamnesi completa e valutazione iridologica</li>
            <li>Percorsi personalizzati di fitoterapia e integrazione</li>
            <li>Gestione di stress, sonno, energia e digestione</li>
            <li>Supporto in menopausa, ciclo, cambi di stagione</li>
            <li>Approccio integrato con il medico curante</li>
          </ul>
        </div>
        <div class=\"service-visual var-2\">
          <svg viewBox=\"0 0 200 200\" fill=\"none\">
            <circle cx=\"100\" cy=\"100\" r=\"68\" stroke=\"#1F3A4D\" stroke-width=\"1.5\"/>
            <path d=\"M100 50 Q 100 80 100 100 M100 100 Q 75 95 65 75 M100 100 Q 125 95 135 75 M100 100 Q 80 115 75 135 M100 100 Q 120 115 125 135\"
                  stroke=\"#1F3A4D\" stroke-width=\"1.5\" stroke-linecap=\"round\" fill=\"none\"/>
            <circle cx=\"100\" cy=\"50\" r=\"4\" fill=\"#A2B891\"/>
            <circle cx=\"65\" cy=\"75\" r=\"3.5\" fill=\"#A2B891\"/>
            <circle cx=\"135\" cy=\"75\" r=\"3.5\" fill=\"#A2B891\"/>
            <circle cx=\"75\" cy=\"135\" r=\"3.5\" fill=\"#A2B891\"/>
            <circle cx=\"125\" cy=\"135\" r=\"3.5\" fill=\"#A2B891\"/>
            <circle cx=\"100\" cy=\"100\" r=\"5\" fill=\"#1F3A4D\"/>
            <text x=\"100\" y=\"180\" text-anchor=\"middle\" font-family=\"Fraunces\" font-size=\"11\" font-style=\"italic\" fill=\"#4A7894\">natura</text>
          </svg>
        </div>
      </article>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 8 — SERVIZIO 03: CHAKRA → FARMACISTA-COSMETOLOGA
# ═══════════════════════════════════════════════════════════════════════════════

P8_OLD = """      <!-- SERVIZIO 3: CHAKRA -->
      <article class=\"service reveal\">
        <div>
          <div class=\"service-num\">SERVIZIO 03</div>
          <h2>Meditazione dei <em>Chakra</em></h2>
          <p>Sette centri energetici, dalla base della colonna alla sommità del capo. La tradizione yogica ne fa una mappa dell'essere — noi la usiamo come bussola per ritrovare il centro, dopo settimane in cui l'abbiamo perso.</p>
          <p>Sessioni guidate, in piccoli gruppi o individuali. Niente esoterismo: pratica concreta, respiro, consapevolezza.</p>
          <ul>
            <li>Meditazioni guidate sui sette chakra</li>
            <li>Tecniche di respirazione (pranayama)</li>
            <li>Visualizzazioni cromatiche e suoni armonici</li>
            <li>Sessioni in gruppo o personali</li>
            <li>Approccio laico, accessibile a tutti</li>
          </ul>
        </div>
        <div class=\"service-visual var-3\">
          <svg viewBox=\"0 0 200 200\" fill=\"none\">
            <circle cx=\"100\" cy=\"40\" r=\"6\" fill=\"#9B7BC7\"/>
            <circle cx=\"100\" cy=\"62\" r=\"6\" fill=\"#5B7CC7\"/>
            <circle cx=\"100\" cy=\"84\" r=\"6\" fill=\"#5BA8E0\"/>
            <circle cx=\"100\" cy=\"106\" r=\"6\" fill=\"#5BC78C\"/>
            <circle cx=\"100\" cy=\"128\" r=\"6\" fill=\"#E8C95B\"/>
            <circle cx=\"100\" cy=\"150\" r=\"6\" fill=\"#E8945B\"/>
            <circle cx=\"100\" cy=\"172\" r=\"6\" fill=\"#C75B5B\"/>
            <line x1=\"100\" y1=\"46\" x2=\"100\" y2=\"166\" stroke=\"#1F3A4D\" stroke-width=\"1\" opacity=\".3\"/>
          </svg>
        </div>
      </article>"""

P8_NEW = """      <!-- SERVIZIO 3: FARMACISTA-COSMETOLOGA -->
      <article class=\"service reveal\">
        <div>
          <div class=\"service-num\">SERVIZIO 03</div>
          <h2>Farmacista <em>cosmetologa</em></h2>
          <p>Non c'è una crema "giusta" in assoluto. C'è la crema giusta <em>per la tua pelle</em>, in <em>questo</em> momento della tua vita, con <em>queste</em> esigenze. Per arrivarci serve sapere cosa cercare — e cosa evitare.</p>
          <p>La nostra farmacista cosmetologa analizza la pelle, legge gli INCI, smonta le formulazioni e ricostruisce con te una routine che funziona davvero: niente prodotti inutili, niente promesse esagerate, solo ciò che la pelle chiede.</p>
          <ul>
            <li>Analisi della pelle e diagnosi cosmetica</li>
            <li>Lettura critica degli INCI dei tuoi prodotti</li>
            <li>Routine personalizzata viso, corpo, capelli</li>
            <li>Soluzioni per acne, couperose, macchie, antiaging</li>
            <li>Consigli su attivi cosmeceutici e dermocosmesi</li>
          </ul>
        </div>
        <div class=\"service-visual var-3\">
          <svg viewBox=\"0 0 200 200\" fill=\"none\">
            <circle cx=\"100\" cy=\"100\" r=\"72\" stroke=\"#1F3A4D\" stroke-width=\"1.5\"/>
            <rect x=\"82\" y=\"55\" width=\"36\" height=\"60\" rx=\"4\" stroke=\"#1F3A4D\" stroke-width=\"1.5\" fill=\"#EFC5BC\" opacity=\".4\"/>
            <rect x=\"86\" y=\"45\" width=\"28\" height=\"12\" rx=\"2\" stroke=\"#1F3A4D\" stroke-width=\"1.5\" fill=\"none\"/>
            <line x1=\"88\" y1=\"75\" x2=\"112\" y2=\"75\" stroke=\"#1F3A4D\" stroke-width=\"1\" opacity=\".6\"/>
            <line x1=\"88\" y1=\"85\" x2=\"108\" y2=\"85\" stroke=\"#1F3A4D\" stroke-width=\"1\" opacity=\".6\"/>
            <line x1=\"88\" y1=\"95\" x2=\"112\" y2=\"95\" stroke=\"#1F3A4D\" stroke-width=\"1\" opacity=\".6\"/>
            <circle cx=\"100\" cy=\"135\" r=\"8\" stroke=\"#1F3A4D\" stroke-width=\"1.5\" fill=\"#A2B891\" opacity=\".5\"/>
            <path d=\"M100 127 Q 105 130 100 135 Q 95 130 100 127\" fill=\"#1F3A4D\"/>
            <text x=\"100\" y=\"180\" text-anchor=\"middle\" font-family=\"Fraunces\" font-size=\"11\" font-style=\"italic\" fill=\"#4A7894\">essentia</text>
          </svg>
        </div>
      </article>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 9 — MARQUEE (rimuove Shiatsu/Meditazione, aggiunge Naturopatia/Primus)
# ═══════════════════════════════════════════════════════════════════════════════

P9_OLD = """      <span>Fitoterapia</span><span>Erboristeria</span><span>Cosmesi naturale</span><span>Omeopatia</span><span>Tisane artigianali</span><span>Consulenze nutrizionali</span><span>Massaggi Shiatsu</span><span>Meditazione</span>
      <span>Fitoterapia</span><span>Erboristeria</span><span>Cosmesi naturale</span><span>Omeopatia</span><span>Tisane artigianali</span><span>Consulenze nutrizionali</span><span>Massaggi Shiatsu</span><span>Meditazione</span>"""

P9_NEW = """      <span>Fitoterapia</span><span>Erboristeria</span><span>Cosmesi naturale</span><span>Omeopatia</span><span>Tisane artigianali</span><span>Naturopatia</span><span>Cosmetologia</span><span>Pane Primus</span>
      <span>Fitoterapia</span><span>Erboristeria</span><span>Cosmesi naturale</span><span>Omeopatia</span><span>Tisane artigianali</span><span>Naturopatia</span><span>Cosmetologia</span><span>Pane Primus</span>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 10 — FRASE PAGINA CONTATTI
# ═══════════════════════════════════════════════════════════════════════════════

P10_OLD = "Per le consulenze su appuntamento (nutrizione, Shiatsu, meditazione) ti chiediamo di chiamare prima — così ti dedichiamo il tempo che meriti."
P10_NEW = "Per le consulenze su appuntamento (nutrizione, naturopatia, cosmetologia) ti chiediamo di chiamare prima — così ti dedichiamo il tempo che meriti."


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 11 — META DESCRIPTION
# ═══════════════════════════════════════════════════════════════════════════════

P11_OLD = '<meta name="description" content="Parafarmacia Erboristeria Viale Umberto 1° – Reggio Emilia. Fitoterapia, erboristeria, cosmesi, omeopatia. Tisane artigianali, consulenze nutrizionali, massaggi Shiatsu e meditazione dei chakra."'
P11_NEW = '<meta name="description" content="Parafarmacia Erboristeria Viale Umberto 1° – Reggio Emilia. Fitoterapia, erboristeria, cosmesi, omeopatia. Tisane artigianali, consulenze nutrizionali, naturopatia, farmacista cosmetologa, punto vendita Pane Primus e stanze per consulenze su appuntamento."'


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 12 — CSS per le nuove sezioni (rooms + primus) e mini-form
# ═══════════════════════════════════════════════════════════════════════════════
#
# Lo iniettiamo subito prima della chiusura </style>. Usiamo come ancora
# il commento ".reveal{" che dovrebbe essere unico nel file CSS.

P12_ANCHOR = """.reveal{
  opacity: 0;
  transform: translateY(30px);
  transition: opacity .9s ease, transform .9s ease;
}
.reveal.visible{
  opacity: 1; transform: none;
}

</style>"""

P12_NEW = """.reveal{
  opacity: 0;
  transform: translateY(30px);
  transition: opacity .9s ease, transform .9s ease;
}
.reveal.visible{
  opacity: 1; transform: none;
}

/* ============================================================
   STANZE PER CONSULENZE
============================================================ */
.rooms-section{
  padding: 80px 0 100px;
  background:
    radial-gradient(ellipse 600px 400px at 20% 30%, var(--salvia-soft) 0%, transparent 65%),
    radial-gradient(ellipse 700px 500px at 80% 80%, var(--azzurro-soft) 0%, transparent 60%),
    var(--azzurro-aria);
  border-top: 1px solid rgba(31,58,77,.08);
}
.rooms-header{
  text-align: center;
  max-width: 760px;
  margin: 0 auto 60px;
}
.rooms-header h2{
  font-size: clamp(36px, 5.5vw, 56px);
  font-weight: 300;
  margin: 18px 0 22px;
}
.rooms-header h2 em{ color: var(--azzurro-deep); font-weight: 400; }
.rooms-header .lead{
  font-size: 17px;
  color: var(--grigio);
  line-height: 1.7;
}

.rooms-grid{
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-bottom: 70px;
}
.room-card{
  background: var(--bianco);
  border-radius: var(--r-lg);
  padding: 40px 36px;
  box-shadow: var(--ombra-card);
  border: 1px solid rgba(31,58,77,.06);
  transition: transform .3s ease, box-shadow .3s ease;
}
.room-card:hover{
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(31,58,77,.06), 0 30px 80px -20px rgba(31,58,77,.22);
}
.room-num{
  font-family: var(--display);
  font-size: 16px;
  color: var(--azzurro-deep);
  letter-spacing: 0.04em;
  margin-bottom: 18px;
  display: inline-flex; align-items: center; gap: 12px;
}
.room-num::after{
  content: ""; width: 40px; height: 1px; background: currentColor;
}
.room-card h3{
  font-size: clamp(26px, 3.5vw, 34px);
  font-weight: 300;
  margin-bottom: 16px;
}
.room-card h3 em{ color: var(--azzurro-deep); font-weight: 400; }
.room-card p{
  font-size: 16px;
  color: var(--grigio);
  margin-bottom: 22px;
  line-height: 1.65;
}
.room-card ul{
  list-style: none;
  padding: 0;
  border-top: 1px solid rgba(31,58,77,.08);
  padding-top: 20px;
}
.room-card ul li{
  position: relative;
  padding-left: 22px;
  margin-bottom: 10px;
  font-size: 15px;
  color: var(--testo);
}
.room-card ul li::before{
  content: "";
  position: absolute;
  left: 0; top: 9px;
  width: 10px; height: 1px;
  background: var(--azzurro-deep);
}

.rooms-cta{
  background: var(--bianco);
  border-radius: var(--r-lg);
  padding: 50px 48px;
  box-shadow: var(--ombra-card);
  border: 1px solid rgba(31,58,77,.06);
  max-width: 720px;
  margin: 0 auto;
}
.rooms-cta h3{
  font-size: clamp(26px, 3.5vw, 36px);
  font-weight: 300;
  margin-bottom: 14px;
  text-align: center;
}
.rooms-cta h3 em{ color: var(--azzurro-deep); font-weight: 400; }
.rooms-cta > p{
  text-align: center;
  color: var(--grigio);
  font-size: 16px;
  margin-bottom: 32px;
  line-height: 1.6;
}
.rooms-form .field{
  margin-bottom: 18px;
}
.rooms-form label{
  display: block;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--azzurro-deep);
  margin-bottom: 8px;
}
.rooms-form input,
.rooms-form textarea{
  width: 100%;
  padding: 14px 16px;
  border: 1px solid rgba(31,58,77,.15);
  border-radius: var(--r-sm);
  font-family: var(--body);
  font-size: 16px;
  color: var(--inchiostro);
  background: var(--azzurro-aria);
  transition: border-color .25s, background .25s;
}
.rooms-form input:focus,
.rooms-form textarea:focus{
  outline: none;
  border-color: var(--azzurro-deep);
  background: var(--bianco);
}
.rooms-form textarea{
  resize: vertical;
  min-height: 100px;
  font-family: var(--body);
}
.field-action{
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
  margin-top: 8px;
}
.field-hint{
  font-size: 13px;
  color: var(--grigio);
  font-style: italic;
}

@media (max-width: 768px){
  .rooms-section{ padding: 60px 0 80px; }
  .rooms-grid{ grid-template-columns: 1fr; gap: 20px; }
  .room-card{ padding: 32px 26px; }
  .rooms-cta{ padding: 36px 24px; }
  .field-action{ flex-direction: column; align-items: stretch; gap: 12px; }
  .field-action .btn{ width: 100%; justify-content: center; }
  .field-hint{ text-align: center; }
}

/* ============================================================
   PANE PRIMUS
============================================================ */
.primus-section{
  padding: 110px 0;
  background:
    radial-gradient(ellipse 600px 400px at 80% 20%, var(--rosa-soft) 0%, transparent 60%),
    radial-gradient(ellipse 700px 500px at 10% 90%, var(--salvia-soft) 0%, transparent 65%),
    linear-gradient(180deg, var(--azzurro-aria) 0%, var(--bianco) 100%);
  border-top: 1px solid rgba(31,58,77,.06);
  border-bottom: 1px solid rgba(31,58,77,.06);
}
.primus-grid{
  display: grid;
  grid-template-columns: 1fr 1.1fr;
  gap: 80px;
  align-items: center;
}
.primus-image{
  position: relative;
}
.primus-img-wrap{
  position: relative;
  aspect-ratio: 1;
  border-radius: var(--r-xl);
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(31,58,77,.06), 0 40px 100px -30px rgba(31,58,77,.3);
  background:
    radial-gradient(ellipse 600px 400px at 40% 30%, #F5E6D3 0%, transparent 70%),
    linear-gradient(135deg, #E8C99B 0%, #D4A574 100%);
}
.primus-img-wrap img{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.primus-img-placeholder{
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}
.primus-img-placeholder svg{ width: 70%; height: auto; }
.primus-img-wrap:not(.no-img) .primus-img-placeholder{ display: none; }

.primus-text .eyebrow{ margin-bottom: 24px; }
.primus-text h2{
  font-size: clamp(36px, 5.5vw, 56px);
  font-weight: 300;
  margin-bottom: 24px;
  line-height: 1.1;
}
.primus-text h2 em{
  color: #8B5E34;
  font-weight: 400;
}
.primus-text p{
  font-size: 17px;
  color: var(--grigio);
  margin-bottom: 18px;
  line-height: 1.7;
}
.primus-text p strong{ color: var(--inchiostro); font-weight: 500; }
.primus-text p em{ color: var(--azzurro-deep); font-style: italic; font-weight: 500; }

.primus-features{
  list-style: none;
  padding: 0;
  margin: 28px 0 36px;
  border-top: 1px solid rgba(31,58,77,.08);
  padding-top: 24px;
}
.primus-features li{
  position: relative;
  padding-left: 26px;
  margin-bottom: 12px;
  font-size: 16px;
  color: var(--testo);
}
.primus-features li::before{
  content: "";
  position: absolute;
  left: 0; top: 11px;
  width: 12px; height: 1px;
  background: #8B5E34;
}
.primus-features strong{ color: var(--inchiostro); font-weight: 500; }
.primus-cta-row{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

@media (max-width: 900px){
  .primus-section{ padding: 80px 0; }
  .primus-grid{ grid-template-columns: 1fr; gap: 50px; }
  .primus-img-wrap{ max-width: 480px; margin: 0 auto; }
}
@media (max-width: 540px){
  .primus-text h2{ font-size: clamp(30px, 7vw, 42px); }
  .primus-text p{ font-size: 16px; }
  .primus-cta-row{ flex-direction: column; }
  .primus-cta-row .btn{ width: 100%; justify-content: center; }
}

</style>"""


# ═══════════════════════════════════════════════════════════════════════════════
#  PATCH 13 — JS submitRoomsForm (mailto handler per la sezione stanze)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Lo iniettiamo dopo il blocco BURGER, prima del REVEAL ON SCROLL.

P13_ANCHOR = """/* ============== REVEAL ON SCROLL ============== */"""

P13_NEW = """/* ============== ROOMS FORM (mailto) ============== */
function submitRoomsForm(e){
  e.preventDefault();
  const name    = document.getElementById('roomsName').value.trim();
  const contact = document.getElementById('roomsContact').value.trim();
  const message = document.getElementById('roomsMessage').value.trim();
  const subject = encodeURIComponent('Richiesta affitto stanza — ' + (name || 'consulenze'));
  const body = encodeURIComponent(
    'Buongiorno,\\n\\n' +
    'sono ' + name + ' e sono interessato/a all\\'affitto di una delle stanze per consulenze.\\n\\n' +
    'Recapito: ' + contact + '\\n\\n' +
    'Disponibilità e necessità:\\n' + message + '\\n\\n' +
    'Resto in attesa di un vostro riscontro.\\nGrazie,\\n' + name
  );
  window.location.href = 'mailto:parafarmaciavialeumberto@gmail.com?subject=' + subject + '&body=' + body;
  return false;
}

/* ============== REVEAL ON SCROLL ============== */"""


# ═══════════════════════════════════════════════════════════════════════════════
#  ESECUZIONE
# ═══════════════════════════════════════════════════════════════════════════════

PATCHES: list[tuple[str, str, str]] = [
    ("01 cache-buster articles.json",          P1_OLD,         P1_NEW),
    ("02 orari mercoledì",                     P2_OLD,         P2_NEW),
    ("03 footer orari",                        P3_OLD,         P3_NEW),
    ("04a CSS menu mobile",                    P4_CSS_OLD,     P4_CSS_NEW),
    ("04b JS burger",                          P4_JS_OLD,      P4_JS_NEW),
    ("05 sezione stanze consulenze",           P5_ANCHOR,      P5_NEW),
    ("06 sezione Pane Primus",                 P6_ANCHOR,      P6_NEW),
    ("07 servizio 02: Shiatsu → Naturopata",   P7_OLD,         P7_NEW),
    ("08 servizio 03: Chakra → Cosmetologa",   P8_OLD,         P8_NEW),
    ("09 marquee",                             P9_OLD,         P9_NEW),
    ("10 frase contatti",                      P10_OLD,        P10_NEW),
    ("11 meta description",                    P11_OLD,        P11_NEW),
    ("12 CSS sezioni nuove",                   P12_ANCHOR,     P12_NEW),
    ("13 JS rooms form (mailto)",              P13_ANCHOR,     P13_NEW),
]


def apply_patches(content: str) -> tuple[str, list[str], list[str]]:
    """Applica tutte le patch. Restituisce (nuovo_contenuto, applicate, fallite)."""
    applied: list[str] = []
    failed: list[str] = []

    for name, old, new in PATCHES:
        if new in content:
            print(f"  ⊝ {name:50s} già applicata, skip")
            continue
        if old not in content:
            print(f"  ✗ {name:50s} BLOCCO ORIGINALE NON TROVATO")
            failed.append(name)
            continue
        content = content.replace(old, new, 1)
        print(f"  ✓ {name:50s} applicata")
        applied.append(name)

    return content, applied, failed


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python patch_index_html.py path/to/index.html")
        return 1

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"File non trovato: {target}")
        return 1

    original = target.read_text(encoding="utf-8")
    backup = target.with_suffix(target.suffix + ".bak")
    backup.write_text(original, encoding="utf-8")
    print(f"Backup salvato in: {backup}\n")

    print(f"Applico {len(PATCHES)} patch su {target}...\n")
    content, applied, failed = apply_patches(original)

    print(f"\n— Riepilogo —")
    print(f"  Applicate:    {len(applied)}")
    print(f"  Fallite:      {len(failed)}")
    print(f"  Già presenti: {len(PATCHES) - len(applied) - len(failed)}")

    if content == original:
        print("\nNessuna modifica effettiva. File non riscritto.")
        return 0 if not failed else 2

    target.write_text(content, encoding="utf-8")
    print(f"\n✓ {target} aggiornato.")
    print(f"  (Per ripristinare: cp {backup} {target})")

    if failed:
        print("\n⚠ ATTENZIONE: alcune patch non sono state applicate perché")
        print("  il blocco originale non è stato trovato. Probabili cause:")
        print("    - il file index.html è già stato modificato a mano")
        print("    - una virgoletta o uno spazio è diverso")
        print("  Le patch fallite vanno applicate manualmente:")
        for name in failed:
            print(f"    - {name}")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
