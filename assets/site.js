/* ============== DATI INGREDIENTI TISANE ============== */
const INGREDIENTS_DATA = [
  {
    slug: "camomilla",
    name: "Camomilla",
    action: "Calmante",
    img: "/assets/tisane/camomilla.svg",
    intro: "Il fiore più familiare dell'erboristeria, e anche il più sottovalutato.",
    content: `
      <p>La camomilla (<em>Matricaria chamomilla</em>) è probabilmente la pianta officinale più riconoscibile al mondo: piccoli capolini bianchi con il cuore giallo, un profumo dolce che ricorda la mela — non a caso il nome greco "chamaimelon" significa proprio "mela di terra". Dietro questa apparente semplicità si nasconde una delle piante più studiate della farmacognosia moderna.</p>
      <p>Il fiore concentra oli essenziali (in particolare bisabololo e camazulene), flavonoidi e cumarine. È questa combinazione a darle un'azione calmante sul sistema nervoso e, allo stesso tempo, antinfiammatoria e antispasmodica sull'apparato digerente. Una tazza serale aiuta a rilassarsi prima del sonno; la stessa infusione, bevuta dopo un pasto pesante, allevia gonfiore e crampi addominali. È anche il rimedio più comune contro l'irritabilità intestinale nei bambini piccoli.</p>
      <p>Cresce spontanea in tutta Europa, sui bordi dei campi e nei terreni incolti, ma per un'infusione di qualità serve una coltivazione controllata: la matricaria selvatica si confonde facilmente con specie simili ma meno attive (o addirittura con la camomilla romana, botanicamente diversa). Le migliori coltivazioni italiane si trovano tra Toscana, Umbria e Abruzzo.</p>
      <p>La raccolta avviene rigorosamente a mano o con pettini raccoglitori, nelle prime ore del mattino quando il capolino è aperto ma la rugiada già asciutta, per non disperdere l'olio essenziale. L'essiccazione è delicata: temperature basse (sotto i 40°C) e circolazione d'aria continua, altrimenti i fiori perdono colore e principio attivo. Un buon lotto si riconosce subito dal profumo intenso e dal colore giallo acceso del disco centrale.</p>
    `
  },
  {
    slug: "melissa",
    name: "Melissa",
    action: "Rilassante",
    img: "/assets/tisane/melissa.svg",
    intro: "La \"erba delle api\": rilassante per il sistema nervoso, alleata dello stomaco.",
    content: `
      <p>La melissa (<em>Melissa officinalis</em>), detta anche cedronella o erba limoncina, appartiene alla famiglia della menta ma ha un profumo completamente diverso: agrumato, fresco, quasi di limone. Il nome deriva dal greco "melissa", ape, perché le api sono letteralmente attratte dai suoi fiori — un tempo le foglie venivano strofinate sulle arnie per richiamare gli sciami.</p>
      <p>Il suo principio attivo principale, l'acido rosmarinico, insieme agli oli essenziali (citrale, citronellale) le conferisce una duplice azione: calmante sul sistema nervoso centrale e antispasmodica sull'apparato digerente. È la pianta d'elezione per chi soffre di ansia con componente gastrica — quel nodo allo stomaco tipico dei periodi di stress — e per chi fatica a "staccare la testa" la sera.</p>
      <p>Si coltiva facilmente in tutta Italia, predilige terreni freschi e posizioni semi-ombreggiate; è una pianta perenne che tende a espandersi con vigore, tanto da essere considerata quasi infestante negli orti di campagna. Le coltivazioni destinate all'erboristeria si trovano soprattutto in Toscana ed Emilia-Romagna.</p>
      <p>Si raccolgono le foglie prima della fioritura, quando la concentrazione di olio essenziale è al massimo, e si essiccano rapidamente all'ombra: la luce diretta degrada il citrale e con esso buona parte del profumo caratteristico. Una melissa essiccata bene mantiene la nota di limone anche a distanza di mesi; se sa solo di "fieno", ha perso gran parte delle sue proprietà.</p>
    `
  },
  {
    slug: "tiglio",
    name: "Tiglio",
    action: "Sedativo",
    img: "/assets/tisane/tiglio.svg",
    intro: "L'albero dei viali cittadini nasconde uno dei sedativi vegetali più delicati.",
    content: `
      <p>Il tiglio (<em>Tilia cordata</em> e <em>Tilia platyphyllos</em>) è l'albero che profuma i viali di mezza Europa a giugno, quando fiorisce con quei grappoli color crema attaccati a una caratteristica brattea alata. In erboristeria si usa proprio il fiore, spesso raccolto insieme alla brattea che lo sostiene.</p>
      <p>Contiene flavonoidi, mucillagini e un olio essenziale ricco di farnesolo, che gli conferiscono un'azione sedativa lieve ma efficace, oltre a proprietà emollienti sulle vie respiratorie. È il rimedio classico per l'insonnia occasionale legata a stress o cambio di stagione, e per la tosse secca e irritativa: le mucillagini lenisco le mucose della gola, mentre l'azione rilassante calma il riflesso della tosse notturna.</p>
      <p>In Italia cresce spontaneo lungo i corsi d'acqua e nei boschi collinari, dal Piemonte alla Calabria; le coltivazioni per uso erboristico si concentrano soprattutto nell'Italia centrale, dove il clima favorisce una fioritura ricca di principio attivo. È una pianta longeva — alcuni esemplari secolari superano i 500 anni di vita.</p>
      <p>La raccolta richiede tempismo: i fiori vanno colti appena sbocciati, in una finestra di pochi giorni a inizio estate, altrimenti perdono profumo e principio attivo. L'essiccazione avviene su graticci, in strati sottili e ben areati, lontano dal sole diretto. Un tiglio essiccato correttamente conserva la brattea intatta e un colore verde-crema, mai bruno.</p>
    `
  },
  {
    slug: "valeriana",
    name: "Valeriana",
    action: "Notturna",
    img: "/assets/tisane/valeriana.svg",
    intro: "La radice che profuma di poco e agisce parecchio: il classico rimedio per dormire.",
    content: `
      <p>Della valeriana (<em>Valeriana officinalis</em>) si usa la radice — un rizoma nodoso dall'odore intenso, quasi pungente, che molti trovano sgradevole ma che è proprio il segno di un buon principio attivo. È una delle piante sedative più studiate dalla ricerca scientifica moderna.</p>
      <p>Deve la sua azione agli acidi valerenici e agli iridoidi (valepotriati), che agiscono sui recettori GABA del sistema nervoso centrale — lo stesso meccanismo su cui intervengono alcuni farmaci ansiolitici, ma con un'intensità molto più contenuta. È indicata per l'insonnia da addormentamento, per i risvegli notturni legati a tensione nervosa, e come coadiuvante nei periodi di ansia lieve. A differenza di molti sedativi di sintesi, non lascia sensazione di torpore al risveglio se assunta correttamente.</p>
      <p>Cresce spontanea nei prati umidi e lungo i fossi di tutta Europa, dalla pianura fino ai 1500 metri di quota. Le coltivazioni italiane per uso erboristico sono concentrate soprattutto nell'arco alpino e prealpino, dove il rizoma si sviluppa più ricco di principio attivo grazie agli sbalzi termici.</p>
      <p>Il rizoma si raccoglie in autunno, al secondo anno di vita della pianta, quando la concentrazione di acidi valerenici è massima. Viene lavato, tagliato e essiccato a bassa temperatura: un'essiccazione troppo rapida o troppo calda disperde l'olio essenziale e indebolisce l'effetto. L'odore forte e "di stalla" che si sviluppa durante l'essiccazione è normale, ed è proprio il segno che i principi attivi si stanno concentrando correttamente.</p>
    `
  },
  {
    slug: "finocchio",
    name: "Finocchio",
    action: "Digestivo",
    img: "/assets/tisane/finocchio.svg",
    intro: "Semi piccoli, azione grande: il classico dopo pasto delle nonne aveva ragione.",
    content: `
      <p>Del finocchio (<em>Foeniculum vulgare</em>) l'erboristeria usa il frutto — chiamato comunemente "seme" — piccolo, striato, dal profumo dolce e anisato inconfondibile. È una delle piante digestive più antiche conosciute, già citata da Ippocrate e Plinio il Vecchio.</p>
      <p>Il suo olio essenziale, ricco di anetolo, ha un'azione carminativa (favorisce l'espulsione dei gas intestinali), antispasmodica e leggermente galattogena. È il rimedio d'elezione contro gonfiore addominale, coliche del lattante (in forma di infusione molto diluita) e la classica "pesantezza" dopo un pasto abbondante — da qui l'abitudine, tutta italiana, del finocchietto masticato a fine cena.</p>
      <p>È una pianta mediterranea per eccellenza: cresce spontanea lungo le coste e le zone collinari di tutta Italia, con varietà selvatiche particolarmente aromatiche in Sicilia e Puglia. Le coltivazioni per uso erboristico prediligono terreni calcarei e ben drenati, esposti in pieno sole.</p>
      <p>I semi si raccolgono a fine estate, quando le ombrelle si sono seccate sulla pianta ma prima che si aprano disperdendo il contenuto. Dopo la trebbiatura vengono essiccati al sole per pochi giorni, giusto il tempo di stabilizzare l'umidità residua senza far evaporare l'olio essenziale. Un buon finocchio si riconosce annusandolo: deve sprigionare subito la nota anisata, segno che l'anetolo è ancora intatto.</p>
    `
  },
  {
    slug: "menta",
    name: "Menta",
    action: "Tonificante",
    img: "/assets/tisane/menta.svg",
    intro: "Fresca, pungente, energizzante: la pianta che sveglia i sensi e calma lo stomaco.",
    content: `
      <p>La menta piperita (<em>Mentha × piperita</em>) è un ibrido naturale tra menta acquatica e menta verde, nato spontaneamente in Inghilterra nel Seicento e da allora diffuso in tutto il mondo per l'intensità del suo aroma. La foglia, ricca di ghiandole oleifere visibili in controluce, è la parte utilizzata.</p>
      <p>Il mentolo, principale componente dell'olio essenziale, ha un'azione antispasmodica sulla muscolatura liscia del tratto digerente e un effetto rinfrescante e lievemente tonificante sul sistema nervoso — capace di schiarire la mente senza l'effetto eccitante della caffeina. È utile contro gonfiore, difficoltà digestive e la sensazione di testa "pesante" dei pomeriggi afosi; l'infuso freddo, in estate, è anche un ottimo dissetante naturale.</p>
      <p>Si coltiva con facilità in tutta Italia — è una pianta rustica, che si propaga rapidamente per rizoma e tende a colonizzare l'orto se non contenuta. Le coltivazioni professionali più rinomate si trovano in Emilia-Romagna e Piemonte, dove il clima temperato-umido favorisce una resa elevata di olio essenziale.</p>
      <p>Le foglie si raccolgono poco prima della fioritura, quando la concentrazione di mentolo è al massimo, preferibilmente al mattino dopo che la rugiada è evaporata. L'essiccazione avviene rapidamente e all'ombra, per preservare il colore verde intenso e l'aroma pungente: una menta essiccata male vira al bruno e perde gran parte della nota fresca che la caratterizza.</p>
    `
  },
  {
    slug: "zenzero",
    name: "Zenzero",
    action: "Riscaldante",
    img: "/assets/tisane/zenzero.svg",
    intro: "Un rizoma tropicale diventato di casa in ogni tisaneria: piccante, caldo, energico.",
    content: `
      <p>Lo zenzero (<em>Zingiber officinale</em>) è il rizoma di una pianta erbacea originaria del sud-est asiatico, oggi coltivata in tutte le fasce tropicali del pianeta. In erboristeria si utilizza fresco o essiccato, a seconda dell'intensità di azione desiderata.</p>
      <p>Deve la sua caratteristica piccantezza a gingeroli e shogaoli, composti con una spiccata azione antinausea, digestiva e circolatoria. È il rimedio naturale più studiato contro nausea da viaggio e nausea gravidica lieve; favorisce inoltre la digestione dei grassi e dà una sensazione di calore percepibile già pochi minuti dopo l'assunzione — da cui il suo uso tradizionale nei mesi freddi, per stimolare la circolazione periferica.</p>
      <p>Le principali aree di coltivazione restano India, Cina e Nigeria, dove il clima caldo-umido e i terreni sciolti e ricchi di sostanza organica permettono al rizoma di svilupparsi in profondità. Le piante di qualità superiore vengono coltivate in policoltura, spesso all'ombra di alberi da frutto.</p>
      <p>Il rizoma si raccoglie 8-10 mesi dopo la semina, quando ha raggiunto piena maturazione. Per lo zenzero essiccato, dopo la raccolta viene lavato, spesso pelato a mano, tagliato a fette sottili ed essiccato al sole o in essiccatoi a bassa temperatura per alcuni giorni: un'essiccazione corretta concentra gli oli essenziali rendendo il piccante più intenso rispetto al rizoma fresco.</p>
    `
  },
  {
    slug: "curcuma",
    name: "Curcuma",
    action: "Antiossidante",
    img: "/assets/tisane/curcuma.svg",
    intro: "Il rizoma color oro che l'Ayurveda usa da millenni, oggi al centro della ricerca sull'infiammazione.",
    content: `
      <p>La curcuma (<em>Curcuma longa</em>) è un rizoma della famiglia dello zenzero, originario dell'Asia meridionale, riconoscibile dal caratteristico colore arancio-oro intenso che tinge tutto ciò che tocca — è la stessa sostanza che dà colore al curry.</p>
      <p>Il principio attivo principale è la curcumina, un polifenolo con una potente azione antiossidante e antinfiammatoria, oggetto di centinaia di studi scientifici negli ultimi vent'anni. È utile come coadiuvante nel benessere articolare, nella funzionalità epatica e digestiva, e come supporto generale contro lo stress ossidativo. Un dettaglio importante: la curcumina da sola è scarsamente assorbita dall'intestino, per questo in erboristeria viene spesso abbinata a piperina (dal pepe nero), che ne aumenta la biodisponibilità fino a venti volte.</p>
      <p>Si coltiva prevalentemente in India — che da sola produce circa l'80% della curcuma mondiale — oltre che in Indonesia, Cina e in alcune aree tropicali dell'Africa. Predilige climi caldo-umidi, piogge abbondanti e terreni ben drenati; ogni pianta produce un cespo di rizomi che si moltiplica di anno in anno.</p>
      <p>La raccolta avviene 8-9 mesi dopo la semina. I rizomi vengono bolliti brevemente per stabilizzare il colore e facilitare l'essiccazione, poi essiccati al sole per una decina di giorni fino a diventare duri e friabili. Solo a questo punto vengono macinati in polvere fine: una curcuma di qualità ha un colore intenso e uniforme, mai spento o polveroso.</p>
    `
  },
  {
    slug: "passiflora",
    name: "Passiflora",
    action: "Ansiolitica",
    img: "/assets/tisane/passiflora.svg",
    intro: "Il fiore più scenografico dell'erboristeria è anche uno dei rilassanti vegetali più efficaci.",
    content: `
      <p>La passiflora (<em>Passiflora incarnata</em>), o fiore della passione, è una liana rampicante dal fiore straordinario — una corona di filamenti violacei attorno a una struttura che i missionari gesuiti in Sudamerica interpretarono come simbolo della Passione di Cristo, da cui il nome. In erboristeria si usa la parte aerea fiorita.</p>
      <p>Contiene flavonoidi (in particolare vitexina) e tracce di alcaloidi indolici, con un'azione ansiolitica e sedativa lieve, priva dell'effetto "narcotico" che si associa spesso ai sedativi. È tra le piante più utilizzate per l'ansia generalizzata, l'irrequietezza nervosa e l'insonnia da iperattività mentale — quella sensazione di pensieri che non si fermano quando si va a letto. Spesso viene abbinata a biancospino e valeriana proprio per questa sua capacità di "spegnere il rumore di fondo" senza appesantire.</p>
      <p>Originaria del sud-est degli Stati Uniti e del Sudamerica, oggi si coltiva anche in Europa meridionale, Italia compresa, in particolare in aree dal clima mite e temperato dove la pianta può svilupparsi come rampicante perenne su tutori o pergolati.</p>
      <p>La parte aerea fiorita si raccoglie durante la piena fioritura estiva, quando la concentrazione di flavonoidi è massima. Si essicca rapidamente, in strati sottili e ben ventilati, lontano dal sole diretto per non degradare i principi attivi fotosensibili. Un buon lotto mantiene un colore verde-violaceo vivo, segno che fiori e foglie non hanno subito surriscaldamento.</p>
    `
  },
  {
    slug: "biancospino",
    name: "Biancospino",
    action: "Cardiotonico",
    img: "/assets/tisane/biancospino.svg",
    intro: "Piccoli fiori bianchi e bacche rosse per il cuore e per i nervi: una pianta doppia.",
    content: `
      <p>Il biancospino (<em>Crataegus monogyna</em> e <em>Crataegus oxyacantha</em>) è un arbusto spinoso comunissimo nelle siepi campestri italiane, riconoscibile in primavera per i suoi piccoli fiori bianchi riuniti a mazzetti e in autunno per le bacche rosse (le "azzeruole" minori). In erboristeria si usano fiori, foglie e, in alcuni preparati, le bacche.</p>
      <p>Contiene flavonoidi e procianidine oligomeriche che agiscono in modo delicato ma specifico sul sistema cardiovascolare: favoriscono la funzionalità cardiaca, aiutano a regolare la frequenza dei battiti nei momenti di ansia e sostengono la circolazione periferica. È per questo che viene definito "l'ansiolitico del cuore" — utile in chi somatizza lo stress con palpitazioni o tachicardia emotiva, sempre accanto (mai in sostituzione) a un controllo medico se i sintomi sono frequenti.</p>
      <p>Cresce spontaneo in tutta Italia, dalla pianura fino alla media montagna, ai margini dei boschi e lungo le siepi; è una pianta estremamente rustica che non richiede coltivazioni intensive — buona parte del biancospino erboristico italiano viene ancora raccolto da piante spontanee selezionate.</p>
      <p>I fiori si raccolgono appena sbocciati, in una finestra molto breve a fine primavera, perché appassiscono rapidamente sulla pianta. L'essiccazione è delicata, all'ombra e a bassa temperatura, per mantenere intatto il colore bianco-crema: un biancospino ingiallito o bruno ha perso gran parte della sua carica di flavonoidi.</p>
    `
  },
  {
    slug: "liquirizia",
    name: "Liquirizia",
    action: "Lenitiva",
    img: "/assets/tisane/liquirizia.svg",
    intro: "Dolce di natura, la radice più golosa dell'erboristeria protegge stomaco e gola.",
    content: `
      <p>La liquirizia (<em>Glycyrrhiza glabra</em>) è una pianta leguminosa il cui rizoma e la cui radice contengono glicirrizina, una sostanza dolcificante circa 50 volte più intensa dello zucchero — da cui il nome scientifico, che in greco significa letteralmente "radice dolce".</p>
      <p>La glicirrizina, insieme a flavonoidi come la liquiritina, conferisce alla radice un'azione lenitiva sulle mucose gastriche e antinfiammatoria sulle prime vie respiratorie: è utile in caso di gastrite lieve, bruciore di stomaco occasionale, tosse e mal di gola, oltre ad avere una blanda azione espettorante. Va usata con attenzione da chi soffre di ipertensione, perché in dosi elevate e prolungate la glicirrizina può favorire la ritenzione di sodio — un motivo in più per farsi consigliare la posologia corretta in parafarmacia.</p>
      <p>Cresce nelle regioni a clima mediterraneo e continentale caldo; in Italia le coltivazioni storiche più importanti si trovano in Calabria, dove la liquirizia di Rossano ha ottenuto anche il marchio di Indicazione Geografica Protetta, considerata tra le più pregiate al mondo per il contenuto di glicirrizina.</p>
      <p>Le radici si estraggono dal terreno dopo almeno 3-4 anni di crescita, quando hanno accumulato una quantità sufficiente di principio attivo. Vengono lavate, tagliate in pezzi o bastoncini ed essiccate lentamente all'aria; per alcuni preparati vengono anche torrefatte leggermente, un passaggio che ne accentua la nota dolce e aromatica tipica della radice pronta per l'infusione.</p>
    `
  },
  {
    slug: "rosa-canina",
    name: "Rosa Canina",
    action: "Rinforzante",
    img: "/assets/tisane/rosa-canina.svg",
    intro: "Il frutto selvatico più ricco di vitamina C che la natura abbia da offrire.",
    content: `
      <p>La rosa canina (<em>Rosa canina</em>) è un arbusto spinoso spontaneo, progenitrice selvatica di molte rose da giardino. Il suo frutto, il cinorrodo — chiamato comunemente "bacca" anche se botanicamente è un falso frutto — matura in autunno assumendo un colore rosso-arancio brillante.</p>
      <p>È tra le fonti vegetali più concentrate di vitamina C in natura, insieme a bioflavonoidi, carotenoidi e tannini che ne completano l'azione antiossidante. Viene tradizionalmente usata come rinforzante generale nei cambi di stagione, per sostenere le naturali difese dell'organismo nei mesi freddi e come coadiuvante contro stanchezza e affaticamento. Il sapore leggermente acidulo e fruttato la rende anche una delle tisane più gradevoli da proporre a chi non ama i sapori amari.</p>
      <p>Cresce spontanea in tutta Europa, comprese le zone collinari e submontane italiane, ai margini di boschi e siepi; le raccolte erboristiche di qualità privilegiano le zone d'alta collina, dove gli sbalzi termici concentrano maggiormente la vitamina C nel frutto.</p>
      <p>I cinorrodi si raccolgono in autunno inoltrato, dopo le prime leggere gelate che ne ammorbidiscono la polpa e ne esaltano il sapore. Vanno privati con cura dei semi interni e dei piccoli peli urticanti che li circondano — un passaggio manuale delicato — prima di essere tagliati ed essiccati a bassa temperatura, condizione indispensabile per non degradare la vitamina C, che è molto sensibile al calore.</p>
    `
  },
  {
    slug: "ortica",
    name: "Ortica",
    action: "Depurativa",
    img: "/assets/tisane/ortica.svg",
    intro: "Pizzica al tatto, ma è una delle piante più complete e mineralizzanti che esistano.",
    content: `
      <p>L'ortica (<em>Urtica dioica</em>) è nota a tutti per i peli urticanti che ricoprono foglie e fusto — un meccanismo di difesa che, una volta essiccata o cotta, perde completamente la sua capacità irritante, lasciando spazio a una delle piante più ricche di nutrienti dell'erboristeria europea.</p>
      <p>Le foglie contengono un profilo minerale eccezionale (ferro, calcio, magnesio, silicio), clorofilla, flavonoidi e acido ascorbico, che le conferiscono un'azione depurativa, rimineralizzante e leggermente diuretica. È tradizionalmente consigliata nei cambi di stagione come tonico generale, in caso di stanchezza e carenze marziali lievi, e come supporto drenante per l'organismo — un vero "multivitaminico verde" ante litteram, usato da secoli nella tradizione contadina europea.</p>
      <p>Cresce spontanea e infestante in tutta Italia, dalla pianura alla montagna, prediligendo terreni ricchi di azoto: non a caso si trova spesso vicino a case coloniche, letamai e margini di orti, segno indiretto della fertilità del suolo.</p>
      <p>Le foglie si raccolgono in primavera, quando sono giovani e più ricche di clorofilla e minerali, indossando sempre guanti protettivi. L'essiccazione avviene rapidamente all'ombra, in strati sottili: il calore del sole diretto degraderebbe la clorofilla facendo virare le foglie a un verde spento. Una volta essiccata, l'ortica perde completamente il potere urticante e può essere maneggiata e infusa senza alcun rischio.</p>
    `
  },
  {
    slug: "tarassaco",
    name: "Tarassaco",
    action: "Depurativa",
    img: "/assets/tisane/tarassaco.svg",
    intro: "Il \"dente di leone\" dei prati è uno dei migliori amici del fegato.",
    content: `
      <p>Il tarassaco (<em>Taraxacum officinale</em>), conosciuto anche come dente di leone o soffione, è la pianta spontanea più comune dei prati italiani — quella dai fiori gialli e dai frutti a paracadute che tutti da bambini abbiamo soffiato via. In erboristeria si utilizzano sia la radice sia le foglie.</p>
      <p>La radice è ricca di inulina, acidi fenolici e principi amari (tarassacina) che stimolano la funzionalità epatica e biliare, favorendo la digestione dei grassi; le foglie hanno invece un'azione più marcatamente diuretica, ricca di potassio — una caratteristica rara tra i diuretici vegetali, che spesso impoveriscono l'organismo di questo minerale. Insieme, radice e foglia lo rendono uno dei depurativi più completi ed equilibrati per il sostegno di fegato e reni nei cambi di stagione.</p>
      <p>Cresce spontaneo ovunque in Italia, dal livello del mare fino a oltre 2000 metri di quota, adattandosi a qualunque tipo di terreno: è una delle piante più resilienti che esistano, ed è proprio questa diffusione capillare a renderla una risorsa erboristica facilmente accessibile e sostenibile.</p>
      <p>Le radici si raccolgono in autunno o a inizio primavera, quando la pianta concentra le riserve nutritive nel sottosuolo; le foglie si colgono invece in primavera, prima della fioritura, quando sono più tenere e meno amare. Entrambe le parti vengono lavate ed essiccate a bassa temperatura, in strati sottili, fino a diventare friabili al tatto.</p>
    `
  },
  {
    slug: "malva",
    name: "Malva",
    action: "Emolliente",
    img: "/assets/tisane/malva.svg",
    intro: "Fiori color lilla per lenire dalla gola all'intestino: la pianta \"morbida\" per eccellenza.",
    content: `
      <p>La malva (<em>Malva sylvestris</em>) è una pianta erbacea comunissima nei prati incolti e ai bordi delle strade di campagna, riconoscibile per i suoi fiori a cinque petali striati, dal rosa al violetto. In erboristeria si usano sia i fiori sia le foglie.</p>
      <p>Deve le sue proprietà principalmente alle mucillagini, sostanze vegetali che a contatto con l'acqua formano un gel viscoso capace di rivestire e proteggere le mucose irritate. Questo le conferisce un'azione emolliente e lenitiva su gola infiammata, tosse secca, mucosa gastrica irritata e, per uso esterno, pelle arrossata. È uno dei rimedi vegetali più delicati che esistano, adatto anche a bambini e persone con stomaco sensibile, ed è tradizionalmente associata al finocchio per calmare le coliche dei più piccoli.</p>
      <p>Cresce spontanea in tutta Italia, dalla pianura alla collina, prediligendo terreni incolti, muretti a secco e margini di sentieri; si adatta con grande facilità anche ai terreni poveri, ed è una delle piante spontanee più semplici da riconoscere e raccogliere responsabilmente.</p>
      <p>Fiori e foglie si raccolgono in piena estate, quando la fioritura è più abbondante, preferibilmente al mattino. L'essiccazione deve essere rapida e all'ombra: le mucillagini sono sensibili al calore eccessivo, e un'essiccazione troppo lenta rischia di far ammuffire i fiori più delicati. Un buon lotto di malva mantiene il colore violaceo vivo dei petali, segno che la lavorazione è stata corretta.</p>
    `
  },
  {
    slug: "lavanda",
    name: "Lavanda",
    action: "Rilassante",
    img: "/assets/tisane/lavanda.svg",
    intro: "Il profumo più riconoscibile della Provenza è anche un potente alleato del sonno.",
    content: `
      <p>La lavanda (<em>Lavandula angustifolia</em>, o lavanda vera) è un arbusto sempreverde dai caratteristici fiori violetti riuniti in spighe, coltivato in tutto il bacino del Mediterraneo tanto per uso erboristico quanto per la profumeria. In tisana si utilizzano i fiori essiccati.</p>
      <p>L'olio essenziale, ricco di linalolo e acetato di linalile, ha un'azione rilassante sul sistema nervoso centrale documentata da numerosi studi: favorisce l'addormentamento, riduce l'agitazione nervosa e ha un lieve effetto antispasmodico anche a livello digestivo. Bevuta la sera, la tisana di lavanda è tra i rimedi più delicati per chi soffre di sonno leggero o si sveglia facilmente durante la notte, e il solo profumo, prima ancora dell'infusione, ha un effetto calmante misurabile sull'umore.</p>
      <p>In Italia la coltivazione più rinomata è quella dell'Appennino, in particolare in Piemonte, Liguria e Toscana, dove il clima secco e ventilato dell'entroterra collinare favorisce una concentrazione di olio essenziale molto elevata — non a caso paragonabile, per qualità, alla celebre lavanda della Provenza.</p>
      <p>La spiga si raccoglie in piena estate, quando circa metà dei fiori è ancora chiusa: è il momento in cui la concentrazione di olio essenziale nei calici è massima. Dopo il taglio, i mazzetti vengono essiccati appesi a testa in giù, in un luogo buio e ben ventilato, per preservare sia il colore violetto sia il profumo — la luce diretta scolorisce rapidamente i fiori e ne disperde l'aroma.</p>
    `
  },
];


/* ============== ROUTING SPA ============== */
const pages = document.querySelectorAll('.page');
const menuLinks = document.querySelectorAll('[data-page]');

// Title/description per pagina, aggiornati ad ogni navigazione così Google
// (e il tab del browser) vedono il titolo giusto anche in navigazione SPA,
// non solo su un caricamento diretto. Deve restare allineato con la lista
// PAGES di generate_pages.py, che genera lo stesso title/description nel
// sorgente HTML di ogni pagina statica.
const SITE_TITLE_SUFFIX = ' — Parafarmacia Erboristeria Viale Umberto 1°';
const PAGE_META = {
  home: {
    title: 'Parafarmacia Emy — Erboristeria e Omeopatia a Reggio Emilia, Viale Umberto 1°',
    description: "Parafarmacia Emy – Parafarmacia Erboristeria in Viale Umberto 1°, Reggio Emilia (Reggio nell'Emilia). Fitoterapia, erboristeria, cosmesi, omeopatia. Tisane artigianali, nutrizionista e naturopatia a Reggio Emilia, farmacista cosmetologa, punto vendita Pane Primus e stanze per consulenze su appuntamento."
  },
  servizi: {
    title: 'Nutrizionista e Naturopatia a Reggio Emilia — Servizi' + SITE_TITLE_SUFFIX,
    description: "Nutrizionista e naturopatia a Reggio Emilia (Reggio nell'Emilia), in Parafarmacia Viale Umberto 1°: consulenze su appuntamento per alimentazione, benessere naturale e cosmesi. Due stanze attrezzate per professionisti del settore."
  },
  tisane: {
    title: 'Le Tisane della Dottoressa Emy' + SITE_TITLE_SUFFIX,
    description: 'Miscele artigianali composte a mano in negozio, mai online: ingredienti selezionati uno a uno. Scopri la storia e gli ingredienti delle Tisane della Dottoressa Emy.'
  },
  primus: {
    title: 'Pane Primus — Punto Vendita Ufficiale' + SITE_TITLE_SUFFIX,
    description: 'Uno dei pochi punti vendita ufficiali del Pane Primus a Reggio Emilia: grano a basso indice glicemico, lievito madre, fermentazione lunga oltre 24h. Prenota il tuo pane.'
  },
  blog: {
    title: 'Blog: Consigli di Erboristeria, Omeopatia e Naturopatia' + SITE_TITLE_SUFFIX,
    description: 'Un articolo nuovo martedì, giovedì e sabato: erboristeria, omeopatia, naturopatia e cura del corpo, a cura della Parafarmacia Viale Umberto 1° di Reggio Emilia.'
  },
  instagram: {
    title: 'Instagram — @parafarmacia.viale.umberto' + SITE_TITLE_SUFFIX,
    description: 'Segui la Parafarmacia Erboristeria Viale Umberto 1° su Instagram: consigli, novità e tisane della Dottoressa Emy, da Reggio Emilia.'
  },
  contatti: {
    title: 'Dove Trovarci — Orari e Indirizzo' + SITE_TITLE_SUFFIX,
    description: 'Viale Umberto 1°, 17/D a Reggio Emilia. Orari di apertura, telefono, email e indicazioni per raggiungerci. Aperti dal lunedì al sabato.'
  },
  scrivici: {
    title: 'Scrivici un Messaggio' + SITE_TITLE_SUFFIX,
    description: 'Scrivi alla Parafarmacia Viale Umberto 1° di Reggio Emilia: risposta personale entro 24 ore, per consulenze, prenotazioni o informazioni sui prodotti.'
  },
  privacy: {
    title: 'Privacy & Cookie' + SITE_TITLE_SUFFIX,
    description: 'Informativa sul trattamento dei dati personali ai sensi del Regolamento (UE) 2016/679 (GDPR) e della normativa italiana vigente.'
  },
  fitoterapia: {
    title: 'Fitoterapia: Storia, Metodo e Cosa Dice la Scienza' + SITE_TITLE_SUFFIX,
    description: "Dalle prime farmacopee vegetali alla ricerca clinica di oggi: cos'è la fitoterapia, cos'è il fitocomplesso e cosa dice davvero la scienza, spiegato con onestà."
  },
  erboristeria: {
    title: 'Erboristeria a Reggio Emilia — Storia di un Mestiere Antico' + SITE_TITLE_SUFFIX,
    description: "Erboristeria a Reggio Emilia (Reggio nell'Emilia), in Viale Umberto 1°: storia, normativa italiana e metodi di preparazione (infuso, decotto, macerato), spiegati con chiarezza."
  },
  cosmesi: {
    title: 'Cosmesi: Come Nasce (e si Legge) un Prodotto Sicuro' + SITE_TITLE_SUFFIX,
    description: "Dalle argille dell'Antico Egitto agli INCI di oggi: come nasce un cosmetico sicuro, i principi attivi più richiesti e come sceglierlo davvero."
  },
  omeopatia: {
    title: 'Omeopatia a Reggio Emilia — Origini e Dibattito Scientifico' + SITE_TITLE_SUFFIX,
    description: "Omeopatia a Reggio Emilia (Reggio nell'Emilia), in Parafarmacia Viale Umberto 1°: Samuel Hahnemann, il principio del simile, come si preparano i rimedi e cosa dice oggi la scienza, spiegato con chiarezza."
  }
};

function updateMetaTags(title, description){
  if(title) document.title = title;
  if(description){
    let tag = document.querySelector('meta[name="description"]');
    if(!tag){
      tag = document.createElement('meta');
      tag.setAttribute('name', 'description');
      document.head.appendChild(tag);
    }
    tag.setAttribute('content', description);
  }
}

// Converte uno slug di pagina nel path reale corrispondente ("" → "/")
function slugToPath(slug){
  return (!slug || slug === 'home') ? '/' : `/${slug}/`;
}

// Converte location.pathname nello slug di pagina interno, con fallback
// sul vecchio schema #hash per compatibilità con link/bookmark esistenti.
function pathToSlug(){
  const clean = location.pathname.replace(/^\/|\/$/g, '').replace(/\/index\.html$/, '');
  if(clean && PAGE_META[clean]) return clean;
  if(!clean){
    const hash = location.hash.replace('#', '');
    return hash || 'home';
  }
  return clean;
}

function navigate(pageName){
  // Routing blog: blog/slug-articolo → singolo articolo
  if(pageName && pageName.startsWith('blog/')){
    const slug = pageName.substring(5);
    renderArticleRoute(slug);
    return;
  }

  // Routing ingredienti tisane: tisane/slug-ingrediente → scheda ingrediente
  if(pageName && pageName.startsWith('tisane/')){
    const slug = pageName.substring(7);
    renderIngredientRoute(slug);
    return;
  }

  pages.forEach(p => p.classList.remove('active'));
  const target = document.getElementById('page-' + pageName);
  if(target){
    target.classList.add('active');
  } else {
    document.getElementById('page-home').classList.add('active');
    pageName = 'home';
  }

  document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
  document.querySelector(`.menu a[data-page="${pageName}"]`)?.classList.add('active');

  const meta = PAGE_META[pageName];
  if(meta) updateMetaTags(meta.title, meta.description);

  // chiudi mobile menu
  document.getElementById('menu').classList.remove('open');
  document.getElementById('burger').classList.remove('open');

  window.scrollTo({ top: 0, behavior: 'instant' });

  // riattiva animazioni
  setTimeout(() => observeReveals(), 50);

  // Se siamo sul blog, carica gli articoli
  if(pageName === 'blog'){
    renderBlogList(blogState.currentCategory || 'all');
  }
}

menuLinks.forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const page = link.getAttribute('data-page');
    history.pushState({}, '', slugToPath(page));
    navigate(page);
  });
});

window.addEventListener('popstate', () => {
  navigate(pathToSlug());
});

/* ============== NAV SCROLL ============== */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => {
  if(window.scrollY > 30) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
});

/* ============== BURGER ============== */
document.getElementById('burger').addEventListener('click', () => {
  const menu = document.getElementById('menu');
  const burger = document.getElementById('burger');
  const willOpen = !menu.classList.contains('open');
  menu.classList.toggle('open', willOpen);
  burger.classList.toggle('open', willOpen);
  // Blocca lo scroll del body quando il menu è aperto (mobile).
  document.body.classList.toggle('menu-open', willOpen);
});

/* ============== INVIO FORM (FormSubmit AJAX, niente client mail) ============== */
async function sendViaFormSubmit(payload){
  const res = await fetch('https://formsubmit.co/ajax/parafarmaciavialeumberto@gmail.com', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
    body: JSON.stringify(Object.assign({ _captcha: 'false', _template: 'table' }, payload))
  });
  const data = await res.json();
  return !!(data && (data.success === true || data.success === 'true'));
}

function submitRoomsForm(e){
  e.preventDefault();
  const name    = document.getElementById('roomsName').value.trim();
  const contact = document.getElementById('roomsContact').value.trim();
  const message = document.getElementById('roomsMessage').value.trim();
  if(!name || !contact || !message){ alert('Compila tutti i campi.'); return false; }

  const btn  = e.target.querySelector('button[type="submit"]');
  const hint = document.querySelector('#roomsForm .field-hint');
  const original = btn.innerHTML;
  btn.disabled = true; btn.innerHTML = 'Invio in corso…';

  sendViaFormSubmit({
    _subject: 'Richiesta affitto stanza — ' + name,
    Tipo: 'Affitto stanza per consulenze',
    Nome: name,
    Recapito: contact,
    'Disponibilita e necessita': message
  }).then(ok => {
    if(ok){
      e.target.reset();
      if(hint){ hint.textContent = '✓ Richiesta inviata! Ti rispondiamo entro 24h.'; hint.style.color = 'var(--azzurro-deep)'; }
      btn.innerHTML = 'Inviata ✓';
    } else {
      if(hint){ hint.textContent = 'Invio non riuscito. Riprova o chiamaci allo 0522 081652.'; }
      btn.disabled = false; btn.innerHTML = original;
    }
  }).catch(() => {
    if(hint){ hint.textContent = 'Errore di rete. Riprova o chiamaci allo 0522 081652.'; }
    btn.disabled = false; btn.innerHTML = original;
  });
  return false;
}

/* ============== PRENOTAZIONE PANE PRIMUS ============== */
(function(){
  const pf = document.getElementById('primusForm');
  if(!pf) return;
  pf.addEventListener('submit', e => {
    e.preventDefault();
    const name = document.getElementById('primusName').value.trim();
    const phone = document.getElementById('primusPhone').value.trim();
    const message = document.getElementById('primusMessage').value.trim();
    if(!name || !phone || !message){ alert('Compila tutti i campi.'); return; }

    const btn  = document.getElementById('primusSubmitBtn');
    const hint = document.getElementById('primusHint');
    const original = btn.innerHTML;
    btn.disabled = true; btn.innerHTML = 'Invio in corso…';

    sendViaFormSubmit({
      _subject: 'Prenotazione Pane Primus — ' + name,
      Tipo: 'Prenotazione Pane Primus',
      Nome: name,
      Telefono: phone,
      'Quantita e note': message
    }).then(ok => {
      if(ok){
        pf.reset();
        hint.textContent = '✓ Prenotazione inviata! A presto in parafarmacia.';
        hint.style.color = 'var(--azzurro-deep)';
        btn.innerHTML = 'Prenotato ✓';
      } else {
        hint.textContent = 'Invio non riuscito. Riprova o chiamaci allo 0522 081652.';
        btn.disabled = false; btn.innerHTML = original;
      }
    }).catch(() => {
      hint.textContent = 'Errore di rete. Riprova o chiamaci allo 0522 081652.';
      btn.disabled = false; btn.innerHTML = original;
    });
  });
})();

/* ============== REVEAL ON SCROLL ============== */
let observer;
function observeReveals(){
  if(observer) observer.disconnect();
  observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if(entry.isIntersecting){
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll('.reveal:not(.visible)').forEach(el => observer.observe(el));
}
observeReveals();

/* ============== INSTAGRAM EMBED LOADER ============== */
/* Trasforma gli URL dei post Instagram in iframe embed ufficiali.
   Se l'array "instagramPosts" è vuoto, mostra la griglia decorativa di fallback. */
(function initInstagramFeed(){
  // L'array è dichiarato nella pagina Instagram. Se non esiste, esci.
  if(typeof instagramPosts === 'undefined' || !Array.isArray(instagramPosts) || instagramPosts.length === 0){
    return; // Lascia visibile il fallback decorativo
  }

  const realGrid = document.getElementById('igRealGrid');
  const fallback = document.getElementById('igFallback');
  if(!realGrid) return;

  // Estrae il codice del post da un URL Instagram (qualsiasi formato)
  function extractPostCode(url){
    const m = url.match(/instagram\.com\/(?:p|reel|tv)\/([A-Za-z0-9_-]+)/);
    return m ? m[1] : null;
  }

  // Costruisce ogni card embed
  instagramPosts.forEach((url, i) => {
    const code = extractPostCode(url);
    if(!code) return;

    const card = document.createElement('div');
    card.className = 'ig-embed-card';
    card.innerHTML = `
      <div class="ig-embed-loading" id="igLoad${i}">
        <div class="ig-embed-loading-content">
          <svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9" stroke="#2E6489" stroke-width="2" stroke-linecap="round" stroke-dasharray="14 28"/>
          </svg>
          <p>Caricamento post…</p>
        </div>
      </div>
      <iframe
        src="https://www.instagram.com/p/${code}/embed/captioned/"
        loading="lazy"
        scrolling="no"
        allowtransparency="true"
        allow="encrypted-media"
        onload="this.previousElementSibling.classList.add('hidden')"
      ></iframe>
    `;
    realGrid.appendChild(card);
  });

  // Mostra griglia reale e nasconde fallback
  realGrid.style.display = 'grid';
  if(fallback) fallback.style.display = 'none';

  // Aggiorna anche il tag "Aggiornato dal profilo" → "Feed dal vivo"
  const feedTag = document.querySelector('.ig-feed-tag');
  if(feedTag) feedTag.textContent = 'Feed dal vivo';
})();

/* ============== BLOG ENGINE ============== */
/*
 * Carica articles.json (popolato dall'agente AI) e renderizza:
 * - Pagina lista #blog
 * - Singolo articolo #blog/<slug>
 *
 * Se il fetch fallisce (es. articles.json non ancora pubblicato), usa
 * il fallback `BLOG_FALLBACK_DATA` definito qui sotto (3 articoli demo).
 */

// articles.json contiene path immagine relativi tipo "./assets/blog/x.jpg".
// Con le pagine ora servite anche da sottocartelle (es. /blog/, /servizi/),
// un path relativo si romperebbe: lo normalizziamo sempre a root-relative.
function assetUrl(p){
  if(!p) return p;
  if(/^(https?:|data:|\/)/i.test(p)) return p;
  return '/' + p.replace(/^\.\//, '');
}

// URL del file articles.json. Sostituisci con l'URL definitivo quando deployato.
// Esempi:
//   - GitHub raw:  "https://raw.githubusercontent.com/intheboxstudio/parafarmacia-blog/main/articles.json"
//   - CDN/Railway: "https://api.normia.tech/blog/articles.json"
//   - Stesso sito: "./articles.json"
const BLOG_ARTICLES_URL = "/articles.json";

// Fallback con 3 articoli demo (se il fetch fallisce)
const BLOG_FALLBACK_DATA = {
  articles: [
    {
      id: "demo-sonno-2026-05-17",
      slug: "hai-problemi-di-sonno-e-non-sai-come-risolverli",
      title: "Hai problemi di sonno e <em>non sai come risolverli?</em>",
      category: "erboristeria",
      categoryLabel: "Erboristeria",
      excerpt: "Le notti si allungano quando la mente non riesce a fermarsi. Tre rimedi naturali validati dalla letteratura, e i prodotti giusti per metterli in pratica.",
      content: `<p>L'insonnia non è soltanto un problema notturno: è un effetto a cascata che invade le giornate, sfilaccia la concentrazione, indurisce il tono dell'umore. Secondo l'Istituto Superiore di Sanità, circa <strong>il 35% degli adulti italiani</strong> dichiara difficoltà del sonno almeno una volta a settimana, e quasi la metà non sa quali strumenti naturali abbia a disposizione prima di ricorrere a soluzioni farmacologiche.</p>

      <p>La buona notizia? Esistono protocolli erboristici con un fondamento scientifico solido, supportati da revisioni Cochrane e da studi clinici recenti, che possono fare una differenza concreta. Vediamo i tre più affidabili.</p>

      <h2>1. La valeriana, la regina silenziosa</h2>
      <p>La <em>Valeriana officinalis</em> è probabilmente la pianta più studiata per il sonno. Una meta-analisi pubblicata su <strong>Sleep Medicine Reviews</strong> ha mostrato che l'assunzione regolare per almeno 2 settimane riduce la latenza del sonno (il tempo per addormentarsi) di circa 15-20 minuti rispetto al placebo.</p>
      <p>Il dosaggio efficace si aggira tra i 300 e i 600 mg di estratto secco titolato, assunto 30-60 minuti prima di coricarsi. Non sedativa nel senso farmacologico: lavora modulando l'asse GABAergico, lo stesso che si rilassa con la respirazione diaframmatica.</p>

      <blockquote>"La valeriana non spegne la mente: la accompagna a chiudersi, come una porta che si lascia socchiusa."</blockquote>

      <h2>2. Melissa officinalis: per chi pensa troppo</h2>
      <p>Se quando ti corichi parte il flusso dei pensieri — la lista della spesa, quella mail dimenticata, la conversazione di ieri — la <em>Melissa officinalis</em> è la pianta giusta. Uno studio del 2024 pubblicato su <em>Phytotherapy Research</em> ha confermato che riduce significativamente i sintomi dell'ansia notturna in soggetti con stress moderato.</p>
      <p>Funziona bene in sinergia con la valeriana — non a caso le miscele tradizionali le accoppiano spesso.</p>

      <h2>3. La passiflora, per le notti senza fine</h2>
      <p>La <em>Passiflora incarnata</em> è la scelta migliore per chi si sveglia di notte e fatica a riaddormentarsi. Agisce sui recettori GABA-A e sul sistema benzodiazepinico naturale, ma senza creare dipendenza né rebound mattutino.</p>

      <h3>Cosa NON fare</h3>
      <ul>
        <li>Aspettarsi un effetto sedativo immediato come quello dei farmaci. Le piante lavorano in 7-14 giorni di assunzione continuativa.</li>
        <li>Combinare più rimedi naturali senza una guida professionale. Anche le sinergie più note vanno calibrate.</li>
        <li>Trascurare l'igiene del sonno: luce blu, cene tardive, caffè dopo le 16 vanificano qualsiasi tisana.</li>
      </ul>

      <p>In parafarmacia troverai sia le miscele pronte di marchi che selezioniamo con cura, sia la nostra linea di tisane artigianali dove la Dottoressa Emy può comporre per te una formula su misura, partendo dalle tue specifiche difficoltà notturne.</p>`,
      image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 600'><defs><linearGradient id='g1' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%23C9DEEC'/><stop offset='100%' stop-color='%234A88AD'/></linearGradient></defs><rect width='800' height='600' fill='url(%23g1)'/><circle cx='580' cy='180' r='80' fill='%23FFF8EE' opacity='.85'/><circle cx='620' cy='160' r='75' fill='url(%23g1)'/><g stroke='%23FFFFFF' stroke-width='1' fill='none' opacity='.4'><circle cx='150' cy='400' r='3'/><circle cx='220' cy='450' r='2'/><circle cx='100' cy='480' r='2'/><circle cx='300' cy='420' r='3'/><circle cx='400' cy='470' r='2'/><circle cx='480' cy='440' r='2'/></g><path d='M 100 580 Q 200 500 300 540 T 500 520 T 700 550 L 700 600 L 100 600 Z' fill='%231F3A4D' opacity='.3'/></svg>",
      date: "2026-05-17T10:00:00+02:00",
      readingTime: "6 min",
      products: [
        { brand: "Esi", name: "Sonno No Stress", description: "Compresse con melatonina, valeriana e passiflora. La formula più richiesta per addormentarsi in modo naturale." },
        { brand: "Naturalsalus", name: "Sonno Mente", description: "Gocce a base di estratti titolati di passiflora, biancospino e melissa. Adatto anche a chi si sveglia nella notte." },
        { brand: "Bromatech", name: "Acronelle", description: "Probiotico specifico per l'asse intestino-cervello. La salute del microbiota influisce direttamente sulla qualità del sonno." }
      ],
      sources: [
        { name: "Istituto Superiore di Sanità — Insonnia", url: "https://www.iss.it" },
        { name: "Cochrane Review — Valerian for Insomnia", url: "https://www.cochranelibrary.com" },
        { name: "Humanitas — Disturbi del sonno", url: "https://www.humanitas.it" }
      ]
    },
    {
      id: "demo-stress-2026-05-16",
      slug: "vuoi-gestire-lo-stress-quotidiano-con-dolcezza",
      title: "Vuoi gestire lo stress quotidiano <em>con dolcezza?</em>",
      category: "omeopatia",
      categoryLabel: "Omeopatia",
      excerpt: "L'omeopatia non è magia: è un protocollo che lavora sui sintomi specifici. Per lo stress moderato esistono rimedi precisi, e abbiamo studiato quali funzionano davvero.",
      content: `<p>Lo stress non è un'unica esperienza: è una costellazione di sintomi che si manifestano in modo diverso da persona a persona. C'è chi lo somatizza nello stomaco, chi sulla pelle, chi nella mandibola serrata, chi nei pensieri ossessivi prima di addormentarsi. L'approccio omeopatico — quando applicato con rigore — prevede esattamente questa personalizzazione: si sceglie il rimedio in base al <em>tipo</em> di stress, non solo alla sua intensità.</p>

      <p>Vediamo i tre granuli più documentati dalla letteratura, con indicazioni precise su quando usarli.</p>

      <h2>Gelsemium 9 CH: per l'ansia anticipatoria</h2>
      <p>È il rimedio classico per chi vive lo stress <strong>prima</strong> di un evento: un esame, una presentazione, una visita medica. Tremori alle mani, bocca asciutta, voglia di scappare. Una pubblicazione del 2023 sull'<em>European Journal of Integrative Medicine</em> ha documentato un'efficacia statisticamente significativa rispetto al placebo nei test prima di prestazioni accademiche.</p>

      <h2>Ignatia 9 CH: per le emozioni trattenute</h2>
      <p>Se lo stress nasce da emozioni che non sono state espresse — un lutto recente, una delusione, una separazione — il rimedio classico è <em>Ignatia amara</em>. Il quadro tipico include sospiri profondi, nodo in gola, sintomi paradossali.</p>

      <h2>Argentum Nitricum 9 CH: per chi anticipa il peggio</h2>
      <p>Per la persona che vive lo stress come un costante "e se succedesse questo?". Pensiero anticipatorio, bisogno di certezze, sintomi gastrici sotto pressione.</p>

      <blockquote>"L'omeopatia chiede una cosa difficile: ascoltarsi prima di curarsi."</blockquote>

      <h3>Quando non basta</h3>
      <p>Importante essere chiari: l'omeopatia funziona bene su stress moderato. Per stati ansiosi marcati, disturbi del sonno persistenti, o sintomatologia depressiva, è essenziale rivolgersi a uno specialista. Non sostituisce mai una valutazione medica.</p>

      <p>In parafarmacia trovi tutti e tre i rimedi nei granuli da 4 g delle linee più affidabili — Boiron, Lehning, Loacker — oltre alla consulenza per individuare il rimedio più adatto al tuo quadro.</p>`,
      image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 600'><defs><linearGradient id='g2' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%23F8DED7'/><stop offset='100%' stop-color='%23EFC5BC'/></linearGradient></defs><rect width='800' height='600' fill='url(%23g2)'/><g fill='%23FFFFFF' opacity='.7'><circle cx='400' cy='300' r='80'/><circle cx='400' cy='300' r='60' fill='%23F8DED7'/><circle cx='400' cy='300' r='40' fill='%23FFFFFF'/><circle cx='400' cy='300' r='20' fill='%23B25849'/></g><g stroke='%23B25849' stroke-width='1.5' fill='none' opacity='.6'><circle cx='200' cy='200' r='40'/><circle cx='600' cy='400' r='35'/><circle cx='150' cy='450' r='25'/><circle cx='650' cy='150' r='30'/></g></svg>",
      date: "2026-05-16T10:00:00+02:00",
      readingTime: "5 min",
      products: [
        { brand: "Naturalsalus", name: "Relax Sciroppo", description: "Sciroppo a base di estratti vegetali calmanti, indicato per stress quotidiano e tensione nervosa lieve." },
        { brand: "Esi", name: "Tranquilly", description: "Compresse con magnesio, valeriana e griffonia. Supporto naturale per l'equilibrio emotivo." },
        { brand: "Solime", name: "Pappa Reale Bio", description: "Tonico naturale ricco di vitamine B. Adatto nei periodi di stress prolungato e affaticamento mentale." }
      ],
      sources: [
        { name: "European Journal of Integrative Medicine", url: "https://www.sciencedirect.com" },
        { name: "Ministero della Salute — Medicina non convenzionale", url: "https://www.salute.gov.it" },
        { name: "AIFA — Medicinali omeopatici", url: "https://www.aifa.gov.it" }
      ]
    },
    {
      id: "demo-pelle-2026-05-15",
      slug: "la-pelle-secca-non-ti-lascia-vivere-serena",
      title: "La pelle secca <em>non ti lascia vivere serena?</em>",
      category: "cura-del-corpo",
      categoryLabel: "Cura del corpo",
      excerpt: "Non è solo questione di crema: la pelle secca cronica nasce dalla barriera cutanea compromessa. Tre strategie cosmetiche evidence-based, e i prodotti che funzionano davvero.",
      content: `<p>Quando la pelle "tira" appena uscita dalla doccia, prude la sera, mostra micro-desquamazioni invisibili sotto il fondotinta — non si tratta di una pelle "che ha bisogno di idratazione". Si tratta di una <strong>barriera cutanea alterata</strong>, e la differenza è sostanziale: idratare una barriera che perde acqua è come riempire una vasca senza tappo.</p>

      <p>La dermatologia moderna ha chiarito che la riparazione della barriera lipidica richiede ingredienti specifici, in concentrazioni precise. Non basta una crema "ricca": serve un protocollo.</p>

      <h2>Ceramidi 2, 3, 5: i mattoni veri</h2>
      <p>Le ceramidi rappresentano oltre il 50% dei lipidi della barriera cutanea. Quando scendono, l'acqua transepidermica evapora più velocemente. Le formulazioni cosmetiche di nuova generazione contengono ceramidi biomimetiche identiche a quelle umane: i loro effetti clinici sono documentati in revisioni del <em>Journal of Investigative Dermatology</em>.</p>

      <h2>Niacinamide: il regolatore</h2>
      <p>La vitamina B3 topica, alla concentrazione del 4-5%, stimola la sintesi endogena di ceramidi e migliora la coesione tra i corneociti. È uno degli ingredienti cosmetici più studiati degli ultimi 20 anni — e uno dei più dimenticati nelle creme da farmacia banali.</p>

      <h2>Burro di karité grezzo: l'occlusivo che ripara</h2>
      <p>Un occlusivo lipidico applicato alla sera "sigilla" il film idrolipidico mentre la pelle si rigenera. Il burro di karité non raffinato — quello giallastro, leggermente granuloso — contiene fitosteroli e tocoferolo naturale che hanno un ruolo attivo, non solo barriera.</p>

      <blockquote>"Una pelle sana non è una pelle invisibile: è una pelle che fa il suo lavoro senza chiederti attenzioni."</blockquote>

      <h3>Il protocollo serale che consigliamo</h3>
      <ol>
        <li>Detersione delicata con olio o latte, mai con saponi schiumogeni</li>
        <li>Tonico riequilibrante senza alcol (pH 5,5)</li>
        <li>Siero con niacinamide</li>
        <li>Crema con ceramidi</li>
        <li>Sulle zone più secche, un velo di burro di karité</li>
      </ol>

      <p>Da noi trovi tre linee che lavorano specificamente sulla barriera cutanea — formulazioni dermocompatibili, senza profumi sintetici, senza tensioattivi aggressivi.</p>`,
      image: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 800 600'><defs><linearGradient id='g3' x1='0%' y1='0%' x2='100%' y2='100%'><stop offset='0%' stop-color='%23E4EFF7'/><stop offset='100%' stop-color='%239CC2DA'/></linearGradient></defs><rect width='800' height='600' fill='url(%23g3)'/><g opacity='.85'><circle cx='320' cy='280' r='40' fill='%23FFFFFF'/><rect x='280' y='320' width='80' height='180' rx='6' fill='%23FFFFFF'/><circle cx='550' cy='250' r='35' fill='%23F8DED7'/><rect x='515' y='285' width='70' height='200' rx='8' fill='%23F8DED7'/></g><g stroke='%231F3A4D' stroke-width='1' fill='none' opacity='.3'><circle cx='150' cy='400' r='100'/><circle cx='650' cy='450' r='80'/></g></svg>",
      date: "2026-05-15T10:00:00+02:00",
      readingTime: "7 min",
      products: [
        { brand: "Lovrèn", name: "Cera Reparative Cream", description: "Crema viso con ceramidi 2-3-5 e niacinamide al 4%. Rigenera la barriera in 14 giorni." },
        { brand: "Algàdemy", name: "Sea Mineral Serum", description: "Siero a base di acqua di mare ricca di minerali bioidentici. Rinforza la pelle dall'interno." },
        { brand: "Solime", name: "Burro di Karité Bio", description: "Burro di karité grezzo non raffinato, da agricoltura biologica. Per zone secche e screpolature." }
      ],
      sources: [
        { name: "Journal of Investigative Dermatology", url: "https://www.jidonline.org" },
        { name: "Humanitas — Dermatite e xerosi cutanea", url: "https://www.humanitas.it" },
        { name: "Mayo Clinic — Dry skin overview", url: "https://www.mayoclinic.org" }
      ]
    }
  ]
};

// State
let blogState = {
  articles: [],
  filteredArticles: [],
  currentCategory: 'all',
  currentSlug: null,
  loaded: false,
};

// Util: formatta data ISO in italiano leggibile
function formatBlogDate(iso){
  const d = new Date(iso);
  const months = ['gennaio','febbraio','marzo','aprile','maggio','giugno','luglio','agosto','settembre','ottobre','novembre','dicembre'];
  return `${d.getDate()} ${months[d.getMonth()]} ${d.getFullYear()}`;
}

// Util: escape HTML
function esc(s){ return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function escAttr(s){ return esc(s); }

// Carica articoli (con fallback locale)
async function loadBlogArticles(){
  if(blogState.loaded) return blogState.articles;
  try{
    // Cache buster: GitHub Pages e il CDN davanti servono spesso
    // articles.json dalla cache anche dopo che l'agente AI ha pushato
    // la nuova versione. Il timestamp forza una richiesta fresca.
    const cacheBuster = Date.now();
    const res = await fetch(BLOG_ARTICLES_URL + '?_=' + cacheBuster, { cache: 'no-store' });
    if(!res.ok) throw new Error('Fetch failed');
    const data = await res.json();
    blogState.articles = Array.isArray(data.articles) ? data.articles : [];
  } catch(e){
    console.info('[Blog] Uso dati fallback (articles.json non ancora pubblicato)');
    blogState.articles = BLOG_FALLBACK_DATA.articles;
  }
  // Ordina per data discendente (più recenti prima)
  blogState.articles.sort((a, b) => new Date(b.date) - new Date(a.date));
  blogState.loaded = true;
  return blogState.articles;
}

// Renderizza card per la griglia
function renderBlogCard(article){
  return `
    <article class="blog-card" data-slug="${escAttr(article.slug)}">
      <div class="blog-card-img">
        <img src="${escAttr(assetUrl(article.image))}" alt="${escAttr(article.categoryLabel)}" loading="lazy"/>
      </div>
      <div class="blog-card-body">
        <span class="blog-tag cat-${escAttr(article.category)}">${esc(article.categoryLabel)}</span>
        <h4>${article.title}</h4>
        <p>${esc(article.excerpt)}</p>
        <div class="blog-card-meta">
          <span>${esc(formatBlogDate(article.date))}</span>
          <span class="dot"></span>
          <span>${esc(article.readingTime)} lettura</span>
          <span class="read-more">Leggi →</span>
        </div>
      </div>
    </article>
  `;
}

// Renderizza featured
function renderFeaturedArticle(article){
  return `
    <div class="featured-img">
      <img src="${escAttr(assetUrl(article.image))}" alt="${escAttr(article.categoryLabel)}" loading="lazy"/>
    </div>
    <div class="featured-content">
      <span class="blog-tag cat-${escAttr(article.category)}">${esc(article.categoryLabel)} · In evidenza</span>
      <h2>${article.title}</h2>
      <p class="excerpt">${esc(article.excerpt)}</p>
      <div class="featured-meta">
        <span>${esc(formatBlogDate(article.date))}</span>
        <span class="dot"></span>
        <span>${esc(article.readingTime)} lettura</span>
        <span class="dot"></span>
        <span class="read-more" style="color:var(--azzurro-deep); font-weight:600;">Leggi l'articolo →</span>
      </div>
    </div>
  `;
}

// Renderizza pagina lista blog
async function renderBlogList(category = 'all'){
  const loading = document.getElementById('blogLoading');
  const featuredSection = document.getElementById('blogFeaturedSection');
  const gridSection = document.getElementById('blogGridSection');
  const grid = document.getElementById('blogGrid');
  const featured = document.getElementById('blogFeatured');
  const empty = document.getElementById('blogEmpty');
  const counter = document.getElementById('blogCounter');

  loading.classList.add('visible');
  featuredSection.style.display = 'none';
  gridSection.style.display = 'none';

  await loadBlogArticles();

  // Filtra
  const filtered = category === 'all'
    ? blogState.articles
    : blogState.articles.filter(a => a.category === category);

  blogState.filteredArticles = filtered;
  blogState.currentCategory = category;

  loading.classList.remove('visible');

  if(filtered.length === 0){
    featuredSection.style.display = 'none';
    gridSection.style.display = 'block';
    grid.innerHTML = '';
    empty.style.display = 'block';
    counter.textContent = '';
    return;
  }

  empty.style.display = 'none';

  // Articolo featured = il più recente
  const [first, ...rest] = filtered;
  featured.innerHTML = renderFeaturedArticle(first);
  featured.dataset.slug = first.slug;
  featuredSection.style.display = 'block';

  // Resto in griglia
  if(rest.length > 0){
    grid.innerHTML = rest.map(renderBlogCard).join('');
    gridSection.style.display = 'block';
  } else {
    gridSection.style.display = 'none';
  }

  counter.textContent = `${filtered.length} articol${filtered.length === 1 ? 'o' : 'i'}`;

  // Bind click handlers
  document.querySelectorAll('.blog-card, .featured-article').forEach(card => {
    card.addEventListener('click', () => {
      const slug = card.dataset.slug;
      if(slug){
        history.pushState({}, '', `#blog/${slug}`);
        renderArticleRoute(slug);
      }
    });
  });
}

// Renderizza singolo articolo
async function renderSingleArticle(slug){
  await loadBlogArticles();
  const article = blogState.articles.find(a => a.slug === slug);
  const container = document.getElementById('singleArticle');

  if(!article){
    container.innerHTML = `
      <div class="wrap">
        <div class="blog-empty" style="padding: 120px 20px;">
          <p>Articolo non trovato.</p>
          <a href="/blog/" data-page="blog" class="btn btn-primary" style="margin-top:20px;">Torna al blog</a>
        </div>
      </div>
    `;
    bindMenuLinks();
    return;
  }

  const related = blogState.articles
    .filter(a => a.slug !== slug && a.category === article.category)
    .slice(0, 3);

  updateMetaTags(
    article.title.replace(/<[^>]*>/g, '') + SITE_TITLE_SUFFIX,
    article.excerpt
  );

  container.innerHTML = `
    <section class="article-hero">
      <div class="wrap">
        <a href="/blog/" data-page="blog" class="article-back">Torna al blog</a>
        <div class="article-meta-row">
          <span class="blog-tag cat-${escAttr(article.category)}">${esc(article.categoryLabel)}</span>
          <span class="dot"></span>
          <span>${esc(formatBlogDate(article.date))}</span>
          <span class="dot"></span>
          <span>${esc(article.readingTime)} di lettura</span>
        </div>
        <h1 class="article-title">${article.title}</h1>
        <div class="article-hero-img">
          <img src="${escAttr(assetUrl(article.image))}" alt="${escAttr(article.title.replace(/<[^>]*>/g,''))}"/>
        </div>
      </div>
    </section>

    <div class="wrap">
      <div class="article-content">
        <div class="excerpt-lead">${esc(article.excerpt)}</div>
        ${article.content}
      </div>

      ${article.products && article.products.length > 0 ? `
      <div class="article-products">
        <div class="section-eyebrow">Prodotti consigliati</div>
        <h3>Le soluzioni che <em>trovi da noi</em></h3>
        <p class="products-lead">Selezione di prodotti dei marchi presenti in parafarmacia, scelti dalla Dottoressa Emy come soluzioni concrete per quanto descritto sopra.</p>
        <div class="products-grid">
          ${article.products.map(p => `
            <div class="product-card">
              <div class="product-brand">${esc(p.brand)}</div>
              <h4>${esc(p.name)}</h4>
              <p>${esc(p.description)}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${article.sources && article.sources.length > 0 ? `
      <div class="article-sources">
        <h5>Fonti consultate</h5>
        <ul>
          ${article.sources.map(s => `
            <li><a href="${escAttr(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>
          `).join('')}
        </ul>
      </div>
      ` : ''}

      <div class="article-disclaimer">
        <strong>Una nota importante.</strong> Le informazioni di questo articolo hanno carattere divulgativo e non sostituiscono il parere del tuo medico o farmacista di fiducia. In caso di sintomi persistenti, allergie note o assunzione di farmaci, chiedi sempre una consulenza professionale prima di iniziare qualsiasi integrazione o cosmesi attiva.
      </div>

      <div class="article-cta">
        <span class="eyebrow" style="justify-content:center; display:flex;">Vuoi un consiglio personale?</span>
        <h3>Passa in <em>parafarmacia</em></h3>
        <p>La Dottoressa Emy può ascoltare il tuo caso specifico e suggerirti la soluzione più adatta. Senza fretta.</p>
        <a href="/contatti/" data-page="contatti" class="btn btn-primary">Come trovarci →</a>
      </div>
    </div>

    ${related.length > 0 ? `
    <section class="related-articles">
      <div class="wrap">
        <h3>Altri articoli <em>sullo stesso tema</em></h3>
        <div class="related-grid">
          ${related.map(renderBlogCard).join('')}
        </div>
      </div>
    </section>
    ` : ''}
  `;

  // Bind click handlers per related + back
  bindMenuLinks();
  container.querySelectorAll('.blog-card').forEach(card => {
    card.addEventListener('click', () => {
      const s = card.dataset.slug;
      if(s){
        history.pushState({}, '', `#blog/${s}`);
        renderArticleRoute(s);
      }
    });
  });

  window.scrollTo({ top: 0, behavior: 'instant' });
}

// Route: gestisce #blog vs #blog/slug
function renderArticleRoute(slug){
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-article').classList.add('active');
  document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
  document.querySelector('.menu a[data-page="blog"]')?.classList.add('active');
  blogState.currentSlug = slug;
  renderSingleArticle(slug);
}

/* ============== SCHEDA INGREDIENTE TISANA ============== */

function renderIngredientRoute(slug){
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-ingredient').classList.add('active');
  document.querySelectorAll('.menu a').forEach(a => a.classList.remove('active'));
  document.querySelector('.menu a[data-page="tisane"]')?.classList.add('active');
  renderSingleIngredient(slug);
  window.scrollTo({ top: 0, behavior: 'instant' });
}

function renderSingleIngredient(slug){
  const container = document.getElementById('ingredientContainer');
  const ing = (typeof INGREDIENTS_DATA !== 'undefined' ? INGREDIENTS_DATA : []).find(i => i.slug === slug);

  if(!ing){
    container.innerHTML = `
      <section class="article-hero">
        <div class="wrap">
          <a class="article-back" data-page="tisane" href="/tisane/">Torna alle tisane</a>
          <h1 class="article-title">Ingrediente non trovato</h1>
        </div>
      </section>
      <div class="wrap"><div class="article-content"><p>Prova a tornare alla pagina delle tisane e scegliere un ingrediente dalla griglia.</p></div></div>
    `;
    bindMenuLinks();
    return;
  }

  updateMetaTags(
    `${ing.name} — Tisane` + SITE_TITLE_SUFFIX,
    ing.intro
  );

  container.innerHTML = `
    <section class="article-hero">
      <div class="wrap">
        <a class="article-back" data-page="tisane" href="/tisane/">Torna alle tisane</a>
        <div class="article-meta-row">
          <span>Ingredienti delle nostre tisane</span>
          <span class="dot"></span>
          <span>${esc(ing.action)}</span>
        </div>
        <h1 class="article-title">${esc(ing.name)}</h1>
        <div class="article-hero-img" style="background:var(--azzurro-luce); display:flex; align-items:center; justify-content:center;">
          <img src="${escAttr(ing.img)}" alt="${escAttr(ing.name)}" style="width:auto; height:100%; max-height:340px; object-fit:contain;"/>
        </div>
      </div>
    </section>

    <div class="wrap">
      <div class="article-content">
        <div class="excerpt-lead">${esc(ing.intro)}</div>
        ${ing.content}
      </div>

      <div class="article-disclaimer">
        <strong>Una nota importante.</strong> Le informazioni di questa scheda hanno carattere divulgativo e non sostituiscono il parere del tuo medico o farmacista di fiducia, specialmente in caso di terapie in corso, gravidanza o allattamento.
      </div>

      <div class="article-cta">
        <span class="eyebrow" style="justify-content:center; display:flex;">Vuoi assaggiarla?</span>
        <h3>Vieni a scoprirla in <em>parafarmacia</em></h3>
        <p>La Dottoressa Emy può consigliarti la miscela giusta in cui trovi questo ingrediente, su misura per te.</p>
        <a href="/contatti/" data-page="contatti" class="btn btn-primary">Come trovarci →</a>
      </div>
    </div>
  `;

  bindMenuLinks();
}

// Click sugli ingredienti nella griglia della pagina Tisane
document.getElementById('herbsGrid')?.addEventListener('click', e => {
  const card = e.target.closest('.herb');
  if(!card) return;
  const slug = card.dataset.slug;
  if(slug){
    history.pushState({}, '', `#tisane/${slug}`);
    renderIngredientRoute(slug);
  }
});

// Re-bind dei link menu in contenuti generati dinamicamente
function bindMenuLinks(){
  document.querySelectorAll('[data-page]').forEach(link => {
    if(link._bound) return;
    link._bound = true;
    link.addEventListener('click', e => {
      e.preventDefault();
      const page = link.getAttribute('data-page');
      history.pushState({}, '', slugToPath(page));
      navigate(page);
    });
  });
}

// Filtri click handler
document.querySelectorAll('.blog-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.blog-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderBlogList(btn.dataset.cat);
  });
});


/* ============== FORM ============== */
const form = document.getElementById('contactForm');
const success = document.getElementById('formSuccess');

form.addEventListener('submit', e => {
  e.preventDefault();

  const titolo = document.getElementById('f-titolo').value.trim();
  const msg = document.getElementById('f-msg').value.trim();
  const nome = document.getElementById('f-nome').value.trim();
  const contatto = document.getElementById('f-contatto').value.trim();
  const privacy = document.getElementById('f-privacy').checked;

  if(!titolo || !msg || !nome || !contatto){
    alert('Compila tutti i campi richiesti.');
    return;
  }
  if(!privacy){
    alert('Per inviare il messaggio devi accettare l\'informativa privacy.');
    return;
  }

  const btn = form.querySelector('.form-submit');
  const original = btn.innerHTML;
  btn.disabled = true; btn.innerHTML = 'Invio in corso…';

  sendViaFormSubmit({
    _subject: '[Sito web] ' + titolo,
    Oggetto: titolo,
    Messaggio: msg,
    Nome: nome,
    Contatto: contatto
  }).then(ok => {
    if(ok){
      form.reset();
      success.classList.add('visible');
      btn.innerHTML = 'Inviato ✓';
    } else {
      alert('Invio non riuscito. Riprova, oppure scrivici a parafarmaciavialeumberto@gmail.com');
      btn.disabled = false; btn.innerHTML = original;
    }
  }).catch(() => {
    alert('Errore di rete. Riprova o chiamaci allo 0522 081652.');
    btn.disabled = false; btn.innerHTML = original;
  });
});

/* ============== RECENSIONI GOOGLE ============== */
/*
 * Carica reviews.json (popolato da reviews_agent.py una volta al giorno)
 * e renderizza il riepilogo + le card nella sezione "Cosa dicono di noi"
 * in fondo alla home page. Stesso pattern del blog: fetch con cache-buster,
 * fallback silenzioso se il file non esiste ancora.
 */
(function initGoogleReviews(){
  const STAR_FULL = '<svg viewBox="0 0 24 24" fill="#F5A623"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';
  const STAR_EMPTY = '<svg viewBox="0 0 24 24" fill="none" stroke="#D8C79A" stroke-width="1.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>';

  function starsHtml(rating){
    const r = Math.round(rating || 0);
    let html = '';
    for(let i = 1; i <= 5; i++) html += (i <= r ? STAR_FULL : STAR_EMPTY);
    return html;
  }

  function escR(s){ return String(s ?? '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }

  function reviewCard(rv){
    const initial = escR((rv.author || '?').trim().charAt(0).toUpperCase());
    const avatar = rv.authorPhoto
      ? `<img class="review-avatar" src="${escR(rv.authorPhoto)}" alt="${escR(rv.author)}" loading="lazy" referrerpolicy="no-referrer">`
      : `<div class="review-avatar-fallback">${initial}</div>`;
    return `
      <article class="review-card">
        <div class="review-head">
          ${avatar}
          <div>
            <div class="review-author">${escR(rv.author)}</div>
            <div class="review-time">${escR(rv.relativeTime || '')}</div>
          </div>
        </div>
        <div class="review-stars stars">${starsHtml(rv.rating)}</div>
        <p class="review-text">${escR(rv.text)}</p>
      </article>
    `;
  }

  async function loadReviews(){
    const summary = document.getElementById('reviewsSummary');
    const grid = document.getElementById('reviewsGrid');
    const empty = document.getElementById('reviewsEmpty');
    const googleLink = document.getElementById('reviewsGoogleLink');
    if(!summary || !grid) return;

    try{
      const cacheBuster = Date.now();
      const res = await fetch('/reviews.json?_=' + cacheBuster, { cache: 'no-store' });
      if(!res.ok) throw new Error('Fetch failed');
      const data = await res.json();
      const reviews = Array.isArray(data.reviews) ? data.reviews : [];

      if(data.mapsUrl && googleLink) googleLink.href = data.mapsUrl;

      if(reviews.length === 0){
        empty.style.display = 'block';
        return;
      }

      if(data.rating){
        summary.innerHTML = `
          <span class="stars">${starsHtml(data.rating)}</span>
          <span class="score">${Number(data.rating).toFixed(1)}</span>
          <span class="count">su ${escR(data.userRatingsTotal || reviews.length)} recensioni Google</span>
        `;
      }

      grid.innerHTML = reviews.map(reviewCard).join('');
    } catch(e){
      console.info('[Reviews] reviews.json non ancora disponibile');
      empty.style.display = 'block';
    }
  }

  loadReviews();
})();

(function(){
  'use strict';
  var farfalla = document.getElementById('farfalla');
  var path     = document.getElementById('farfalla-path');
  if (!farfalla || !path) return;

  var lunghezza = path.getTotalLength();
  var posX = 0, posY = 0, angolo = 0;
  var primoFrame = true;

  function progressoScroll(){
    var sc  = document.scrollingElement || document.documentElement;
    var max = sc.scrollHeight - window.innerHeight;
    if (max <= 0) return 0;
    var p = sc.scrollTop / max;
    return Math.min(1, Math.max(0, p));
  }

  function puntoInPixel(distanza){
    var pt = path.getPointAtLength(distanza);
    return {
      x: pt.x / 100 * window.innerWidth,
      y: pt.y / 100 * window.innerHeight
    };
  }

  function frame(){
    var d      = progressoScroll() * lunghezza;
    var qui    = puntoInPixel(d);
    var avanti = puntoInPixel(Math.min(lunghezza, d + 1));
    var target = Math.atan2(avanti.y - qui.y, avanti.x - qui.x) * 180 / Math.PI + 90;

    if (primoFrame){
      posX = qui.x; posY = qui.y; angolo = target; primoFrame = false;
    } else {
      posX += (qui.x - posX) * 0.075;
      posY += (qui.y - posY) * 0.075;
      var diff = target - angolo;
      while (diff >  180) diff -= 360;
      while (diff < -180) diff += 360;
      angolo += diff * 0.075;
    }

    farfalla.style.transform =
      'translate(' + (posX - 46) + 'px,' + (posY - 39.5) + 'px) rotate(' + angolo + 'deg)';

    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  window.addEventListener('load', function(){
    var sc = document.scrollingElement || document.documentElement;
    if (sc.scrollHeight - window.innerHeight <= 0){
      console.warn('[farfalla] La pagina non è scrollabile: la farfalla resta ferma al punto di partenza.');
    }
  });
})();

/* ============== INIT ROUTING ============== */
// Deve girare per ultimo: navigate('blog') tocca blogState (dichiarato più
// sopra con `let` nel BLOG ENGINE), quindi va chiamato solo a script
// completamente valutato per evitare un ReferenceError da temporal dead zone.
navigate(pathToSlug());
