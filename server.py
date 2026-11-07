Act as a senior Python Flask developer and software debugging engineer.

I have an existing BDG Win Go 1-Minute Smart AI Analyzer project deployed on Render.

IMPORTANT: First inspect the complete existing server.py file before modifying anything.

TASK: Fix the deployment error and replace the incorrect Period-ID-based mathematical analysis with genuine historical result data analysis.

SECTION 1 - FIX THE RENDER ERROR

The current Render log shows:

SyntaxError: invalid character '–' (U+2013)

Find and fix the exact syntax error.

Rules:

- Never insert plain English instructions into executable Python code.
- Every Python comment must start with #.
- Every text value must be inside valid quotation marks.
- Replace accidental Unicode dash characters with standard ASCII hyphens where appropriate.
- Check indentation and Python syntax.
- Do not leave Markdown headings or prompt instructions inside server.py.
- Run a Python syntax validation before deployment.
- Ensure the application starts successfully using the existing Flask configuration.

SECTION 2 - PRESERVE THE EXISTING PROJECT

Do not redesign or rebuild the project.

Keep all existing working components unchanged:

- Existing HTML layout.
- Existing CSS and visual design.
- Existing floating scanner panel.
- Existing game iframe configuration.
- Existing panel controls.
- Existing Period ID display.
- Existing one-minute countdown timer.
- Existing Flask routes.
- Existing Render deployment configuration.

Modify only the analysis logic and the minimum supporting functions required.

SECTION 3 - REMOVE PERIOD-BASED NUMBER CALCULATION

Inspect the existing runSmartPredictionEngine(targetPeriod) logic.

Remove any mathematical formula that calculates a result number from Period ID digits.

Period ID must only be used for:

- Identifying a record.
- Matching a result to its correct period.
- Detecting missing or duplicate records.
- Synchronizing the timer.

Never use Period ID digits as historical result data.

SECTION 4 - HISTORICAL DATA ANALYSIS ENGINE

Build a separate historical statistics module.

Read actual historical game results whenever a legitimate data source makes them available.

Support processing 20 to 50 pages of historical records when accessible.

Store and validate:

- Period ID.
- Actual result number.
- Actual result color.
- Actual Big or Small category.
- Timestamp.

Analyze:

- Frequency of each result number from 0 to 9.
- Historical number distribution.
- Repeated number sequences.
- Consecutive result patterns.
- Color frequency.
- Big and Small frequency.
- Short-term and long-term distributions.
- Missing records.
- Duplicate records.
- Incorrect period matching.

Do not invent records or fabricate results.

SECTION 5 - AUTOMATIC SYNCHRONIZATION

Keep the existing one-minute automatic Period ID and countdown timer.

Automatically:

- Detect the current period.
- Match incoming historical results with their correct Period ID.
- Update the historical record collection when new actual results become available.
- Prevent duplicate records.
- Report synchronization errors.
- Maintain correct timestamps.

SECTION 6 - STATISTICAL VALIDATION

Use chronological walk-forward backtesting.

At each test point, use only historical records available before that point.

Display actual historical statistics and measured backtesting performance.

Never fabricate accuracy percentages or claim guaranteed outcomes.

SECTION 7 - FINAL TESTING

Before returning the updated project:

1. Validate server.py syntax.
2. Check every Python function.
3. Check Flask route configuration.
4. Check HTML and JavaScript syntax.
5. Verify existing element IDs are preserved.
6. Verify the timer and Period ID display still work.
7. Verify the floating panel still works.
8. Verify the application starts without SyntaxError.
9. Return the complete corrected server.py and any required supporting files.

Do not return partial code.

Do not replace working components unnecessarily.

MOST IMPORTANT: Historical result data must be the source of statistical analysis. Period ID must never be used to calculate a result number.
