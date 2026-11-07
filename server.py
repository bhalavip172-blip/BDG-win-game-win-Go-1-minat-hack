
Act as a Senior Python Flask Developer, Historical Data Analyst, and Software Engineer.

I have an existing BDG Win Go 1-Minute Smart AI Analyzer project. Your task is to modify ONLY its existing analysis engine.

1. STRICT PRESERVATION RULE

Keep the complete existing project exactly as it is.

DO NOT change:

- Existing BDG Win game URL.
- Existing game iframe.
- HTML page layout.
- CSS styling, colors, gradients, and animations.
- Floating scanner panel.
- Panel position, size, and draggable behavior.
- Minimize and toggle buttons.
- Existing Flask server configuration.
- Render deployment configuration.
- Existing Auto Period ID system.
- Existing 1-minute countdown timer.
- Existing responsive mobile design.

Do not rebuild the project from scratch.

Do not remove existing working features.

2. REPLACE THE INCORRECT ANALYSIS LOGIC

Inspect the existing function named:

runSmartPredictionEngine(targetPeriod)

The current implementation calculates a number using the Period ID digits and a mathematical formula.

Replace this Period-ID-based result calculation with a genuine historical-data analysis module.

IMPORTANT:
Period ID must ONLY identify and synchronize records. It must NEVER be used as a mathematical source for calculating a game result.

3. HISTORICAL DATA ANALYSIS

Analyze all genuinely available historical game records.

Support retrieving and processing 20–50 pages of historical records when the source makes them accessible.

For every record, maintain:

- Period ID
- Actual result number
- Actual color
- Actual Big/Small category
- Timestamp

Analyze:

- Number frequency from 0 to 9.
- Historical number distribution.
- Repetition patterns.
- Consecutive result sequences.
- Color distribution.
- Big/Small distribution.
- Short-term and long-term statistical differences.
- Missing records.
- Duplicate records.
- Incorrect period-result matching.

Never invent missing historical results.

4. AUTOMATIC DATA SYNCHRONIZATION

Keep the existing one-minute period synchronization.

The system must:

- Detect the current Period ID.
- Match each historical result with its correct Period ID.
- Detect when a new period begins.
- Update historical records automatically when genuine data is available.
- Keep the countdown timer synchronized.
- Prevent duplicate records.
- Display synchronization errors clearly.

5. STATISTICAL VALIDATION

Implement genuine walk-forward backtesting.

Evaluate the analysis using only historical records that would have been available at each test point.

Display:

- Number of records analyzed.
- Historical frequency.
- Actual distribution.
- Backtesting results.
- Data quality.
- Model limitations.

Never display fabricated accuracy percentages.

6. FLOATING PANEL

Keep the existing floating panel design unchanged.

Update only its data values using the historical analysis module.

Display:

- Current Period ID.
- Countdown Timer.
- Historical Record Count.
- Last Actual Result.
- Number Frequency.
- Color Statistics.
- Big/Small Statistics.
- Historical Pattern Summary.
- Data Synchronization Status.
- Backtesting Performance.

7. CODE QUALITY

Preserve existing working code wherever possible.

Use the existing Flask architecture.

Avoid unnecessary dependencies.

Handle missing data and network errors safely.

Do not use random numbers or fabricated formulas.

8. FINAL REQUIREMENT

Before making changes, inspect the complete existing source code.

Modify ONLY the analysis engine and the minimum supporting data functions required.

Keep the existing game URL, iframe, floating panel, HTML design, timer, Period ID synchronization, and Render deployment unchanged.

Return the complete updated source code, not partial snippets.

Test the updated code for syntax errors and verify that existing features remain functional.
