# Orchestration Human Study (NLI)

A jsPsych-based psychology experiment for studying how people answer multiple-choice mathematics questions with the option to outsource to human or AI agents.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Running Locally](#running-locally)
- [Deploying to Pavlovia](#deploying-to-pavlovia)
- [Running on Prolific](#running-on-prolific)
- [Configuration](#configuration)
- [Project Structure](#project-structure)

---

## Overview

This experiment presents participants with mathematics questions across three difficulty levels:
- Elementary Mathematics
- High School Mathematics
- College Mathematics

Participants can either:
- **Solve themselves**: +10 points (correct) / 0 points (incorrect)
- **Outsource to Human Agent**: +3 points (correct) / -7 points (incorrect)
- **Outsource to AI Agent**: +7 points (correct) / -3 points (incorrect)

Estimated duration: **45 minutes**

---

## Prerequisites

- **Node.js** (v14 or higher)
- **npm** (comes with Node.js)
- **Python 3** (for local server, optional)
- **Git** (for Pavlovia deployment)

---

## Running Locally

### Step 1: Install Dependencies

```bash
cd "/path/to/orchestration_human-study (NLI)"
npm install
```

### Step 2: Start a Local Server

**Option A: Using Python (recommended)**
```bash
python -m http.server 8080
```

**Option B: Using Node.js http-server**
```bash
npx http-server -p 8080
```

**Option C: Using PHP**
```bash
php -S localhost:8080
```

### Step 3: Open in Browser

Navigate to: **http://localhost:8080**

### Local Development Tips

To skip consent forms and reduce delays during development, edit `task.js`:

```javascript
var official_run = false  // Set to false to skip consent/instructions
var simulate = true       // Set to true to skip required answers
```

---

## Deploying to Pavlovia

Pavlovia is a platform for hosting online behavioral experiments. Follow these steps to deploy:

### Step 1: Create a Pavlovia Account

1. Go to [https://pavlovia.org](https://pavlovia.org)
2. Click **Register** and create an account
3. Verify your email address

### Step 2: Install Pavlovia Plugin

The experiment already includes the Pavlovia plugin via CDN in `index.html`:
```html
<script type="text/javascript" src="https://pavlovia.org/lib/jspsych-pavlovia-2020.2.js"></script>
```

### Step 3: Create a New Project on Pavlovia

1. Log in to Pavlovia
2. Go to **Dashboard** → **Experiments**
3. Click **New Project** → **Create from scratch**
4. Name your project (e.g., `orchestration-human-study`)
5. Set visibility to **Private** or **Public** as needed

### Step 4: Push Code to Pavlovia GitLab

```bash
# Initialize git if not already done
git init

# Add Pavlovia as remote (replace USERNAME and PROJECT_NAME)
git remote add pavlovia https://gitlab.pavlovia.org/USERNAME/PROJECT_NAME.git

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Push to Pavlovia
git push -u pavlovia main
```

### Step 5: Activate the Experiment

1. Go to your project on Pavlovia Dashboard
2. Click **Change to PILOTING** to test
3. Once tested, click **Change to RUNNING** to collect data
4. Note: Running experiments require **credits** (1 credit per participant)

### Step 6: Get Your Experiment URL

Your experiment URL will be:
```
https://run.pavlovia.org/USERNAME/PROJECT_NAME/
```

---

## Running on Prolific

Prolific is a participant recruitment platform. Here's how to integrate:

### Step 1: Create a Prolific Account

1. Go to [https://www.prolific.com](https://www.prolific.com)
2. Sign up as a **Researcher**
3. Add funds to your account

### Step 2: Configure URL Parameters

The experiment automatically captures Prolific URL parameters in `task.js`:

```javascript
var prolific_id = jsPsych.data.getURLVariable('PROLIFIC_PID');
var study_id = jsPsych.data.getURLVariable('STUDY_ID');
var session_id = jsPsych.data.getURLVariable('SESSION_ID');
```

### Step 3: Create a New Study on Prolific

1. Log in to Prolific
2. Click **New Study**
3. Fill in study details:
   - **Study name**: Your study title
   - **Description**: Brief description for participants
   - **Estimated completion time**: 45 minutes
   - **Reward**: Calculate based on your hourly rate (e.g., $9.00 for $12/hr)

### Step 4: Set Up Study URL

In the **Study Link** section:

1. Select **I'll use a URL to an external website**
2. Enter your Pavlovia URL with query parameters:
   ```
   https://run.pavlovia.org/USERNAME/PROJECT_NAME/?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID={{%STUDY_ID%}}&SESSION_ID={{%SESSION_ID%}}
   ```

### Step 5: Configure Completion URL

The experiment redirects to Prolific upon completion. Update the completion code in `task.js` if needed:

```javascript
jsPsych.init({
    timeline: timeline,
    on_finish: function () {
        // Update this URL with your study's completion code
        window.location = "https://app.prolific.com/submissions/complete?cc=YOUR_COMPLETION_CODE"
    },
    // ...
});
```

To get your completion code:
1. In Prolific study settings, go to **Study completion**
2. Select **I'll redirect them using a URL**
3. Copy the completion code provided

### Step 6: Set Screening Criteria (Optional)

Configure participant filters:
- Location (e.g., US, UK)
- Language (e.g., English fluent)
- Demographics (age, education, etc.)

### Step 7: Launch Your Study

1. Review all settings
2. Click **Publish** to start recruitment
3. Monitor progress in the Prolific dashboard

---

## Configuration

Key configuration variables in `task.js`:

| Variable | Default | Description |
|----------|---------|-------------|
| `official_run` | `true` | Show consent form and instructions |
| `no_server` | `true` | Run without backend server |
| `simulate` | `false` | Skip required answers (for testing) |
| `num_batches` | `5` | Number of question batches |
| `total_time` | `45` | Estimated study duration (minutes) |
| `base_rate` | `12` | Base hourly rate ($) |
| `bonus_rate` | `13` | Bonus hourly rate ($) |

---

## Project Structure

```
orchestration_human-study (NLI)/
├── index.html              # Main HTML entry point
├── task.js                 # Main experiment logic
├── consent.html            # Consent form
├── custom_styling.css      # Custom styles
├── package.json            # Node.js dependencies
├── resources/
│   └── batches.js          # Question data (variant_batches)
├── feedback_imgs/          # Correct/Incorrect feedback images
├── node_modules/           # Dependencies (jspsych, jquery)
└── data/                   # Collected data (local)
```

---

## Troubleshooting

### CORS Errors
If you see CORS errors, make sure you're running via a local server, not opening `index.html` directly.

### Pavlovia Not Saving Data
- Ensure the experiment is in **RUNNING** mode (not PILOTING for paid runs)
- Check that you have enough credits
- Verify the `pavlovia_init` and `pavlovia_finish` blocks are in the timeline

### Prolific Completion Issues
- Verify the completion URL matches your Prolific study settings
- Test the full flow in PILOTING mode first

---

## Support

For experiment-related issues, contact: **tracelabcds@gmail.com**
