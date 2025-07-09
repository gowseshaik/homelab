<span style="color:#4caf50;"><b>Created:</b> 2025-07-08</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-08</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

```bash
$ sudo dmidecode -t memory | grep -E 'Size:|Locator:' | grep -B1 'Size:' | grep 'Locator\|Size'
$ sudo dmidecode -t memory | grep -E 'Size:|Locator:'
        Size: 8 GB
        Locator: ChannelA-DIMM0
        Bank Locator: BANK 0
        Size: 8 GB
        Locator: ChannelB-DIMM0
        Bank Locator: BANK 2
```

