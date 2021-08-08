---
defaults:
- 'false'
flags:
- dot
minimums: []
title: compound
types:
- bool
used_by: G
---
If true, allow edges between clusters.

See [`lhead`]({{< ref "lhead.md" >}}) and [`ltail`]({{< ref "ltail.md" >}}).

{{< dot_card >}}
digraph {
  compound=true;

  subgraph cluster_a {
    label="Cluster A";
    node1; node3; node5; node7;
  }
  subgraph cluster_b {
    label="Cluster B";
    node2; node4; node6; node8;
  }

  node1 -> node2 [label="1"];
  node3 -> node4 [label="2" ltail="cluster_a"];
  
  node5 -> node6 [label="3" lhead="cluster_b"];
  node7 -> node8 [label="4" ltail="cluster_a" lhead="cluster_b"];
}
{{< /dot_card >}}
