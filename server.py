You are an expert Python Flask developer and code maintenance engineer.

I have an EXISTING working BDG Win Go 1-Minute Smart AI Analyzer project.

YOUR TASK IS TO MAKE A SMALL, TARGETED CODE MODIFICATION.

CRITICAL: DO NOT REBUILD THE PROJECT. DO NOT REWRITE THE ENTIRE FILE.

1. PRESERVE THE ORIGINAL PROJECT

Keep the existing code and functionality unchanged wherever possible.

Do not modify:

- Existing HTML design.
- Existing CSS.
- Existing game URL.
- Existing iframe.
- Existing floating scanner panel.
- Existing panel controls.
- Existing Flask routes.
- Existing Render configuration.
- Existing one-minute timer.
- Existing automatic Period ID synchronization.

2. FIX THE ANALYSIS SOURCE

Inspect the existing analysis function.

The current code uses Period ID digits and a mathematical formula to calculate a number.

Do not use Period ID digits as result data.

Period ID must only identify and match the correct historical record.

3. HISTORICAL DATA MODULE

Make a separate module that analyzes actual historical result records already available to the application.

Use the available historical records to calculate:

- Frequency of each result number.
- Number distribution.
- Historical repetitions.
- Consecutive result sequences.
- Color frequency.
- Big and Small frequency.
- Short-term and long-term statistics.

Use up to 20-50 historical pages only when they are genuinely accessible from the existing data source.

Do not fabricate historical results.

Do not assume that a Period ID is a result number.

4. SAFE INTEGRATION

Do not delete existing working functions unnecessarily.

Keep the existing timer and automatic Period ID system.

Connect the historical statistics module to the existing panel using the existing HTML element IDs wherever possible.

Do not change the visual layout.

5. TEST BEFORE SAVING

Before modifying the file:

- Create a backup of the original server.py.
- Inspect the complete source code.
- Identify the exact function that needs modification.

After modifying:

- Run Python syntax validation.
- Check Flask startup.
- Check HTML and JavaScript syntax.
- Verify that existing functions still work.

6. STRICT OUTPUT RULE

IMPORTANT:
Do not paste this prompt into server.py.

This is an instruction for editing the existing source code, NOT executable Python code.

Return:

1. A short explanation of the exact lines changed.
2. A minimal code patch or diff.
3. The complete corrected file only if necessary.
4. Confirmation that syntax validation passed.

Never replace the complete working project with a new demo or unrelated implementation.
