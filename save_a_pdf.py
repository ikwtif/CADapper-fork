import time
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.lib.colors import (
    black,
    purple,
    white,
    yellow
)

"""
issue emtpy page after 'voorblad'
comment Story.append(PageBreak()) --- possible fix?

added to \lib\site-packages\reportlab\platypus\doctemplate.py

class BaseDocTemplate
    def handle_pageBreak()
            '''ignore page break on empty page'''
            if self._curPageFlowableCount == 1:
                return

set to '==1' instead of '==0' because footer/header????
"""





class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
            canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 10.5*cm
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.75)
        self.line(2*cm, 3.4*cm, A4[0] - 2*cm, 3.4*cm)
        self.setFont('Times-Roman', 10)
        """
        self.drawCentredString(A4[0]-x, 65, page)
        """
        #added footer
        self.setFont('Helvetica-Bold', 9, leading=None)
        self.drawCentredString(10.5*cm, 3*cm, 'Veiligheidscoördinatie - Topografie - EPB/EPC verslaggeving - Stabiliteitsberekeningen - Blowerdoortest')
        self.setFont('Helvetica', 9, leading=None)
        self.drawString(2*cm, 2.6*cm, 'Kantoor: Bergestraat 49/3, 9550 Herzele ')
        self.drawRightString(A4[0]-2*cm, 2.6*cm, 'Tel: 054/59.82.82')
        self.drawString(2*cm, 2.3*cm, 'Rekening: Belfius BE63 0688 9630 7208')
        self.drawRightString(A4[0]-2*cm, 2.3*cm, 'Fax: 054/59.84.59')
        self.drawString(2*cm, 2*cm, 'BTW: 0508.800.434')
        self.restoreState()

    def add_header(self, Story, styles):
        self.I = Image('Topco_logo.png')
        self.I.drawHeight = 3.25*cm
        self.I.drawWidth = 3*cm
        self.T1 = Paragraph('''<para align=Left spaceb=20><font size=20>TOPCO</font><font size=10><strong>+</strong></font><font size=6>bvba</font></para>''', styles["Topco"])
        self.T2 = Paragraph('''<font size=6>Bergestraat 49/3 <br/> \
        9550 Herzele</font>''', styles["Text"])
        self.data = [[self.I, self.T1],['',self.T2]]
        t = Table(self.data,2*[3.5*cm],2*[1.75*cm], style=[
                                                ('ALIGN',(0,0),(1,0),'LEFT'),        # removed grid ('GRID',(0,0),(-1,-1),0.25,colors.black),
                                                ('VALIGN',(0,1),(0,-1),'MIDDLE'),
                                                ('VALIGN',(0,0),(0,0),'TOP'),
                                                ('VALIGN',(1,0),(1,0),'MIDDLE'),
                                                ('VALIGN',(-1,-1),(-1,-1),'MIDDLE'),
                                                ('LEFTPADDING',(0,0),(1,0), 0)
                                                ], hAlign='LEFT') #horizontal align table
        Story.append(t)
        Story.append(Spacer(1,2))

    def voorblad(self, Story, styles):
        #dossiernummer
        self.ptext = '<font size=10><u>Ref.: {}</u></font>'.format(self.dossier_nummer)
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 20))

        #betreft stabiliteitsstudie
        self.ptext = '<para align=Center><font size=14><strong>Betreft: stabiliteitsstudie</strong></font></para>'
        Story.append(Paragraph(self.ptext, styles["Textborder"]))
        Story.append(Spacer(1, 40))

        #werfadres
        self.ptext = 'Bouwheer: <br/> \
        {} <br/> \
        {} <br/> \
        {}'.format(self.woning_naam, self.werf_straat, self.werf_gemeente)
        Story.append(Paragraph(self.ptext, styles["Textcenter"]))
        Story.append(Spacer(1, 40))

        #architect
        self.ptext = 'Architect: <br/> \
        {} <br/> \
        {} <br/> \
        {}'.format(self.architect_naam, self.architect_straat, self.architect_gemeente)
        Story.append(Paragraph(self.ptext, styles["Textcenter"]))
        Story.append(Spacer(1, 40))

        #aannemer
        self.ptext = 'Aannemer: <br/> \
        {} <br/> \
        {} <br/> \
        {}'.format(self.aannemer_naam, self.aannemer_straat, self.aannemer_gemeente)
        Story.append(Paragraph(self.ptext, styles["Textcenter"]))
        Story.append(Spacer(1, 40))

        #ingenieur
        self.ptext = 'Ingenieur: <br/> \
        {}'.format(self.ingenieur_naam)
        Story.append(Paragraph(self.ptext, styles["Textcenter"]))
        Story.append(Spacer(1, 40))

        #datum
        self.ptext = '{}'.format(self.datum)
        Story.append(Paragraph(self.ptext, styles["Textcenter"]))
        Story.append(Spacer(1, 40))

    def inhouds_tafel(self, Story, styles):

        Story.append(Spacer(1, 20))

        #betreft stabiliteitsstudie
        self.ptext = '<para align=Center><font size=14><strong>Overzicht inhoud bundel</strong></font></para>'
        Story.append(Paragraph(self.ptext, styles["Textborder"]))
        Story.append(Spacer(1, 80))


        #lijst
        self.ptext = '<font size=14>1. Algemene beschrijving beton, staal en \
        uitvoeringstechnieken voor stabiliteit</font>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 40))

        self.ptext = '<font size=14>2. Meetstaat stabiliteit</font>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 40))


        self.ptext = '<font size=14>3. Staalborderel</font>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 40))


        self.ptext = '<font size=14>Plannen en uitvoeringsdetails in bijlage</font>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 40))

    def beschrijving(self, Story, styles):

        #dossiernummer
        self.ptext = '<font size=10><u>Dossiernr.: {}</u></font>'.format(self.dossier_nummer)
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))
        #beton
        """beschrijving beton"""

        self.ptext = '<font size=12><strong>Betreft: Beschrijving Beton voor stabiliteit</strong></font>'
        Story.append(Paragraph(self.ptext, styles["Border"]))
        Story.append(Spacer(1, 12))
        #1
        self.ptext = '<u>1. Algemene specificaties en eisen</u>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        ptext = 'De vervaardiging, specificatie en eigenschappen van het beton en \
        de productiecontrole moeten voldoen aan de eisen en de richtlijnen van de normen \
        NBN EN206-1:2001 en NBN B 15001:2004 «Beton – Eisen, gedraging, vervaardiging en \
        overeenkomstigheid». Beide normen zijn in hun geheel van toepassing. \
        Dit bestek vult beide normen aan waar een keuze moet gemaakt worden. \
        Alle betonsoorten zijn van het type ‘met gespecificeerde eigenschappen’. \
        Dit impliceert dat de aannemer verantwoordelijk is voor de levering van \
        beton dat beantwoordt aan de basiseisen en de eventuele aanvullende \
        eisen vereist door dit lastenboek en door beide voornoemde normen.'

        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2
        self.ptext = '<u>2. Bijzondere specificaties</u>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = 'De gebruikte terminologie is die van de normen \
        <b>NBN EN 206-1:2001 en NBN B 15 001:2004</b>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2.1
        self.ptext = '<u>2.1 Eisen</u>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Sterkteklasse:</u> C 25/30 (funderingen) C30/37 (balken & kolommen) <br/> \
        <u>Duurzaamheidseisen met B1 (gebruiksdomein) en B2 (omgevingsklasse): </u><br/> \
        Gewapend beton (GB) en EE1 (geen vorst en fundering onder vorstgrens,...) \
        en EE2 voor de gewapende betonbalken <br/> \
        <u>Concistentieklasse:</u> S3 <br/> \
        <u>Nominale grootste korrelafmeting (Dmax):</u> 20, 22 of 32 <br/> \
        <u>Aanvullende eisen:</u> /'
        Story.append(Paragraph(self.ptext, styles["Textborder"]))
        Story.append(Spacer(1, 12))

        #2.2 tot 2.2.2
        self.ptext = '2.2 Controle op de bouwplaats van de conformiteit met de eisen <br/> \
        2.2.1 Voor de aanvang van het storten moet de aannemer de herkomst van het \
        beton melden aan de bouwheer: hetzij gefabriceerd op de bouwplaats, \
        hetzij afkomstig van niet-BENOR centrale of BENOR-centrale.  <br/> \
        2.2.2 Het beton afkomstig van een centrale beschikkend over de BENOR-licentie \
        werd geproduceerd onder controle van een derde partij. Het moet niet meer gecontroleerd \
        worden op de bouwplaats. De herkomst van een BENOR-centrale wordt bewezen door leveringsbonnen \
        die het BENOR-labeldragen en het identificatienummer toegekend door het \
        BENOR-certificatieinstelling. Op de bon moeten alle eisen van 2.1 en alle gegevens \
        volgens artikel 7.3 van bovenvernoemde normen vermeld staan. De leveringsbonnen worden \
        bewaard op de bouwplaats en blijven ter beschikking van de bouwheer.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2.2.3
        self.ptext = '2.2.3 Beton dat niet geleverd of gefabriceerd wordt onder het BENOR-merk valt volledig \
        onder de verantwoordelijkheid van de aannemer zelfs als hij de fabricage ervan toevertrouwt \
        aan een derde (niet-BENOR) centrale. De aannemer moet bijgevolg het chronologische verloop \
        van het storten van het beton (samenstelling, hoeveelheden en uitgevoerde controles) in het \
        logboek bijhouden. Bovendien moet hij zich, door middel van regelmatige controles, \
        vergewissen van de conformiteit met de eisen. Deze controle slaat op alle factoren die \
        de kwaliteit van het beton kunnen aantasten, zoals vermeld in hoofdstuk 9 van NBN EN 206-1:2001. \
        De schriftelijke verslagen van de uitgevoerde controles en van de bekomen resultaten moeten \
        op eenvoudige aanvraag aan de bouwheer overhandigd kunnen worden.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2.2.3.1
        self.ptext = '2.2.3.1 Controle van de sterkteklasse \
        Wat de sterkteklasse van het beton in het bijzonder betreft zijn de \
        controlemodaliteiten als volgt:'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '&bull;  De aannemer zal alle controlewerkzaamheden i. v. m. de sterkte van het beton, \
        op zijn kosten, toevertrouwen aan een erkend laboratorium, en dit vanaf de monsterneming \
        van het beton op de bouwplaats tot het verbrijzelen van de proefstukken. <br/> \
        &bull;  Ongeacht de plaats waar het beton gefabriceerd wordt, gebeuren de monsternemingen \
        altijd op de bouwplaats. De monsternemingen hebben plaats ten minste 1 maal per productie- \
        of leveringsdag van het beton, voor iedere gefabriceerde of geleverde sterkteklasse. \
        Indien de gefabriceerde of geleverde hoeveelheid van één dag voor een zelfde sterkteklasse \
        meer dan 75 m3 bedraagt, wordt overgegaan tot een monsterneming per schijf van 75 m3, \
        waarbij uit elke aangebroken schijf een monster genomen wordt. <br/> \
        &bull;  Elke monsterneming moet afkomstig zijn van een verschillende lading of truckmixer. \
        Uit elke monsterneming worden 3 kubusvormige proefstukken vervaardigd van 150 mm zijde. \
        Op 28 dagen worden de proefstukken onderworpen aan een drukproef. Het RESULTAAT dat de \
        monsterneming kenmerkt, is het gemiddelde van de 3 proeven. De controle slaat op elke groep \
        van 3 opeenvolgende resultaten, waarbij ieder resultaat slechts tot één groep behoort \
        (sterkteklasse). Het gemiddelde van de 3 opeenvolgende resultaten moet hoger liggen dan \
        of gelijk zijn aan : fck,cube + 8 ( in N/mm2) Elk resultaat moet hoger zijn dan of gelijk \
        aan: fck,cube - 1 (in N/mm2). fckcube is het tweede getal in de genormaliseerde aanduiding \
        C25/30 van de sterkteklasse (cfr. 2.1). De resultaten die geen deel uitmaken van een groep \
        van 3 opeenvolgende resultaten (zoals de laatste resultaten van een serie die geen veelvoud \
        is van 3) moeten alle hoger liggen dan of gelijk zijn aan fck,cube + 5 (in N/mm2). \
        Het erkende laboratorium dat aangeduid is om de proeven uit te voeren bezorgt een kopie \
        van de proefverslagen rechtstreeks aan de bouwheer.'
        Story.append(Paragraph(self.ptext, styles["Textbullet"]))
        Story.append(Spacer(1, 12))

        #2.2.3.2
        self.ptext = '2.2.3.2 Controle van de consistentie <br/> \
        De aannemer voert de controles op de consistentie van het gefabriceerde of geleverde beton uit \
        met dezelfde frequentie als die op de sterkteklasse. Daartoe moet hij beschikken over het \
        nodige materiaal.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))


        #2.2.3.3
        self.ptext = '2.2.3.3 Andere controles <br/> \
        De bouwheer behoudt zich het recht toe op zijn kosten alle controles uit te voeren of te laten \
        uitvoeren m. b. t. tot andere eisen dan die van de sterkte- of consistentieklasse.  <br/> \
        De aannemer wordt geacht hem hiertoe, kosteloos, de nodige assistentie te verlenen.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2.2.3.3
        self.ptext = '2.3 Transport, verwerking en nabehandeling van het verse beton <br/> \
        De aannemer wordt geacht de nodige maatregelen te treffen om de kwaliteit van het beton te \
        vrijwaren tijdens het transport op de bouwplaats, de verwerking en de duur van de verharding. \
        Deze maatregelen worden besproken in NBN ENV 13670-1:2000 ‘Het vervaardigen van \
        betonconstructies – Deel 1 Algemeen gedeelte’. <br/> \
        Telkens de bouwheer of zijn afgevaardigde, in het kader van zijn opdracht van algemeen toezicht \
        op de werken, op de bouwplaats komt, zal hij streng toekijken op de strikte naleving van \
        deze maatregelen.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #2.4
        self.ptext = '2.4 Nalatigheid (inbreuk, overtreding) en niet-conformiteit <br/> \
        Wanneer de bouwheer merkt dat de technische en administratieve vereisten m. b. t. de kwaliteit \
        van het beton niet of onvoldoende nageleefd worden, stelt hij hiervan een proces-verbaal op en \
        verwittigt hij de aannemer. Als deze laatste geen aannemelijke verklaring kan geven, wordt hem \
        automatisch een forfaitaire boete van …EUR per overtreding aangerekend. Beton dat niet conform \
        is met de vereiste sterkte wordt geweigerd en afgebroken. Op vraag van de aannemer, en op zijn \
        kosten, kan evenwel een bijkomend onderzoek gevoerd worden naar de reëe kwaliteit van het beton \
        in het bouwwerk. Naar gelang de uitslag van dat onderzoek kan de bouwheer besluiten het beton \
        niet af te breken maar wel een korting toe te passen evenredig met de ernst van het sterktegebrek \
        en de hoeveelheid verdacht beton.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        """---------------------------------------------------------------------"""
        #staal
        """beschrijving staal"""

        self.ptext = '<font size=12><strong>Betreft: Beschrijving Staal voor stabiliteit</strong></font>'
        Story.append(Paragraph(self.ptext, styles["Border"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Staalsoort:</u> BE500 <br/> \
        Alle informatie over het gewenste staaldiameter en lengte: zie wapeningsplan.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        """---------------------------------------------------------------------"""
        #opmerkinen aannemer
        """ opmerkingen aannemer"""

        self.ptext = '<font size=12><strong>Betreft: Algemene opmerkingen (voor aannemer)</strong></font>'
        Story.append(Paragraph(self.ptext, styles["Border"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Dekking:</u> \
        op de wapeningstekening is de dekking aangegeven. Veelal wordt gewerkt \
        met supporters om de bovenwapening op te vlechten. De richting van deze supporters kan van \
        belang zijn om te vermijden dat bij overlappen van wapeningsnetten en andere extra \
        wapeningsstaven de dekking aan de bovenzijde gegarandeerd blijft. Door de supporters in de \
        richting van de onderste staven van het bovennet te plaatsen, wordt al winst geboekt. \
        Denk er vooral aan om voldoende supporters aan te brengen bij de beëindiging van de netten. \
        Door het lopen op de netten kan anders dit net naar beneden worden getrapt. Bij grote \
        vloervelden dient de dekking aan de bovenzijde te worden gecontroleerd met behulp van een \
        waterpassing.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Schone bekisting:</u> \
        zeker bij schoonwerk beton dient een schoonmaakbeurt te \
        worden ingelast. Zaagsel, binddraad (voor zover niet RVS), papier, peuken, enz. dienen te \
        worden verwijderd, meestal met water, soms met lucht. Als we hiervoor water gebruiken, denk \
        dan aan een controleerbare waterafvoer.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))


        self.ptext = '<u>Sparingen:</u> \
        zorg ervoor dat een bekisting voor de sparing goed is verankerd, \
        zodat deze niet kan opdrijven of vollopen. Bij trapsparingen is het van belang dat de bekisting \
        ca. 5mm doorloopt in de wand. Hierdoor ontstaat een verdiepte strook in de trapopgang die \
        eenvoudig kan worden gerepareerd. Houden we dit gelijk, dan is het risico aanwezig dat we een \
        lichte verdikking krijgen die vervolgens moet worden opengehakt. Als we een grote sparing moeten \
        maken omdat er bijvoorbeeld een bouwkraan midden in een vloer wordt opgesteld, zorg dan voor \
        een afgetekende afbakening aan de onderzijde van de vloer, dus door op de bekisting een lat aan \
        te brengen ter plaatse van de stortnaad. Na het aanstorten van deze grote sparing is deze \
        sponning eenvoudig te repareren> '
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Stekken:</u> \
        we zien wel eens dat de uitstekende wapening van heipalen is afgedekt \
        met een felgekleurde emmer. Waarom wordt dit niet toegepast bij de hoger gelegen vloervelden? \
        Het is een prima beveiliging. Overigens, zorg voor een schoring van stekken, zeker als deze als \
        stek voor prefab beton is bedoeld. Ook kan worden gedacht aan een hulpstaaf om een rij van \
        stekken uit te lijnen. Vermijd dat stekken na het storten worden aangebracht, de aansluiting \
        van de beton rondom de stekken is niet meer gegarandeerd.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Randbekisting:</u> \
        zeker daar waar ankers worden ingestort voor het later aanbrengen \
        van een geveldragerconstructie, is het belangrijk dat de zijkant van de kist, bij een vloer, niet \
        kan wijken. Soms past men een omgezette verzinkte plaat toe als eindbekisting, deze zijn absoluut \
        niet stijf genoeg. Ook voor het doorlopen van de spouwisolatie dient de randkist voldoende stijf \
        te worden uitgevoerd.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Prefab:</u> \
        let erop dat bij het instorten van prefab voorzieningen, zoals balkons \
        e.d. dat de wapening, zoals een Isokorf, op de juiste hoogte zit in het vloerveld. Als men een \
        vloerveld sterk getoogd heeft met de gedachte dat deze na verharding recht komt te hangen, dan \
        kan de wapening van het prefab wel eens te laag uitkomen in de bekisting van de vloer. Bij een \
        tunnelbekisting wordt extra attentie gevraagd voor het probleem van het nazakken. Balkons kunnen \
        zelfs gaan scheuren aan de onderzijde door deze doorbuiging.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Scheuren van jong beton:</u> \
        We onderscheiden sedimentatie scheuren, die ontstaan \
        na het storten. De zwaardere delen van het mengsel zakken onder invloed van de zwaartekracht na. \
        Als er nu een obstakel aanwezig is, zoals een staaf van de bovenwapening, zal de sedimentatie \
        links en rechts ongehinderd kunnen plaatsvinden, en er boven dit obstakel een scheur ontstaan. \
        Bij vloeren herkent men deze scheurvorming op de plaats van beugels. Bij kolommen is dit \
        herkenbaar doordat de bovenkant enigszins scheurt ter hoogte van de beugels. Daarnaast \
        onderscheiden we plastische krimpscheuren. Een gevolg van het nazakken is, dat er een dun laagje \
        water op het betonoppervlak verschijnt. De verdamping hiervan kan zich doorzetten in de poriën \
        van de top van de beton. De poriën vernauwen zich wat scheurvorming met zich mee kan brengen. \
        Het verloop hiervan kan grillig zijn. Afdekken of nathouden is dus belangrijk.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Legplannen:</u> \
        Legplannen voor afdekken in predallen, welfsels of potten en balken dienen steeds aan het \
        ingenieursbureau voorgelegd te worden ter goedkeuring.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Aansluiting metalen profielen met beton:</u> \
        Bij de aansluiting van predallen of potten en balken met een metalen profiel is een lichte \
        afscheuring van het beton steeds mogelijk aangezien het om twee verschillende materialen gaat. \
        Deze lichte afschuiving kan zich voortzetten in het pleisterwerk waardoor hierin scheurtjes \
        kunnen ontstaan. Om dit tegen te gaan dient de aannemer pleisterwerken een betongaas aan te \
        brengen bij de aansluiting van het profiel met het beton zodat het pleisterwerk hier plaatselijk \
        gewapend wordt.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Brandweerstand:</u> \
        Alle constructie-elementen dienen brandwerend behandeld of uitgevoerd te worden zodat \
        aan de in norm gevraagde brandweerstand voldaan wordt.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Afbraakwerken – stabiliteit:</u> \
        We adviseren om een gespecialiseerde schoringsfirma te raadplegen alvorens de afbraakwerken \
        te starten. Tijdens de afbraakwerken dient de stabiliteit van de (naastliggende) woning(en) \
        gewaarborgd te blijven. Indien dit niet verzekerd kan worden, dient de aannemer afbraakwerken \
        de nodige maatregelen te treffen alvorens verder af te breken.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        self.ptext = '<u>Kelderwerken:</u> \
        Bij werken in de diepte (zoals kelderwerken) dient de aannemer maatregelen te nemen om te \
        voorkomen dat tijdens de werken de kelder gaat opdrijven ten gevolge van de opwaartse \
        grondwaterdruk. De meest aangewezen manier om opdrijving tegen te gaan is het voorzien van \
        pompen die de grondwatertafel verlagen. Bij een verlaging van de grondwatertafel dient de \
        stabiliteit van omliggende woningen wel gewaarborgd te blijven. <br/> \
        Bij enige twijfel dient een gespecialiseerde firma aangesteld te worden. <br/> \
        Gelieve ons steeds te contacteren wanneer blijkt dat er een hoge grondwaterstand is. \
        Verder dient er ook rekening mee gehouden te worden dat de stabiliteit van naastgelegen \
        woningen moet gewaarborgd blijven bij kelderwerken. Bij eventuele twijfels dient eveneens \
        een gespecialiseerde firma aangesteld worden. De uitgravingen voor de kelderwerken dienen \
        te gebeuren volgens het natuurlijk talud van de grond. Indien uitgravingen volgens het \
        natuurlijk talud onmogelijk zijn door externe factoren, dient de bouwput beschermd worden \
        tegen inkalven. Deze beschermen kan gebeuren door het plaatsen van een beschoeiing. Voor de \
        plaatsing en berekeningen van deze beschoeiing dient contact opgenomen te worden met een \
        gespecialiseerde firma.'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))

        #opgelet
        self.ptext = '<strong><u>Opgelet:</u> De aannemer dient ons minstens 24 uur voor het storten van \
        het beton te verwittigen zodat wij de geplaatste wapening kunnen controleren. </strong>'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))
        #vragen
        self.ptext = 'Voor vragen en/of opmerkingen, gelieve ons daarvan tijdig op de hoogte te brengen. <br/> \
        Filip Vanderlinden (054/59.82.82) <br/> \
        Jan Steenhoudt (0498/29.49.42) <br/> \
        Maarten Van Nieuwenhove (0498/97.70.01)'
        Story.append(Paragraph(self.ptext, styles["Text"]))
        Story.append(Spacer(1, 12))



#-----------------------------------------------------------------------------


#class names are always CamelCase
class GetSave(FooterCanvas):
    """
    woning_naam = "naam"
    woning_straat = "woning_straat"
    woning_gemeente = "woning_gemeente"
    architect_naam = "Architect_naam"
    architect_straat = "Architect_straat"
    architect_gemeente = "Architect_gemeente"
    aannemer_naam = "aannemer_naam"
    aannemer_straat= "aannemer_straat"
    aannemer_gemeente = "aannemer_gemeente"
    ingenieur_naam = "ingenieur_naam"
    datum = time.strftime("%d/%m/%Y")
    dossier = "x"
    """
    def add_styles(self, styles):
            #Topco
        self.Topco = styles.add(ParagraphStyle(name='Topco', alignment=TA_LEFT,
                fontName= 'Helvetica',
                fontSize= 20,
                borderpadding = 20,
                ))
            #border
        self.Border = styles.add(ParagraphStyle(name='Border', alignment=TA_JUSTIFY,
                fontName= 'Times-Bold',
                fontSize= 11,
                leftIndent= 5,
                borderColor= black,
                borderWidth= 0.5,
                borderPadding= 5,
                borderRadius= 0,
                spaceBefore= 10,
                spaceAfter= 10
                ))
            #text
        self.Text = styles.add(ParagraphStyle(name='Text', alignment=TA_JUSTIFY,
                fontName= 'Helvetica',
                fontSize= 10
                ))
            #text centered
        self.Text_center = styles.add(ParagraphStyle(name='Textcenter', alignment=TA_CENTER,
                fontName= 'Helvetica',
                fontSize= 14,
                leading = 18
                ))
            #textborder
        self.Text_border = styles.add(ParagraphStyle(name='Textborder', alignment=TA_JUSTIFY,
                fontName= 'Helvetica',
                fontSize= 10,
                leftIndent= 5,
                borderColor= black,
                borderWidth= 0.5,
                borderPadding= 5,
                borderRadius= 0,
                spaceBefore= 10,
                spaceAfter= 10
                ))
            #bullet
        self.Bullet = styles.add(ParagraphStyle(name='Textbullet', alignment=TA_JUSTIFY,
                fontName= 'Helvetica',
                fontSize= 10,
                leftIndent = 25,
                leading = 12,
                bulletIndent = 10,
                bulletFontName = 'Symbol',
                bulletFontSize = 20
                ))


    def __init__(self, newer_dict, pdfpath, **kwargs):
        #self.newer_dict = newer_dict
        self.pdfpath = pdfpath
        self.woning_naam = newer_dict['bouwheer']
        self.werf_straat = newer_dict['werfadres']
        self.werf_gemeente = newer_dict['werfgemeente']
        self.woning_straat = newer_dict['woning straat']
        self.woning_gemeente = newer_dict['woning gemeente']
        self.architect_naam = newer_dict['architect']
        self.architect_straat = newer_dict['architect straat']
        self.architect_gemeente = newer_dict['architect gemeente']
        self.aannemer_naam = newer_dict['aannemer']
        self.aannemer_straat= newer_dict['aannemer straat']
        self.aannemer_gemeente = newer_dict['aannemer gemeente']
        self.ingenieur_naam = newer_dict['ingenieur']
        self.datum = time.strftime("%d/%m/%Y")
        self.dossier_nummer = newer_dict['dossier_nummer']

        #adding styles
        styles=getSampleStyleSheet()
        self.add_styles(styles)

        # Content
        Story = []

            # voorblad
        self.add_header(Story, styles)
        self.voorblad(Story, styles)
        Story.append(PageBreak()) #comment out for empty page bug??

            #inhoudstafel
        self.add_header(Story, styles)
        self.inhouds_tafel(Story, styles)
        Story.append(PageBreak())

            #bundel
        self.add_header(Story, styles)
        self.beschrijving(Story, styles)


        # Build pdf
        #pdfpath = self.folder_scan[self.newer_dict['dossier']]['path'] + "//Stabiliteit//Algemene documenten//stabiliteitsbundel.pdf"
        doc = SimpleDocTemplate(self.pdfpath, pagesize=A4,
                            rightMargin= 2*cm,
                            leftMargin= 2*cm,
                            topMargin= 2*cm,
                            bottomMargin=100
                            )
        doc.multiBuild(Story, canvasmaker = FooterCanvas)
