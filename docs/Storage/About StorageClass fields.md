<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

| Field                    | What it Does                                                           | Common Values                                                                                                                           |
| ------------------------ | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| **reclaimPolicy**        | Tells Kubernetes what to do with the actual disk when you delete a PVC | • `Delete` – also deletes the PV and its data• `Retain` – keeps the PV and data for manual cleanup                                      |
| **volumeBindingMode**    | Controls when Kubernetes assigns a PV to a PVC                         | • `Immediate` – binds as soon as PVC is created• `WaitForFirstConsumer` – waits until a pod uses the PVC, so PV lands on the right node |
| **allowVolumeExpansion** | Lets you grow the size of a volume after the PVC is already created    | • `true` – you can increase PVC’s storage size• `false` – size is fixed once PVC is made                                                |
- **Use `Delete`** reclaimPolicy if you want cleanup to happen automatically.
- **Use `WaitForFirstConsumer`** bindingMode for StatefulSets or multi-zone clusters so the volume shows up on the pod’s node.
- **Set allowVolumeExpansion to `true`** if you expect to need more space later.

