# From Math to Model: GAMS & GAMSPy workshop

Notebooks for a 90-minute, example-driven introduction to algebraic modeling with GAMSPy.

## 0. Install Miniconda and set up Python

1. **Install Miniconda.** Download the installer for your system from <https://www.anaconda.com/download/success> (scroll to *Miniconda Installers*) and run it with the default options. Or, from a terminal:

   ```bash
   # macOS (Apple silicon; use MacOSX-x86_64 for Intel Macs)
   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
   bash Miniconda3-latest-MacOSX-arm64.sh

   # Linux
   curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh
   ```

   Close and reopen your terminal afterwards. On Windows, use the **Anaconda Prompt** from the Start menu for the commands below.

2. **Create and activate a Python 3.14 environment:**

   ```bash
   conda create -n gamspy python=3.14 -y
   conda activate gamspy
   ```

   If conda asks you to accept its Terms of Service, answer yes.

3. **Install the workshop packages** from the `workshop` folder:

   ```bash
   cd workshop
   pip install -r requirements.txt
   ```

Run `conda activate gamspy` each time you open a new terminal.

## Before the workshop (10 minutes)

1. **Install your free academic license (recommended).** Sign up at the GAMS Academic Program (<https://www.gams.com/academics/>), copy your access code, then run:

   ```bash
   gamspy install license <your-access-code>
   gamspy show license
   ```

   No license yet? That's fine. GAMSPy's built-in demo license runs every model in this workshop.

2. **Check that it works:**

   ```bash
   python hello_gamspy.py
   ```

   You should see `Status: OPTIMAL`.

3. **Open the notebooks** with `jupyter lab` (or in VS Code).

## What's in here

| File | Act | Problem type | What you learn |
| --- | --- | --- | --- |
| `hello_gamspy.py` | Setup | LP | Your installation and license work |
| `00_matrix_vs_algebra.ipynb` | Opening · Why an AML? | LP | The coffee network solved twice from one spreadsheet: a hand-built matrix with `scipy.linprog`, and GAMSPy algebra. Same answer, same shadow prices. |
| `01_coffee_network.ipynb` | 1 · Supply chain | LP | Sets, parameters, equations; reading a solution; shadow prices; what-if loops |
| `02_blending_exercise.ipynb` | Exercise · Process | LP (+ NLP stretch) | Write a model yourself; nonconvex pooling and local optima |
| `02_blending_solution.ipynb` | | | Solutions to the exercise |
| `03_unit_commitment.ipynb` | 2 · Energy | MIP | Binary on/off decisions, time lags, relaxation vs. integer |
| `04_portfolio.ipynb` | 3 · Finance | QCP, MIQCP | Quadratic risk, the efficient frontier, a cap on holdings |
| `app.py` | Finale · Deploy | QCP / MIQCP | The portfolio model as a web app: `streamlit run app.py` |
| `data/coffee_network.xlsx` | | | The coffee network data as a spreadsheet: Farms, Roasteries, Cafes and Settings sheets |
| `data/sector_returns_simulated.csv` | | | Simulated daily returns for 12 fictional sector funds (not real market data) |

Each notebook has **Core** tasks (everyone) and **Stretch** tasks (if you finish early).

## Running on Google Colab

No local install? Every notebook runs on [Google Colab](https://colab.research.google.com). Skip section 0 and *Before the workshop*, and **run the setup cell at the top of each notebook first**.

**Open a notebook in the browser:** in Colab choose *File → Open notebook → GitHub*, paste `https://github.com/boxblox/csmio_26`, and pick a notebook from `workshop/`.

**Or from VS Code** with the Google Colab extension: open the notebook locally and select a Colab kernel. The code then runs on a Google machine, not on your computer. That machine cannot see your local files: its working directory is `/content`, not this repo.

What the setup cell does:

- **Packages.** It runs `%pip install` for the packages the notebook needs. `%pip` installs into the notebook's own kernel, so the same cell works on Colab, in Jupyter and in VS Code. Running locally after `pip install -r requirements.txt`? It just reports that everything is already installed.
- **Data files.** Notebooks 00 and 04 need files from `data/`. If a file is missing, the setup cell downloads it from this repo on GitHub (`REPO_RAW`, the `main` branch). Locally the files already exist, so nothing is downloaded. If you change a data file, push it before running on Colab, or upload your copy into a `data/` folder in Colab's Files pane.
- **License (optional).** To use your academic license on Colab, uncomment the `!gamspy install license <your-access-code>` line in the setup cell.

Good to know:

- **Colab sessions are temporary.** When the runtime disconnects or restarts, installed packages, downloaded data and your license are gone. Re-run the setup cell.
- **Save your work.** Notebooks opened from GitHub are not saved automatically. Use *File → Save a copy in Drive*.
- **`app.py` is not a notebook.** The Streamlit app needs a local install (`streamlit run app.py`).

## Solvers

A fresh `pip install gamspy` includes CPLEX, CONOPT, PATH and SBB, which cover everything here. `gamspy list solvers --all` shows more you can add with `gamspy install solver <name>`.

## Units and conventions

- Coffee network: tonnes, and costs in $1,000 per tonne.
- Unit commitment: MW, $ per MWh, $ per start-up.
- Portfolio: yearly returns and volatility, computed from daily data.

Tested with GAMSPy 1.28.
