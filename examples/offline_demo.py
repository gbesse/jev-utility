# Purpose: Demonstrate provider-neutral threshold and calibration analysis.
from jev_utility import *
probabilities=[.05,.2,.4,.65,.9];labels=[0,0,1,1,1]
report=calibration_report(probabilities,labels,5)
print({"source":"synthetic probabilities","decision":analyze(1,4,report),"calibration":{"brier":report["brier"],"ece":report["ece"]},"human_band":abstention_band(1,4,.1,.95)})
