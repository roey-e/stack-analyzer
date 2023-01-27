# Stack Analyzer

Stack Analyzer is a tool for static analysis of C/C++ callstacks. It provides estimation for stack memory consumption of the developer's C/C++ program.

The tool analyzes GCC's `-fcallgraph-info` output files. The feature is supported since GCC version 10.

# Features

* Convert GCC's `ci` files to `networkx.DiGraph` graph object.
* Get most memory consuming callstack.
* Get maximum callstack memory consumption.
* Make memory consumption calculations from an input function name.

## Limitations

* C only.
* Recursion calls are dismissed.

# Roadmap

* CLI.
* C++ support.
* Get all callstacks sorted by memory consumption.
* Recursion flattening directives from user input.
* Dynamic function calls hints from user input.
