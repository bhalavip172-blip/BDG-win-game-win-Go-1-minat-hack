You are editing an existing Python Flask project.

PROJECT: BDG Win Go 1-Minute Smart AI Analyzer.

IMPORTANT: Make a minimal patch to the existing source code. Do not rebuild the project.

MY ONLY REQUEST:
Replace the existing Period-ID-based mathematical analysis with genuine historical result statistics.

STEP 1: INSPECT

- Read the complete existing server.py.
- Find the current analysis function.
- Identify exactly where Period ID digits are being used to calculate a result.
- Inspect how historical results are currently stored or retrieved.

STEP 2: PRESERVE EVERYTHING
Do not modify:

- Existing game URL or iframe.
- Existing HTML and CSS design.
- Floating scanner panel.
- Panel position, buttons, and controls.
- Flask routes.
- One-minute timer.
- Automatic Period ID synchronization.
- Render configuration.
- Existing working functions.

STEP 3: CHANGE ONLY THE ANALYSIS MODULE

- Stop using Period ID digits as a source for result calculations.
- Keep Period ID only for matching and identifying historical records.
- Use genuine historical result records as the source of statistical analysis.
- Analyze all genuinely available historical records, including up to 20-50 pages if the existing source supports them.
- Calculate historical number frequencies from 0 to 9.
- Analyze historical number distributions, repetitions, sequences, color frequencies, and Big/Small frequencies.
- Detect missing records and duplicate records.
- Keep historical statistics separate from Period ID synchronization.
- Do not invent or fabricate historical data.

STEP 4: SAFE CODE MODIFICATION

- Modify only the required existing function and its minimum supporting functions.
- Do not paste this instruction text into server.py.
- Do not insert Markdown headings into Python code.
- Do not replace the complete source file.
- Do not introduce unnecessary libraries.
- Keep the original code as a backup.
- Show the exact code diff before applying changes.

STEP 5: VALIDATION
Before saving:

- Run Python syntax validation.
- Check imports and indentation.
- Check Flask startup.
- Check existing HTML element IDs.
- Check JavaScript syntax.
- Verify that the original timer, panel, game iframe, and routes remain unchanged.

If the historical data source cannot be accessed, stop and report the exact missing dependency. Do not create fake data or pretend the analysis works.

FINAL OUTPUT:
Return only the minimal source-code patch, explain the changed lines, and report the validation results.

Do not commit or deploy code that fails syntax validation.
