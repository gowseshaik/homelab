<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

##### Build
```
go build -o k8sgo k8sgo.go
```
##### Run
```
./k8sgo
```

📦 For Distribution

When building for different platforms:

##### For Linux
```
GOOS=linux GOARCH=amd64 go build -o k8sgo-linux k8sgo.go  
```

##### For Windows  
```
GOOS=windows GOARCH=amd64 go build -o k8sgo-windows.exe k8sgo.go
```

##### For macOS
```
GOOS=darwin GOARCH=amd64 go build -o k8sgo-macos k8sgo.go
```
