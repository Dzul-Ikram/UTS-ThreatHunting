import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
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
        self.drawString(54, 40, "Dzul Ikram A.S. Sambaiyang | https://github.com/Dzul-Ikram/UTS-Threat-hunting")
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
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6
    )

    subsec_title_style = ParagraphStyle(
        'SubSecTitle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1e293b"),
        alignment=4, # Justified
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'AcademicBodyBold',
        parent=body_style,
        fontName='Times-Bold'
    )

    code_style = ParagraphStyle(
        'AcademicCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a")
    )

    th_style = ParagraphStyle(
        'AcademicTH',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=8,
        leading=10.5,
        alignment=1, # Center
        textColor=colors.HexColor("#0f172a")
    )

    td_style = ParagraphStyle(
        'AcademicTD',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b")
    )

    td_code = ParagraphStyle(
        'AcademicTDCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
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

    # Pagebreak to start actual content on Page 2
    story.append(PageBreak())

    # =========================================================================
    # HALAMAN 2: LAPORAN ANALISIS THREAT HUNTING
    # =========================================================================
    
    # Header Dokumen
    story.append(Paragraph("<b>LAPORAN HASIL THREAT HUNTING TELEMETRI ENTERPRISE</b>", ParagraphStyle(
        'DocHeader', parent=styles['Normal'], fontName='Times-Bold', fontSize=13, leading=17, alignment=1, spaceAfter=2
    )))
    story.append(Paragraph("Studi Kasus: WitFoo Precinct 6 Enterprise SOC Telemetry (Campaign Partition 233678)", ParagraphStyle(
        'DocSub', parent=styles['Normal'], fontName='Times-Italic', fontSize=10, leading=14, alignment=1, spaceAfter=10, textColor=colors.HexColor("#475569")
    )))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#334155"), spaceAfter=10))

    # Executive Summary
    story.append(Paragraph("<b>Executive Summary</b>", subsec_title_style))
    exec_summary_text = (
        "Investigasi threat hunting berbasis hipotesis (*hypothesis-based threat hunting*) dilakukan terhadap dataset "
        "telemetri enterprise riil <b>WitFoo Precinct 6</b> yang mencakup 2.250.185 sinyal keamanan dari 158 tools SOC. "
        "Hasil investigasi berhasil mengungkap kampanye <b>Data Theft terkoordinasi (Partisi 233678)</b> pada tenant <b>ORG-0003</b>. "
        "Insiden kunci berpusat pada <b>25512200-01d5-11ee-8c41-374f8f3a6a1c (Defiant Pike 233678)</b> dengan skor kecurigaan tertinggi "
        "<b>0.859 (85.9%)</b>. Host internal <b>192.168.96.104</b> (resepsionis nirkabel NORHQ) terdeteksi melakukan koneksi C2 keluar "
        "menuju IP eksternal <b>100.64.43.120:443</b>. Korelasi silang antara <b>FireEye Endpoint Security (HX Series)</b> "
        "(rule: <i>FireEye HX Domain Match</i>) dan <b>Cisco Stealthwatch NDR</b> (rule: <i>Stealthwatch High Concern Index Alarm</i>) "
        "membuktikan adanya aktivitas transmisi data abnormal dan komunikasi domain jahat, yang terjadi serentak dengan pemindaian lateral di cabang Loxley, Atlanta, Conyers, dan Northbrook."
    )
    story.append(Paragraph(exec_summary_text, body_style))
    story.append(Spacer(1, 6))

    # SOAL 1
    story.append(Paragraph("1. Analisis Landscape Studi Kasus & Attack Lifecycle (Bobot: 15 Poin)", sec_title_style))
    story.append(Paragraph(
        "Berdasarkan analisis empiris terhadap telemetri dataset WitFoo Precinct 6, landscape ancaman dikarakterisasi sebagai berikut:",
        body_style
    ))

    # Tabel Profil Landscape (Lebar total: 504 pt)
    landscape_table_data = [
        [Paragraph("Komponen Landscape", th_style), Paragraph("Karakteristik & Analisis Evidence", th_style)],
        [
            Paragraph("<b>Threat Actor</b>", td_style),
            Paragraph("Financially Motivated Cybercrime Group / Initial Access Broker (IAB). Karakteristik sindikat kejahatan siber yang menargetkan kompromi perimeter web dan workstation enterprise untuk pencurian data dan monetisasi infrastruktur korban (SEO spam/judi online redirect).", td_style)
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
            Paragraph("<b>Target</b>", td_style),
            Paragraph("Aset korporat ORG-0003: Workstation internal 192.168.96.104 di kantor pusat (NORHQ_WAP_RECEPTION) dan switch/gateway cabang Atlanta, Conyers, Loxley, Northbrook.", td_style)
        ],
        [
            Paragraph("<b>Attack Lifecycle</b>", td_style),
            Paragraph("1. Initial Access (T1190) &rarr; 2. Execution (T1059 / Web Shell) &rarr; 3. Discovery (T1046) &rarr; 4. Lateral Movement (T1021) &rarr; 5. Exfiltration (T1041 / T1567).", td_style)
        ]
    ]
    t_landscape = Table(landscape_table_data, colWidths=[120, 384], repeatRows=1)
    t_landscape.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_landscape)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Diferensiasi Fakta, Asumsi, dan Hipotesis:</b>", subsec_title_style))
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
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fha)
    story.append(Spacer(1, 10))

    # SOAL 2
    story.append(Paragraph("2. Perumusan Threat Hunting Hypothesis (Bobot: 15 Poin)", sec_title_style))
    
    h1_text = (
        "<b>Hipotesis 1 (H1: Outbound C2 Beaconing & Web-Based Data Theft):</b><br/>"
        "<i>'Terdapat host internal di segmen resepsionis/WAP kantor pusat (NORHQ) yang mengalami kompromi dan secara aktif melakukan komunikasi outbound tidak wajar ke domain C2 berbahaya via protokol HTTPS (port 443) untuk melakukan eksfiltrasi data rahasia.'</i><br/>"
        "• <b>Tujuan Investigasi:</b> Mendeteksi kanal komunikasi C2 aktif, mengidentifikasi proses inisiator pada sistem operasi host, memvalidasi domain IOC, dan memastikan integritas data korporat.<br/>"
        "• <b>Ruang Lingkup:</b> Host 192.168.96.104 (MAC: 00:A5:54:CB:19:84), Time Window: 2023-06-02 20:00:00 s/d 23:59:59 UTC.<br/>"
        "• <b>Data yang Dibutuhkan:</b> Network Flow Logs (Meraki WAP, Cisco ASA), EDR Process & Domain Match Logs (FireEye HX), Cisco Stealthwatch HCI alarms.<br/>"
        "• <b>Langkah Penyelidikan:</b> 1) Filter flow log keluar ke 100.64.43.120:443; 2) Ekstrak nama domain yang memicu FireEye HX Domain Match; 3) Periksa process tree di host; 4) Evaluasi volume transfer byte pada Stealthwatch.<br/>"
        "• <b>Kriteria Validasi:</b> SUPPORTED bila terbukti korelasi domain match EDR + alarm lonjakan HCI + deny log firewall. REJECTED bila koneksi terbukti update software resmi vendor. INCONCLUSIVE bila log EDR tidak tersedia.<br/>"
        "• <b>Tindakan Lanjutan:</b> Jika Terbukti: Isolasi host dari jaringan, sinkhole domain C2 pada DNS internal, cabut kredensial aktif, lakukan memory dump triage. Jika Terbantahkan: Lakukan tuning signature EDR.<br/>"
        "• <b>Status:</b> <b>SUPPORTED (Tervalidasi).</b>"
    )
    story.append(Paragraph(h1_text, body_style))
    story.append(Spacer(1, 4))

    h2_text = (
        "<b>Hipotesis 2 (H2: Coordinated Multi-Branch Lateral Reconnaissance):</b><br/>"
        "<i>'Penyerang memanfaatkan host perantara di jaringan cabang (Loxley/Atlanta/Conyers) untuk melakukan pemindaian horizontal dan probing lateral movement pada port non-standar (13731, 8880, 4112, 4010) secara terkoordinasi.'</i><br/>"
        "• <b>Tujuan Investigasi:</b> Memetakan penyebaran infeksi lateral antar kantor cabang dan mendeteksi aktivitas pemindaian port (service discovery) sebelum eksfiltrasi dilakukan.<br/>"
        "• <b>Ruang Lingkup:</b> Host cabang 100.64.41.160 (Loxley), 100.64.27.241 (Atlanta), Window: 2023-06-02 18:00:00 s/d 2023-06-03 02:00:00 UTC.<br/>"
        "• <b>Data yang Dibutuhkan:</b> Cisco Stealthwatch Flow Logs, Meraki L7 & Firewall deny alarms, Windows Event 5156.<br/>"
        "• <b>Langkah Penyelidikan:</b> 1) Ekstraksi event network flow pada port anomali (13731, 8880, 4112, 4010); 2) Hitung jumlah distinct destination IP per host asal; 3) Evaluasi alarm penimbunan data (data hoarding) Stealthwatch.<br/>"
        "• <b>Kriteria Validasi:</b> SUPPORTED bila terbukti 1 host memindai >10 target dalam waktu singkat tanpa tujuan bisnis sah. REJECTED bila port terbukti software backup terdistribusi resmi. INCONCLUSIVE bila log flow lokal tidak lengkap.<br/>"
        "• <b>Tindakan Lanjutan:</b> Jika Terbukti: Terapkan microsegmentation antar cabang, blokir port 13731/8880 pada router ACL. Jika Terbantahkan: Daftarkan port aplikasi ke dalam CMDB.<br/>"
        "• <b>Status:</b> <b>SUPPORTED (Tervalidasi).</b>"
    )
    story.append(Paragraph(h2_text, body_style))
    story.append(Spacer(1, 8))

    # Page break for neat layout before Soal 3
    story.append(PageBreak())

    # SOAL 3
    story.append(Paragraph("3. Telemetry Correlation & Evidence Timeline (Bobot: 20 Poin)", sec_title_style))
    story.append(Paragraph(
        "Korelasi dilakukan menggunakan minimal dua sumber data independen yang saling memvalidasi: <b>FireEye Endpoint Security (HX Series)</b> sebagai sumber telemetri EDR dan <b>Cisco Stealthwatch</b> sebagai sumber telemetri NDR, didukung log perimeter <b>Cisco Meraki WAP</b>.",
        body_style
    ))

    # Tabel Timeline yang pas dengan lebar 504 pt dan cell padding rapi
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
            Paragraph("Pengintaian port anomali 4010 di kantor cabang Northbrook.", td_style)
        ],
        [
            Paragraph("2023-06-02 20:10:07<br/>1685736607.650", td_style),
            Paragraph("100.64.41.160:54117 &rarr;<br/>100.64.39.193:13731", td_code),
            Paragraph("TCP Flow Deny<br/>(Mass Sweep - 29 leads)", td_style),
            Paragraph("Cisco Stealthwatch<br/>(Loxley MX67C)", td_style),
            Paragraph("Pemindaian horizontal masif terhadap 15 node pada port 13731 yang memicu alarm HCI.", td_style)
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
    # Exact width sum: 85 + 110 + 95 + 95 + 119 = 504 pt
    t_timeline = Table(timeline_table_data, colWidths=[85, 110, 95, 95, 119], repeatRows=1)
    t_timeline.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_timeline)
    story.append(Spacer(1, 10))

    # SOAL 4
    story.append(Paragraph("4. Klasifikasi Temuan (IOC, IOA, TTP) & Pemetaan MITRE ATT&CK (Bobot: 20 Poin)", sec_title_style))
    
    ioc_text = (
        "<b>A. Klasifikasi Temuan Investigasi:</b><br/>"
        "• <b>IOC (Indicators of Compromise):</b> IP External C2: <font face='Courier'>100.64.43.120</font>, "
        "Host Internal Terkompromi: <font face='Courier'>192.168.96.104</font> (MAC: <font face='Courier'>00:A5:54:CB:19:84</font>), "
        "C2 Port: <font face='Courier'>443/TCP</font>, Scanning Probed Ports: <font face='Courier'>13731, 8880, 4112, 4010</font>, "
        "Rule Signatures: <font face='Courier'>FireEye HX Domain Match</font>, <font face='Courier'>Stealthwatch High Concern Index Alarm</font>.<br/>"
        "• <b>IOA (Indicators of Attack):</b> Lonjakan anomali <i>High Concern Index (0.859)</i> pada Cisco Stealthwatch; "
        "Pola koneksi outbound burst ke port 443 dari workstation nirkabel resepsionis di luar jam kerja; "
        "Pemindaian masif multi-node berurutan (15 target internal) dari satu workstation cabang.<br/>"
        "• <b>TTP:</b> Penyamaran lalu lintas data theft di dalam protokol HTTPS terenkripsi standar (port 443); "
        "Pemanfaatan port non-standar high range untuk menghindari deteksi firewall; "
        "Pemanfaatan workstation resepsionis pada segmen wireless WAP sebagai titik pivot awal."
    )
    story.append(Paragraph(ioc_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>B. Pemetaan MITRE ATT&CK Matrix:</b>", subsec_title_style))
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
    # Width sum: 110 + 120 + 214 + 60 = 504 pt
    t_mitre = Table(mitre_table_data, colWidths=[110, 120, 214, 60], repeatRows=1)
    t_mitre.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (3,1), (3,-1), 'CENTER'),
    ]))
    story.append(t_mitre)
    story.append(Spacer(1, 4))

    attribution_text = (
        "<b>C. Batasan Atribusi (Attribution Limitations):</b><br/>"
        "1. <i>Sanitasi IP (RFC 6598):</i> Alamat IP publik telah disanitasi menggunakan skema HMAC konsisten ke blok CGNAT (100.64.0.0/10), sehingga resolusi geolokasi presisi (AS Number / Negara C2) tidak dapat dipastikan 100%.<br/>"
        "2. <i>Enkripsi TLS 1.3:</i> Lalu lintas port 443 terenkripsi end-to-end tanpa SSL Decryption appliance pada gateway WAP, sehingga muatan file spesifik yang dicoba dieksfiltrasi tidak dapat didekripsi dari paket mentah.<br/>"
        "3. <i>Ketiadaan File Hash:</i> Data network syslog murni tidak menyertakan hash SHA256 proses biner yang berjalan, sehingga atribusi ke unit APT spesifik dibatasi pada tingkat profil taktis (Cybercrime IAB)."
    )
    story.append(Paragraph(attribution_text, body_style))
    story.append(Spacer(1, 10))

    # SOAL 5
    story.append(Paragraph("5. Threat Hunting Queries & Detection Engineering (Bobot: 20 Poin)", sec_title_style))
    
    q1_text = (
        "<b>Query 1: Cross-Source Temporal Join (Platform: Splunk SPL)</b><br/>"
        "Kueri ini mendeteksi korelasi antara alarm kecocokan domain jahat di EDR dan aksi blokir koneksi keluar port 443 di firewall perimeter dalam jendela waktu 5 menit:<br/>"
        "<font face='Courier' size='7.5'>"
        "(index=edr product_name=\"FireEye Endpoint Security*\" matched_rules=\"*Domain Match*\") OR "
        "(index=network message_type=\"firewall_action\" action IN (\"deny\",\"block\") dst_port=443)<br/>"
        "| eval hunting_ip = coalesce(src_ip, clientip)<br/>"
        "| stats earliest(_time) as first_seen, latest(_time) as last_seen, "
        "values(product_name) as sensors, values(matched_rules) as rules, "
        "values(dst_ip) as target_c2, count by hunting_ip<br/>"
        "| where mvcount(sensors) >= 2 AND count >= 2 AND (last_seen - first_seen) <= 300"
        "</font><br/>"
        "• <b>Field yang Dicari:</b> src_ip, dst_ip, dst_port=443, product_name, matched_rules, action.<br/>"
        "• <b>Logika Korelasi:</b> Temporal join 5 menit (300 detik) antar 2 sensor independen (EDR + Firewall) berdasarkan IP inisiator.<br/>"
        "• <b>Kemungkinan False Positive:</b> Update browser/antivirus yang menghubungi mirror IP baru yang sempat masuk blacklist usang.<br/>"
        "• <b>Detection Tuning:</b> Whitelist subnet IP CDN resmi (Microsoft/AWS) dan tetapkan syarat minimal 2 sensor berbeda."
    )
    story.append(Paragraph(q1_text, body_style))
    story.append(Spacer(1, 4))

    q2_text = (
        "<b>Query 2: Multi-Branch Lateral Probing & Port Sweeping (Platform: SQL / Python Pandas)</b><br/>"
        "Kueri ini mendeteksi aktivitas pemindaian horizontal internal pada port anomali non-standar lintas kantor cabang:<br/>"
        "<font face='Courier' size='7.5'>"
        "SELECT src_ip, stream_name, COUNT(DISTINCT dst_ip) AS distinct_targets, COUNT(*) AS probe_count<br/>"
        "FROM network_signals<br/>"
        "WHERE protocol = 'tcp' AND dst_port IN (13731, 8880, 4112, 4010) AND action IN ('deny', 'block', 'drop')<br/>"
        "GROUP BY src_ip, stream_name<br/>"
        "HAVING COUNT(DISTINCT dst_ip) >= 5;"
        "</font><br/>"
        "• <b>Field yang Dicari:</b> dst_port IN (13731, 8880, 4112, 4010), dst_ip (distinct), src_ip, stream_name, action.<br/>"
        "• <b>Logika Korelasi:</b> Agregasi penolakan koneksi pada port anomali dengan ambang batas (threshold) minimal 5 host target berbeda.<br/>"
        "• <b>Kemungkinan False Positive:</b> Pemindai kerentanan internal resmi (Nessus/Qualys) atau daemon backup terdistribusi.<br/>"
        "• <b>Detection Tuning:</b> Daftarkan IP scanner ke whitelist CMDB dan tingkatkan severity jika pemindaian terjadi di luar jam kerja."
    )
    story.append(Paragraph(q2_text, body_style))
    story.append(Spacer(1, 10))

    # SOAL 6
    story.append(Paragraph("6. Rekomendasi Deteksi, Prioritas Tindak Lanjut & Bukti Demo (Bobot: 10 Poin)", sec_title_style))

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
    # Width sum: 90 + 304 + 110 = 504 pt
    t_rec = Table(rec_table_data, colWidths=[90, 304, 110], repeatRows=1)
    t_rec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_rec)
    story.append(Spacer(1, 8))

    demo_text = (
        "<b>Tautan Demo & Bukti Reproduktibilitas Analisis:</b><br/>"
        "• <b>Repository GitHub:</b> <a href='https://github.com/Dzul-Ikram/UTS-Threat-hunting'>https://github.com/Dzul-Ikram/UTS-Threat-hunting</a><br/>"
        "• <b>Live Interactive Dashboard (GitHub Pages):</b> <a href='https://dzul-ikram.github.io/UTS-Threat-hunting/'>https://dzul-ikram.github.io/UTS-Threat-hunting/</a><br/>"
        "• <b>Jupyter Notebook Reproduksi:</b> <font face='Courier'>Threat_Hunting_Investigation.ipynb</font> (tersedia di repository untuk verifikasi kueri dan ekstraksi data secara langsung).<br/>"
        "<i>Dashboard interaktif menyajikan visualisasi timeline forensik, distribusi telemetri, matriks MITRE ATT&CK, dan kueri analitik.</i>"
    )
    story.append(Paragraph(demo_text, body_style))

    # Build PDF with AcademicNumberedCanvas
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Laporan PDF Akademik berhasil dibuat di: {pdf_path}")

if __name__ == "__main__":
    generate_academic_pdf()
