
| Assumption (which is wrong)  | **Description**                                                            | **Impact**                                                             |
| ---------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Git = Single Source of Truth | Assuming Git always has the correct desired state                          | May lead to ignoring live drift or emergency changes outside Git       |
| "Sync = Deploy"              | Believing `argocd app sync` is equivalent to a full deployment             | Ignores that partial syncs or hooks may not trigger everything         |
| Manual Override Ignorance    | Not tracking manual `kubectl` changes because "ArgoCD will sync it anyway" | Causes hidden drift and misalignment with Git                          |
| UI-Only Comfort              | Relying only on ArgoCD UI instead of CLI or automation                     | Slows down automation, less reproducible workflows                     |
| Overtrusting Health Status   | Assuming "Healthy" status means the app works perfectly                    | Health checks are often superficial and may not reflect runtime issues |
| One Repo Fits All            | Keeping all apps and configs in a single monorepo                          | Makes scaling, ownership, and access control harder                    |
| Ignoring Namespaces          | Deploying all apps in `default` or one namespace                           | Security, RBAC, and observability become messy                         |
| No Environment Parity        | Assuming dev/stage/prod ArgoCD instances behave the same                   | Misconfigurations due to mismatched secrets, resources, or RBAC        |
| Tooling                      | Thinking ArgoCD replaces Helm/Kustomize completely                         | Leads to neglecting proper templating and environment layering         |
