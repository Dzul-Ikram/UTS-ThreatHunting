"""
Threat Hunting & Cyber Threat Intelligence (THCTI) Academic Report Generator
Author: Dzul Ikram A.S. Sambaiyang (24.83.1130)
Dataset: WitFoo Precinct 6 Enterprise SOC Telemetry (Campaign Partition 233678)
Institution: Universitas Amikom Yogyakarta
Font: Times New Roman (TrueType) with Courier New for technical tokens/queries
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

# ---------------------------------------------------------------------------
# Register TrueType Times New Roman & Courier New from Windows Fonts
# ---------------------------------------------------------------------------
pdfmetrics.registerFont(TTFont('TNR',    'C:/Windows/Fonts/times.ttf'))
pdfmetrics.registerFont(TTFont('TNR-B',  'C:/Windows/Fonts/timesbd.ttf'))
pdfmetrics.registerFont(TTFont('TNR-I',  'C:/Windows/Fonts/timesi.ttf'))
pdfmetrics.registerFont(TTFont('TNR-BI', 'C:/Windows/Fonts/timesbi.ttf'))
registerFontFamily('TNR', normal='TNR', bold='TNR-B',
                   italic='TNR-I', boldItalic='TNR-BI')

pdfmetrics.registerFont(TTFont('CourierNew',   'C:/Windows/Fonts/cour.ttf'))
pdfmetrics.registerFont(TTFont('CourierNew-B', 'C:/Windows/Fonts/courbd.ttf'))
registerFontFamily('CourierNew', normal='CourierNew', bold='CourierNew-B')

# ---------------------------------------------------------------------------
# Paths & Colors
# ---------------------------------------------------------------------------
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
pdf_path      = os.path.join(BASE_DIR, "Laporan_Threat_Hunting_Ujian.pdf")
logo_path     = os.path.join(BASE_DIR, "logo_amikom.png")
chart_path    = os.path.join(BASE_DIR, "campaign_charts.png")
lifecycle_img = os.path.join(BASE_DIR, "attack_lifecycle_diagram.png")

BLUE       = colors.HexColor("#1a56db")
DARK       = colors.HexColor("#0f172a")
BODY_COLOR = colors.HexColor("#1e293b")
MUTED      = colors.HexColor("#475569")


# ---------------------------------------------------------------------------
# Canvas with Academic Header & Footer (skips Cover Page 1)
# ---------------------------------------------------------------------------
class AcademicCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont('TNR', 10)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_hf(num_pages)
            super().showPage()
        super().save()

    def _draw_hf(self, total):
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setFont('TNR', 8.5)
        self.setFillColor(MUTED)
        self.drawString(
            54, 748,
            "UTS Threat Hunting & Cyber Threat Intelligence \u2013 "
            "S1 Teknik Komputer, Universitas Amikom Yogyakarta"
        )
        self.drawRightString(558, 748, "NIM 24.83.1130")
        self.setStrokeColor(colors.HexColor("#94a3b8"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)

        self.setFont('TNR', 8)
        self.drawString(
            54, 34,
            "Dzul Ikram A.S. Sambaiyang \u2013 Laporan Investigasi Threat Hunting (Partisi 233678)"
        )
        self.drawRightString(558, 34, f"Halaman {self._pageNumber} dari {total}")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.line(54, 44, 558, 44)
        self.restoreState()


# ---------------------------------------------------------------------------
# Report Generator
# ---------------------------------------------------------------------------
def generate_report():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=52,
    )

    S = getSampleStyleSheet()

    def _ps(name, **kw):
        defaults = dict(
            parent=S['Normal'],
            fontName='TNR',
            fontSize=9.8,
            leading=13,
            textColor=BODY_COLOR,
        )
        defaults.update(kw)
        return ParagraphStyle(name, **defaults)

    cover_title = _ps('CT', fontName='TNR-B', fontSize=20, leading=26,
                      alignment=1, textColor=colors.black)
    cover_sub   = _ps('CS', fontName='TNR-B', fontSize=15.5, leading=22,
                      alignment=1, textColor=colors.black, spaceAfter=20)
    cover_name  = _ps('CN', fontSize=12, leading=18, alignment=1,
                      textColor=colors.black)
    cover_inst  = _ps('CI', fontName='TNR-B', fontSize=12, leading=18,
                      alignment=1, textColor=colors.black)

    h1 = _ps('H1', fontName='TNR-B', fontSize=12, leading=15.5,
             textColor=DARK, spaceBefore=0, spaceAfter=3)
    h2 = _ps('H2', fontName='TNR-B', fontSize=10.3, leading=13.5,
             textColor=DARK, spaceBefore=5, spaceAfter=2)
    body = _ps('Body', fontSize=9.7, leading=12.8, alignment=4, spaceAfter=3.5)
    body_sm = _ps('BodySm', fontSize=9.3, leading=12.2, alignment=4, spaceAfter=2.5)
    bullet_sm = _ps('BulletSm', fontSize=9.2, leading=12.0, alignment=4,
                    leftIndent=10, firstLineIndent=-8, spaceAfter=2.2)

    code_box = _ps(
        'CodeBox',
        fontName='CourierNew',
        fontSize=7.7,
        leading=10.2,
        textColor=DARK,
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.6,
        borderPadding=6,
        borderRadius=3,
        spaceBefore=7,
        spaceAfter=9,
    )

    prio_p1 = _ps(
        'PrioP1', fontSize=9.0, leading=11.8, alignment=4,
        backColor=colors.HexColor("#fef2f2"),
        borderColor=colors.HexColor("#dc2626"),
        borderWidth=0.6, borderPadding=5, borderRadius=2,
        spaceBefore=6, spaceAfter=8,
    )
    prio_p2 = _ps(
        'PrioP2', fontSize=9.0, leading=11.8, alignment=4,
        backColor=colors.HexColor("#fffbeb"),
        borderColor=colors.HexColor("#d97706"),
        borderWidth=0.6, borderPadding=5, borderRadius=2,
        spaceBefore=4, spaceAfter=8,
    )
    prio_p3 = _ps(
        'PrioP3', fontSize=9.0, leading=11.8, alignment=4,
        backColor=colors.HexColor("#eff6ff"),
        borderColor=colors.HexColor("#2563eb"),
        borderWidth=0.6, borderPadding=5, borderRadius=2,
        spaceBefore=4, spaceAfter=8,
    )

    th = _ps('TH', fontName='TNR-B', fontSize=8.3, leading=10.5,
             alignment=1, textColor=DARK)
    td = _ps('TD', fontSize=8.2, leading=10.5, textColor=BODY_COLOR)

    def lnk(url, label=None):
        label = label or url
        return f"<a href='{url}' color='#1a56db'><u>{label}</u></a>"

    def mono(t):
        return f"<font face='CourierNew' size='8'>{t}</font>"

    story = []

    # =====================================================================
    # PAGE 1 – COVER RESMI UNIVERSITAS AMIKOM YOGYAKARTA
    # =====================================================================
    story.append(Spacer(1, 32))
    story.append(Paragraph("UJIAN TENGAH SEMESTER", cover_title))
    story.append(Paragraph("THREAT HUNTING &amp; CYBER THREAT INTELLIGENCE", cover_sub))
    story.append(Spacer(1, 24))
    if os.path.exists(logo_path):
        img = Image(logo_path, width=160, height=160)
        img.hAlign = 'CENTER'
        story.append(img)
    else:
        story.append(Spacer(1, 160))
    story.append(Spacer(1, 48))
    story.append(Paragraph(
        "Dzul Ikram A.S. Sambaiyang &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 24.83.1130", cover_name))
    story.append(Spacer(1, 78))
    for t in [
        "PROGRAM STUDI S1 TEKNIK KOMPUTER",
        "FAKULTAS ILMU KOMPUTER",
        "UNIVERSITAS AMIKOM YOGYAKARTA",
        "YOGYAKARTA",
        "2026",
    ]:
        story.append(Paragraph(t, cover_inst))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 2 – SOAL 1: ANALISIS LANDSCAPE & ATTACK LIFECYCLE
    # =====================================================================
    story.append(Paragraph("<b>1. Analisis Landscape &amp; Attack Lifecycle</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=4))
    story.append(Paragraph(
        "Investigasi dilakukan pada dataset telemetri SOC enterprise <b>WitFoo Precinct 6</b> "
        "(2.250.185 catatan telemetri: 2.011.674 <i>live signals</i> dan 238.511 <i>incident "
        "signals</i> dari 51.371 insiden). Analisis berfokus pada kampanye terkoordinasi "
        "<b>Partisi 233678</b> pada tenant <b>ORG-0003</b> yang terdiri atas <b>9 insiden</b> "
        "(total <b>67 triggering leads</b>) bertipe modus operandi <b>Data Theft</b> dengan "
        "status akhir <b>Disrupted</b>.", body_sm))

    story.append(Paragraph("<b>a) Identifikasi Threat Actor &amp; Tingkat Kemampuan</b>", h2))
    story.append(Paragraph(
        "Pelaku diklasifikasikan sebagai <i>Financially Motivated Cybercrime Group / Opportunistic "
        "Multi-Site Intrusion Operator</i> dengan tingkat kemampuan <b>menengah ke atas "
        "(Capable)</b>. Kemampuan ini tercermin dari tiga indikator utama: (1) eksekusi probe "
        "simultan lintas 8 gateway Meraki MX/WAP (jeda &le;0,10 detik antar cabang pada "
        "20:10:07 UTC), (2) pemanfaatan protokol HTTPS standar (" + mono("443/TCP") + ") dari "
        "segmen nirkabel resepsionis untuk menyamarkan komunikasi Command &amp; Control (C2), serta "
        "(3) penggunaan kombinasi port anomali tinggi (" + mono("13731, 8880, 4112, 4010, 12344") + ") "
        "dan layanan administrasi jarak jauh (" + mono("22 SSH, 3389 RDP, 88 Kerberos") + ").", body_sm))

    story.append(Paragraph("<b>b) Motivasi dan Target Aset</b>", h2))
    story.append(Paragraph(
        "Motivasi utama adalah <b>keuntungan finansial</b> melalui pencurian data korporat sensitif "
        "(<i>Data Theft</i>) dan perolehan akses lateral persisten di jaringan enterprise ORG-0003. "
        "Target operasional meliputi: (1) workstation nirkabel terkelola " + mono("192.168.96.104") + " "
        "(MAC " + mono("00:A5:54:CB:19:84") + ") pada segmen " + mono("NORHQ_WAP_RECEPTION") + ", "
        "(2) gateway utama pusat data " + mono("NORDC_MX400_1") + " (11 leads), serta (3) 6 segmen "
        "kantor cabang: Loxley (" + mono("M52") + "), Conyers (" + mono("M38") + "), Atlanta ("
        + mono("M34") + "), ForestPark (" + mono("M24") + "), FtWalton (" + mono("M58") + "), dan "
        "Northbrook (" + mono("M29") + ").", body_sm))

    story.append(Paragraph("<b>c) Tahapan Attack Lifecycle yang Relevan</b>", h2))
    if os.path.exists(lifecycle_img):
        li = Image(lifecycle_img, width=500, height=111)
        li.hAlign = 'CENTER'
        story.append(li)
        story.append(Spacer(1, 2))
    story.append(Paragraph(
        "Alur intrusi berevolusi dari pemindaian awal di cabang Loxley (17:41 UTC), gelombang "
        "pengintaian paralel di Conyers/NORDC/ForestPark (18:42 UTC), hingga eskalasi serentak "
        "pada pukul 20:10:07 UTC ketika host " + mono("192.168.96.104") + " menghubungi IP eksternal "
        + mono("100.64.43.120:443") + " (insiden <b>Defiant Pike 233678</b>, skor 0.859). Setelah "
        "koneksi utama diputus oleh WAP Meraki, aktivitas berlanjut ke Conyers (" + mono("12344")
        + ", skor tertinggi 0.876 pada <b>Old-fashioned Stingray</b>), Atlanta (" + mono("8880") + "), "
        "hingga probing layanan " + mono("SSH/RDP") + " sampai 05:42 UTC keesokan hari.", body_sm))

    story.append(Paragraph("<b>d) Diferensiasi Fakta, Asumsi, dan Hipotesis</b>", h2))
    story.append(Paragraph(
        "\u2022 <b>FAKTA (Terobservasi Langsung):</b> Host " + mono("192.168.96.104") + " (MAC "
        + mono("00:A5:54:CB:19:84") + ") melakukan koneksi keluar ke " + mono("100.64.43.120:443")
        + " pada syslog 2023-06-02 20:10:07.681 UTC (tercatat di Precinct 21:19:28 UTC) dan diblokir "
        "oleh " + mono("NORHQ_WAP_RECEPTION") + " (" + mono("flows deny") + "). FireEye HX memicu "
        "<i>Domain Match</i> dan Stealthwatch memicu <i>High Concern Index Alarm</i> (skor 0.8594). "
        "Seluruh 67 leads kampanye berstatus " + mono("block/Disrupted") + ".", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>ASUMSI (Dideduksi / Perlu Keterbatasan):</b> Klasifikasi <i>Data Theft</i> dan tag "
        "awal " + mono("T1190") + " berasal dari mesin korelasi otomatis Precinct tanpa bukti paket "
        "TLS terdekripsi. IP blok " + mono("100.64.0.0/10") + " adalah hasil sanitasi RFC 6598 yang "
        "diasumsikan merepresentasikan C2 eksternal serta node pivot internal antar cabang.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>HIPOTESIS (Harus Divalidasi):</b> (H1) Workstation " + mono("192.168.96.104") + " "
        "terinfeksi komponen C2 aktif yang berupaya mengekfiltrasi data via HTTPS; (H2) Anomali port "
        "lintas 8 gateway (" + mono("13731, 8880, 4112, 4010, 12344") + ") merupakan kampanye "
        "pengintaian lateral terkoordinasi oleh satu klaster ancaman yang sama.", bullet_sm))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 3 – SOAL 2: PERUMUSAN THREAT HUNTING HYPOTHESIS
    # =====================================================================
    story.append(Paragraph("<b>2. Perumusan Threat Hunting Hypothesis</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=5))
    story.append(Paragraph(
        "Pendekatan <i>Hypothesis-Based Threat Hunting</i> dirumuskan untuk menguji secara terukur "
        "apakah anomali pada Partisi 233678 merupakan intrusi nyata atau sekadar <i>noise</i> "
        "operasional. Dua hipotesis utama ditetapkan dengan cakupan, data, metode uji, dan rencana "
        "tindakan berikut:", body))

    # --- Hipotesis 1 ---
    story.append(Paragraph(
        "<b>Hipotesis 1 (H1): Outbound C2 Beaconing &amp; Upaya Eksfiltrasi Data via HTTPS</b>", h2))
    story.append(Paragraph(
        "<i>\u201cTerdapat host internal pada segmen nirkabel resepsionis kantor pusat (NORHQ) yang "
        "terkompromi dan secara aktif menginisiasi komunikasi outbound tidak sah ke infrastruktur "
        "Command &amp; Control (C2) eksternal menggunakan protokol terenkripsi HTTPS (port 443) "
        "untuk melakukan eksfiltrasi data rahasia korporat.\u201d</i>", body_sm))
    story.append(Paragraph(
        "\u2022 <b>Tujuan Investigasi:</b> Memverifikasi apakah koneksi keluar port 443 merupakan C2 "
        "beaconing aktif, mengidentifikasi pengguna dan proses endpoint inisiator, serta memastikan "
        "apakah muatan data telah sempat keluar sebelum diblokir perimeter.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Ruang Lingkup (Host / User / Time Window):</b> Host terkelola "
        + mono("192.168.96.104") + " (MAC " + mono("00:A5:54:CB:19:84") + ") di "
        + mono("NORHQ_WAP_RECEPTION") + "; <b>User Scope:</b> akun sesi pada jam kejadian "
        "(syslog Meraki tidak memuat field " + mono("username") + ", sehingga korelasi ke log DHCP, "
        "RADIUS, dan Windows Event 4624 wajib dilakukan); <b>Time Window:</b> 2023-06-02 "
        "19:30:00 s/d 22:00:00 UTC.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Data yang Dibutuhkan:</b> Meraki WAP Syslog (" + mono("flows deny") + "), "
        "FireEye Endpoint Security HX alerts (<i>Domain Match</i> &amp; process tree), Cisco "
        "Stealthwatch NDR (<i>High Concern Index Alarm</i>), serta log DHCP/RADIUS.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Langkah Penyelidikan:</b> (1) Tarik seluruh event outbound ke "
        + mono("100.64.43.120:443") + "; (2) Triangulasi antara blokir Meraki WAP, alert "
        "<i>FireEye HX Domain Match</i>, dan skor HCI Stealthwatch; (3) Evaluasi selisih antara "
        "waktu syslog (" + mono("20:10:07 UTC") + ") dan waktu ingest (" + mono("21:19:28 UTC")
        + "); (4) Periksa byte transfer dan sesi autentikasi pengguna terkait.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Kriteria Validasi:</b> <font color='#15803d'><b>SUPPORTED</b></font> bila EDR "
        "Domain Match, NDR High Concern Index, dan Firewall Deny terjadi simultan pada host yang "
        "sama; <b>REJECTED</b> bila domain cocok adalah pembaruan software resmi (false positive); "
        "<b>INCONCLUSIVE</b> bila log EDR lokal dan autentikasi RADIUS hilang.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Tindakan Lanjutan:</b> <i>Jika Terbukti:</i> Isolasi host " + mono("192.168.96.104")
        + ", blokir IOC C2 pada perimeter &amp; sinkhole DNS, cabut kredensial sesi user terkait, "
        "serta akuisisi memory dump/disk forensik. <i>Jika Terbantahkan:</i> Dokumentasikan alasan "
        "teknis dan lakukan <i>tuning</i> rule FireEye/Stealthwatch agar tidak memicu alarm berulang.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Hasil Uji:</b> <font color='#15803d'><b>SUPPORTED</b></font> \u2013 Terkonfirmasi "
        "oleh 3 sumber independen (FireEye HX + Stealthwatch 0.8594 + Meraki WAP Deny).", bullet_sm))
    story.append(Spacer(1, 5))

    # --- Hipotesis 2 ---
    story.append(Paragraph(
        "<b>Hipotesis 2 (H2): Multi-Branch Lateral Reconnaissance &amp; Port Sweeping</b>", h2))
    story.append(Paragraph(
        "<i>\u201cKelompok penyerang memanfaatkan node terkompromi lintas kantor cabang dan data center "
        "untuk menjalankan pemindaian layanan (service discovery) serta percobaan lateral movement "
        "secara terkoordinasi pada port non-standar dan layanan admin jarak jauh.\u201d</i>", body_sm))
    story.append(Paragraph(
        "\u2022 <b>Tujuan Investigasi:</b> Memetakan cakupan penyebaran horizontal antar cabang, "
        "mengidentifikasi pola probing port anomali maupun port remote admin, serta memastikan "
        "efektivitas kontrol isolasi antar segmen jaringan cabang.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Ruang Lingkup (Host / User / Time Window):</b> Node pada 8 sensor/gateway ("
        + mono("M52 Loxley, M38 Conyers, NORDC_MX400_1, M34 Atlanta, M24 ForestPark, M58 FtWalton, "
        "M29 Northbrook") + "), mencakup " + mono("100.64.41.160") + ", " + mono("100.64.41.216")
        + ", dan " + mono("100.64.27.241") + "; <b>User Scope:</b> lalu lintas inter-host unauthenticated "
        "(audit akun service/admin bila sesi port 22/88/3389 berhasil); <b>Time Window:</b> "
        "2023-06-02 17:41:00 s/d 2023-06-03 06:15:00 UTC.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Data yang Dibutuhkan:</b> Cisco Stealthwatch Flow Logs &amp; HCI Alarms, Meraki MX "
        "Layer-3/7 Deny Logs, serta Windows Security Log (Event ID 5156 / 4625 bila tersedia).",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Langkah Penyelidikan:</b> (1) Agregasi seluruh leads berstatus " + mono("block")
        + " per " + mono("stream/gateway") + "; (2) Hitung variasi " + mono("dst_port") + " dan jumlah "
        "<i>distinct target host</i> (" + mono("15 node") + " pada insiden <i>Amiable Ant</i>); "
        "(3) Bandingkan timestamp syslog guna mendeteksi <i>synchronized bursts</i> antar cabang.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Kriteria Validasi:</b> <font color='#15803d'><b>SUPPORTED</b></font> bila "
        "ditemukan ledakan probe terblokir lintas &ge;3 cabang pada port anomali/admin secara "
        "berdekatan tanpa tiket perubahan TI; <b>REJECTED</b> bila port berasal dari vulnerability "
        "scanner/agent backup resmi; <b>INCONCLUSIVE</b> bila NetFlow internal tidak lengkap.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Tindakan Lanjutan:</b> <i>Jika Terbukti:</i> Tutup port anomali (" + mono("13731, "
        "8880, 4112, 4010, 12344") + ") di ACL router cabang, batasi SSH/RDP melalui bastion host, dan "
        "terapkan segmentasi mikro antar cabang. <i>Jika Terbantahkan:</i> Daftarkan port sah ke "
        "CMDB dan kecualikan IP layanan resmi pada kebijakan deteksi SOC.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Hasil Uji:</b> <font color='#15803d'><b>SUPPORTED</b></font> \u2013 Ditemukan 63 "
        "leads Stealthwatch lintas 7 gateway cabang/DC dengan pola burst terkoordinasi.", bullet_sm))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 4 – SOAL 3: TELEMETRY CORRELATION & EVIDENCE TIMELINE
    # =====================================================================
    story.append(Paragraph(
        "<b>3. Telemetry Correlation &amp; Evidence Timeline</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=4))
    story.append(Paragraph(
        "Investigasi mengorelasikan 3 sumber telemetri independen: <b>(1) FireEye Endpoint Security "
        "(HX Series)</b> [EDR \u2013 2 leads / 3,0%, rule <i>Domain Match</i>], <b>(2) Cisco "
        "Stealthwatch</b> [NDR \u2013 65 leads / 97,0%, rule <i>High Concern Index Alarm</i>], dan "
        "<b>(3) Cisco Meraki MX/WAP Syslog</b> [Perimeter Firewall pada 8 gateway termasuk "
        + mono("NORHQ_WAP_RECEPTION") + " dengan " + mono("flows deny") + "]. Grafik di bawah "
        "memperlihatkan sebaran skor kecurigaan 9 insiden serta proporsi sumber sensornya:", body_sm))

    if os.path.exists(chart_path):
        ci = Image(chart_path, width=495, height=163)
        ci.hAlign = 'CENTER'
        story.append(ci)
        story.append(Spacer(1, 2))

    story.append(Paragraph(
        "<b>Evidence Timeline Kronologis</b> (diurutkan berdasarkan <i>Syslog Event Time</i> beserta "
        "waktu ingest <i>Precinct Observed</i>):", h2))

    tl_data = [
        [Paragraph("Timestamp (UTC)<br/>Syslog / Observed", th),
         Paragraph("Host / Entitas &amp; Port", th),
         Paragraph("Aktivitas &amp; Status", th),
         Paragraph("Sumber Event (Sensor)", th),
         Paragraph("Relevansi Forensik thd. Investigasi", th)],
        [Paragraph("2023-06-02 17:41:19<br/><i>(Obs: 17:55:07)</i>", td),
         Paragraph(mono("100.64.34.88:50687") + "<br/>\u2192 " + mono(".43.124:9831"), td),
         Paragraph("TCP Port Probe<br/>(Action: block)", td),
         Paragraph("Stealthwatch NDR<br/>(" + mono("M52_MX67C_Loxley") + ")", td),
         Paragraph("Sinyal pembuka kampanye; memicu alarm HCI awal di cabang Loxley (<i>High Panda</i>).", td)],
        [Paragraph("2023-06-02 18:42:38<br/><i>(Obs: 18:49:13)</i>", td),
         Paragraph(mono("100.64.43.119") + "<br/>\u2192 " + mono(".40.174:443"), td),
         Paragraph("TCP Multi-Site Sweep<br/>(:443, 13486, 43009)", td),
         Paragraph("Stealthwatch NDR<br/>(NORDC, Conyers, ForestPk)", td),
         Paragraph("Gelombang paralel pertama menyentuh gateway pusat data (" + mono("NORDC_MX400_1") + ").", td)],
        [Paragraph("2023-06-02 20:10:07.58<br/><i>(Obs: 21:19:28)</i>", td),
         Paragraph(mono("100.64.42.192:42840") + "<br/>\u2192 " + mono(".43.121:4010"), td),
         Paragraph("TCP Anomalous Port<br/>(Action: block)", td),
         Paragraph("Stealthwatch NDR<br/>(" + mono("Northbrook") + " &amp; " + mono("Loxley :13731") + ")", td),
         Paragraph("Probe Northbrook (:4010) &amp; Loxley (:13731) terjadi tepat 31\u2013100 ms sebelum puncak NORHQ.", td)],
        [Paragraph("<b>2023-06-02 20:10:07.68<br/><i>(Obs: 21:19:28)</i></b>", td),
         Paragraph("<b>" + mono("192.168.96.104:64813") + "<br/>\u2192 " + mono("100.64.43.120:443") + "</b>", td),
         Paragraph("<b>HTTPS Outbound C2<br/>&amp; Flows Deny</b>", td),
         Paragraph("<b>FireEye HX (EDR) +<br/>Stealthwatch + Meraki WAP</b>", td),
         Paragraph("<b>PUNCAK KORELASI (Skor 0.8594):</b> EDR <i>Domain Match</i> + NDR <i>HCI</i> + Blokir WAP di " + mono("NORHQ") + " (<i>Defiant Pike</i>).", td)],
        [Paragraph("2023-06-02 21:22:41<br/><i>(Obs: 21:57:25)</i>", td),
         Paragraph(mono("100.64.41.216:40414") + "<br/>\u2192 " + mono(".43.132:12344"), td),
         Paragraph("TCP Port 12344<br/>(Action: block)", td),
         Paragraph("Stealthwatch NDR<br/>(" + mono("M38_MX67C_Conyers") + ")", td),
         Paragraph("Memicu skor kecurigaan tertinggi kampanye (<b>0.8763</b>, <i>Old-fashioned Stingray</i>).", td)],
        [Paragraph("2023-06-02 22:01:42<br/><i>(Obs: 22:57:54)</i>", td),
         Paragraph(mono("100.64.27.241") + " \u2192 " + mono(":8880") + "<br/>" + mono("100.64.26.213") + " \u2192 " + mono(":4112"), td),
         Paragraph("TCP Lateral Probing<br/>(Selisih 18 ms)", td),
         Paragraph("Stealthwatch NDR<br/>(Atlanta &amp; Conyers)", td),
         Paragraph("Percobaan lanjutan tersinkronisasi pasca kegagalan C2 resepsionis NORHQ.", td)],
        [Paragraph("2023-06-02 23:36\u201300:07<br/><i>(Obs: 00:14\u201301:38)</i>", td),
         Paragraph(mono(".43.110") + "\u2192" + mono(":3389") + "<br/>" + mono(".43.113") + "\u2192" + mono(":22"), td),
         Paragraph("RDP/SSH Admin Probe<br/>(Action: block)", td),
         Paragraph("Stealthwatch NDR<br/>(Atlanta &amp; Loxley)", td),
         Paragraph("Pergeseran taktik menuju layanan remote admin standar (" + mono("22/SSH, 3389/RDP") + ").", td)],
    ]
    t_tl = Table(tl_data, colWidths=[80, 108, 70, 98, 148], repeatRows=1)
    t_tl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_tl)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Analisis Korelasi Lintas Sumber:</b> Korelasi timestamp syslog membuktikan sinkronisasi "
        "ketat: pada 20:10:07 UTC, probe di Northbrook (" + mono(".581s") + ") dan Loxley ("
        + mono(".650s") + ") disusul dalam 31 ms oleh koneksi keluar workstation terkelola "
        + mono("192.168.96.104") + " (MAC " + mono("00:A5:54:CB:19:84") + ") ke "
        + mono("100.64.43.120:443") + " (" + mono(".681s") + "). Pada titik ini FireEye HX mengaitkan "
        "domain tujuan dengan indikator berbahaya, Stealthwatch menaikkan indeks bahaya hingga 0.8594, "
        "dan Meraki WAP memutus aliran data sehingga insiden tercatat <i>Disrupted</i>.", body_sm))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 5 – SOAL 4: KLASIFIKASI TEMUAN & PEMETAAN MITRE ATT&CK
    # =====================================================================
    story.append(Paragraph(
        "<b>4. Klasifikasi Temuan &amp; Pemetaan MITRE ATT&amp;CK</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=4))

    story.append(Paragraph("<b>a) Klasifikasi Temuan (IOC, IOA, dan TTP)</b>", h2))
    story.append(Paragraph(
        "\u2022 <b>IOC (Indicators of Compromise \u2013 Artefak Statis):</b> IP Eksternal C2 "
        + mono("100.64.43.120") + "; Workstation internal terkompromi " + mono("192.168.96.104")
        + " (MAC " + mono("00:A5:54:CB:19:84") + ", sensor " + mono("192.168.92.29") + "); Sumber "
        "skor tertinggi Conyers " + mono("100.64.41.216") + " \u2192 " + mono("100.64.43.132:12344")
        + "; Port C2 " + mono("443/TCP") + "; Port anomali/admin terblokir: "
        + mono("13731, 8880, 4112, 4010, 12344, 13486, 13495, 22, 3389, 88") + "; Signature aktif: "
        "<i>FireEye HX Domain Match</i> &amp; <i>Stealthwatch High Concern Index Alarm</i>.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>IOA (Indicators of Attack \u2013 Anomali Perilaku):</b> Aktivitas serentak dalam "
        "rentang &le;100 ms lintas lokasi terpisah (Northbrook, Loxley, NORHQ pada 20:10:07 UTC serta "
        "Atlanta &amp; Conyers pada 22:01:42 UTC); kemunculan 29 <i>leads</i> melibatkan 15 node pada "
        "insiden <i>Amiable Ant</i>; lonjakan <i>Concern Index</i> ke 0.8594\u20130.8763; serta "
        "koneksi keluar port 443 dari perangkat resepsionis yang memicu alarm eksfiltrasi NDR.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>TTP (Tactics, Techniques, and Procedures):</b> Memanfaatkan protokol HTTPS standar "
        "(443/TCP) untuk mengkamuflase kanal C2/eksfiltrasi (<i>Protocol Masquerading</i>), "
        "memanfaatkan segmen nirkabel tamu/resepsionis sebagai titik pijakan (<i>wireless pivot</i>), "
        "serta mengombinasikan port acak tinggi dengan layanan remote admin standar lintas cabang.",
        bullet_sm))

    story.append(Paragraph("<b>b) Pemetaan Teknik &amp; Sub-Teknik MITRE ATT&amp;CK</b>", h2))
    mitre_data = [
        [Paragraph("Taktik", th), Paragraph("Teknik &amp; Sub-Teknik", th),
         Paragraph("Alasan Pemetaan &amp; Dasar Evidence Telemetri", th),
         Paragraph("Confidence", th)],
        [Paragraph("Initial Access<br/>(TA0001)", td),
         Paragraph("<b>T1190</b><br/>Exploit Public-Facing App", td),
         Paragraph("Ditandai otomatis pada metadata laporan Precinct (" + mono("attack_reports")
                   + ") sebagai hipotesis vektor masuk awal pada perimeter organisasi ORG-0003.", td),
         Paragraph("<b>Medium</b>", td)],
        [Paragraph("Command &amp;<br/>Control (TA0011)", td),
         Paragraph("<b>T1071.001</b><br/>Application Layer: Web Protocols", td),
         Paragraph("Host " + mono("192.168.96.104") + " menghubungi " + mono("100.64.43.120:443")
                   + " (HTTPS) dan cocok dengan aturan C2 blacklist pada <i>FireEye HX Domain Match</i>.", td),
         Paragraph("<b>High</b>", td)],
        [Paragraph("Exfiltration<br/>(TA0010)", td),
         Paragraph("<b>T1041</b><br/>Exfiltration Over C2 Channel", td),
         Paragraph("Modus operandi resmi kampanye adalah <i>Data Theft</i> dengan korelasi alarm "
                   "<i>Stealthwatch High Concern Index</i> (0.8594) tepat saat C2 diputus WAP.", td),
         Paragraph("<b>High</b>", td)],
        [Paragraph("Exfiltration<br/>(TA0010)", td),
         Paragraph("<b>T1567</b><br/>Exfiltration Over Web Service", td),
         Paragraph("Upaya transfer keluar memanfaatkan kanal web HTTPS (443/TCP) dari endpoint dan "
                   "gateway data center (" + mono("NORDC_MX400_1") + ") guna mengelabui filter standar.", td),
         Paragraph("<b>High</b>", td)],
        [Paragraph("Discovery<br/>(TA0007)", td),
         Paragraph("<b>T1046</b><br/>Network Service Discovery", td),
         Paragraph("Pemindaian lintas 8 gateway pada port bervariasi (" + mono("13731, 4010, 8880, "
                   "4112, 12344") + ") dengan 29 leads dan 15 node di insiden <i>Amiable Ant</i>.", td),
         Paragraph("<b>High</b>", td)],
        [Paragraph("Lateral Movement<br/>(TA0008)", td),
         Paragraph("<b>T1021 / T1021.004</b><br/>Remote Services (SSH/RDP)", td),
         Paragraph("Upaya koneksi terblokir ke port layanan administrasi jarak jauh "
                   + mono("22/TCP (SSH)") + " dan " + mono("3389/TCP (RDP)") + " di cabang Atlanta "
                   "&amp; Loxley (23:36\u201300:07 UTC).", td),
         Paragraph("<b>Medium</b>", td)],
    ]
    t_mitre = Table(mitre_data, colWidths=[80, 114, 248, 62], repeatRows=1)
    t_mitre.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (3, 1), (3, -1), 'CENTER'),
    ]))
    story.append(t_mitre)
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>c) Batasan Atribusi (Attribution Limitations)</b>", h2))
    story.append(Paragraph(
        "\u2022 <b>Sanitasi Identitas &amp; Alamat IP:</b> Sesuai dokumentasi dataset ("
        + mono("graph_metadata.json") + "), alamat IP publik/eksternal disanitasi ke ruang "
        + mono("RFC 6598 (100.64.0.0/10)") + " dan RFC 5737, serta IP privat di-remap ke blok RFC 1918. "
        "Hal ini menutup informasi Autonomous System (ASN), WHOIS, nama domain literal, serta "
        "geolokasi server C2 sebenarnya.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Enkripsi TLS &amp; Ketiadaan Payload/Process Telemetry:</b> Syslog Meraki WAP hanya "
        "merekam header L3/L4 (" + mono("src/dst IP, port, MAC") + ") tanpa inspeksi SSL/TLS, hash "
        "biner executable (" + mono("SHA-256") + "), maupun command-line proses EDR secara langsung. "
        "Selain itu, field " + mono("username") + " kosong pada seluruh 67 leads kampanye.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Implikasi Analitik:</b> Atribusi dibatasi pada tingkat profil perilaku dan modus "
        "operandi (<i>Financially Motivated Cybercrime / Data Theft</i>) dan tidak dapat menunjuk "
        "secara sah kelompok APT atau aktor negara tertentu.", bullet_sm))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 6 – SOAL 5: HUNTING QUERIES & DETECTION ENGINEERING
    # =====================================================================
    story.append(Paragraph(
        "<b>5. Threat Hunting Queries &amp; Detection Engineering</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=4))
    story.append(Paragraph(
        "Disusun dua kueri hunting yang dapat dijalankan ulang (<i>reproducible</i>) di SIEM (Splunk "
        "SPL) dan mesin analitik data (SQL / Python Pandas) beserta analisis false positive, ide "
        "detection rule, dan tuning:", body_sm))

    # --- Query 1 ---
    story.append(Paragraph(
        "<b>Query 1: Cross-Source C2 &amp; Exfiltration Correlator (Platform: Splunk SPL)</b>", h2))
    story.append(Paragraph(
        '(index=edr product_name="FireEye Endpoint Security*" matched_rules="*Domain Match*") OR<br/>'
        '(index=network stream="meraki*" action IN ("deny","block") dst_port=443)<br/>'
        '| eval host_key = coalesce(src_ip, clientip)<br/>'
        '| stats earliest(_time) as t_min, latest(_time) as t_max, dc(product_name) as sensor_cnt,<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;values(product_name) as sensors, values(dst_ip) as c2_ips, '
        'count by host_key<br/>'
        '| where sensor_cnt &gt;= 2 AND count &gt;= 2 AND (t_max - t_min) &lt;= 300',
        code_box))
    story.append(Paragraph(
        "\u2022 <b>Event &amp; Field yang Dicari:</b> Field " + mono("src_ip / clientip, dst_ip, "
        "dst_port=443, product_name, matched_rules, action, _time") + " dari dua indeks berbeda "
        "(EDR FireEye HX dan Firewall/WAP Meraki).", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Logika Filter &amp; Korelasi:</b> Melakukan temporal join dalam rentang 300 detik "
        "(5 menit) berbasis IP inisiator (" + mono("host_key") + "). Syarat "
        + mono("dc(product_name) >= 2") + " menjamin konfirmasi silang minimal dua sensor berbeda.",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Kemungkinan False Positive:</b> Pembaruan browser/antivirus atau akses CDN "
        "terenkripsi ke IP mirror yang sempat masuk daftar blokir threat intel usang.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Ide Detection Rule &amp; Tuning:</b> <i>Rule:</i> Buat SIEM Correlation Alert "
        "berseverity <b>Critical</b> dan pemicu otomatis playbook SOAR (isolasi NAC sementara + ambil "
        "log DHCP/RADIUS host) bila rule EDR <i>Domain Match</i> bertemu blokir outbound 443 dalam "
        "&le;5 menit. <i>Tuning:</i> Kecualikan subnet ASN/CDN resmi (Microsoft, AWS, Google) serta "
        "kedaluwarsakan indikator CTI di atas 30 hari.", bullet_sm))
    story.append(Spacer(1, 4))

    # --- Query 2 ---
    story.append(Paragraph(
        "<b>Query 2: Multi-Branch Lateral Probing &amp; Port Sweep Detector (Platform: SQL / Pandas)</b>",
        h2))
    story.append(Paragraph(
        'SELECT src_ip, stream_name, COUNT(DISTINCT dst_ip) AS distinct_targets,<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;COUNT(DISTINCT dst_port) AS distinct_ports, COUNT(*) AS hits<br/>'
        'FROM network_signals<br/>'
        'WHERE protocol = \'tcp\' AND action IN (\'deny\', \'block\', \'drop\')<br/>'
        '&nbsp;&nbsp;AND dst_port IN (13731, 8880, 4112, 4010, 12344, 13486, 22, 3389, 88)<br/>'
        'GROUP BY src_ip, stream_name<br/>'
        'HAVING COUNT(DISTINCT dst_ip) &gt;= 3 OR COUNT(*) &gt;= 5;',
        code_box))
    story.append(Paragraph(
        "\u2022 <b>Event &amp; Field yang Dicari:</b> Field " + mono("src_ip, dst_ip, dst_port, "
        "stream_name, protocol='tcp', action") + " untuk menangkap upaya scanning baik ke port anomali "
        "kampanye (" + mono("13731, 8880, 4112, 4010, 12344") + ") maupun layanan admin ("
        + mono("22, 3389, 88") + ").", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Logika Filter &amp; Korelasi:</b> Mengelompokkan koneksi berstatus " + mono("deny/"
        "block") + " per pasangan sumber dan gateway cabang (" + mono("stream_name") + ") untuk "
        "mendeteksi pola <i>one-to-many</i> (&ge;3 target IP) atau pengulangan agresif (&ge;5 hits).",
        bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Kemungkinan False Positive:</b> Aktivitas vulnerability scanner internal resmi "
        "(Nessus/Qualys), server monitoring infrastruktur, atau agen backup terdistribusi.", bullet_sm))
    story.append(Paragraph(
        "\u2022 <b>Ide Detection Rule &amp; Tuning:</b> <i>Rule:</i> Implementasikan Sigma/SIEM Alert "
        "<b>High Severity</b> jika satu IP non-scanner memicu blokir lintas &ge;2 gateway cabang "
        "berbeda dalam 15 menit (indikasi <i>Campaign Pivot</i>). <i>Tuning:</i> Whitelist IP "
        "authorized scanner di CMDB SOC dan naikkan skor risiko 2&times; jika terjadi di luar jam "
        "operasional (22:00\u201306:00).", bullet_sm))
    story.append(PageBreak())

    # =====================================================================
    # PAGE 7 – SOAL 6: LAPORAN THREAT HUNTING SINGKAT & LINK DEMO
    # =====================================================================
    story.append(Paragraph(
        "<b>6. Laporan Threat Hunting Singkat &amp; Rekomendasi Tindak Lanjut</b>", h1))
    story.append(HRFlowable(width="100%", thickness=0.7,
                            color=colors.HexColor("#334155"), spaceAfter=4))

    story.append(Paragraph("<b>a) Executive Summary</b>", h2))
    story.append(Paragraph(
        "Investigasi threat hunting berbasis hipotesis pada dataset telemetri WitFoo Precinct 6 "
        "(tenant <b>ORG-0003</b>) mengidentifikasi kampanye terkoordinasi <b>Data Theft (Partisi "
        "233678)</b> berupa 9 insiden dan 67 leads berstatus <i>Disrupted</i>. Insiden kunci "
        "<b>Defiant Pike 233678</b> (skor 0.8594) mengungkap upaya komunikasi C2/eksfiltrasi keluar "
        "dari workstation resepsionis nirkabel " + mono("192.168.96.104") + " ke "
        + mono("100.64.43.120:443") + ", bersamaan dengan pemindaian lateral lintas 7 gateway cabang "
        "dan data center " + mono("NORDC_MX400_1") + ".", body_sm))

    story.append(Paragraph("<b>b) Metodologi &amp; Temuan Utama</b>", h2))
    story.append(Paragraph(
        "Menggunakan kerangka <i>Hypothesis-Based Threat Hunting</i> (H1 &amp; H2), "
        "<i>Cross-Source Temporal Correlation</i>, dan pemetaan <i>MITRE ATT&amp;CK</i> terhadap "
        "telemetri EDR (FireEye HX), NDR (Cisco Stealthwatch), dan Firewall (Meraki MX/WAP). "
        "<b>Temuan Utama:</b> (1) Upaya koneksi C2 HTTPS keluar dari " + mono("192.168.96.104")
        + " berhasil dicegah pada 20:10:07.681 UTC; (2) Pemindaian multi-cabang terjadi serentak di "
        "Northbrook, Loxley, Conyers (<i>Old-fashioned Stingray</i> skor 0.8763), Atlanta, ForestPark, "
        "FtWalton, dan NORDC, dilanjutkan probe layanan admin SSH (22) &amp; RDP (3389).", body_sm))

    story.append(Paragraph("<b>c) Evidence Pendukung, Confidence Level &amp; Dampak Potensial</b>", h2))
    story.append(Paragraph(
        "\u2022 <b>Evidence Pendukung:</b> (1) <i>FireEye HX Domain Match</i> pada "
        + mono("192.168.96.104") + " (MAC " + mono("00:A5:54:CB:19:84") + "); (2) <i>Stealthwatch High "
        "Concern Index Alarm</i> (skor 0.8594 s/d 0.8763); (3) Log " + mono("NORHQ_WAP_RECEPTION flows "
        "deny") + " yang memutus koneksi port 443; (4) 63 leads lateral/port sweep pada 7 gateway "
        "(termasuk 29 leads pada 15 node di <i>Amiable Ant</i>).<br/>"
        "\u2022 <b>Tingkat Keyakinan (Confidence Level):</b> <b>HIGH</b> untuk keterjadian infeksi "
        "workstation &amp; aktivitas probing (tervalidasi 3 sensor independen); <b>MEDIUM</b> untuk "
        "atribusi pelaku &amp; isi muatan paket (terbatas sanitasi IP RFC 6598, enkripsi TLS, dan "
        "absennya field user/hash proses).<br/>"
        "\u2022 <b>Dampak Potensial:</b> Kebocoran data rahasia korporat (<i>Data Theft</i>), potensi "
        "perluasan kompromi ke server pusat data (" + mono("NORDC_MX400_1") + ") via SSH/RDP, dan "
        "penyalahgunaan segmen nirkabel tamu/resepsionis untuk persistensi akses.", body_sm))

    story.append(Paragraph("<b>d) Rekomendasi Deteksi &amp; Prioritas Tindak Lanjut</b>", h2))
    story.append(Paragraph(
        "<b>Prioritas 1 (Immediate \u2013 0 s/d 24 Jam | PIC: Tim SOC &amp; IR):</b> Isolasi penuh host "
        + mono("192.168.96.104") + " dari jaringan; terapkan blokir permanen IP " + mono("100.64.43.120")
        + " dan DNS sinkhole; korelasikan log DHCP/RADIUS dengan Event 4624 untuk identifikasi user "
        "sesi serta lakukan reset kredensial akun terkait.", prio_p1))
    story.append(Paragraph(
        "<b>Prioritas 2 (Short-Term \u2013 1 s/d 3 Hari | PIC: Network &amp; Security Eng.):</b> Blokir "
        "port anomali kampanye (" + mono("13731, 8880, 4112, 4010, 12344") + ") pada ACL seluruh router "
        "Meraki cabang; terapkan microsegmentation antara segmen Wi-Fi resepsionis dan jaringan data "
        "center (" + mono("NORDC") + "); batasi akses SSH/RDP lewat VPN MFA/bastion.", prio_p2))
    story.append(Paragraph(
        "<b>Prioritas 3 (Long-Term \u2013 1 s/d 2 Minggu | PIC: Security Architect):</b> Deploy "
        "rule korelasi SIEM otomatis (Query 1 &amp; Query 2); aktifkan kebijakan TLS Inspection terbatas "
        "untuk visibilitas eksfiltrasi HTTPS; serta audit integrasi log autentikasi AD ke SIEM.",
        prio_p3))

    story.append(Paragraph("<b>e) Lampiran Link Demo &amp; Penjelasan Proses Analisis</b>", h2))
    story.append(Paragraph(
        "\u2022 <b>Google Colab Notebook (Interaktif &amp; Dapat Dijalankan Ulang):</b><br/>"
        "&nbsp;&nbsp;" + lnk("https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ")
        + "<br/>"
        "\u2022 <b>Repository GitHub (Source Code, Dataset JSON &amp; Skrip Analisis):</b><br/>"
        "&nbsp;&nbsp;" + lnk("https://github.com/Dzul-Ikram/UTS-ThreatHunting") + "<br/>"
        "\u2022 <b>File Jupyter Notebook Reproduksi:</b><br/>"
        "&nbsp;&nbsp;" + lnk(
            "https://github.com/Dzul-Ikram/UTS-ThreatHunting/blob/main/Threat_Hunting_Investigation.ipynb",
            "https://github.com/Dzul-Ikram/UTS-ThreatHunting/blob/main/Threat_Hunting_Investigation.ipynb"
        ) + "<br/>"
        "<i><b>Pemenuhan Ketentuan Demo:</b> Notebook pada tautan di atas secara terbuka "
        "memperlihatkan: (1) proses pencarian, ekstraksi, dan kueri korelasi lintas sumber EDR "
        "(FireEye HX), NDR (Stealthwatch), dan Firewall (Meraki) atas 67 leads dari "
        + mono("campaign_telemetry.json") + "; (2) penyusunan <b>Evidence Timeline</b> kronologis "
        "beserta diagram visualisasi skor kecurigaan dan sebaran sensor; serta (3) dasar pengambilan "
        "keputusan analitik (triangulasi bukti H1/H2, confidence scoring, hingga prioritas tindak "
        "lanjut P1\u2013P3).</i>", body_sm))

    doc.build(story, canvasmaker=AcademicCanvas)
    print(f"Laporan PDF berhasil dibuat: {pdf_path}")


if __name__ == "__main__":
    generate_report()
