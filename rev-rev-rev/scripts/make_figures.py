"""Deterministic teaching figures. No measurements of a real target.

Run from any directory. Data and numerical summaries are exported for inspection.
Figures use English technical labels; their Bengali reading guides are in chapters.
"""
import csv
import json
import math
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".cache" / "matplotlib"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import seaborn as sns

OUT = ROOT / "assets" / "figures"
DATA = ROOT / "data"
OUT.mkdir(parents=True, exist_ok=True)
DATA.mkdir(exist_ok=True)
BG, INK, BLUE, TEAL, GOLD, RED = "#f6f4ef", "#172e3b", "#3465a4", "#137e7e", "#d08b19", "#b64848"
sns.set_theme(style="whitegrid", font="DejaVu Sans", rc={
    "figure.facecolor": BG, "axes.facecolor": BG, "text.color": INK,
    "axes.labelcolor": INK, "axes.titleweight":"bold", "font.size":12,
    "axes.spines.top":False, "axes.spines.right":False})
manifest = []


def save(fig, name, kind="conceptual", source=None):
    fig.text(.02, .018, "RELAYDESK FIELD NOTES  /  " + ("SYNTHETIC TEACHING DATA" if kind == "synthetic" else "CONCEPTUAL MODEL"),
             fontsize=8, color="#52636b")
    fig.savefig(OUT / (name + ".png"), dpi=170, bbox_inches="tight", facecolor=BG)
    fig.savefig(OUT / (name + ".svg"), bbox_inches="tight", facecolor=BG)
    manifest.append({"file":name,"kind":kind,"data":source})
    plt.close(fig)


def canvas(title, subtitle="", size=(12, 7)):
    fig, ax = plt.subplots(figsize=size)
    ax.set(xlim=(0, 12), ylim=(0, 7))
    ax.axis("off")
    fig.suptitle(title, fontsize=23, x=.07, ha="left", y=.98)
    if subtitle:
        ax.text(0, 6.85, subtitle, fontsize=11, color="#52636b")
    return fig, ax


def box(ax, x, y, w, h, label, color=TEAL, fontsize=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.12",
                              facecolor=color, edgecolor="none"))
    ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=fontsize, color="white", linespacing=1.5)


def arrow(ax, start, end, label=None, rad=0, color=INK):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=16,
                                connectionstyle=f"arc3,rad={rad}", linewidth=1.7, color=color))
    if label:
        ax.text((start[0]+end[0])/2, (start[1]+end[1])/2+.13, label,
                fontsize=10, ha="center", bbox={"facecolor":BG,"edgecolor":"none","pad":2})


def write_csv(name, fields, rows):
    with (DATA / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(fields)
        writer.writerows(rows)


fig, ax = canvas("01  /  A screen is only one layer", "Box sizes are illustrative, not percentages.")
layers = [("VISIBLE EXPERIENCE", "screens  /  keyboard  /  loading  /  errors", BLUE),
          ("BEHAVIORAL CONTRACT", "validation  /  permissions  /  state transitions", TEAL),
          ("DURABLE SYSTEM", "transactions  /  versions  /  duplicate handling", "#376878"),
          ("OPERATIONAL LIFE", "retries  /  telemetry  /  recovery  /  deployment", "#5d536b")]
for i, (title, sub, color) in enumerate(layers):
    y = 5.1-i*1.35
    box(ax, .6, y, 10.8, 1.05, title+"\n"+sub, color)
save(fig,"01-system-layers")

fig, ax = canvas("02  /  Trace a claim all the way to a result")
labels = ["E-017\nEvidence", "REQ-02\nRequirement", "ADR-04\nDecision",
          "CODE\nImplementation", "TEST-02\nScenario", "RUN-01\nActual result"]
points = [(0,4.5),(4.2,4.5),(8.4,4.5),(0,1.5),(4.2,1.5),(8.4,1.5)]
for (x,y), label in zip(points, labels):
    box(ax,x,y,3.2,1.25,label,BLUE if y>3 else TEAL)
arrow(ax,(3.3,5.1),(4.1,5.1)); arrow(ax,(7.5,5.1),(8.3,5.1))
arrow(ax,(10,4.4),(1.6,2.85),"decision becomes code",rad=.06)
arrow(ax,(3.3,2.1),(4.1,2.1)); arrow(ax,(7.5,2.1),(8.3,2.1))
ax.text(0,.35,"Context + artifact + limitation belong with every important claim.",fontsize=13)
save(fig,"02-evidence-chain")

priority = [("Tenant boundary",5,.9,1),("Duplicate create",5,.8,2),("Stale update",4,.7,2),
            ("Search freshness",3,.6,2),("Hover timing",1,.4,1)]
write_csv("priority.csv",["question","impact_1_to_5","uncertainty_0_to_1","effort_hours","score"],
          [(*row,row[1]*row[2]/row[3]) for row in priority])
fig, ax = plt.subplots(figsize=(11,5.5))
values=[r[1]*r[2]/r[3] for r in priority]
bars=ax.barh([r[0] for r in priority],values,color=[RED,TEAL,BLUE,BLUE,"#8999a1"])
ax.invert_yaxis(); ax.bar_label(bars,fmt="%.2f",padding=5)
ax.set(xlabel="Toy priority score = impact × uncertainty / effort",xlim=(0,5.2),title="03  /  Which uncertainty deserves attention first?")
fig.tight_layout(rect=(0,.07,1,1)); save(fig,"03-experiment-priority","synthetic","data/priority.csv")

fig, ax = canvas("04  /  Timeout does not reveal the outcome")
for x,y,label,color in [(0,5.4,"Idle",BLUE),(4.1,5.4,"Validating",BLUE),(8.2,5.4,"Validation error",RED),
                        (4.1,3.6,"Submitting",TEAL),(0,1.7,"Success",TEAL),
                        (4.1,1.7,"Conflict",GOLD),(8.2,1.7,"Outcome unknown",GOLD),(8.2,.1,"Reconcile / replay",BLUE)]:
    box(ax,x,y,3.1,1,label,color,12)
arrow(ax,(3.2,5.9),(4,5.9)); arrow(ax,(7.3,5.9),(8.1,5.9),"invalid")
arrow(ax,(5.65,5.3),(5.65,4.7),"valid")
arrow(ax,(4.2,3.5),(1.55,2.85),"confirmed")
arrow(ax,(5.65,3.5),(5.65,2.85),"stale")
arrow(ax,(7.2,3.5),(9.75,2.85),"timeout")
arrow(ax,(9.75,1.6),(9.75,1.2))
ax.text(.1,.5,"Replay confirms the existing operation;\notherwise keep the outcome unresolved.",fontsize=12)
save(fig,"04-ui-state")

fig, ax = canvas("05  /  One record, several representations")
box(ax,0,3,3.4,1.4,"Ticket store\nauthoritative",TEAL)
for y,label in [(5.1,"Client cache"),(3.6,"Search projection"),(2.1,"Dashboard count"),(.6,"Notification via outbox")]:
    box(ax,7.4,y,4.2,1.1,label,BLUE,12)
    arrow(ax,(3.5,3.7),(7.3,y+.55))
ax.text(.1,.15,"Deletion and versioning must account for derived copies too.",fontsize=14)
save(fig,"05-data-map")

fig, axes = plt.subplots(1,2,figsize=(13,6),sharey=True)
for ax, title in zip(axes,["Blind overwrite: a change is lost","Version condition: stale write rejected"]):
    ax.set(xlim=(0,10),ylim=(5,-.7),title=title,xticks=[2,8],xticklabels=["Client A","Client B"],yticks=range(5),yticklabels=["read","read","write","write","final"])
    ax.plot([2,2],[-.3,4.5],color="#aab6bc"); ax.plot([8,8],[-.3,4.5],color="#aab6bc")
for ax in axes:
    ax.text(2,0,"read v1",ha="center",bbox={"facecolor":BG,"edgecolor":"none"})
    ax.text(8,1,"read v1",ha="center",bbox={"facecolor":BG,"edgecolor":"none"})
    ax.text(8,2,"save → v2",ha="center",color=TEAL,bbox={"facecolor":BG,"edgecolor":"none"})
axes[0].text(2,3,"save old copy",ha="center",color=RED,bbox={"facecolor":BG,"edgecolor":"none"})
axes[0].text(5,4,"B's value disappears",ha="center",color=RED)
axes[1].text(2,3,"expected v1 ≠ v2",ha="center",color=RED,bbox={"facecolor":BG,"edgecolor":"none"})
axes[1].text(5,4,"Conflict; refresh and decide",ha="center",color=TEAL)
fig.suptitle("06  /  A stale snapshot is not permission to overwrite",fontsize=20)
fig.tight_layout(rect=(0,.06,1,.92)); save(fig,"06-concurrency")

fig, ax = canvas("07  /  Outbox closes one gap; replay still matters")
box(ax,.1,4.5,3.3,1.4,"Ticket + outbox\nONE DB COMMIT",TEAL)
box(ax,4.6,4.5,2.6,1.4,"Worker\nreads pending",BLUE)
box(ax,8.4,4.5,3.3,1.4,"External provider\nside effect",BLUE)
arrow(ax,(3.5,5.2),(4.5,5.2)); arrow(ax,(7.3,5.2),(8.3,5.2))
box(ax,4.6,1.1,2.6,1.4,"Mark delivered",TEAL)
arrow(ax,(10,4.4),(7.3,1.8),"ACK gap: crash here",color=RED)
ax.text(.1,2.6,"Crash before the mark:\nevent stays pending;\nworker replays it.",fontsize=12,color=RED)
ax.text(.2,.2,"Fake provider in the lab deduplicates by durable event ID.",fontsize=13)
save(fig,"07-outbox")

fig, ax = plt.subplots(figsize=(12,5.7))
spans=[("HTTP create",0,120), ("Authorization",5,8),("Database transaction",18,80),
       ("Response encoding",100,15),("Async worker (linked)",300,70)]
for i,(name,start,duration) in enumerate(spans):
    ax.barh(i,duration,left=start,color=TEAL if i!=4 else GOLD,height=.55)
    ax.text(start+duration+5,i,f"{duration} ms",va="center")
ax.set(yticks=range(len(spans)),yticklabels=[s[0] for s in spans],xlabel="Time since request start (ms)",xlim=(0,420),title="08  /  Request latency and async completion are different")
ax.invert_yaxis(); ax.axvspan(120,300,alpha=.07,color=GOLD)
ax.text(210,2.5,"queue / scheduling delay\nnot part of the HTTP duration",ha="center",fontsize=10)
fig.tight_layout(rect=(0,.06,1,1)); save(fig,"08-trace","synthetic")

latencies=np.array([100]*90+[200]*5+[1500]*5)
def percentile_nearest_rank(values,p): return int(np.sort(values)[math.ceil(len(values)*p/100)-1])
summary={"sample_count":100,"mean_ms":float(latencies.mean()),
         "p50_ms":percentile_nearest_rank(latencies,50),"p95_ms":percentile_nearest_rank(latencies,95),
         "p99_ms":percentile_nearest_rank(latencies,99),"percentile_method":"nearest rank"}
write_csv("latency.csv",["request","latency_ms"],enumerate(latencies.tolist(),1))
fig, axes=plt.subplots(1,2,figsize=(13,5.5))
sns.histplot(latencies,bins=[0,150,300,600,900,1200,1600],ax=axes[0],color=TEAL)
axes[0].set(xlabel="Latency (ms)",ylabel="Requests",title="90 fast + 5 medium + 5 slow")
metrics=[summary[k] for k in ["mean_ms","p50_ms","p95_ms","p99_ms"]]
bars=axes[1].bar(["Mean","p50","p95","p99"],metrics,color=[BLUE,TEAL,GOLD,RED])
axes[1].bar_label(bars,padding=4); axes[1].set(ylabel="Latency (ms)",ylim=(0,1750),title="Nearest-rank percentiles; n=100")
fig.suptitle("09  /  The average hides the slowest journeys",fontsize=20)
fig.tight_layout(rect=(0,.07,1,.92)); save(fig,"09-latency","synthetic","data/latency.csv")

backlog=0; rows=[(0,0,0,0)]
for minute in range(1,16):
    arrival=12 if minute<=10 else 4
    processed=min(backlog+arrival,10)
    backlog=backlog+arrival-processed
    rows.append((minute,arrival,processed,backlog))
write_csv("queue.csv",["minute","arrivals","processed","backlog"],rows)
fig,ax=plt.subplots(figsize=(11,5.5))
ax.step([r[0] for r in rows],[r[3] for r in rows],where="post",color=TEAL,linewidth=3)
ax.fill_between([r[0] for r in rows],[r[3] for r in rows],step="post",alpha=.14,color=TEAL)
ax.axvline(10,color=RED,linestyle="--"); ax.text(10.2,17,"arrivals: 12 → 4 / min")
ax.set(xlabel="Minute",ylabel="Pending jobs",title="10  /  Queue growth is a rate mismatch",xticks=range(0,16),ylim=(0,24))
fig.tight_layout(rect=(0,.07,1,1)); save(fig,"10-queue","synthetic","data/queue.csv")

rng=np.random.default_rng(42); no_jitter=np.tile([1,3,7],40)
jitter=np.cumsum(rng.uniform(0,[1,2,4],size=(40,3)),axis=1).ravel()
write_csv("retries.csv",["policy","retry_time_seconds"],[("fixed_backoff",float(t)) for t in no_jitter]+[("full_jitter",float(t)) for t in jitter])
fig,axes=plt.subplots(2,1,figsize=(11,6),sharex=True,sharey=True)
bins=np.arange(0,7.51,.25)
for ax, values, title,color in zip(axes,[no_jitter,jitter],["Same delays: retries cluster","Full jitter: retries spread"],[RED,TEAL]):
    ax.hist(values,bins=bins,color=color); ax.set(title=title,ylabel="Retries / 250 ms")
axes[1].set_xlabel("Seconds after initial failure (40 clients; three retries each)")
fig.tight_layout(rect=(0,.07,1,1)); save(fig,"11-retries","synthetic","data/retries.csv")

matrix=np.array([[1,1,1,1,0],[1,1,1,2,0],[1,1,0,0,0],[1,3,0,0,0],[0,0,0,0,0]])
features=["Create","Assign","Search","Notify","Export"]
columns=["Happy path","Error","Persistence","Authorization","Recovery"]
write_csv("verification.csv",["feature"]+columns,[[feature,*row.tolist()] for feature,row in zip(features,matrix)])
fig,ax=plt.subplots(figsize=(12,5.5))
from matplotlib.colors import ListedColormap, BoundaryNorm
colors=ListedColormap(["#dce2e5",TEAL,RED,GOLD]); norm=BoundaryNorm([-.5,.5,1.5,2.5,3.5],4)
labels=np.array(["NOT RUN","PASS","FAIL","BLOCKED"])[matrix]
sns.heatmap(matrix,cmap=colors,norm=norm,annot=labels,fmt="",cbar=False,linewidths=3,linecolor=BG,
            xticklabels=columns,yticklabels=features,ax=ax,annot_kws={"fontsize":10})
ax.set_title("12  /  A feature is not verified in every dimension",pad=16)
fig.tight_layout(rect=(0,.07,1,1)); save(fig,"12-verification","synthetic","data/verification.csv")

counts={"PASS":42,"FAIL":3,"BLOCKED":2,"NOT IMPLEMENTED":3}
write_csv("fidelity.csv",["status","count"],counts.items())
fig,ax=plt.subplots(figsize=(12,4.5)); left=0
for (status,count),color in zip(counts.items(),[TEAL,RED,GOLD,"#798b96"]):
    ax.barh(0,count,left=left,color=color,height=.6,label=f"{status}: {count}")
    ax.text(left+count/2,0,str(count),color="white",ha="center",va="center",fontweight="bold")
    left+=count
ax.set(yticks=[],xlabel="Enumerated acceptance scenarios (denominator = 50)",xlim=(0,50),title="13  /  42 / 50 = 84% of this scenario set")
ax.legend(loc="upper center",bbox_to_anchor=(.5,-.22),ncol=2,frameon=False)
fig.tight_layout(rect=(0,.12,1,1)); save(fig,"13-fidelity","synthetic","data/fidelity.csv")

plan=[("Observe",1,3),("Evidence",4,3),("UI + API",7,4),("Domain + data",11,4),
      ("Build a slice",15,4),("Compare",19,4),("Failure + security",23,4),("Release review",27,4)]
write_csv("practice-plan.csv",["phase","start_day","days"],plan)
fig,ax=plt.subplots(figsize=(12,6))
for i,(phase,start,length) in enumerate(plan):
    ax.barh(i,length,left=start-.5,color=TEAL if i%2 else BLUE,height=.65)
    ax.text(start+(length-1)/2,i,f"{start}–{start+length-1}",ha="center",va="center",color="white")
ax.set(yticks=range(len(plan)),yticklabels=[r[0] for r in plan],xticks=[1,5,10,15,20,25,30],xlim=(.5,30.5),xlabel="Practice day",title="14  /  Thirty days, eight concrete deliverables")
ax.invert_yaxis(); fig.tight_layout(rect=(0,.07,1,1)); save(fig,"14-practice","synthetic","data/practice-plan.csv")

(DATA / "summary.json").write_text(json.dumps({"kind":"synthetic_teaching_data","seed":42,"latency":summary,
    "fidelity":{"total":50,"passed":42,"pass_rate":.84},"queue":{"peak":max(r[3] for r in rows),"end":rows[-1][3]}},indent=2)+"\n")
manifest_path=OUT/"manifest.json"
existing=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
extras=[entry for entry in existing if entry.get("generator")=="scripts/make_visual_stories.py"]
manifest_path.write_text(json.dumps(manifest+extras,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"Created {len(manifest)} figures, PNG + SVG, and inspectable teaching data.")
