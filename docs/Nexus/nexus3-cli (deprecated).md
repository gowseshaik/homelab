<span style="color:#4caf50;"><b>Created:</b> 2025-07-06</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-07-06</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>
there is an **official Nexus CLI tool** called **`nexus3-cli`**, which is open-source and supports basic operations for **Nexus Repository Manager 3**.

### 📦 Tool: `nexus3-cli`

|Feature|Description|
|---|---|
|Tool Name|`nexus3-cli`|
|Language|Python|
|Maintained by|Community (not Sonatype)|
|Install via|`pip install nexus3-cli`|
|Supported operations|Repositories, users, roles, blobstores, cleanup|
### ✅ Install it

```bash
pip install nexus3-cli
```

### ✅ Recommended Fix: Use a **virtual environment**
```
python3 -m venv ~/venvs/nexus3-cli
source ~/venvs/nexus3-cli/bin/activate
pip install nexus3-cli
pip install setuptools
```

🧪 Optional: Install with `pipx` (preferred for CLI tools)

```bash
# Install `pipx`:
$ sudo apt install pipx
$ pipx inject nexus3-cli setuptools
# Install `nexus3-cli`:
$ pipx install nexus3-cli
$ pipx ensurepath
$ source ~/.bashrc

$ nexus3 --help
```
### 🔧 Basic Usage

```bash
nexus3 --help
```

Example: list all hosted repos

```bash
nexus3 repository list --host http://localhost:8081 --user admin --password 'yourpass'
```

### 🛠️ Key Features Supported

|Command|What it does|
|---|---|
|`repository list/create/delete`|Manage repositories|
|`user list/create/delete`|Manage users|
|`blobstore list/create`|Manage blob stores|
|`script list/run/delete`|Manage Groovy scripts (REST automation)|
### 🧩 Alternatives

|Tool|Type|Notes|
|---|---|---|
|`nexus3-cli`|CLI tool|Python-based, good for admin automation|
|REST API|HTTP-based|Official API by Sonatype, full control via scripts|
|Groovy scripts|Embedded|Run via UI/API, full server-side admin access|
