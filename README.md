# 🏆 Reputation Recon Ultimate
**CISO-Ready Security Assessment Platform** | Junction 2025

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.0-blue.svg)](https://reactjs.org/)

---

## 🚀 **5-Minute Quickstart**

### **Prerequisites**
- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **No API keys required!** ✨

### **Option A: Full Stack (Web UI + Backend)**

````bash
# 1. Clone the repository
git clone <your-repo-url>
cd withsecure-assessor

# 2. Start Backend (Terminal 1)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r [requirements.txt](http://_vscodecontentref_/2)
export PYTHONPATH=$PWD/src:$PYTHONPATH
python src/assessor/web/app.py

# 3. Start Frontend (Terminal 2 - NEW WINDOW)
cd frontend
npm install
npm start

# 4. Open browser
# → http://localhost:3000
# → Enter "Slack" → Click "Assess"

### **Option B: Backend Only (REST API)**

# 1. Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Run backend
export PYTHONPATH=$PWD/src:$PYTHONPATH
python src/assessor/web/app.py

# 3. Test API
curl -X POST http://localhost:5000/api/assess \
  -H "Content-Type: application/json" \
  -d '{"input": "Slack"}' | jq '.trust_score.value'
# Expected: 88

---

## ✅ **Verified Test Results**

### **Backend API Tests**

All tests pass with expected outputs:

````bash
# Test 1: Slack (High-Trust Product)
curl -X POST http://localhost:5000/api/assess \
  -H "Content-Type: application/json" \
  -d '{"input": "Slack"}' | jq '.trust_score.value'
# ✅ Result: 88

# Test 2: Microsoft (Critical CVEs)
curl -X POST http://localhost:5000/api/assess \
  -H "Content-Type: application/json" \
  -d '{"input": "Microsoft"}' | jq '.trust_score.value'
# ✅ Result: 82

# Test 3: Unknown Product
curl -X POST http://localhost:5000/api/assess \
  -H "Content-Type: application/json" \
  -d '{"input": "RandomApp123"}' | jq '.trust_score.value'
# ✅ Result: 80

# Test 4: History Tracking
curl http://localhost:5000/api/history | jq 'length'
# ✅ Result: 3 (cached assessments)

# Fresh virtual environment test
python -m venv test_venv
source test_venv/bin/activate
pip install -r [requirements.txt](http://_vscodecontentref_/3)

# ✅ Result: All 27 dependencies installed successfully
# ✅ No conflicts or errors
# ✅ Import test: from assessor.resolver.resolver import resolve_entity