# Purpose: Analyze JSONL probabilities from any provider.
import argparse,json,sys
from pathlib import Path
from .core import *
def main(argv=None):
 p=argparse.ArgumentParser(prog="jev-utility");p.add_argument("command",choices=["threshold","calibrate","band","voi","sensitivity","report"]);p.add_argument("input",nargs="?");p.add_argument("--cost-fp",type=float,default=1);p.add_argument("--cost-fn",type=float,default=1);p.add_argument("--cost-human",type=float,default=.1);p.add_argument("--human-accuracy",type=float,default=.95);p.add_argument("--method",choices=["platt","isotonic"],default="platt");p.add_argument("--html");a=p.parse_args(argv)
 try:
  rows=[json.loads(x) for x in Path(a.input).read_text().splitlines() if x.strip()] if a.input else [];probs=[float(r["probability"]) for r in rows];labels=[int(r["label"]) for r in rows]
  if a.command=="threshold":result=analyze(a.cost_fp,a.cost_fn,calibration_report(probs,labels) if rows else None)
  elif a.command=="calibrate":result=calibration_split(probs,labels,a.method);result.pop("transform")
  elif a.command=="band":result=abstention_band(a.cost_fp,a.cost_fn,a.cost_human,a.human_accuracy)
  else: result={"probabilities":len(probs),"note":"Provide a problem through the Python API for multi-action VOI and sensitivity"}
  if a.command=="report":Path(a.html).write_text(html_report(result))
  else:print(json.dumps(result,indent=2))
 except Exception as error:print(f"jev-utility: {error}",file=sys.stderr);raise SystemExit(1)
