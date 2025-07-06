<span style="color:#4caf50;"><b>Created:</b> 2025-06-22</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
```bash
# For Shell
oc exec -it myingress-68dc769f7f-8cbpp -- sh

# to run some command and sub commands
oc exec -it ibmmq-68dc769f7f-8cbpp -c qmgr -- cat /etc/mqm/qm.ini
oc exec -it ibmmq-68dc769f7f-8cbpp -- runmqsc < mq.mqsc.rollback
oc exec -it myingress-68dc769f7f-8cbpp -- ls /path/to/dir

# for multiple paths
oc exec -it myingress-68dc769f7f-8cbpp -- ls -ltr /home/user/somepath/onepath /home/user/somepath/twopath
```