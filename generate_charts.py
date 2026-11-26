import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

# Set matplotlib cache directory to local folder to avoid permission errors
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ['MPLCONFIGDIR'] = os.path.join(BASE_DIR, '.matplotlib_cache')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

# Register Times New Roman from Windows Fonts for consistent academic typography
TNR_REG = 'C:/Windows/Fonts/times.ttf'
TNR_BOLD = 'C:/Windows/Fonts/timesbd.ttf'
if os.path.exists(TNR_REG):
    fm.fontManager.addfont(TNR_REG)
if os.path.exists(TNR_BOLD):
    fm.fontManager.addfont(TNR_BOLD)
plt.rcParams['font.family'] = 'Times New Roman'

# ---------------------------------------------------------------------------
# 1. Load campaign telemetry data
# ---------------------------------------------------------------------------
with open(os.path.join(BASE_DIR, 'campaign_telemetry.json'), 'r', encoding='utf-8') as f:
    campaign_incidents = json.load(f)

campaign_incidents_sorted = sorted(
    campaign_incidents,
    key=lambda x: (x.get('suspicion_score', 0), x.get('name', ''))
)

timeline_records = []
for inc in campaign_incidents:
    for l in inc.get('leads', []):
        timeline_records.append({
            "Epoch": l.get('observed_at', 0),
            "Incident": inc.get('name'),
            "Sensor Source": l.get('product')
        })

df_timeline_all = pd.DataFrame(timeline_records)

# ---------------------------------------------------------------------------
# 2. Generate Dual Chart: Suspicion Score Barh + Multi-Sensor Pie (Soal 3)
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.25), dpi=300,
                         gridspec_kw={'width_ratios': [1.35, 1.0]})

inc_names = [i.get('name', 'Incident') for i in campaign_incidents_sorted]
inc_scores = [i.get('suspicion_score', 0) for i in campaign_incidents_sorted]
bar_colors = [
    '#b45309' if n == 'Defiant Pike 233678' else '#1e3a8a'
    for n in inc_names
]

bars = axes[0].barh(inc_names, inc_scores, color=bar_colors, height=0.62, edgecolor='none')
axes[0].set_xlabel('Suspicion Score (0.00 - 1.00)', fontsize=8.5, fontweight='bold', color='#1e293b')
axes[0].set_title('Tingkat Kecurigaan 9 Insiden Kampanye 233678 (ORG-0003)',
                  fontsize=9, fontweight='bold', pad=8, color='#0f172a')
axes[0].set_xlim(0, 1.05)
axes[0].tick_params(axis='both', labelsize=7.5)
axes[0].grid(axis='x', linestyle='--', alpha=0.45, color='#94a3b8')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)

for bar, name in zip(bars, inc_names):
    w = bar.get_width()
    suffix = " (EDR+NDR)" if name == 'Defiant Pike 233678' else ""
    col = '#b45309' if name == 'Defiant Pike 233678' else '#1e3a8a'
    axes[0].text(w + 0.015, bar.get_y() + bar.get_height()/2, f"{w:.3f}{suffix}",
                 va='center', ha='left', fontsize=7, fontweight='bold', color=col)

# Right subplot: Pie Chart with clean external legend (no overlapping text)
sensor_counts = df_timeline_all['Sensor Source'].value_counts()
total_leads = int(sensor_counts.sum())
short_labels = []
for src, cnt in sensor_counts.items():
    pct = 100.0 * cnt / total_leads
    if 'FireEye' in src:
        short_labels.append(f"FireEye HX EDR ({cnt} leads / {pct:.1f}%)")
    else:
        short_labels.append(f"Cisco Stealthwatch NDR ({cnt} leads / {pct:.1f}%)")

pie_colors = ['#1e3a8a', '#d97706', '#0284c7', '#0d9488']
wedges, _ = axes[1].pie(
    sensor_counts,
    labels=None,
    colors=pie_colors[:len(sensor_counts)],
    startangle=140,
    explode=[0.0, 0.10][:len(sensor_counts)],
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5}
)
axes[1].legend(
    wedges, short_labels,
    title='Sumber Telemetri (Total 67 Leads)',
    title_fontsize=7.5,
    fontsize=7.2,
    loc='upper center',
    bbox_to_anchor=(0.5, -0.02),
    frameon=True,
    facecolor='#f8fafc',
    edgecolor='#cbd5e1'
)
axes[1].set_title('Distribusi Sumber Telemetri Forensik\n(Multi-Sensor Triangulation)',
                  fontsize=9, fontweight='bold', pad=8, color='#0f172a')

plt.subplots_adjust(wspace=0.25, bottom=0.20)
plt.tight_layout()
chart_out = os.path.join(BASE_DIR, 'campaign_charts.png')
plt.savefig(chart_out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Chart saved successfully to {chart_out}")

# ---------------------------------------------------------------------------
# 3. Generate Attack Lifecycle Diagram (Soal 1)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 2.15), dpi=300)
ax.set_xlim(0, 12.2)
ax.set_ylim(0, 2.3)
ax.axis('off')

ax.text(6.1, 2.12,
        'Pemetaan Attack Lifecycle Kampanye Data Theft (Partisi 233678 \u2013 Tenant ORG-0003)',
        ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0f172a')

stages = [
    ("1. Initial Access", "T1190 (TA0001)", "Eksposur layanan publik\n& foothold endpoint WAP\n(Asumsi / Tag Precinct)", "#1e3a8a"),
    ("2. Execution", "TA0002", "Eksekusi proses jaringan\ndi 192.168.96.104 &\nhost cabang ORG-0003", "#1d4ed8"),
    ("3. Discovery", "T1046 (TA0007)", "Port sweep multi-cabang\nLoxley, Northbrook,\nConyers, ForestPark", "#0369a1"),
    ("4. Lateral Move", "T1021 (TA0008)", "Probing SSH (22), RDP\n(3389), Kerberos (88),\n13731, 8880, 4112", "#0f766e"),
    ("5. C2 Channel", "T1071.001 (TA0011)", "Outbound HTTPS :443 ke\n100.64.43.120 + FireEye\nHX Domain Match", "#b45309"),
    ("6. Exfiltration", "T1041 / T1567", "Stealthwatch HCI 0.859\nMeraki WAP Deny\n(Status: Disrupted)", "#991b1b"),
]

box_w = 1.72
box_h = 1.45
gap = 0.28
start_x = 0.22
y0 = 0.25

for idx, (title, mitre, detail, col) in enumerate(stages):
    x = start_x + idx * (box_w + gap)
    # Outer rounded card
    card = FancyBboxPatch(
        (x, y0), box_w, box_h,
        boxstyle="round,pad=0.04,rounding_size=0.08",
        linewidth=1.1, edgecolor=col, facecolor='#f8fafc'
    )
    ax.add_patch(card)
    # Header bar
    hdr = FancyBboxPatch(
        (x, y0 + box_h - 0.36), box_w, 0.36,
        boxstyle="round,pad=0.04,rounding_size=0.06",
        linewidth=0, facecolor=col
    )
    ax.add_patch(hdr)
    ax.text(x + box_w/2, y0 + box_h - 0.18, title,
            ha='center', va='center', fontsize=7.8, fontweight='bold', color='white')
    ax.text(x + box_w/2, y0 + box_h - 0.56, mitre,
            ha='center', va='center', fontsize=7.0, fontweight='bold', color=col)
    ax.text(x + box_w/2, y0 + 0.42, detail,
            ha='center', va='center', fontsize=6.5, color='#334155', linespacing=1.28)

    if idx < len(stages) - 1:
        arr = FancyArrowPatch(
            (x + box_w + 0.05, y0 + box_h/2),
            (x + box_w + gap - 0.05, y0 + box_h/2),
            arrowstyle='-|>', mutation_scale=11, linewidth=1.3, color='#475569'
        )
        ax.add_patch(arr)

lifecycle_out = os.path.join(BASE_DIR, 'attack_lifecycle_diagram.png')
plt.savefig(lifecycle_out, dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Lifecycle diagram saved successfully to {lifecycle_out}")
