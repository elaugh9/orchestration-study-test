// ============================================================
// CONFIGURATION — adjust these numbers to change the experiment
// ============================================================
var STARTING_BUDGET    = 48;
var TRAINING_BUDGET    = 12;  // separate budget for practice — resets to STARTING_BUDGET for main trials
var AI_PRICE_CHEAP     = 2;
var AI_PRICE_EXPENSIVE = 6;

// 36 main trials: 12 per difficulty (6 cheap + 6 expensive)
var MAIN_PER_DIFF = 12;
var MAIN_CHEAP_PER_DIFF = 6;
var MAIN_EXPENSIVE_PER_DIFF = 6;

// AI incorrect counts per difficulty — 2 wrong total (easy:1, medium:1, hard:0) = 34/36 ≈ 95% accurate
var AI_INCORRECT_COUNTS = { easy: 1, medium: 1, hard: 0 };

// 6 training trials: 2 per difficulty (1 cheap + 1 expensive)
var TRAINING_PER_DIFF = 2;

// Bonus added to budget for each correct answer (both training and main)
var CORRECT_BONUS = 1;

// ============================================================
// CONDITION ASSIGNMENT
// For lab use: append ?condition=always-available OR
//              ?condition=elective-budget  to the URL.
// Example: http://localhost:8080?condition=elective-budget
// If no URL parameter is given, defaults to elective-budget.
// ============================================================
var urlParams = new URLSearchParams(window.location.search);
var condition = urlParams.get('condition') || 'elective-budget';
var budget = TRAINING_BUDGET;  // starts at training budget; reset to STARTING_BUDGET before main trials

var subject_id = jsPsych.randomization.randomID(10);
jsPsych.data.addProperties({ subject_id: subject_id, condition: condition });

// ============================================================
// GLOBAL STATE for the inline AI-help button
// (needs to be global so the onclick handler in the HTML can reach it)
// ============================================================
var _currentAIPrice  = 0;
var _currentAIAnswer = '';
var _aiPurchasedThisTrial = false;
var _selectedAnswer = null; // captured on radio click, before DOM is cleared
var _sliderMoved = false;

function requestAIHelp() {
    if (_aiPurchasedThisTrial) return; // can only buy once per trial
    if (budget < _currentAIPrice) return;

    budget -= _currentAIPrice;
    _aiPurchasedThisTrial = true;

    // Show the AI recommendation box
    var aiRec = document.getElementById('ai-recommendation');
    if (aiRec) aiRec.style.display = 'block';

    // Hide the buy button so they can't press it again
    var btn = document.getElementById('ai-help-btn');
    if (btn) btn.style.display = 'none';

    // Update the budget display on screen immediately
    var budgetEl = document.getElementById('budget-display');
    if (budgetEl) budgetEl.innerHTML = 'Budget remaining: <strong>' + budget + ' units</strong>';
}

// Called when a radio button is selected — stores the answer and enables Submit
function updateSubmitState() {
    var submitBtn = document.getElementById('jspsych-html-slider-response-next');
    if (!submitBtn) return;

    if (_selectedAnswer && _sliderMoved) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-disabled');
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('btn-disabled');
    }
}

function onAnswerSelected() {
    var selected = document.querySelector('input[name="maze-answer"]:checked');
    if (selected) {
        _selectedAnswer = selected.value; // save now, before DOM is cleared
    }
    updateSubmitState();
}

// ============================================================
// TRIAL SELECTION
// Returns { training: [...], main: [...] }
//
// Training (6 trials): 2 per difficulty, one cheap + one expensive,
//   all drawn from model_correct so AI is always right during training.
//
// Main (24 trials): 8 per difficulty, 4 cheap + 4 expensive,
//   with exactly AI_INCORRECT_COUNTS[diff] AI-wrong trials per difficulty.
// ============================================================
function selectTrials() {
    var mainTrials     = [];
    var trainingTrials = [];

    var difficultyMap = [
        { key: 'easy',   data: maze_data_easy   },
        { key: 'medium', data: maze_data_medium },
        { key: 'hard',   data: maze_data_hard   }
    ];

    difficultyMap.forEach(function(diff) {
        var numIncorrect = AI_INCORRECT_COUNTS[diff.key];
        var numCorrect   = MAIN_PER_DIFF - numIncorrect;

        // Shuffle both pools independently
        var shuffledCorrect   = jsPsych.randomization.shuffle(diff.data.model_correct.slice());
        var shuffledIncorrect = jsPsych.randomization.shuffle(diff.data.model_incorrect.slice());

        // Reserve first TRAINING_PER_DIFF correct mazes for training
        var trainingPool  = shuffledCorrect.slice(0, TRAINING_PER_DIFF);
        var mainCorrect   = shuffledCorrect.slice(TRAINING_PER_DIFF, TRAINING_PER_DIFF + numCorrect);
        var mainIncorrect = shuffledIncorrect.slice(0, numIncorrect);

        // ---- Training trials: 1 cheap + 1 expensive ----
        var trainingPrices = jsPsych.randomization.shuffle([AI_PRICE_CHEAP, AI_PRICE_EXPENSIVE]);
        trainingPool.forEach(function(maze, i) {
            trainingTrials.push({
                maze:        maze,
                difficulty:  diff.key,
                ai_price:    trainingPrices[i],
                is_training: true
            });
        });

        // ---- Main trials: 5 cheap + 5 expensive, prices assigned randomly ----
        var mainPool = jsPsych.randomization.shuffle(mainCorrect.concat(mainIncorrect));
        var mainPrices = [];
        for (var i = 0; i < MAIN_CHEAP_PER_DIFF; i++)     mainPrices.push(AI_PRICE_CHEAP);
        for (var i = 0; i < MAIN_EXPENSIVE_PER_DIFF; i++) mainPrices.push(AI_PRICE_EXPENSIVE);
        mainPrices = jsPsych.randomization.shuffle(mainPrices);

        mainPool.forEach(function(maze, i) {
            mainTrials.push({ maze: maze, difficulty: diff.key, ai_price: mainPrices[i] });
        });
    });

    return {
        training: jsPsych.randomization.shuffle(trainingTrials),
        main:     jsPsych.randomization.shuffle(mainTrials)
    };
}

// ============================================================
// HELPER: build one trial screen (shared by training + main)
// ============================================================
function buildTrialScreen(trialData, labelText, totalLabel) {
    return {
        type: 'html-slider-response',
        stimulus: function() {
            var budgetBar = condition === 'elective-budget'
                ? '<div class="budget-bar" id="budget-display">Budget remaining: <strong>' + budget + ' units</strong></div>'
                : '';

            var aiSection = '';
            if (condition === 'always-available') {
                aiSection = '<div class="ai-recommendation">AI recommends: <strong>' + trialData.maze.m_r + '</strong></div>';
            } else {
                var canAfford = budget >= trialData.ai_price;
                var helpBtn = canAfford
                    ? '<button id="ai-help-btn" class="ai-help-btn" onclick="requestAIHelp()">Request AI Help (' + trialData.ai_price + ' units)</button>'
                    : '<p class="warning">AI help costs <strong>' + trialData.ai_price + ' units</strong> for this trial, but you only have <strong>' + budget + ' units</strong> remaining.</p>';
                aiSection = helpBtn +
                            '<div id="ai-recommendation" class="ai-recommendation" style="display:none">AI recommends: <strong>' + trialData.maze.m_r + '</strong></div>';
            }

            return [
                '<div class="maze-task-row">',
                '  <div class="maze-left">',
                '    <p class="trial-counter">' + labelText + ' of ' + totalLabel + '</p>',
                '    <img src="' + trialData.maze.maze + '" class="maze-img">',
                '    <p class="maze-question">' + trialData.maze.question + '</p>',
                '    <div class="answer-choices">',
                '      <label class="choice-label"><input type="radio" name="maze-answer" value="A" onchange="onAnswerSelected()"><span class="choice-letter">A</span></label>',
                '      <label class="choice-label"><input type="radio" name="maze-answer" value="B" onchange="onAnswerSelected()"><span class="choice-letter">B</span></label>',
                '      <label class="choice-label"><input type="radio" name="maze-answer" value="C" onchange="onAnswerSelected()"><span class="choice-letter">C</span></label>',
                '      <label class="choice-label"><input type="radio" name="maze-answer" value="D" onchange="onAnswerSelected()"><span class="choice-letter">D</span></label>',
                '    </div>',
                '  </div>',
                '  <div class="maze-right">',
                '    ' + budgetBar,
                aiSection,
                '    <p class="confidence-question">How confident are you in your answer?</p>',
                '  </div>',
                '</div>'
            ].join('');
        },
        labels: ['1<br><small>Not at all</small>', '2', '3', '4', '5', '6', '7<br><small>Extremely</small>'],
        min: 1,
        max: 7,
        step: 1,
        slider_start: 1,
        require_movement: false,
        button_label: 'Submit',
        on_start: function() {
            _currentAIPrice       = trialData.ai_price;
            _currentAIAnswer      = trialData.maze.m_r;
            _aiPurchasedThisTrial = false;
            _selectedAnswer       = null;
            _sliderMoved          = false;
        },
        on_load: function() {
            var submitBtn = document.getElementById('jspsych-html-slider-response-next');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.classList.add('btn-disabled');
            }

            var sliderElm = document.getElementById('jspsych-html-slider-response-response');
            if (sliderElm) {
                var moveHandler = function() {
                    _sliderMoved = true;
                    updateSubmitState();
                };
                sliderElm.addEventListener('input', moveHandler);
                sliderElm.addEventListener('change', moveHandler);
                sliderElm.addEventListener('click', moveHandler);
            }

            var rightPane = document.querySelector('.maze-right');
            var sliderContainer = document.querySelector('.jspsych-html-slider-response-container');
            var responseButton = document.getElementById('jspsych-html-slider-response-next');
            if (rightPane && sliderContainer) rightPane.appendChild(sliderContainer);
            if (rightPane && responseButton)  rightPane.appendChild(responseButton);
        }
    };
}

// ============================================================
// TIMELINE BUILDER
// ============================================================
function buildTimeline() {
    var timeline   = [];
    var totalMain  = MAIN_PER_DIFF * 3;        // 36
    var totalTrain = TRAINING_PER_DIFF * 3;    // 6

    // ----------------------------------------------------------
    // 0. CONSENT FORM
    // ----------------------------------------------------------
    timeline.push({
        type: 'survey-html-form',
        preamble: '',
        html: [
            '<div class="screen-container" style="text-align:left; max-width:800px; margin:0 auto;">',
            '  <h1 style="text-align:center;">CONSENT FORM</h1>',
            '  <div style="height:32px;"></div>',
            '  <p style="font-size:20px; font-weight:600; margin-bottom:8px; margin-top:0;">Participant Information Sheet</p>',
            '  <p>Before you decide to take part in this study, it is important for you to understand why the research is being conducted and what it will involve. Please take time to read the following information carefully. If anything is unclear or if you would like more information, you may contact the researcher. Please take time to decide whether or not you wish to take part.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">Purpose of the study</p>',
            '  <p>The purpose of this study is to investigate how access to AI assistance can be structured in decision-making tasks. Instead of making AI assistance continuously available, the study models AI as a limited resource by assigning a cost to its use and giving participants a fixed budget. The goal is to examine how these resource constraints influence when people choose to request AI assistance and how this shapes reliance on AI.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">Do I have to take part?</p>',
            '  <p>No. Taking part in this study is entirely voluntary. If you choose not to take part, or if you decide to withdraw at any time, there will be no penalty or loss to you now or in the future. You may withdraw at any time by closing your browser tab.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">What do I have to do?</p>',
            '  <p>If you decide to take part, you will complete the study online. You will be asked to solve a series of maze tasks of varying difficulty. On each task, you will decide whether to solve the problem independently or to request assistance from an AI system at a given cost, subject to a fixed budget.</p>',
            '  <p>If you request assistance, the AI will provide a suggested answer. The AI system used in this study is simulated and may occasionally provide incorrect suggestions.</p>',
            '  <p>The study includes a short training phase followed by the main task and is expected to take approximately 30 minutes to complete. You will be given detailed instructions before the task begins.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">Will my taking part in this project be kept confidential?</p>',
            '  <p>Yes. Your responses will be recorded using an anonymised participant ID and will not be linked to your personal identity. We will only collect task-related data (such as responses, decisions, and response times). No personally identifiable information will be collected.</p>',
            '  <p>For more general information about how the University uses personal data, please see: <a href="https://www.information-compliance.admin.cam.ac.uk/data-protection/research-participant-data" target="_blank">https://www.information-compliance.admin.cam.ac.uk/data-protection/research-participant-data</a></p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">What will happen to the results of the research project?</p>',
            '  <p>The results of this study will be analysed and may be presented at academic conferences or published in journals. Results will be reported in aggregate form, and no individual participant will be identifiable. The anonymised data may also be used in future related research.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">Ethical review of the study</p>',
            '  <p>This project has been approved by the Cambridge Institute for Technology and Humanity Ethics Committee.</p>',

            '  <p style="font-size:18px; font-weight:600; margin-top:20px; margin-bottom:4px; color:#2b3952;">Contact for further information</p>',
            '  <p>If you have any questions about the study or your participation, please contact: Elaf Almahmoud (<a href="mailto:ea685@cam.ac.uk">ea685@cam.ac.uk</a>)</p>',

            '  <div style="margin-top:32px; padding:16px; border:2px solid #2e436b; border-radius:8px; background-color:#e8f0ff;">',
            '    <label style="display:flex; align-items:flex-start; gap:12px; cursor:pointer; font-size:17px; font-weight:500; color:#2b3952;">',
            '      <input type="checkbox" name="consent" value="yes" required style="margin-top:3px; transform:scale(1.4); flex-shrink:0;">',
            '      <span>I have read and understood the information above and consent to participate in this study.</span>',
            '    </label>',
            '  </div>',
            '</div>'
        ].join(''),
        button_label: 'Continue',
        on_load: function() {
            // Disable Continue until checkbox is checked
            var btn = document.getElementById('jspsych-survey-html-form-next');
            var checkbox = document.querySelector('input[name="consent"]');
            if (btn && checkbox) {
                btn.disabled = true;
                btn.style.opacity = '0.5';
                btn.style.cursor = 'not-allowed';
                checkbox.addEventListener('change', function() {
                    btn.disabled = !checkbox.checked;
                    btn.style.opacity = checkbox.checked ? '1' : '0.5';
                    btn.style.cursor = checkbox.checked ? 'pointer' : 'not-allowed';
                });
            }
        }
    });

    // ----------------------------------------------------------
    // 1. WELCOME
    // ----------------------------------------------------------
    timeline.push({
        type: 'html-button-response',
        stimulus: [
            '<div class="screen-container">',
            '  <h1>Welcome</h1>',
            '  <p>In this study, you will solve a series of maze puzzles.</p>',
            '  <p>For each maze, your task is to answer:</p>',
            '  <p class="highlight-box">Which exit (A, B, C, or D) can be reached from the start?</p>',
            '  <p>Click <strong>Continue</strong> to read the instructions.</p>',
            '</div>'
        ].join(''),
        choices: ['Continue']
    });

    // ----------------------------------------------------------
    // 2. INSTRUCTIONS
    // ----------------------------------------------------------
    var instructionsHTML;
    if (condition === 'always-available') {
        instructionsHTML = [
            '<div class="screen-container">',
            '  <h2>Instructions</h2>',
            '  <p>You will first complete <strong>' + totalTrain + ' training trials</strong> to familiarise yourself with the task.</p>',
            '  <p>Then you will solve <strong>' + totalMain + ' maze puzzles</strong>.</p>',
            '  <p>Mazes vary in difficulty: <strong>easy</strong>, <strong>medium</strong>, and <strong>hard</strong>.</p>',
            '  <p>For each maze, an AI system will show you its <strong>recommended answer</strong>.</p>',
            '  <p>The AI is correct approximately <strong>95% of the time</strong>.</p>',
            '  <p>You can use the AI\'s recommendation or ignore it. The choice is yours.</p>',
            '  <p>You will earn <strong>+' + CORRECT_BONUS + ' units</strong> added to your budget for each correct answer.</p>',
            '  <p>After each answer, rate <strong>how confident</strong> you are on a 1–7 scale.</p>',
            '</div>'
        ].join('');
    } else {
        instructionsHTML = [
            '<div class="screen-container">',
            '  <h2>Instructions</h2>',
            '  <p>You will first complete <strong>' + totalTrain + ' training trials</strong> to familiarise yourself with the task.</p>',
            '  <p>Then you will solve <strong>' + totalMain + ' maze puzzles</strong>.</p>',
            '  <p>Mazes vary in difficulty: <strong>easy</strong>, <strong>medium</strong>, and <strong>hard</strong>.</p>',
            '  <p>During training, you have a practice budget of <strong>' + TRAINING_BUDGET + ' units</strong>.</p>',
            '  <p>Your budget will be <strong>reset to ' + STARTING_BUDGET + ' units</strong> at the start of the main experiment.</p>',
            '  <p>Before each maze, you may choose to <strong>purchase AI assistance</strong>.',
            '     If you do, you will see the AI\'s recommended answer for that maze.</p>',
            '  <p>The AI is correct approximately <strong>95% of the time</strong>.</p>',
            '  <p>Each trial has a cost for AI help. You decide whether it is worth spending your budget.</p>',
            '  <p>You will earn <strong>+' + CORRECT_BONUS + ' units</strong> added to your budget for each correct answer.</p>',
            '  <p>After each answer, rate <strong>how confident</strong> you are on a 1–7 scale.</p>',
            '</div>'
        ].join('');
    }

    timeline.push({
        type: 'html-button-response',
        stimulus: instructionsHTML,
        choices: ['Start Training']
    });

    // ----------------------------------------------------------
    // 3. TRAINING TRIALS (6 trials, no feedback)
    // ----------------------------------------------------------
    var allTrials  = selectTrials();
    var trainTrials = allTrials.training;
    var mainTrials  = allTrials.main;

    trainTrials.forEach(function(trialData, idx) {
        var trainingTrialNum = idx + 1;
        var screen = buildTrialScreen(
            trialData,
            'Training Trial ' + trainingTrialNum,
            totalTrain
        );
        screen.on_finish = function(data) {
            var correct = (_selectedAnswer === trialData.maze.c_r);
            if (correct) budget += CORRECT_BONUS;
            data.trial_type_custom = 'training_trial';
        };
        timeline.push(screen);
    });

    // ----------------------------------------------------------
    // 4. TRANSITION TO MAIN TRIALS — reset budget to full
    // ----------------------------------------------------------
    timeline.push({
        type: 'html-button-response',
        stimulus: function() {
            // Reset budget here so it's full regardless of training spend
            budget = STARTING_BUDGET;
            var budgetNote = condition === 'elective-budget'
                ? '<p>Your budget has been reset to <strong>' + STARTING_BUDGET + ' units</strong> for the main experiment.</p>'
                : '';
            return [
                '<div class="screen-container">',
                '  <h2>Training Complete</h2>',
                '  <p>You are now ready for the main experiment.</p>',
                '  <p>You will solve <strong>' + totalMain + '</strong> maze puzzles.</p>',
                budgetNote,
                '  <p>As in training, there will be no feedback after each trial.</p>',
                '</div>'
            ].join('');
        },
        choices: ['Begin']
    });

    // ----------------------------------------------------------
    // 5. MAIN TRIALS (24 trials, no feedback)
    // ----------------------------------------------------------
    var mainStartTime = null;

    // Record wall-clock start time when the first main trial begins
    timeline.push({
        type: 'call-function',
        func: function() { mainStartTime = Date.now(); }
    });

    mainTrials.forEach(function(trialData, idx) {
        var thisTrialNum = idx + 1;
        var participant_answer = null;
        var is_correct = false;

        var screen = buildTrialScreen(
            trialData,
            'Trial ' + thisTrialNum,
            totalMain
        );
        screen.on_finish = function(data) {
            participant_answer = _selectedAnswer;
            is_correct = (participant_answer === trialData.maze.c_r);
            if (is_correct) budget += CORRECT_BONUS;

            data.trial_type_custom  = 'maze_trial';
            data.subject_id         = subject_id;
            data.trial_number       = thisTrialNum;
            data.condition          = condition;
            data.difficulty         = trialData.difficulty;
            data.maze_id            = trialData.maze.id;
            data.ai_purchased       = condition === 'elective-budget' ? _aiPurchasedThisTrial : 'N/A';
            // Reconstruct budget at trial start (before AI deduction and before bonus)
            var budgetAtTrialStart = budget
                + (_aiPurchasedThisTrial ? trialData.ai_price : 0)
                - (is_correct ? CORRECT_BONUS : 0);
            data.ai_affordable      = condition === 'elective-budget' ? (budgetAtTrialStart >= trialData.ai_price) : 'N/A';
            data.budget_after       = budget;
            data.participant_answer = participant_answer;
            data.correct_answer     = trialData.maze.c_r;
            data.ai_answer          = trialData.maze.m_r;
            data.ai_was_correct     = (trialData.maze.m_r === trialData.maze.c_r);
            data.is_correct         = is_correct;
            data.followed_ai        = (participant_answer === trialData.maze.m_r);
            data.confidence         = data.response;
        };
        timeline.push(screen);
    });

    // ----------------------------------------------------------
    // 6. END SCREEN
    // ----------------------------------------------------------
    timeline.push({
        type: 'html-button-response',
        stimulus: function() {
            var mainElapsedMs = Date.now() - mainStartTime;
            var mainElapsedSec = Math.round(mainElapsedMs / 1000);

            // Save total main-task duration into jsPsych data
            jsPsych.data.addProperties({
                main_task_duration_ms:  mainElapsedMs,
                main_task_duration_sec: mainElapsedSec
            });

            var mazeTrials = jsPsych.data.get().filter({ trial_type_custom: 'maze_trial' }).values();
            var n_correct  = mazeTrials.filter(function(t) { return t.is_correct; }).length;
            var budgetHTML = condition === 'elective-budget'
                ? '<p>Budget remaining: <strong>' + budget + ' units</strong></p>'
                : '';
            return [
                '<div class="screen-container">',
                '  <h2>Thank you!</h2>',
                '  <p>You completed all <strong>' + mazeTrials.length + '</strong> maze puzzles.</p>',
                '  <p>You answered <strong>' + n_correct + '</strong> out of <strong>' + mazeTrials.length + '</strong> correctly.</p>',
                budgetHTML,
                '  <p>Please let the researcher know you are done.</p>',
                '</div>'
            ].join('');
        },
        choices: ['Finish']
    });

    return timeline;
}

// ============================================================
// START
// ============================================================
jsPsych.init({
    timeline: buildTimeline(),
    on_finish: function() {
        jsPsych.data.get().filter({ trial_type_custom: 'maze_trial' }).localSave('csv',
            'maze_' + condition + '_' + subject_id + '_' + Date.now() + '.csv'
        );
    }
});
