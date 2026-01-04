# ERA-5 Data Pipeline for WBGT Calculation

This repo contains Python scripts to:

**download → extract → merge → convert to a single DataFrame**,  
specifically for **WBGT (heat-stress index) calculation**.

---
## ⚙️ Setup
---

### 1. Create CDS API credentials file at
C:\Users<YOUR_USERNAME>.cdsapirc
**Paste this inside the file:**
url: https://cds.climate.copernicus.eu/api

key: <YOUR_API_KEY>
---

### 2. Edit `main.py`
Replace:
- file **location path**
- request **year & month**
- **data** needed from era-5
---
## 🔁 Pipeline Execution
---
### 3. Run `main.py` to download ERA-5 data
### 4. Run `exteract.py` to Extract ZIP-encoded .nc files
### 5. Run `view.py` to create a CSV file with the datas

---
📤 Output Files: era5_all.csv
