# Purpose: Verify decision, calibration, fitting, split and information calculations.
import unittest
from jev_utility import *
PROBLEM={"actions":["accept","reject"],"states":["good","bad"],"utility":{"accept":{"good":10,"bad":-5},"reject":{"good":0,"bad":0}}}
class UtilityTests(unittest.TestCase):
 def test_threshold(self):self.assertEqual(optimal_threshold(1,1),.5);self.assertEqual(optimal_threshold(1,9),.1)
 def test_abstention_and_degenerate(self):
  self.assertTrue(abstention_band(1,1,.01,.99)["worth_asking"]);self.assertFalse(abstention_band(1,1,2,.99)["worth_asking"]);self.assertFalse(abstention_band(1,1,.1,.5)["worth_asking"])
 def test_expected_utility(self):
  result=expected_utility({"good":.8,"bad":.2},PROBLEM);self.assertEqual(result["action"],"accept");self.assertEqual(result["expected_utility"],7)
 def test_calibration_exact_and_edges(self):
  result=calibration_report([0,.25,.75,1],[0,0,1,1],2);self.assertAlmostEqual(result["brier"],.03125);self.assertAlmostEqual(result["ece"],.125);self.assertEqual(sum(x["count"] for x in result["bins"]),4)
 def test_platt_isotonic_and_split(self):
  p=[.05,.1,.2,.4,.6,.8,.9,.95];y=[0,0,0,0,1,1,1,1];fit=fit_platt(p,y);self.assertLess(fit["transform"](.1),fit["transform"](.9))
  iso=fit_isotonic([.1,.2,.3,.4],[0,1,0,1]);values=[iso["transform"](x) for x in [.1,.2,.3,.4]];self.assertEqual(values,sorted(values))
  split=calibration_split(p,y,seed=3);self.assertFalse(set(split["tune_ids"])&set(split["holdout_ids"]))
 def test_voi_dominance_sensitivity_and_claim(self):
  dominant={"actions":["a","b"],"states":["x","y"],"utility":{"a":{"x":1,"y":1},"b":{"x":0,"y":0}}};self.assertEqual(value_of_information(dominant,{"x":.5,"y":.5}),0)
  self.assertIn("assuming calibration",analyze(1,1)["claim"]);self.assertTrue(sensitivity(PROBLEM,{"good":.5,"bad":.5}))
if __name__=="__main__":unittest.main()
