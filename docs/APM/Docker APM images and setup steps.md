<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

```bash
sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.0
sudo docker pull docker.elastic.co/kibana/kibana:8.13.0
sudo docker pull docker.elastic.co/apm/apm-server:8.13.0

sudo docker run -d --name elasticsearch --network=host \
  -e discovery.type=single-node \
  -e xpack.security.enabled=false \
  -e ES_JAVA_OPTS='-Xms1g -Xmx1g' \
  docker.elastic.co/elasticsearch/elasticsearch:8.13.0

sudo docker run -d --name kibana --network=host \
  -e ELASTICSEARCH_HOSTS=http://localhost:9200 \
  docker.elastic.co/kibana/kibana:8.13.0

sudo docker run -d --name apm-server --network=host \
  -e ELASTICSEARCH_HOSTS=http://localhost:9200 \
  -e KIBANA_HOST=http://localhost:5601 \
  docker.elastic.co/apm/apm-server:8.13.0


http://10.189.65.114:9200/
http://10.189.65.114:5601/
http://10.189.65.114:8200/
```

Here is a simple Java Spring Boot app that sends traces to Elastic APM.

---

### 1. Create `pom.xml` (Maven) with dependencies:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">

  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>apm-demo</artifactId>
  <version>1.0.0</version>
  <packaging>jar</packaging>

  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.7.0</version>
  </parent>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
<build>
  <plugins>
    <plugin>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-maven-plugin</artifactId>
      <version>2.7.0</version>
      <executions>
        <execution>
          <goals>
            <goal>repackage</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>

</project>
```

---

### 2. Create `src/main/java/com/example/apmdemo/ApmDemoApplication.java`:

```java
package com.example.apmdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
public class ApmDemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(ApmDemoApplication.class, args);
    }
}

@RestController
class HelloController {

    @GetMapping("/hello")
    public String hello() throws InterruptedException {
        // Simulate work
        Thread.sleep(100);
        return "Hello from APM Demo!";
    }
}
```

---

### 3. Run the app with Elastic APM Agent:

- Download Elastic APM Java agent jar:
    

```bash
curl -L -o elastic-apm-agent.jar https://search.maven.org/remotecontent?filepath=co/elastic/apm/elastic-apm-agent/1.51.0/elastic-apm-agent-1.51.0.jar
```

- Run Spring Boot app:
    

```bash
mvn clean package

java -javaagent:/path/to/elastic-apm-agent.jar \
     -Delastic.apm.service_name=apm-demo-app \
     -Delastic.apm.server_urls=http://localhost:8200 \
     -Delastic.apm.application_packages=com.example.apmdemo \
     -jar target/apm-demo-1.0.0.jar

java -javaagent:/home/ubuntu/SpringBootApp-demo/elastic-apm-agent.jar \
     -Delastic.apm.service_name=apm-demo-app \
     -Delastic.apm.server_urls=http://localhost:8200 \
     -Delastic.apm.application_packages=com.example.apmdemo \
     -jar target/apm-demo-1.0.0.jar
```

---

### 4. Test

```bash
curl http://localhost:8080/hello
```

---

You should see traces in Kibana APM dashboard under service name **`apm-demo-app`**.

Your app ran correctly (no errors shown) and Java version is fine (OpenJDK 11).

Now open a new terminal and test:

```bash
curl http://localhost:8080/hello
```

If still no response, check:

```bash
ss -tuln | grep 8080
```

to verify if app is listening.

---

If still not accessible, try adding this to your `application.properties` (create in `src/main/resources`):

```
server.address=0.0.0.0
server.port=8080
```

Rebuild and rerun the app. This forces Spring Boot to listen on all interfaces.

To confirm your Java app is sending data to Elastic APM:

---

### 1. Check APM Server logs

Inside the VM running APM Server container, run:

```bash
sudo docker logs apm-server --tail 50
```

Look for lines showing incoming transactions or no connection errors.

---

### 2. Query APM Server API for received data (quick test)

```bash
curl -s http://localhost:8200/intake/v2/events | jq
```

(It usually returns empty unless you POST data, so mainly use logs.)

---

### 3. Check Kibana APM Dashboard

- Open Kibana UI:  
    `http://localhost:5601`
    
- Go to **Observability > APM**
    
- Look for your service name (e.g., `apm-demo-app`).
    
- You should see transaction traces, errors, and metrics from your app.

---
### 4. Enable DEBUG logging on APM agent (optional)

Add to your Java run command for detailed agent logs:

```bash
-Delastic.apm.log_level=DEBUG
```

Example:

```bash
java -javaagent:/path/to/elastic-apm-agent.jar \
     -Delastic.apm.service_name=apm-demo-app \
     -Delastic.apm.server_urls=http://localhost:8200 \
     -Delastic.apm.application_packages=com.example.apmdemo \
     -Delastic.apm.log_level=DEBUG \
     -jar target/apm-demo-1.0.0.jar
```

Check your app console for APM communication logs.

---

### Summary:

- **Best way:** Use Kibana APM UI to see live traces.
    
- **Logs:** Check APM Server and Java app logs for errors or sent data.
    
- **Debug mode:** Helps troubleshoot agent communication.
    

---

Let me know if you want a script to pull recent APM logs or export Kibana dashboards.