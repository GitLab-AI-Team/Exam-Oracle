# 1) main.py

The sole purpose main is to orchestrate the request cycle. The cycle is broken down into 5 steps:

a) verify webhook secret
b) handle merge requests
c) find/fetch MR changes
d) analyze risk (using a helper class)
e) post/update a comment

The main class is made simple (not smart/ML) to ensure stability and delegates the operations to separate classes.

# 2) gitlab_client.py

(Used in 3rd step of main.py pipeline)

This is a supporting class

Obtains MR
Finds changes
Obtains/creates/updates MR notes

Follows Single Responsibility Principle; only does operations pertaining to the MR.
Methods are used in main.py
Makes changes easier

# 3) risk_engine.py

(Used in 4th step of main.py pipeline)

Finds risk level from path (RiskResult)

Scores 0-10 and sees if it the MR changes are low/medium/high risk and returns reasons why they are that risk

Returns a class RiskResult(...) since returning the whole class means it is well-defined and returns exactly as intended.

Why not dictionary? Dctionary/tuple makes it harder to extend/no structure guarantee.
Typos may occur, no type guarantee, no auto-complete help.


# 4) reporter.py


(Used in 5th step of main.py pipeline)

Forms the report as a comment series based on the result from risk_engine.py

Upserts risk comment (if one exists, update it. if not, create a new one)

# 5) models.py  

(Usedw in 2nd step of main.py pipeline)

Pulls ONLY what we need from the GitLab webhook 

Defines what we need from a MergeRequest with action as open/update/merge/close as the main ones we'll use (discards other action types in main.py)

# g6) config.py 

Makes sure obtaining GITLAB webhook secrets and configs are only done from a single class (Single Responsibility Principle). 

Ensures that obtaining the GitLab token is not written everywhere.


# -----

Main takeaway: main.py is the pipeline for the backend; the other classes are supporting classes that have a single responsibility to ensure changes/updates to any part of the code is only done in a single class (does not affect the rest).


Test Case:

Run on Powershell Terminal:

.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000

When running the application, you will not be able to write anymore to the terminal. Open a new terminal window to run a separate powershell and paste the code below.
Score risk will be 3 (auth = +2 points from the first line and +1 for lack of test/spec heuristic in second line)

Test 1:

$body = @{
  title = "Debug: auth change"
  changes = @(
    @{ new_path = "auth/login.py"; diff = "+ changed auth logic`n- old line" },
    @{ new_path = "src/service.py"; diff = "+ new behavior" }
  )
} | ConvertTo-Json -Depth 6

# Expected score: 3

Test 2:

$body = @{
  title = "Debug: CI change"
  changes = @(
    @{ new_path = ".gitlab-ci.yml"; diff = "+ change pipeline" }
  )
} | ConvertTo-Json -Depth 6

Expected score: 3
High file count + risky file

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/debug/analyze" -ContentType "application/json" -Body $body

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/debug/analyze" -ContentType "application/json" -Body $body

# If you want to request the full reasons, posted as a JSON file (from reporter.py)

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/debug/analyze" -ContentType "application/json" -Body $body |
  ConvertTo-Json -Depth 10

# TO RUN

Type into terminal:

cd C:\Users\youre\exam-oracle\mr-risk-scout
.\.venv\Scripts\Activate.ps1
python -m app.main

uvicorn app.main:app --reload --port 8000 # now you may start up the application
open a new terminal specifically for powershell, since you are no longer able to type once uvicorn starts up

.\.venv\Scripts\Activate.ps1
python -m pytest -q