# Advent of code
https://adventofcode.com/

# inputs

The creator of Advent of Code does not want the inputs to be leaked.
That's why they are in private git submodules.

# git stuff
## cloning repo
```bash
git clone --recursive git@github.com:DerEmperor/AdventOfCode.git
```

if you forgot the `--recursive`:
```bash
git submodule update --init --recursive
```

## add submodule for new year
```bash
git submodule add git@github.com:DerEmperor/AdventOfCodeInputs2024.git ./2024/inputs
```
