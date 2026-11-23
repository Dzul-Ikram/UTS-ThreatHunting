import os
import json
import matplotlib.pyplot as plt
import pandas as pd

# Set matplotlib cache directory to local folder to avoid permission errors
os.environ['MPLCONFIGDIR'] = os.path.join(os.path.dirname(__file__), '.matplotlib_cache')

# 1. Load campaign data
with open('campaign_telemetry.json', 'r', encoding='utf-8') as f:
    campaign_incidents = json.load(f)

# Sort incidents so highest suspicion score is at top
campaign_incidents_sorted = sorted(campaign_incidents, key=lambda x: x.get('suspicion_score', 0))

# 2. Extract telemetry leads for sensor distribution
timeline_records = []
for inc in campaign_incidents:
    for l in inc.get('leads', []):
        timeline_records.append({
            "Epoch": l.get('epoch', 0),
            "Source Entity": f"{l.get('src_ip', 'Unknown')}:{l.get('src_port', '')}",
            "Destination Entity": f"{l.get('dst_ip', 'Unknown')}:{l.get('dst_port', '')}",
            "Activity / Protocol": f"{str(l.get('protocol', '')).upper()} ({str(l.get('action', '')).upper()})",
            "Detection Rule / Lead": l.get('description'),
            "Sensor Source": l.get('product')
        })

df_timeline_all = pd.DataFrame(timeline_records)

# 3. Create figure with 2 subplots as requested
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axes = plt.subplots(1, 2, figsize=(10, 3.1), dpi=300)

# Plot 1: Horizontal Bar for Suspicion Score
inc_names = [i.get('name', 'Incident') for i in campaign_incidents_sorted]
inc_scores = [i.get('suspicion_score', 0) for i in campaign_incidents_sorted]

bars = axes[0].barh(inc_names, inc_scores, color='#1e3a8a', height=0.62)
axes[0].set_xlabel('Suspicion Score (0.0 - 1.0)', fontsize=8, fontweight='bold', color='#1e293b')
axes[0].set_title('Tingkat Kecurigaan Insiden dalam Kampanye 233678\n(Tenant ORG-0003)', fontsize=8.5, fontweight='bold', pad=6, color='#0f172a')
axes[0].set_xlim(0, 1.0)
axes[0].tick_params(axis='both', labelsize=7)
axes[0].grid(axis='x', linestyle='--', alpha=0.5)

# Value labels on bars
for bar in bars:
    w = bar.get_width()
    axes[0].text(w + 0.02, bar.get_y() + bar.get_height()/2, f"{w:.3f}", 
                 va='center', ha='left', fontsize=6.8, fontweight='bold', color='#1e3a8a')

# Plot 2: Pie Chart for Sensors
# In campaign telemetry leads: Stealthwatch (NDR) and FireEye HX (EDR), plus perimeter Meraki WAP
# Let's count sensor leads
sensor_counts = df_timeline_all['Sensor Source'].value_counts()
if len(sensor_counts) > 0:
    pie_colors = ['#1e3a8a', '#0284c7', '#0d9488', '#d97706']
    wedges, texts, autotexts = axes[1].pie(
        sensor_counts, 
        labels=sensor_counts.index, 
        autopct='%1.1f%%', 
        colors=pie_colors[:len(sensor_counts)],
        startangle=140,
        textprops={'fontsize': 7, 'color': '#1e293b'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.2}
    )
    for at in autotexts:
        at.set_fontsize(7.2)
        at.set_fontweight('bold')
        at.set_color('white')

axes[1].set_title('Distribusi Sumber Telemetri Forensik\n(Multi-Sensor Telemetry)', fontsize=8.5, fontweight='bold', pad=6, color='#0f172a')

# Mengatur jarak antar subplot agar rapi
plt.subplots_adjust(wspace=0.38)
plt.tight_layout()

chart_out = os.path.join(os.path.dirname(__file__), 'campaign_charts.png')
plt.savefig(chart_out, dpi=300, bbox_inches='tight')
plt.close()
print(f"Chart saved successfully to {chart_out}")
