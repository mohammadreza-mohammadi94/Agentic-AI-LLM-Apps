### 📌 `CONTRIBUTING.md`

# Contributing to AgenticAI 🚀

Thank you for considering contributing to **AgenticAI**!  
To keep everything consistent and organized, please follow the guidelines below.


## 📦 Setup Instructions
1. Fork the repository.
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/AgenticAI.git
   cd AgenticAI
    ```

3. Create a virtual environment:

   ```bash
   python -m venv ai
   source ai/bin/activate   # Linux / Mac
   ai\Scripts\activate      # Windows
   ```
4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```


## 🔥 Development Workflow

* **Main branch (`main`)** is always stable. Never commit directly to it.
* For any new work:

  1. Create a branch:

     ```bash
     git checkout -b feat/your-feature
     ```
  2. Make your changes.
  3. Run code formatting and linting:

     ```bash
     black .
     flake8 .
     ```
  4. Commit your changes with a meaningful message:

     ```bash
     git commit -m "feat: short description of change"
     ```
  5. Push to your fork and open a Pull Request (PR).


## 📝 Branch Naming Conventions

* `feat/*` → New feature
* `fix/*` → Bug fix
* `chore/*` → Maintenance / minor changes
* `docs/*` → Documentation updates
* `test/*` → Adding or improving tests


## 🤖 Automated Project Index

* Each new project should be added under the appropriate folder in `projects/`.
* The GitHub Actions workflow will **automatically update**:

  * `PROJECTS_INDEX.md`
  * The project index section inside `README.md`
* ⚠️ No need to manually edit these sections.


## 💬 Communication

* For questions, suggestions, or ideas, please open an **Issue**.
* For contributions, use **Pull Requests** with clear descriptions.

