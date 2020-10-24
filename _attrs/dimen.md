---
defaults:
- '2'
flags:
- neato
- fdp
- sfdp
minimums:
- '2'
name: dimen
types:
- int
used_by: G
---
Set the number of dimensions used for rendering. 

The maximum value allowed is `10`.

If both `dimen` and `dim` are set, the latter specifies
the dimension used for layout, and the former for rendering.
If only `dimen` is set, this is used for both layout and rendering
dimensions.

Note that, at present, all aspects of rendering are 2D. This includes
the shape and size of nodes, overlap removal, and edge routing. Thus,
for `dimen > 2`, the only valid information is the `pos`
attribute of the nodes.

All other coordinates will be 2D and, at best, will reflect a projection
of a higher-dimensional point onto the plane.
