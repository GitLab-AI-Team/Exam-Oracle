# MR Risk Scout

MR Risk Scout is an event-driven system that analyzes GitLab merge requests and flags potentially high-risk changes early in the development workflow.
It uses webhook triggers, simulates or fetches diffs, and rule-based scoring to generate actionable feedback for reviewers.

# How it Works

The GitLab Webhook is sent to a FLASK server, which processes the payload. The system checks for change data (simulated in development or fetched via GitLab API in production), analyzing the changes using a risk engine, and generates a structured MR Risk comment.

### System Flow

Webhook → Flask Server → Webhook Handler → Diff Fetch (if needed) → Risk Engine → Comment Output

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

Scores 0-10 and sees if the MR changes are low/medium/high risk and returns reasons why they are that risk

Returns a class RiskResult(...) since returning the whole class means it is well-defined and returns exactly as intended.

Why not dictionary? Dictionary/tuple makes it harder to extend/no structure guarantee.
Typos may occur, no type guarantee, no auto-complete help.


# 4) reporter.py


(Used in 5th step of main.py pipeline)

Forms the report as a comment series based on the result from risk_engine.py

Upserts risk comment (if one exists, update it. if not, create a new one)

# 5) models.py  

(Used in 2nd step of main.py pipeline)

Pulls ONLY what we need from the GitLab webhook 

Defines what we need from a MergeRequest with action as open/update/merge/close as the main ones we'll use (discards other action types in main.py)

# 6) config.py 

Makes sure obtaining GITLAB webhook secrets and configs are only done from a single class (Single Responsibility Principle). 

Ensures that obtaining the GitLab token is not written everywhere.

# 7) webhook_handler.py

Fetches the MR Changes

For webhook payloads, it will scan for changes and if there are not, check if there is a project_id and mr_iid and use GitLab Merge Request API for fetching changes instead.

MR Risk Analysis comment is also defined here

# 8) server.py

Opens FLASK server, allowing POST requests to be sent, with defined bodies converted to JSON.
Returns the result of the POST request

# -----

Main takeaway: main.py is the pipeline for the backend; the other classes are supporting classes that have a single responsibility to ensure changes/updates to any part of the code is only done in a single class (does not affect the rest).

server.py opens up the FLASK server for POST requests
webhook_handler creates the pipeline for the webhook MR Risk Analysis


# Running the Application

Idea: Open up the FLASK server.
We want to define a webhook payload, send the POST request and retrieve comments for the MR Risk output

1) Open the FLASK server.
python server.py

2) Define the body
Open a powershell terminal:

 $body = @{
    object_kind = "merge_request"
    object_attributes = @{
        title = "Test MR"
    }
    changes = @(
        @{
            new_path = "auth/login.py"
            diff = "+ change"
        }
    )
} | ConvertTo-Json -Depth 5

3) Send the POST request
Invoke-RestMethod -Method Post `
    -Uri "http://127.0.0.1:5000/webhook" `
    -ContentType "application/json" `
    -Body $body

This should post that there is an MR Risk Analysis done
Now you just need to find the comments

4) $response.comment

Example Output:

🚨 MR Risk Analysis

Risk Score: 3

Reasons:
- Touches higher-risk areas (auth/infra/config/migrations/etc).
- No obvious test changes detected.
