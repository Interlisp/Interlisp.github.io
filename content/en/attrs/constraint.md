---
defaults:
- 'true'
flags:
- dot
minimums: []
name: constraint
types:
- bool
used_by: E
---
If false, the edge is not used in ranking the nodes. For example,
in the graph:

```dot
digraph G {
  a -> c;
  a -> b;
  b -> c [constraint=false];
}
```

the edge `b -> c` does not add a constraint during rank
assignment, so the only constraints are that `a` be above `b` and `c`,
yielding the graph:

<IMG SRC="constraint.gif">