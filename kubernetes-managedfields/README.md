### Overview

These little experiments try to answer a question regarding Kubernetes objects' `.metadata.managedFields`.

**Question**: When manager A already owns field X, and then manager B sets X to the same value, what does this leave the managedFields saying about X?

The original question was asked [here](https://kubernetes.slack.com/archives/C0EG7JC6T/p1726079535895249) in [sig-api-machinery Slack channel](https://kubernetes.slack.com/messages/sig-api-machinery). 

Kubernetes [docs](https://kubernetes.io/docs/reference/using-api/server-side-apply/#apply-and-update) says that two operations (HTTP PATCH and HTTP PUT) "update `.metadata.managedFields`, but behave a little differently". These experiments try to answer the question for both operations.

Experiments are performed on commit [7ee17ce9b7c2a22e63e2bbd79d48d3fe349a9386](https://github.com/kubernetes/kubernetes/tree/7ee17ce9b7c2a22e63e2bbd79d48d3fe349a9386) of k/k.
```
commit 7ee17ce9b7c2a22e63e2bbd79d48d3fe349a9386 (HEAD -> master, upstream/master, upstream/HEAD)
Merge: 2fb37e24891 3d3ba6f8981
Author: Kubernetes Prow Robot <20407524+k8s-ci-robot@users.noreply.github.com>
Date:   Mon Sep 30 17:00:07 2024 +0100

    Merge pull request #126488 from haircommander/cri-stats-suffix-hack
    
    kubelet: don't use cadvisor stats if PodAndContainerStatsFromCRI feature is enabled
```

### Apply (HTTP PATCH)
Experiment shows that this operation results in co-ownership of a field by setting the same value.

Details are documented [here](./apply_HTTP-PATCH.md).

### Update (HTTP PUT)
Experiment shows that this operation doesn't change the owner of a field by setting the same value.

Steps are detailed [here](./update_HTTP-PUT.md).

### Tests (coming soon)
I found it interesting to write some more unit tests. More to be shared here very soon.
