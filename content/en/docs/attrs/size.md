---
defaults: []
flags: []
minimums: []
title: size
types:
- double
- point
used_by: G
---
Maximum width and height of drawing, in inches.

If only a single number is given, this is used for both the width
and the height.

If defined and the drawing is larger than the given size, 
the drawing is uniformly scaled down so that it fits within the given size.

If `size` ends in an exclamation point `"!"`, then `size` is taken to be the
desired minimum size. In this case, if both dimensions of the drawing are
less than `size`, the drawing is scaled up uniformly until at least one
dimension equals its dimension in `size`.

There is some interaction between the `size` and [`ratio`]({{< ref "ratio.md" >}})
attributes.
