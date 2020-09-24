# SAT solver with DPLL, group 3, KR course 2020

Python version: 3.6+
Requirements: pygame version 1.9.6 (run command "pip install pygame==1.9.6" to install it onto python)
            
This program expects a SAT problem presented as CNF Formula in DIMACS format as an input.
It applies a DPLL algorithm with optional choice of branching heuristic, and finds a solution. 

If the problem is satisfiable, one solution will be saved in the output file.
If the problem is not satisfiable, the output will contain an empty file.

# Usage:
```bash
python SAT.py Sn sudoku_dimacs_file 

python SAT.py branching_heuristic input_file [-h] [-r RULES] [-v VERBOSE] [-d DRAW] [-f FLAGGED_OUTPUT] 
```
Branching Heuristics code mappings:
```
'S1': 'RANDOM',                  
'S2': 'DLIS',
'S3': 'DLCS',
'S4': 'JEROSLOW_WANG',
'S5': 'JEROSLOW_WANG_TWO_SIDED'
'S6': 'DLIS_negated',
```
There are additional useful options which can be requested, for instance the following command will
 - look for a solution to the SAT encoded in sudoku_13 file
 - draw the found sudoku solution 
 - safe the output file with name indicating the heuristic (in this example, sudoku_13_JEROSLOW_WANG_TWO_SIDED.out)
```python
python SAT.py S5 sudoku_13 -f=True -d=True
```
By default, we assume that the input file is a complete CNF formula, encoded in DIMACS format.
Also in case the input represents a Sudoku game, we therefore expect the input file to include the encoded rules.  
However, for convenience, if the input is a Sudoku game, there is an option to only provide the game formula, without the Sudoku rules, or provide Rules as a separate file.

Please use a -help flag for more options  
 
## The Algorithm
DPLL Algorithm with several different branching heuristics. 
The problem Φ is defined as a CNF formula 

```
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
```
S1 = Random
S2 = DLIS (Dynamic Largest Individual Sum)   
S3 = DLCS (Dynamic Largest Combined Sum)
S4 = Jeroslow-Wang 
S5 = Two sided Jeroslow-Wang
S6 = DLIS-negated (Our own heuristic which will negate the litaral chosen with DLIS)
```
 
