```bash
gouse@gouse$ docker stats --no-stream
CONTAINER ID   NAME                        CPU %     MEM USAGE / LIMIT     MEM %     NET I/O          BLOCK I/O         PIDS
2eb6278369ae   dev-cluster-control-plane   14.56%    543.7MiB / 15.37GiB   3.45%     491kB / 4.52MB   1.21MB / 813MB    271
462f01578a57   dev-cluster-worker          2.62%     107.9MiB / 15.37GiB   0.69%     2.28MB / 237kB   418kB / 122MB     83
8ea6e48720e9   dev-cluster-worker2         1.19%     108.6MiB / 15.37GiB   0.69%     2.28MB / 241kB   295kB / 122MB     83
fdd41c690bfb   harbor-log                  0.00%     16.27MiB / 15.37GiB   0.10%     34.8kB / 126B    15.3MB / 8.19kB   10


gouse@gouse$ docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"
NAME                        MEM USAGE / LIMIT
dev-cluster-control-plane   543.1MiB / 15.37GiB
dev-cluster-worker          107.8MiB / 15.37GiB
dev-cluster-worker2         108.1MiB / 15.37GiB
harbor-log                  16.27MiB / 15.37GiB

```