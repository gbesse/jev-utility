# Purpose: Closed-form thresholds, calibration fits and utility diagnostics.
from __future__ import annotations
import html,json,math,random

def optimal_threshold(cost_fp:float,cost_fn:float)->float:
    if cost_fp<0 or cost_fn<0 or cost_fp+cost_fn<=0:raise ValueError("Costs must be non-negative and not both zero")
    return cost_fp/(cost_fp+cost_fn)
def abstention_band(cost_fp,cost_fn,cost_human,human_accuracy,steps=10000):
    if not 0<=human_accuracy<=1:raise ValueError("human_accuracy must be in [0,1]")
    worth=[]
    for i in range(steps+1):
        p=i/steps; auto=min(cost_fn*p,cost_fp*(1-p)); human=cost_human+(1-human_accuracy)*(cost_fn*p+cost_fp*(1-p))
        if human<auto:worth.append(p)
    return {"lower":min(worth) if worth else None,"upper":max(worth) if worth else None,"worth_asking":bool(worth),
            "reason":None if worth else "Human cost/accuracy never beats automatic action"}
def expected_utility(probabilities,problem):
    states=problem["states"];actions=problem["actions"];rows=[]
    for action in actions:
        utility=sum(probabilities[state]*problem["utility"][action][state] for state in states);rows.append((action,utility))
    rows.sort(key=lambda x:x[1],reverse=True)
    return {"action":rows[0][0],"expected_utility":rows[0][1],"margin":rows[0][1]-rows[1][1] if len(rows)>1 else math.inf,"ranking":rows}
def calibration_report(probabilities,labels,bins=10):
    if len(probabilities)!=len(labels) or not probabilities:raise ValueError("Aligned non-empty probabilities and labels required")
    table=[];ece=0
    for index in range(bins):
        lo=index/bins;hi=(index+1)/bins;members=[(p,int(y)) for p,y in zip(probabilities,labels) if lo<=p<=hi and (p<hi or index==bins-1)]
        if members:
            mean=sum(p for p,_ in members)/len(members);rate=sum(y for _,y in members)/len(members);ece+=len(members)/len(labels)*abs(mean-rate)
            table.append({"lower":lo,"upper":hi,"count":len(members),"mean_probability":mean,"observed_rate":rate})
        else:table.append({"lower":lo,"upper":hi,"count":0,"mean_probability":None,"observed_rate":None})
    return {"brier":sum((p-int(y))**2 for p,y in zip(probabilities,labels))/len(labels),"ece":ece,"bins":table,"count":len(labels)}
def _sigmoid(x):return 1/(1+math.exp(-max(-40,min(40,x))))
def fit_platt(probabilities,labels,iterations=2000,rate=.05):
    """Fit sigmoid(a*logit(p)+b) using deterministic batch gradient descent."""
    a,b=1.,0.;xs=[math.log(min(.999999,max(.000001,p))/(1-min(.999999,max(.000001,p)))) for p in probabilities]
    for _ in range(iterations):
        errors=[_sigmoid(a*x+b)-y for x,y in zip(xs,labels)];a-=rate*sum(e*x for e,x in zip(errors,xs))/len(xs);b-=rate*sum(errors)/len(xs)
    return {"a":a,"b":b,"transform":lambda p:_sigmoid(a*math.log(min(.999999,max(.000001,p))/(1-min(.999999,max(.000001,p)))))}
def fit_isotonic(probabilities,labels):
    ordered=sorted(zip(probabilities,map(float,labels)));blocks=[[p,p,y,1] for p,y in ordered]
    i=0
    while i<len(blocks)-1:
        if blocks[i][2]/blocks[i][3]>blocks[i+1][2]/blocks[i+1][3]:
            blocks[i]=[blocks[i][0],blocks[i+1][1],blocks[i][2]+blocks[i+1][2],blocks[i][3]+blocks[i+1][3]];blocks.pop(i+1);i=max(0,i-1)
        else:i+=1
    points=[{"lower":a,"upper":b,"value":total/count} for a,b,total,count in blocks]
    def transform(p):
        nearest=min(points,key=lambda x:0 if x["lower"]<=p<=x["upper"] else min(abs(p-x["lower"]),abs(p-x["upper"])))
        return nearest["value"]
    return {"points":points,"transform":transform}
def calibration_split(probabilities,labels,method="platt",seed=7,holdout=.3):
    ids=list(range(len(labels)));random.Random(seed).shuffle(ids);cut=max(1,int(len(ids)*(1-holdout)));tune,held=ids[:cut],ids[cut:]
    fit=(fit_platt if method=="platt" else fit_isotonic)([probabilities[i] for i in tune],[labels[i] for i in tune]);pred=[fit["transform"](probabilities[i]) for i in held]
    return {"tune_ids":tune,"holdout_ids":held,"fit":{k:v for k,v in fit.items() if k!="transform"},"report":calibration_report(pred,[labels[i] for i in held]) if held else None,"transform":fit["transform"]}
def value_of_information(problem,probabilities):
    current=expected_utility(probabilities,problem)["expected_utility"]
    oracle=sum(probabilities[state]*max(problem["utility"][action][state] for action in problem["actions"]) for state in problem["states"])
    return oracle-current
def sensitivity(problem,probabilities,factors=(.25,.5,.75,1,1.25,1.5,2,4)):
    base=expected_utility(probabilities,problem)["action"];result={}
    for action in problem["actions"]:
        for state in problem["states"]:
            key=f"{action}.{state}";changes=[]
            for factor in factors:
                altered=json.loads(json.dumps(problem));altered["utility"][action][state]*=factor
                if expected_utility(probabilities,altered)["action"]!=base:changes.append(factor)
            result[key]={"base_action":base,"flip_factors":changes}
    return result
def analyze(cost_fp,cost_fn,calibration=None,tolerance=.05):
    calibrated=calibration is not None and calibration.get("ece",math.inf)<=tolerance
    return {"threshold":optimal_threshold(cost_fp,cost_fn),"claim":"optimal under the stated costs" if calibrated else "optimal under the stated costs, assuming calibration","calibration_passed":calibrated}
def html_report(data):
    payload=html.escape(json.dumps(data,indent=2));return f"<!doctype html><meta charset=utf-8><title>jev-utility report</title><style>body{{font:16px system-ui;max-width:70rem;margin:2rem auto}}pre{{white-space:pre-wrap;background:#f5f5f5;padding:1rem}}</style><h1>Utility report</h1><pre>{payload}</pre>"
