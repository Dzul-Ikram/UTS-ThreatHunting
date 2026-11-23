# Threat Hunting & Cyber Threat Intelligence (THCTI) Investigation Report
**Studi Kasus:** WitFoo Precinct 6 Enterprise SOC Telemetry (Coordinated Campaign 233678)  
**Institusi:** Program Studi S1 Teknik Komputer, Fakultas Ilmu Komputer, Universitas Amikom Yogyakarta  
**Peneliti:** Dzul Ikram A.S. Sambaiyang

**Repository GitHub:** [https://github.com/Dzul-Ikram/UTS-ThreatHunting](https://github.com/Dzul-Ikram/UTS-ThreatHunting)  
**Google Colab Notebook:** [https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ](https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ)  
**Dataset Source:** [witfoo/precinct6-cybersecurity](https://huggingface.co/datasets/witfoo/precinct6-cybersecurity)

---

## 📌 Ringkasan Eksekutif (Executive Summary)
Investigasi threat hunting berbasis hipotesis (*Hypothesis-Based Threat Hunting*) dilakukan terhadap 2.250.185 catatan telemetri riil dari 158 tools SOC enterprise. Melalui korelasi multi-sensor, diidentifikasi kampanye **Data Theft terkoordinasi (Partition 233678)** pada organisasi **ORG-0003** yang terjadi pada **2 Juni 2023**.

Insiden utama berpusat pada **`25512200-01d5-11ee-8c41-374f8f3a6a1c` (Defiant Pike 233678)** dengan skor kecurigaan tertinggi **0.859 (85.9%)**. Host internal terkelola `192.168.96.104` di segmen nirkabel resepsionis (`NORHQ_WAP_RECEPTION`) berupaya melakukan eksfiltrasi data ke server C2 eksternal `100.64.43.120:443`. Korelasi silang antara **FireEye Endpoint Security (HX)** (`FireEye HX Domain Match`) dan **Cisco Stealthwatch NDR** (`Stealthwatch High Concern Index Alarm`) membuktikan adanya aktivitas C2 dan anomali transmisi volume tinggi, yang disertai aktivitas pemindaian lateral di kantor cabang Atlanta, Conyers, Loxley, dan Northbrook.

---

## 📂 Struktur Berkas Investigasi
- **[`Laporan_Threat_Hunting_Ujian.pdf`](Laporan_Threat_Hunting_Ujian.pdf):** Laporan resmi format PDF berstandar akademik (7 halaman, cover resmi Amikom).
- **[`Threat_Hunting_Investigation.ipynb`](Threat_Hunting_Investigation.ipynb):** Jupyter Notebook yang dapat dijalankan ulang (*reproducible code*) untuk ekstraksi data, korelasi, visualisasi, dan pengujian kueri.
- **[`campaign_telemetry.json`](campaign_telemetry.json):** Dataset telemetri kampanye Partisi 233678 (Tenant ORG-0003).
- **[`generate_report_pdf.py`](generate_report_pdf.py):** Skrip generator laporan PDF menggunakan ReportLab.

---

## 🎯 Jawaban Lengkap Soal Ujian (Soal 1 s/d 6)

### 1. Analisis Landscape & Attack Lifecycle
- **Threat Actor:** *Financially Motivated Cybercrime Group / Initial Access Broker (IAB)*. Sindikat kejahatan siber terorganisir yang berfokus pada pencurian data korporat dan kompromi infrastruktur web.
- **Motivasi:** Keuntungan finansial melalui pencurian data sensitif (*Data Theft*) serta pemanfaatan bandwidth dan server korban untuk monetisasi (SEO spam redirect).
- **Kemampuan (Capability):** *Advanced/Capable*. Menguasai teknik komunikasi C2 terenkripsi (HTTPS port 443), penghindaran filter perimeter menggunakan port non-standar (13731, 8880), serta pemindaian horizontal terkoordinasi antar cabang.
- **Target:** Aset internal korporat ORG-0003, workstation resepsionis `192.168.96.104`, dan gateway jaringan cabang.
- **Attack Lifecycle:** Initial Access (T1190) &rarr; Execution (T1059/Web Shell) &rarr; Discovery (T1046) &rarr; Lateral Movement (T1021) &rarr; Exfiltration (T1041/T1567).

#### Tabel Diferensiasi Fakta, Asumsi, dan Hipotesis:
| Kategori | Pernyataan Analisis | Dasar Bukti / Keterbatasan |
| :--- | :--- | :--- |
| **FAKTA** | Host `192.168.96.104` menginisiasi sesi keluar ke `100.64.43.120:443` pada 2023-06-02 21:19:28 UTC. Event diblokir oleh Meraki WAP. FireEye HX memicu *Domain Match* dan Stealthwatch memicu *High Concern Index Alarm*. | Tertera pada 4 triggering leads insiden `25512200` dan log syslog `NORHQ_WAP_RECEPTION`. |
| **ASUMSI** | IP `100.64.43.120` merupakan alamat server C2 penyerang (tersanitasi ke blok RFC 6598). Muatan sesi port 443 berisi data korporat rahasia. | Dideduksi dari klasifikasi Modus Operandi *Data Theft* dan spesifikasi sanitasi HMAC. |
| **HIPOTESIS** | **H1:** Host resepsionis terinfeksi malware yang mengeksekusi C2 beaconing keluar.<br/>**H2:** Aktivitas port 13731 di cabang Loxley (29 leads, 15 node) adalah pemindaian lateral internal. | Proposisi investigatif yang diuji melalui korelasi telemetri EDR, NDR, dan firewall. |

---

### 2. Perumusan Threat Hunting Hypothesis

#### Hipotesis 1 (H1: Outbound C2 Beaconing & Web-Based Data Theft)
- **Pernyataan:** *"Terdapat host internal di segmen resepsionis/WAP kantor pusat (NORHQ) yang mengalami kompromi dan secara aktif melakukan komunikasi outbound tidak wajar ke domain C2 berbahaya via protokol HTTPS (port 443) untuk melakukan eksfiltrasi data rahasia."*
- **Tujuan:** Mendeteksi kanal C2, mengidentifikasi proses inisiator, dan memastikan tidak ada data rahasia yang bocor.
- **Ruang Lingkup:** Host `192.168.96.104` (MAC: `00:A5:54:CB:19:84`), Time Window: `2023-06-02 20:00 - 23:59 UTC`.
- **Data Dibutuhkan:** Network flow logs (Meraki/ASA), EDR Domain & Process logs (FireEye HX), Stealthwatch HCI alarms.
- **Langkah Penyelidikan:**
  1. Filter network flow keluar ke IP `100.64.43.120:443`.
  2. Korelasikan dengan alert domain match pada FireEye HX.
  3. Periksa riwayat transfer byte dan concern index pada Cisco Stealthwatch.
- **Kriteria Validasi:**
  - *Supported:* Terbukti korelasi domain match EDR + alarm lonjakan HCI + deny log firewall. (**Status: SUPPORTED**)
  - *Rejected:* Terbukti merupakan sesi pembaruan software resmi vendor.
  - *Inconclusive:* Log proses EDR lokal hilang dan ketiadaan inspeksi muatan TLS.
- **Tindakan Lanjutan:**
  - *Jika Terbukti:* Isolasi host `192.168.96.104`, sinkhole domain C2, cabut kredensial aktif, lakukan memory triage.
  - *Jika Terbantahkan:* Dokumentasikan false positive dan lakukan tuning pada signature EDR.

#### Hipotesis 2 (H2: Coordinated Multi-Branch Lateral Reconnaissance)
- **Pernyataan:** *"Penyerang memanfaatkan host perantara di jaringan cabang (Loxley/Atlanta/Conyers) untuk melakukan pemindaian horizontal dan probing lateral movement pada port non-standar (13731, 8880, 4112, 4010) secara terkoordinasi."*
- **Tujuan:** Memetakan infeksi lateral dan mendeteksi port sweeping antar subnet kantor cabang.
- **Ruang Lingkup:** Host cabang `100.64.41.160` (Loxley), `100.64.27.241` (Atlanta), Window: `2023-06-02 18:00 - 2023-06-03 02:00 UTC`.
- **Data Dibutuhkan:** Cisco Stealthwatch Flow Logs, Meraki L7 & Firewall deny alarms.
- **Langkah Penyelidikan:**
  1. Kueri event network flow pada port-port anomali (`dport IN [13731, 8880, 4112, 4010]`).
  2. Hitung jumlah *distinct destination IP* yang dihubungi per host asal.
  3. Evaluasi alarm anomali perilaku (*Anomalous Behavior / Suspect Data Hoarding*).
- **Kriteria Validasi:**
  - *Supported:* Terbukti 1 host memindai >10 target dalam rentang waktu singkat tanpa kepentingan bisnis sah. (**Status: SUPPORTED**)
  - *Rejected:* Terbukti merupakan port resmi software backup terdistribusi internal.
  - *Inconclusive:* Ketiadaan visibilitas flow antar switch lokal.
- **Tindakan Lanjutan:**
  - *Jika Terbukti:* Terapkan microsegmentation antar cabang, blokir port anomali pada ACL router cabang.
  - *Jika Terbantahkan:* Daftarkan port aplikasi ke dalam CMDB sistem TI.

---

### 3. Telemetry Correlation & Evidence Timeline
Investigasi menggabungkan **EDR (FireEye Endpoint Security HX)** dan **NDR (Cisco Stealthwatch)**, didukung oleh **Perimeter Log (Cisco Meraki WAP)**:

| Timestamp (UTC / Epoch) | Source & Destination | Aktivitas & Protokol | Sensor / Sumber Event | Relevansi Forensik & Dampak |
| :--- | :--- | :--- | :--- | :--- |
| **2023-06-02 20:10:07**<br/>`1685736607.581` | `100.64.42.192` &rarr;<br/>`100.64.43.121:4010` | TCP Flow Deny<br/>Lateral Probe | Cisco Stealthwatch<br/>*(Northbrook MX67C)* | Pengintaian port anomali 4010 di kantor cabang Northbrook. |
| **2023-06-02 20:10:07**<br/>`1685736607.650` | `100.64.41.160` &rarr;<br/>`100.64.39.193:13731` | TCP Flow Deny<br/>Mass Sweep (29 Leads) | Cisco Stealthwatch<br/>*(Loxley MX67C)* | Pemindaian horizontal masif terhadap 15 node pada port 13731. |
| **2023-06-02 21:19:28**<br/>`1685740768.000` | **`192.168.96.104`** &rarr;<br/>**`100.64.43.120:443`** | **HTTPS Outbound Exfiltration Attempt** | **FireEye Endpoint (HX)** &amp;<br/>**Stealthwatch NDR** | **PUNCAK SERANGAN:** EDR Domain Match + High Concern Index Alarm (Score 0.86). |
| **2023-06-02 21:19:28**<br/>`1685740768.000` | `192.168.96.104` &rarr;<br/>`100.64.43.120` | Firewall Action: DENY/BLOCK | Cisco Meraki WAP<br/>*(NORHQ_WAP_RECEPTION)* | Firewall memotong transmisi data keluar (Status: Disrupted). |
| **2023-06-02 22:01:42**<br/>`1685743302.874` | `100.64.27.241` &rarr;<br/>`100.64.40.28:8880` | TCP Flow Deny<br/>Probing Port 8880 | Cisco Stealthwatch<br/>*(Atlanta MX67C)* | Pengujian service discovery di gateway Atlanta pasca kegagalan di NORHQ. |
| **2023-06-02 22:01:42**<br/>`1685743302.892` | `100.64.26.213` &rarr;<br/>`100.64.41.191:4112` | TCP Flow Deny<br/>Probing Port 4112 | Cisco Stealthwatch<br/>*(Conyers MX67C)* | Upaya persistensi backdoor di cabang Conyers. |

---

### 4. Klasifikasi IOC/IOA/TTP & Pemetaan MITRE ATT&CK

- **IOC (Indicators of Compromise):**
  - External C2 IP: `100.64.43.120`
  - Internal Infected Host: `192.168.96.104` (MAC: `00:A5:54:CB:19:84`)
  - Destination C2 Port: `443/TCP`
  - Scanning Probed Ports: `13731, 8880, 4112, 4010`
  - Matched Signatures: `FireEye HX Domain Match`, `Stealthwatch High Concern Index Alarm`
- **IOA (Indicators of Attack):**
  - Lonjakan anomali *High Concern Index (0.86)* pada Cisco Stealthwatch.
  - Sesi koneksi outbound burst ke port 443 dari workstation resepsionis nirkabel.
  - Pemindaian masif multi-node berurutan (15 target) dari 1 host cabang.
- **TTP (Tactics, Techniques, and Procedures):**
  - Menggunakan port HTTPS 443 standar untuk menyamarkan exfiltration data di antara lalu lintas web normal.
  - Memanfaatkan port non-standar untuk menghindari deteksi perimeter saat lateral movement.
  - Memanfaatkan workstation resepsionis pada segmen wireless WAP sebagai titik pivot.

#### Pemetaan MITRE ATT&CK:
| MITRE Tactic | Technique & ID | Alasan Pemetaan & Dasar Evidence | Confidence |
| :--- | :--- | :--- | :---: |
| **Initial Access (TA0001)** | **T1190** - Exploit Public-Facing App | Eksploitasi web aplikasi perimeter untuk penanaman web shell awal. | **Medium** |
| **Command & Control (TA0011)** | **T1071.001** - Web Protocols (HTTPS) | Koneksi port 443 keluar ke C2 server yang cocok dengan domain blacklist EDR. | **High** |
| **Exfiltration (TA0010)** | **T1041** - Exfiltration Over C2 | Modus operandi Data Theft dengan alarm data hoarding Cisco Stealthwatch. | **High** |
| **Exfiltration (TA0010)** | **T1567** - Exfiltration Over Web Service | Upaya transmisi data via web request untuk mengelabui firewall. | **High** |
| **Discovery (TA0007)** | **T1046** - Network Service Discovery | Host cabang Loxley memindai 15 target internal pada port 13731 (29 leads). | **High** |
| **Lateral Movement (TA0008)** | **T1021** - Remote Services | Percobaan pergerakan lateral internal ke gateway Atlanta (8880) dan Conyers (4112). | **Medium** |

#### Batasan Atribusi (Attribution Limitations):
1. **Sanitasi IP (RFC 6598):** IP publik telah disanitasi menggunakan HMAC konsisten ke blok CGNAT `100.64.0.0/10`, sehingga ASN dan geolokasi negara penyerang tidak dapat ditentukan secara presisi.
2. **Enkripsi TLS 1.3:** Ketiadaan SSL Decryption pada gateway WAP membatasi visibilitas isi muatan file spesifik yang dicuri.
3. **Ketiadaan Hash Executable:** Log flow syslog murni tidak memuat hash SHA256 proses biner, sehingga atribusi ke unit APT spesifik dibatasi pada tingkat kelompok taktis (Cybercrime IAB).

---

### 5. Threat Hunting Queries & Detection Engineering

#### Query 1: Cross-Source Temporal Join (Splunk SPL)
```spl
(index=edr product_name="FireEye Endpoint Security*" matched_rules="*Domain Match*") OR 
(index=network message_type="firewall_action" action IN ("deny", "block") dst_port=443)
| eval hunting_ip = coalesce(src_ip, clientip)
| stats earliest(_time) as first_seen, latest(_time) as last_seen, 
        values(product_name) as sensors, values(matched_rules) as rules, 
        values(dst_ip) as target_c2, count by hunting_ip
| where mvcount(sensors) >= 2 AND count >= 2
| eval time_window_seconds = last_seen - first_seen
| where time_window_seconds <= 300
```
- **Field yang Dicari:** `src_ip`, `dst_ip`, `dst_port=443`, `product_name`, `matched_rules`, `action`.
- **Logika Korelasi:** Menggabungkan log EDR dan Firewall dalam batas jendela waktu 5 menit (300 detik) untuk mengonfirmasi host yang memicu alarm IOC domain sekaligus diblokir firewall.
- **Kemungkinan False Positive:** Pembaruan browser/antivirus yang mengakses IP mirror baru yang sempat masuk blacklist usang.
- **Tuning Rule:** Whitelist subnet resmi vendor (Microsoft/AWS) dan tetapkan syarat minimal 2 produk keamanan berbeda.

#### Query 2: Multi-Branch Lateral Probing & Port Sweeping (Python / Pandas / SQL)
```sql
SELECT 
    src_ip, 
    stream_name, 
    COUNT(DISTINCT dst_ip) AS distinct_targets, 
    COUNT(*) AS probe_count,
    MIN(timestamp) AS start_time,
    MAX(timestamp) AS end_time
FROM network_signals
WHERE protocol = 'tcp' 
  AND dst_port IN (13731, 8880, 4112, 4010) 
  AND action IN ('deny', 'block', 'drop')
GROUP BY src_ip, stream_name
HAVING COUNT(DISTINCT dst_ip) >= 5;
```
- **Field yang Dicari:** `dst_port IN (13731, 8880, 4112, 4010)`, `dst_ip` (distinct), `src_ip`, `stream_name`, `action`.
- **Logika Korelasi:** Mengelompokkan aktivitas koneksi terblokir pada port anomali dengan ambang batas (threshold) minimal 5 host target berbeda.
- **Kemungkinan False Positive:** Pemindai kerentanan internal (Nessus/Qualys) atau daemon backup terjadwal.
- **Tuning Rule:** Kecualikan IP scanner terdaftar dalam CMDB SOC, aktifkan dynamic scoring jika terjadi di luar jam kerja.

---

### 6. Laporan Threat Hunting Singkat & Rekomendasi Tindak Lanjut

- **Executive Summary:** Berdasarkan investigasi telemetri tenant **ORG-0003**, diidentifikasi kampanye **Data Theft (Partisi 233678)** yang berpusat pada insiden kunci **Defiant Pike 233678 (Skor 0.859)**. Workstation resepsionis nirkabel `192.168.96.104` terkompromi dan mengeksekusi C2 beaconing keluar ke IP eksternal `100.64.43.120:443`.
- **Metodologi:** Menerapkan kerangka kerja *Hypothesis-Based Threat Hunting* yang dipadukan dengan *Diamond Model for Intrusion Analysis* dan *MITRE ATT&CK Framework*, mengorelasikan data EDR (FireEye HX), NDR (Cisco Stealthwatch), dan Firewall (Cisco Meraki WAP).
- **Temuan Utama:** Upaya transmisi data korporat via HTTPS port 443 yang terjadi bersamaan dengan pemindaian lateral di cabang Loxley, Atlanta, Conyers, dan Northbrook.
- **Evidence Pendukung:**
  1. Log EDR: *FireEye HX Domain Match* pada host `192.168.96.104` (2023-06-02 21:19:28 UTC).
  2. Log NDR: *Cisco Stealthwatch High Concern Index Alarm* (Concern Score: 0.859 / 85.9%).
  3. Log Perimeter: *Cisco Meraki WAP (NORHQ_WAP_RECEPTION)* memutus transmisi keluar (*action: deny*).
  4. Log Lateral Probe: *Cisco Stealthwatch Loxley* mendeteksi 29 leads pemindaian ke 15 node pada port anomali 13731.
- **Tingkat Keyakinan (Confidence Level):** **HIGH (Tinggi)** untuk keterjadian infeksi host dan aktivitas C2 beaconing (tervalidasi 3 sensor independen); **MEDIUM** untuk atribusi kelompok pelaku spesifik (karena sanitasi IP RFC 6598 dan enkripsi TLS 1.3).
- **Dampak Potensial:** Ancaman eksfiltrasi data rahasia korporat (Data Theft), kompromi segmen jaringan cabang enterprise, dan potensi penanaman backdoor sekunder.

#### Matriks Prioritas Tindak Lanjut:
| Prioritas Tindak Lanjut | Tindakan Remediasi & Rekomendasi Deteksi | Penanggung Jawab & Target Waktu |
| :--- | :--- | :--- |
| **Prioritas 1 (Immediate / Kritis)** | 1. Karantina jaringan logis terhadap host `192.168.96.104`.<br/>2. Blokir IP `100.64.43.120` pada seluruh perimeter firewall dan sinkhole DNS.<br/>3. Reset seluruh kredensial akun yang pernah aktif pada workstation terinfeksi. | Tim SOC / Incident Response<br/>**Target: 0 s/d 24 Jam** |
| **Prioritas 2 (Short-Term / Tinggi)** | 1. Tutup port non-standar (13731, 8880, 4112, 4010) pada ACL router cabang.<br/>2. Terapkan microsegmentation subnet nirkabel resepsionis agar terpisah dari server.<br/>3. Ambil forensic disk/memory dump untuk analisis artefak web shell/backdoor. | Tim Network & Security Engineer<br/>**Target: 1 s/d 3 Hari** |
| **Prioritas 3 (Long-Term / Menengah)** | 1. Deploy kueri korelasi otomatis SIEM (EDR match + outbound deny flow).<br/>2. Terapkan TLS Inspection pada perimeter gateway untuk inspeksi muatan port 443.<br/>3. Lakukan audit integritas direktori web server secara berkala. | Tim Security Architect<br/>**Target: 1 s/d 2 Minggu** |

---

## 🔗 Tautan Demo & Bukti Reproduktibilitas 
- **Google Colab Notebook:** [https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ](https://colab.research.google.com/drive/1ys4l468E6lEuRepVZIOlKEUzR-kNK1LJ)
- **Repository GitHub (Dapat Dijalankan Ulang):** [https://github.com/Dzul-Ikram/UTS-ThreatHunting](https://github.com/Dzul-Ikram/UTS-ThreatHunting)
- **Jupyter Notebook Reproduksi:** [`Threat_Hunting_Investigation.ipynb`](Threat_Hunting_Investigation.ipynb)
- **Unduh Laporan PDF:** [`Laporan_Threat_Hunting_Ujian.pdf`](Laporan_Threat_Hunting_Ujian.pdf)
