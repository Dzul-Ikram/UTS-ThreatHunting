"""
Threat Hunting & Cyber Threat Intelligence (THCTI) Academic Report Generator
Author: Dzul Ikram A.S. Sambaiyang (24.83.1130)
Dataset: WitFoo Precinct 6 Enterprise SOC Telemetry (Campaign Partition 233678)
Institution: Universitas Amikom Yogyakarta
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable
)
from reportlab.pdfgen import canvas

pdf_path = r"d:\threat hunting\Laporan_Threat_Hunting_Ujian.pdf"
logo_path = r"d:\threat hunting\logo_amikom.png"

class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(AcademicNumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super(AcademicNumberedCanvas, self).showPage()
        super(AcademicNumberedCanvas, self).save()

    def draw_decorations(self, page_count):
        # Do not draw header/footer on cover page (Page 1)
        if self._pageNumber == 1:
            return
            
        self.saveState()
        self.setFont("Times-Roman", 9)
        self.setFillColor(colors.HexColor("#334155"))
        
        # Header (Pages >= 2)
        self.drawString(54, 745, "UTS THREAT HUNTING - PROGRAM STUDI S1 TEKNIK KOMPUTER AMIKOM")
        self.drawRightString(558, 745, "24.83.1130")
        self.setStrokeColor(colors.HexColor("#64748b"))
        self.setLineWidth(0.5)
        self.line(54, 738, 558, 738)
        
        # Footer
        footer_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(558, 40, footer_text)
        self.drawString(54, 40, "Dzul Ikram A.S. Sambaiyang | https://github.com/Dzul-Ikram/UTS-ThreatHunting")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 50, 558, 50)
        self.restoreState()

def generate_academic_pdf():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles (Times-Roman based)
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=18,
        leading=24,
        alignment=1, # Center
        textColor=colors.black
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1,
        textColor=colors.black,
        spaceAfter=20
    )

    cover_student_style = ParagraphStyle(
        'CoverStudent',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=18,
        alignment=1,
        textColor=colors.black
    )

    cover_inst_style = ParagraphStyle(
        'CoverInst',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=18,
        alignment=1,
        textColor=colors.black
    )

    # Content Styles
    sec_title_style = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.black,
        spaceBefore=0,
        spaceAfter=6
    )

    subsec_title_style = ParagraphStyle(
        'SubSecTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=5,
        spaceAfter=3
    )

    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=4, # Justified
        spaceAfter=5
    )

    code_block_style = ParagraphStyle(
        'AcademicCodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )

    th_style = ParagraphStyle(
        'AcademicTH',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8,
        leading=10,
        alignment=1, # Center
        textColor=colors.HexColor("#0f172a")
    )

    td_style = ParagraphStyle(
        'AcademicTD',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1e293b")
    )

    td_code = ParagraphStyle(
        'AcademicTDCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # =========================================================================
    # HALAMAN 1: COVER SESUAI FORMAT GAMBAR
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("UTS", cover_title_style))
    story.append(Paragraph("THREAT HUNTING", cover_subtitle_style))
    story.append(Spacer(1, 35))

    # Logo Amikom
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=170, height=170)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
    else:
        story.append(Spacer(1, 170))

    story.append(Spacer(1, 65))
    story.append(Paragraph("Dzul Ikram A.S. Sambaiyang &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 24.83.1130", cover_student_style))
    story.append(Spacer(1, 90))

    story.append(Paragraph("PROGRAM STUDI S1 TEKNIK KOMPUTER", cover_inst_style))
    story.append(Paragraph("FAKULTAS ILMU KOMPUTER", cover_inst_style))
    story.append(Paragraph("UNIVERSITAS AMIKOM YOGYAKARTA", cover_inst_style))
    story.append(Paragraph("YOGYAKARTA", cover_inst_style))
    story.append(Paragraph("2026", cover_inst_style))

    # Selesai Halaman 1
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 2: SOAL 1 (ANALISIS LANDSCAPE & ATTACK LIFECYCLE)
    # =========================================================================
    story.append(Paragraph("<b>1. Analisis Landscape pada Kasus yang Diberikan</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=8))
    
    soal1_intro = (
        "Berdasarkan analisis empiris telemetri SOC enterprise <b>WitFoo Precinct 6</b> pada tenant <b>ORG-0003</b>, "
        "teridentifikasi kampanye serangan terkoordinasi <b>Data Theft (Partisi 233678)</b> yang menargetkan workstation internal "
        "dan gateway cabang. Profiling ancaman dikarakterisasi sebagai berikut:"
    )
    story.append(Paragraph(soal1_intro, body_style))
    story.append(Spacer(1, 4))

    # Tabel Profil Landscape (Lebar total: 504 pt)
    landscape_table_data = [
        [Paragraph("Komponen Landscape", th_style), Paragraph("Karakteristik & Analisis Evidence", th_style)],
        [
            Paragraph("<b>Threat Actor</b>", td_style),
            Paragraph("Financially Motivated Cybercrime Group / Initial Access Broker (IAB). Karakteristik sindikat kejahatan siber yang menargetkan kompromi perimeter web dan workstation enterprise untuk pencurian data dan monetisasi akses (SEO spam/judi online redirect).", td_style)
        ],
        [
            Paragraph("<b>Motivasi</b>", td_style),
            Paragraph("Pencurian data internal korporat (Data Theft), penjualan akses ke dark web, dan pemanfaatan server korporat sebagai relay C2 dan SEO injection.", td_style)
        ],
        [
            Paragraph("<b>Kemampuan (Capability)</b>", td_style),
            Paragraph("Tingkat Menengah ke Atas (Capable/Advanced). Menguasai saluran C2 dinamis terenkripsi HTTPS (port 443), teknik bypass firewall port non-standar (13731, 8880, 4112, 4010), dan pemindaian lateral terkoordinasi antar cabang.", td_style)
        ],
        [
            Paragraph("<b>Target Aset</b>", td_style),
            Paragraph("Aset korporat ORG-0003: Workstation internal 192.168.96.104 di kantor pusat (NORHQ_WAP_RECEPTION) dan switch/gateway cabang Atlanta, Conyers, Loxley, Northbrook.", td_style)
        ],
        [
            Paragraph("<b>Attack Lifecycle</b>", td_style),
            Paragraph("1. Initial Access (T1190) &rarr; 2. Execution (T1059 / Web Shell) &rarr; 3. Discovery (T1046) &rarr; 4. Lateral Movement (T1021) &rarr; 5. Exfiltration (T1041 / T1567).", td_style)
        ]
    ]
    t_landscape = Table(landscape_table_data, colWidths=[115, 389], repeatRows=1)
    t_landscape.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_landscape)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Diferensiasi Fakta, Asumsi, dan Hipotesis Investigasi:</b>", subsec_title_style))
    fha_table_data = [
        [Paragraph("Kategori", th_style), Paragraph("Pernyataan Analisis", th_style), Paragraph("Dasar Bukti / Keterbatasan", th_style)],
        [
            Paragraph("<b>FAKTA</b>", td_style),
            Paragraph("Host 192.168.96.104 menginisiasi sesi TCP keluar ke 100.64.43.120:443 pada 2023-06-02 21:19:28 UTC. Sesi koneksi diblokir (action: deny) oleh sensor NORHQ_WAP_RECEPTION. FireEye HX memicu 'FireEye HX Domain Match' dan Stealthwatch memicu 'High Concern Index Alarm'. Terjadi pemindaian port 13731 di cabang Loxley (29 leads, 15 node).", td_style),
            Paragraph("Tercatat eksplisit pada 4 triggering leads insiden 25512200 dan log syslog NORHQ_WAP_RECEPTION.", td_style)
        ],
        [
            Paragraph("<b>ASUMSI</b>", td_style),
            Paragraph("IP 100.64.43.120 adalah representasi tersanitasi dari server C2 penyerang (HMAC RFC 6598). Muatan sesi port 443 mengandung data korporat yang telah dikumpulkan oleh malware/web shell.", td_style),
            Paragraph("Dideduksi dari klasifikasi Modus Operandi 'Data Theft' dan standar sanitasi dataset.", td_style)
        ],
        [
            Paragraph("<b>HIPOTESIS</b>", td_style),
            Paragraph("H1: Host resepsionis terinfeksi malware yang mengeksekusi C2 beaconing periodik via HTTPS.<br/>H2: Aktivitas port 13731 di cabang Loxley merupakan pemindaian internal lateral reconnaissance sebelum exfiltrasi.", td_style),
            Paragraph("Proposisi investigatif yang diuji menggunakan korelasi telemetri EDR, NDR, dan firewall.", td_style)
        ]
    ]
    t_fha = Table(fha_table_data, colWidths=[70, 274, 160], repeatRows=1)
    t_fha.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fha)

    # Selesai Halaman 2
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 3: SOAL 2 (PERUMUSAN THREAT HUNTING HYPOTHESIS)
    # =========================================================================
    story.append(Paragraph("<b>2. Perumusan Threat Hunting Hypothesis</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=8))
    
    soal2_intro = (
        "Investigasi menerapkan metodologi *Hypothesis-Based Threat Hunting* terukur untuk memverifikasi ada tidaknya "
        "kompromi aktif pada lingkungan jaringan enterprise. Dirumuskan dua hipotesis utama:"
    )
    story.append(Paragraph(soal2_intro, body_style))
    story.append(Spacer(1, 4))

    h1_text = (
        "<b>Hipotesis 1 (H1: Outbound C2 Beaconing & Exfiltration)</b><br/>"
        "<i>'Terdapat host internal di segmen resepsionis/WAP kantor pusat (NORHQ) yang mengalami kompromi dan secara aktif melakukan komunikasi outbound tidak wajar ke domain C2 berbahaya via protokol HTTPS (port 443) untuk melakukan eksfiltrasi data rahasia.'</i><br/>"
        "• <b>Tujuan Investigasi:</b> Mendeteksi kanal komunikasi C2 aktif, mengidentifikasi proses inisiator pada sistem operasi host, memvalidasi domain IOC, dan memastikan integritas data korporat.<br/>"
        "• <b>Ruang Lingkup (Scope):</b> Host 192.168.96.104 (MAC: 00:A5:54:CB:19:84) | Time Window: 2023-06-02 20:00:00 s/d 23:59:59 UTC.<br/>"
        "• <b>Data yang Dibutuhkan:</b> Network Flow Logs (Meraki WAP, Cisco ASA), EDR Process & Domain Match Logs (FireEye HX), Cisco Stealthwatch HCI alarms.<br/>"
        "• <b>Langkah Penyelidikan:</b> 1) Filter flow log keluar ke 100.64.43.120:443; 2) Ekstrak nama domain yang memicu FireEye HX Domain Match; 3) Periksa process tree di host; 4) Evaluasi volume transfer byte pada Stealthwatch.<br/>"
        "• <b>Kriteria Validasi:</b> SUPPORTED bila terbukti korelasi domain match EDR + alarm lonjakan HCI + deny log firewall. REJECTED bila koneksi terbukti update software resmi vendor. INCONCLUSIVE bila log EDR tidak tersedia.<br/>"
        "• <b>Tindakan Lanjutan (Action Plan):</b> Jika Terbukti: Isolasi host dari jaringan, sinkhole domain C2 pada DNS internal, cabut kredensial aktif, lakukan memory dump triage. Jika Terbantahkan: Lakukan tuning signature EDR.<br/>"
        "• <b>Status Validasi:</b> <font color='#15803d'><b>SUPPORTED (Tervalidasi oleh Evidence).</b></font>"
    )
    story.append(Paragraph(h1_text, body_style))
    story.append(Spacer(1, 8))

    h2_text = (
        "<b>Hipotesis 2 (H2: Multi-Branch Lateral Reconnaissance)</b><br/>"
        "<i>'Penyerang memanfaatkan host perantara di jaringan cabang (Loxley/Atlanta/Conyers) untuk melakukan pemindaian horizontal dan probing lateral movement pada port non-standar (13731, 8880, 4112, 4010) secara terkoordinasi.'</i><br/>"
        "• <b>Tujuan Investigasi:</b> Memetakan penyebaran infeksi lateral antar kantor cabang dan mendeteksi aktivitas pemindaian port (service discovery) sebelum eksfiltrasi dilakukan.<br/>"
        "• <b>Ruang Lingkup (Scope):</b> Host cabang 100.64.41.160 (Loxley), 100.64.27.241 (Atlanta) | Time Window: 2023-06-02 18:00:00 s/d 2023-06-03 02:00:00 UTC.<br/>"
        "• <b>Data yang Dibutuhkan:</b> Cisco Stealthwatch Flow Logs, Meraki L7 & Firewall deny alarms, Windows Event 5156.<br/>"
        "• <b>Langkah Penyelidikan:</b> 1) Ekstraksi event network flow pada port anomali (13731, 8880, 4112, 4010); 2) Hitung jumlah distinct destination IP per host asal; 3) Evaluasi alarm penimbunan data (data hoarding) Stealthwatch.<br/>"
        "• <b>Kriteria Validasi:</b> SUPPORTED bila terbukti 1 host memindai >10 target dalam waktu singkat tanpa tujuan bisnis sah. REJECTED bila port terbukti software backup terdistribusi resmi. INCONCLUSIVE bila log flow lokal tidak lengkap.<br/>"
        "• <b>Tindakan Lanjutan (Action Plan):</b> Jika Terbukti: Terapkan microsegmentation antar cabang, blokir port 13731/8880 pada router ACL. Jika Terbantahkan: Daftarkan port aplikasi ke dalam CMDB.<br/>"
        "• <b>Status Validasi:</b> <font color='#15803d'><b>SUPPORTED (Tervalidasi oleh Evidence).</b></font>"
    )
    story.append(Paragraph(h2_text, body_style))

    # Selesai Halaman 3
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 4: SOAL 3 (TELEMETRY CORRELATION & EVIDENCE TIMELINE)
    # =========================================================================
    story.append(Paragraph("<b>3. Telemetry Correlation & Evidence Timeline</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=8))
    
    soal3_intro = (
        "Identifikasi dan korelasi telemetri dilakukan menggunakan minimal dua sumber data independen yang saling memvalidasi: "
        "<b>FireEye Endpoint Security (HX Series)</b> sebagai sumber EDR dan <b>Cisco Stealthwatch</b> sebagai sumber NDR, "
        "didukung sensor perimeter <b>Cisco Meraki WAP (NORHQ_WAP_RECEPTION)</b>. Berikut visualisasi sebaran tingkat kecurigaan, sensor forensik, dan kronologi kejadian hasil korelasi:"
    )
    story.append(Paragraph(soal3_intro, body_style))
    story.append(Spacer(1, 3))

    # Diagram Visualisasi Sebaran Skor Kecurigaan & Sensor Multi-Sumber (Permintaan Soal)
    chart_path = os.path.join(os.path.dirname(__file__), "campaign_charts.png")
    if os.path.exists(chart_path):
        chart_img = Image(chart_path, width=490, height=155)
        chart_img.hAlign = 'CENTER'
        story.append(chart_img)
        story.append(Spacer(1, 4))

    # Tabel Timeline (Lebar total: 504 pt)
    timeline_table_data = [
        [
            Paragraph("Timestamp (UTC / Epoch)", th_style),
            Paragraph("Source & Destination Entity", th_style),
            Paragraph("Aktivitas & Protokol", th_style),
            Paragraph("Sumber Event (Sensor)", th_style),
            Paragraph("Relevansi Forensik & Dampak", th_style)
        ],
        [
            Paragraph("2023-06-02 20:10:07<br/>1685736607.581", td_style),
            Paragraph("100.64.42.192:42840 &rarr;<br/>100.64.43.121:4010", td_code),
            Paragraph("TCP Flow Deny<br/>(Lateral Probe)", td_style),
            Paragraph("Cisco Stealthwatch<br/>(Northbrook MX67C)", td_style),
            Paragraph("Pengintaian awal port anomali 4010 di kantor cabang Northbrook.", td_style)
        ],
        [
            Paragraph("2023-06-02 20:10:07<br/>1685736607.650", td_style),
            Paragraph("100.64.41.160:54117 &rarr;<br/>100.64.39.193:13731", td_code),
            Paragraph("TCP Flow Deny<br/>(Mass Sweep - 29 leads)", td_style),
            Paragraph("Cisco Stealthwatch<br/>(Loxley MX67C)", td_style),
            Paragraph("Pemindaian horizontal masif terhadap 15 node pada port anomali 13731.", td_style)
        ],
        [
            Paragraph("<b>2023-06-02 21:19:28</b><br/>1685740768.000", td_style),
            Paragraph("<b>192.168.96.104:64813</b> &rarr;<br/><b>100.64.43.120:443</b>", td_code),
            Paragraph("<b>HTTPS Outbound Attempt</b><br/>(sport=64813 dport=443)", td_style),
            Paragraph("<b>FireEye Endpoint (HX)</b> &amp;<br/><b>Stealthwatch NDR</b>", td_style),
            Paragraph("<b>PUNCAK SERANGAN:</b> EDR Domain Match + High Concern Index Alarm (Skor 0.86). Host resepsionis terkompromi mengeksekusi C2.", td_style)
        ],
        [
            Paragraph("<b>2023-06-02 21:19:28</b><br/>1685740768.000", td_style),
            Paragraph("192.168.96.104 &rarr;<br/>100.64.43.120", td_code),
            Paragraph("Firewall Action: DENY/BLOCK", td_style),
            Paragraph("Cisco Meraki WAP<br/>(NORHQ_WAP_RECEPTION)", td_style),
            Paragraph("Disrupsi perimeter otomatis: Firewall memutus transmisi data keluar (status: Disrupted).", td_style)
        ],
        [
            Paragraph("2023-06-02 22:01:42<br/>1685743302.874", td_style),
            Paragraph("100.64.27.241:54107 &rarr;<br/>100.64.40.28:8880", td_code),
            Paragraph("TCP Flow Deny<br/>(Probing Port 8880)", td_style),
            Paragraph("Cisco Stealthwatch<br/>(Atlanta MX67C)", td_style),
            Paragraph("Pengujian service discovery di gateway Atlanta pasca kegagalan di kantor pusat.", td_style)
        ],
        [
            Paragraph("2023-06-02 22:01:42<br/>1685743302.892", td_style),
            Paragraph("100.64.26.213:55555 &rarr;<br/>100.64.41.191:4112", td_code),
            Paragraph("TCP Flow Deny<br/>(Probing Port 4112)", td_style),
            Paragraph("Cisco Stealthwatch<br/>(Conyers MX67C)", td_style),
            Paragraph("Upaya persistensi backdoor fallback di cabang Conyers melalui port 4112.", td_style)
        ]
    ]
    t_timeline = Table(timeline_table_data, colWidths=[85, 110, 95, 95, 119], repeatRows=1)
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_timeline)
    story.append(Spacer(1, 5))

    soal3_analysis = (
        "<b>Sintesis Korelasi Forensik Multi-Sumber:</b><br/>"
        "Korelasi silang temporal membuktikan bahwa pada pukul 21:19:28 UTC terjadi puncak intrusi terkoordinasi. "
        "Alert EDR <i>FireEye HX Domain Match</i> mengonfirmasi bahwa workstation resepsionis internal 192.168.96.104 "
        "telah mengeksekusi proses yang mencoba berkomunikasi dengan domain C2 berbahaya. Secara simultan, NDR <i>Cisco Stealthwatch</i> "
        "merekam lonjakan Concern Index hingga skor 0.859 akibat anomali akumulasi data. Transmisi keluar berhasil digagalkan "
        "oleh firewall perimeter <i>Cisco Meraki WAP</i> dengan memutus sesi koneksi port 443 (action: deny), sehingga kebocoran data terhenti."
    )
    story.append(Paragraph(soal3_analysis, body_style))

    # Selesai Halaman 4
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 5: SOAL 4 (KLASIFIKASI TEMUAN & PEMETAAN MITRE ATT&CK)
    # =========================================================================
    story.append(Paragraph("<b>4. Klasifikasi Temuan &amp; Pemetaan MITRE ATT&amp;CK</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=8))
    
    ioc_text = (
        "<b>A. Klasifikasi Temuan Investigasi:</b><br/>"
        "• <b>IOC (Indicators of Compromise):</b> IP External C2: <font face='Courier'>100.64.43.120</font>, "
        "Host Internal Terkompromi: <font face='Courier'>192.168.96.104</font> (MAC: <font face='Courier'>00:A5:54:CB:19:84</font>), "
        "C2 Port: <font face='Courier'>443/TCP</font>, Scanning Probed Ports: <font face='Courier'>13731, 8880, 4112, 4010</font>, "
        "Matched Signatures: <font face='Courier'>FireEye HX Domain Match</font>, <font face='Courier'>Stealthwatch High Concern Index Alarm</font>.<br/>"
        "• <b>IOA (Indicators of Attack):</b> Lonjakan anomali <i>High Concern Index (0.859)</i> pada Cisco Stealthwatch; "
        "Pola koneksi outbound burst ke port 443 dari workstation nirkabel resepsionis di luar jam kerja; "
        "Pemindaian masif multi-node berurutan (15 target internal) dari satu workstation cabang.<br/>"
        "• <b>TTP:</b> Penyamaran lalu lintas data theft di dalam protokol HTTPS terenkripsi standar (port 443); "
        "Pemanfaatan port non-standar high range untuk menghindari deteksi firewall; "
        "Pemanfaatan workstation resepsionis pada segmen wireless WAP sebagai titik pivot awal."
    )
    story.append(Paragraph(ioc_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>B. Pemetaan Mendalam MITRE ATT&CK Matrix:</b>", subsec_title_style))
    mitre_table_data = [
        [Paragraph("Taktik MITRE ATT&CK", th_style), Paragraph("Teknik & ID", th_style), Paragraph("Alasan Pemetaan & Dasar Bukti Telemetri", th_style), Paragraph("Confidence", th_style)],
        [
            Paragraph("Initial Access (TA0001)", td_style),
            Paragraph("<b>T1190</b><br/>Exploit Public-Facing App", td_style),
            Paragraph("Eksploitasi aplikasi web perimeter (sesuai modul kompromi web server & relasi WAF Barracuda) untuk penanaman foothold awal.", td_style),
            Paragraph("Medium", td_style)
        ],
        [
            Paragraph("Command & Control (TA0011)", td_style),
            Paragraph("<b>T1071.001</b><br/>Web Protocols (HTTPS/443)", td_style),
            Paragraph("Host internal 192.168.96.104 menghubungi IP eksternal 100.64.43.120 via port 443 yang terbukti cocok dengan blacklist C2 domain pada FireEye HX.", td_style),
            Paragraph("High", td_style)
        ],
        [
            Paragraph("Exfiltration (TA0010)", td_style),
            Paragraph("<b>T1041</b><br/>Exfiltration Over C2", td_style),
            Paragraph("Modus operandi diklasifikasikan sebagai Data Theft dengan alarm anomali penimbunan data keluar pada Cisco Stealthwatch.", td_style),
            Paragraph("High", td_style)
        ],
        [
            Paragraph("Exfiltration (TA0010)", td_style),
            Paragraph("<b>T1567</b><br/>Exfiltration Over Web Service", td_style),
            Paragraph("Upaya transmisi data keluar menggunakan format web request terenkripsi untuk mengelabui filter perimeter firewall.", td_style),
            Paragraph("High", td_style)
        ],
        [
            Paragraph("Discovery (TA0007)", td_style),
            Paragraph("<b>T1046</b><br/>Network Service Discovery", td_style),
            Paragraph("Host di cabang Loxley (100.64.41.160) memindai 15 target internal pada port anomali 13731 (29 detection leads).", td_style),
            Paragraph("High", td_style)
        ],
        [
            Paragraph("Lateral Movement (TA0008)", td_style),
            Paragraph("<b>T1021</b><br/>Remote Services", td_style),
            Paragraph("Percobaan pergerakan lateral internal ke gateway Atlanta (port 8880) dan Conyers (port 4112).", td_style),
            Paragraph("Medium", td_style)
        ]
    ]
    t_mitre = Table(mitre_table_data, colWidths=[110, 120, 214, 60], repeatRows=1)
    t_mitre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (3,1), (3,-1), 'CENTER'),
    ]))
    story.append(t_mitre)
    story.append(Spacer(1, 6))

    attribution_text = (
        "<b>C. Batasan Atribusi (Attribution Limitations):</b><br/>"
        "1. <i>Sanitasi IP (RFC 6598):</i> Alamat IP publik telah disanitasi menggunakan skema HMAC konsisten ke blok CGNAT (100.64.0.0/10), sehingga resolusi geolokasi presisi (AS Number / Negara C2) tidak dapat dipastikan 100%.<br/>"
        "2. <i>Enkripsi TLS 1.3:</i> Lalu lintas port 443 terenkripsi end-to-end tanpa SSL Decryption appliance pada gateway WAP, sehingga muatan file spesifik yang dicoba dieksfiltrasi tidak dapat didekripsi dari paket mentah.<br/>"
        "3. <i>Ketiadaan File Hash:</i> Data network syslog murni tidak menyertakan hash SHA256 proses biner yang berjalan, sehingga atribusi ke unit APT spesifik dibatasi pada tingkat profil taktis (Cybercrime IAB)."
    )
    story.append(Paragraph(attribution_text, body_style))

    # Selesai Halaman 5
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 6: SOAL 5 (THREAT HUNTING QUERIES & DETECTION ENGINEERING)
    # =========================================================================
    story.append(Paragraph("<b>5. Threat Hunting Queries & Detection Engineering</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=8))
    
    soal5_intro = (
        "Disusun dua kueri deteksi analitis yang dapat dieksekusi pada platform SIEM (Splunk SPL) maupun "
        "data engine analitik (SQL / Python Pandas) untuk mendeteksi korelasi temporal dan pola pemindaian lateral:"
    )
    story.append(Paragraph(soal5_intro, body_style))
    story.append(Spacer(1, 4))

    q1_text = (
        "<b>Query 1: Cross-Source Temporal Join (Platform: Splunk SPL)</b><br/>"
        "Mendeteksi korelasi antara alarm kecocokan domain jahat di EDR dan aksi blokir koneksi keluar port 443 di firewall perimeter dalam jendela waktu 5 menit:<br/>"
        "<font face='Courier' size='7.5'>"
        "(index=edr product_name=\"FireEye Endpoint Security*\" matched_rules=\"*Domain Match*\") OR<br/>"
        "(index=network message_type=\"firewall_action\" action IN (\"deny\",\"block\") dst_port=443)<br/>"
        "| eval hunting_ip = coalesce(src_ip, clientip)<br/>"
        "| stats earliest(_time) as first_seen, latest(_time) as last_seen,<br/>"
        "        values(product_name) as sensors, values(matched_rules) as rules,<br/>"
        "        values(dst_ip) as target_c2, count by hunting_ip<br/>"
        "| where mvcount(sensors) >= 2 AND count >= 2 AND (last_seen - first_seen) <= 300"
        "</font><br/>"
        "• <b>Field yang Dicari:</b> <font face='Courier'>src_ip, dst_ip, dst_port=443, product_name, matched_rules, action, _time</font>.<br/>"
        "• <b>Logika Korelasi:</b> Temporal join 5 menit (300 detik) antar 2 sensor independen (EDR + Firewall) berdasarkan kesamaan IP inisiator.<br/>"
        "• <b>Kemungkinan False Positive:</b> Update browser/antivirus resmi yang menghubungi mirror IP baru yang sempat masuk blacklist usang.<br/>"
        "• <b>Detection Tuning:</b> Whitelist subnet IP CDN resmi (Microsoft/AWS) dan tetapkan syarat mutlak minimal 2 sensor berbeda."
    )
    story.append(Paragraph(q1_text, body_style))
    story.append(Spacer(1, 8))

    q2_text = (
        "<b>Query 2: Multi-Branch Lateral Probing & Port Sweeping (Platform: SQL / Python Pandas)</b><br/>"
        "Mendeteksi aktivitas pemindaian horizontal internal pada port anomali non-standar lintas kantor cabang:<br/>"
        "<font face='Courier' size='7.5'>"
        "SELECT src_ip, stream_name, COUNT(DISTINCT dst_ip) AS distinct_targets, COUNT(*) AS probe_count<br/>"
        "FROM network_signals<br/>"
        "WHERE protocol = 'tcp' AND dst_port IN (13731, 8880, 4112, 4010) AND action IN ('deny', 'block', 'drop')<br/>"
        "GROUP BY src_ip, stream_name<br/>"
        "HAVING COUNT(DISTINCT dst_ip) >= 5;"
        "</font><br/>"
        "• <b>Field yang Dicari:</b> <font face='Courier'>dst_port IN (13731, 8880, 4112, 4010), dst_ip (distinct), src_ip, stream_name, action</font>.<br/>"
        "• <b>Logika Korelasi:</b> Agregasi penolakan koneksi pada port anomali dengan ambang batas (threshold) minimal 5 host target berbeda.<br/>"
        "• <b>Kemungkinan False Positive:</b> Pemindai kerentanan internal resmi (Nessus/Qualys) atau daemon backup terdistribusi internal.<br/>"
        "• <b>Detection Tuning:</b> Daftarkan IP scanner ke whitelist CMDB dan tingkatkan severity jika pemindaian terjadi di luar jam kerja."
    )
    story.append(Paragraph(q2_text, body_style))

    # Selesai Halaman 6
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 7: SOAL 6 (LAPORAN THREAT HUNTING SINGKAT)
    # =========================================================================
    story.append(Paragraph("<b>6. Laporan Threat Hunting Singkat & Rekomendasi Tindak Lanjut</b>", sec_title_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#334155"), spaceAfter=5))

    soal6_body = (
        "<b>A. Executive Summary & Metodologi:</b><br/>"
        "• <b>Executive Summary:</b> Investigasi threat hunting pada telemetri tenant <b>ORG-0003</b> mengungkap kampanye terkoordinasi "
        "<b>Data Theft (Partisi 233678)</b> dengan insiden utama <b>Defiant Pike 233678 (Skor 0.859)</b>. Workstation internal "
        "resepsionis nirkabel <b>192.168.96.104</b> terkompromi dan mengeksekusi C2 beaconing keluar ke IP eksternal <b>100.64.43.120:443</b>.<br/>"
        "• <b>Metodologi:</b> Menerapkan <i>Hypothesis-Based Threat Hunting</i> yang dipadukan dengan <i>Diamond Model for Intrusion Analysis</i> "
        "dan <i>MITRE ATT&CK Framework</i>, mengorelasikan telemetri EDR (FireEye HX), NDR (Cisco Stealthwatch), dan Firewall (Cisco Meraki WAP).<br/><br/>"
        "<b>B. Temuan Utama & Evidence Pendukung:</b><br/>"
        "• <b>Temuan Utama:</b> Upaya eksfiltrasi data korporat via HTTPS port 443 yang terjadi bersamaan dengan pemindaian lateral di cabang Loxley, Atlanta, Conyers, dan Northbrook.<br/>"
        "• <b>Evidence Pendukung:</b><br/>"
        "&nbsp;&nbsp;1. Log EDR: <i>FireEye HX Domain Match</i> pada host 192.168.96.104 (2023-06-02 21:19:28 UTC).<br/>"
        "&nbsp;&nbsp;2. Log NDR: <i>Cisco Stealthwatch High Concern Index Alarm</i> (Concern Score: 0.859 / 85.9%).<br/>"
        "&nbsp;&nbsp;3. Log Perimeter: <i>Cisco Meraki WAP (NORHQ_WAP_RECEPTION)</i> memutus transmisi keluar (action: deny).<br/>"
        "&nbsp;&nbsp;4. Log Lateral Probe: <i>Stealthwatch Loxley</i> mendeteksi 29 leads pemindaian ke 15 node pada port 13731.<br/><br/>"
        "<b>C. Tingkat Keyakinan (Confidence Level) & Dampak Potensial:</b><br/>"
        "• <b>Confidence Level:</b> <b>HIGH (Tinggi)</b> untuk keterjadian infeksi host dan aktivitas C2 beaconing (tervalidasi 3 sensor independen); <b>MEDIUM</b> untuk atribusi kelompok pelaku (adanya sanitasi IP RFC 6598 & enkripsi TLS 1.3).<br/>"
        "• <b>Dampak Potensial:</b> Risiko eksfiltrasi data rahasia korporat, kompromi jaringan cabang nirkabel, dan penanaman backdoor sekunder."
    )
    story.append(Paragraph(soal6_body, body_style))
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>D. Rekomendasi Deteksi & Prioritas Tindak Lanjut:</b>", subsec_title_style))
    rec_table_data = [
        [Paragraph("Tingkat Prioritas", th_style), Paragraph("Tindakan Remediasi & Rekomendasi Deteksi", th_style), Paragraph("Penanggung Jawab & Target Waktu", th_style)],
        [
            Paragraph("<b>P1 (Immediate)</b><br/>Kritis", td_style),
            Paragraph("1. Isolasi jaringan secara logis terhadap host 192.168.96.104.<br/>2. Blokir IP 100.64.43.120 pada seluruh perimeter firewall dan sinkhole DNS.<br/>3. Reset seluruh kredensial akun yang pernah logon pada workstation terinfeksi.", td_style),
            Paragraph("Tim SOC & Incident Response<br/>Target: 0 s/d 24 Jam", td_style)
        ],
        [
            Paragraph("<b>P2 (Short-Term)</b><br/>Tinggi", td_style),
            Paragraph("1. Tutup port non-standar (13731, 8880, 4112, 4010) pada ACL router cabang.<br/>2. Terapkan microsegmentation: isolasi subnet nirkabel resepsionis dari segmen server.<br/>3. Ambil forensic disk/memory dump untuk analisis artefak web shell/backdoor.", td_style),
            Paragraph("Tim Network & Security Engineer<br/>Target: 1 s/d 3 Hari", td_style)
        ],
        [
            Paragraph("<b>P3 (Long-Term)</b><br/>Menengah", td_style),
            Paragraph("1. Deploy kueri korelasi otomatis SIEM (EDR match + outbound deny flow).<br/>2. Terapkan TLS Inspection pada perimeter gateway untuk inspeksi muatan port 443.<br/>3. Lakukan audit integritas direktori web server berkala untuk mencegah SEO spam.", td_style),
            Paragraph("Tim Security Architect<br/>Target: 1 s/d 2 Minggu", td_style)
        ]
    ]
    t_rec = Table(rec_table_data, colWidths=[90, 304, 110], repeatRows=1)
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 4))

    demo_text = (
        "<b>E. Lampiran Link Demo (Sesuai Ketentuan Soal):</b><br/>"
        "• <b>Google Colab Notebook:</b> <a href='https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ'>https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ</a><br/>"
        "• <b>Repository GitHub (Dapat Dijalankan Ulang):</b> <a href='https://github.com/Dzul-Ikram/UTS-ThreatHunting'>https://github.com/Dzul-Ikram/UTS-ThreatHunting</a><br/>"
        "• <b>Jupyter Notebook File:</b> <font face='Courier'>Threat_Hunting_Investigation.ipynb</font> (tersedia di dalam repository GitHub).<br/>"
        "<i>Demo di atas secara transparan memperlihatkan proses kueri event, korelasi multi-sumber telemetri EDR/NDR/Firewall, penyusunan evidence timeline kronologis, dan dasar pengambilan keputusan analisis.</i>"
    )
    story.append(Paragraph(demo_text, body_style))

    # Build PDF with AcademicNumberedCanvas
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Laporan PDF Akademik berhasil dibuat di: {pdf_path}")

if __name__ == "__main__":
    generate_academic_pdf()
