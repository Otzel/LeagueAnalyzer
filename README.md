# LeagueAnalyzer

LeagueAnalyzer is a **League of Legends match tracker** that fetches, stores, and analyzes your match data.

## 🚀 Features
- Automatically fetch match data using Riot API
- Store match history in a local database (`matches.db`)
- Track KDA, CS/min, lane opponent performance, and more
- Add personal notes to each match
- Easy-to-use **Streamlit** web interface

---

# Important
To use this application you need a API-key for the Riot-API. You can create and access one here [**Riot-api**](https://developer.riotgames.com/apis). After logging in you can create and find your key in the dashboard of your profile. 

## 🚀 **Installation Guide**

### **1️⃣ Install Python (If Not Already Installed)**

#### **Windows**:

- **Check if Python is installed**: Open **Command Prompt** (`Win + R`, type `cmd`, press **Enter**) and run:
  ```bash
  python --version
  ```
- If Python is not installed, download it from [python.org](https://www.python.org/downloads/) and install it.
- Make sure to tick the `Add python.exe to PATH` box

#### **Mac**:

- **Check if Python is installed**: Open **Terminal** and run:
  ```bash
  python3 --version
  ```
- If not installed, run:
  ```bash
  xcode-select --install  # Required for command line tools
  brew install python3  # If Homebrew is installed
  ```
- If you **don’t have Homebrew**, install it first:
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  ```

#### **Linux (Debian/Ubuntu)**:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

### **2️⃣ Download LeagueAnalyzer**

#### **Option 1: If You Have Git Installed**
- Can be installed with [**Git Documentation**](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Open a terminal (**Command Prompt**, **PowerShell**, or **Terminal**) and run:
  ```bash
  git clone https://github.com/Otzel/LeagueAnalyzer.git
  cd LeagueAnalyzer
  ```

#### **Option 2: If You DON'T Have Git Installed**

- Go to the [**LeagueAnalyzer GitHub Page**](https://github.com/Otzel/LeagueAnalyzer)
- Click **"Code" → "Download ZIP"**
- Extract the ZIP file
- Open **Command Prompt/Terminal** and navigate to the extracted folder:
  ```bash
  cd path/to/extracted/LeagueAnalyzer
  ```

---

### **3️⃣ Install Dependencies**

Inside the `LeagueAnalyzer` folder, run:

```bash
pip install -r requirements.txt
```

---

### **4️⃣ Run the Application**

```bash
python src/main.py
```

💡 After a few seconds, the web app will open in your browser.\
If it **doesn’t open automatically**, go to [**http://localhost:8501**](http://localhost:8501).

---

## 🔄 **How to Update LeagueAnalyzer**

### **Option 1: If You Installed with Git**

1. Open a terminal and navigate to the `LeagueAnalyzer` folder:
   ```bash
   cd LeagueAnalyzer
   ```
2. Pull the latest updates:
   ```bash
   git pull origin main
   ```
3. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app again:
   ```bash
   python src/main.py
   ```

### **Option 2: If You Downloaded the ZIP File (Not recommended)**

##### You will lose your database if you do this!

1. **Delete the old LeagueAnalyzer folder**.
2. **Download the latest version** from **GitHub Releases**.
3. **Extract the ZIP file** and navigate to the folder.
4. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the app again**:
   ```bash
   python src/main.py
   ```

---

## 🛠 **Troubleshooting**

### **"Python not found" or "Command not recognized"**

- Ensure Python is installed by running:
  ```bash
  python --version
  ```
  or
  ```bash
  python3 --version
  ```

### **"ModuleNotFoundError" (Missing dependencies)**

- Run:
  ```bash
  pip install -r requirements.txt
  ```

### **"Port 8501 is already in use"**

- Run:
  ```bash
  streamlit run src/app/app.py --server.port=8502
  ```
- Then open [**http://localhost:8502**](http://localhost:8502) in your browser.

---

## 🏆 **Contribute & Support**

If you find issues or want to contribute, open a GitHub issue or fork the repo!

---


