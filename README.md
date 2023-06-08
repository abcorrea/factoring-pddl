# Factoring Large Numbers Using PDDL

To execute what we have so far, run 

```
$ ./generate-pddl.py N
```

where `N` is the number you want to factor. This will produce two files: `domain.pddl` and `problem.pddl`. 

This code was only tested with `python3.10` on Ubuntu 22.04. Moreover ,the PDDL files produced were 
tested with [Fast Downward](www.fast-downward.org/) and [Powerlifted](https://github.com/abcorrea/powerlifted)
-- also note that Fast Downward is very slow with `N > 10`.
