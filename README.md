# SAT solver with DPLL group 3
[Link to google docs for tasks, research question and planning.](https://docs.google.com/document/d/1F_wTVEpV_9wb2ctD3C9XG-5DSfD8SNUY4EB0c1tK0Lg/edit?usp=sharing)
            
This program receives an input of satisfabilty problem presented in Conjunctive Normal Form (CNF) and encoded in DIMACS format.
If the problem is satisfiable, one possible solution is output in the resulting file.
If the problem is not satisfiable, the output will contain an empty file.

## Algorithm
DPLL Algorithm with several different branching heuristics. The problem is defined in CNF form

```python
   function DPLL(Φ)
    if Φ is a consistent set of literals then
        return true;
    if Φ contains an empty clause then
        return false;
    for every unit clause {l} in Φ do
       Φ ← unit-propagate(l, Φ);
    for every literal l that occurs pure in Φ do
       Φ ← pure-literal-assign(l, Φ);
    l ← choose-literal(Φ);
    return DPLL(Φ ∧ {l}) or DPLL(Φ ∧ {not(l)});
 ```

## Branching heuristics

RANDOM
```
DLCS (Dynamic Largest Combined Sum):
   - Pick v with largest CP(v)+CN(v) (= most frequent v)
   - If CP(v)>CN(v) then v=1 else v=0
```
 
DLIS (Dynamic Largest Individual Sum):
```
 •Pick v with largest CP(v) or largest CN(v)
 •If CP(v)>CN(v) then v=1 else v=0
```
JEROSLOW-WANG (exponentially higher weight to literals in shorter clauses):
```
 Compute for every clause ω and every variable l in each phase:
 J(l) := Σ((2)^(-|ω|)) ∀l ∈ ω
 Choose a variable l that maximizes J(l).
```
JEROSLOW-WANG-TWO-SIDED:

 
# Usage:
```bash
python SAT.py Sn sudoku_dimacs_file 

python SAT.py [-h] [-r RULES] [-v VERBOSE] [-d DRAW] [-flagged FLAGGED_OUTPUT] branching_heuristic input_file
```
Branching Heuristics code mappings:
```
'S1': 'RANDOM',                  
'S2': 'DLIS_negated',
'S3': 'DLIS',
'S4': 'DLCS',
'S5': 'JEROSLOW_WANG',
'S6': 'JEROSLOW_WANG_TWO_SIDED'
```

#read files and convert to cnf


#instantiate solver

solution_dpll = dpll.Solver(clauses1)

#Run solver

answer = solution_dpll.solve()

solution_dpll.iteration gives the number of iterations taken to reach the solution

solution_dpll.solution outputs the solution as a list of literals


solution_dpll.debug_flag = True will print out step by step information about the solver

solution_dpll.negated_first = True will compute the branch with negated literal fist
Example: if dpll splits on literal t, then it will solve the branch with -t first

Check notebook in notebooks folder for a better demonstration