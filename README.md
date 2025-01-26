## Problem Description

Given an list of _N_ values, we need to detect if any of the following rules are broken and 
the initial point in the pattern for which the rule is broken.

## Control Chart Sensitizing rules
  1. One or more points outside of the control limits (three-sigma)
  2. Two of three consecutive points outside the two-sigma warning limits butstill inside the control limits
  3. Four of five consecutive points beyond the one-sigma limit
  4. Eight consecutive points on one side of the center line. 
  ---
  5. Six points in a row steadily increasing or decreasing
  6. Fifteen points in a row within Zone C, alternating up and down (cyclic)
  7. Fourteen points in a row alternating up and down (cyclic)
  8. Eight points in a row on both sides of the center line with none in Zone C
  9. An unusual or nonrandom pattern in the data
 10. One or more points near a warning or control limit. I am now personally defining this as 0.25 sigma


## Code

- **app.py:** A simple script that loads a dataset, generates a control chart image and runs the
rules.
- **rules.py:** A collection of rules that implement the _sensitizing rules_ above (with the exception
of the vague rule **9**).
- **utils.py:** The implemenation of a helper function for the _sliding window technique_ and an
algorithm to detect cycles.
