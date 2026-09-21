# Utility and calibration method

For false-positive cost `Cfp` and false-negative cost `Cfn`, predicting positive costs `Cfp(1-p)` and predicting negative costs `Cfn·p`. Equality gives `p=Cfp/(Cfp+Cfn)`. This is only optimal under the stated costs when probabilities are calibrated.

The abstention band compares both automatic losses with the declared human cost plus expected residual error at the declared human accuracy. Calibration reports Brier score, expected calibration error and populated reliability bins. Platt scaling fits a sigmoid over logits; isotonic regression uses pooled adjacent violators and can overfit small tuning sets. Both are fitted on a seeded tuning split and evaluated on a disjoint holdout.

Value of information is the expected utility of knowing the state minus the best current expected utility. It is an upper bound on the value of any improved predictor under the declared utility table.
