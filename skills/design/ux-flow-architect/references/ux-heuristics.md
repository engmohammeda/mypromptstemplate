# Usability heuristics — reference

## Nielsen's 10, with concrete mobile checks

### 1. Visibility of system status
- [ ] Every action gives feedback within 100ms (press state) and 400ms (result or progress).
- [ ] Long operations show determinate progress when the total is known.
- [ ] Sync/offline state is visible without the user hunting for it.
- [ ] Destructive/async results are confirmed (snackbar with Undo).

### 2. Match between system and the real world
- [ ] Labels use the user's vocabulary, not internal jargon ("Saved", not "Cached entity").
- [ ] Ordering follows real-world logic (dates newest-first, sizes S→XL).
- [ ] Icons use conventional meanings; ambiguous icons always carry a text label.

### 3. User control and freedom
- [ ] Every screen has a clear, obvious exit; back always does the expected thing.
- [ ] Destructive actions are undoable (5–10s Undo) rather than confirmed.
- [ ] Long processes can be cancelled; partially entered data is preserved.
- [ ] No dead-ends: every error state offers a way forward.

### 4. Consistency and standards
- [ ] Same word for the same concept everywhere ("Delete" vs "Remove" — choose one).
- [ ] Platform conventions respected (back gesture, share sheet, date pickers).
- [ ] Component behaviour identical across screens.

### 5. Error prevention
- [ ] Constrain input instead of validating after the fact (pickers, masks, keyboards by type).
- [ ] Disable or hide impossible actions, and explain why when disabled.
- [ ] Confirm only genuinely destructive, irreversible actions — and name what will be lost.
- [ ] Guard against double submission.

### 6. Recognition rather than recall
- [ ] Options are visible; the user never memorises a code or a previous screen's value.
- [ ] Search shows recent queries and suggestions.
- [ ] Forms show the entered data when confirming.

### 7. Flexibility and efficiency of use
- [ ] Shortcuts for repeat users (swipe actions, long-press menus, defaults from history).
- [ ] Sensible defaults so the common case needs zero input.
- [ ] Bulk actions where users act repeatedly.

### 8. Aesthetic and minimalist design
- [ ] Each screen contains only what serves its single primary job.
- [ ] Secondary information is progressively disclosed.
- [ ] No decorative content competing with the primary action.

### 9. Help users recognise, diagnose and recover from errors
- [ ] Error text: what happened + why + exactly what to do next.
- [ ] Errors appear next to the offending field, not only at the top.
- [ ] No error codes without human language (a code may be appended for support).
- [ ] Never blame the user ("Invalid input" → "Enter a date after today").

### 10. Help and documentation
- [ ] Contextual help where the confusion happens, not in a separate manual.
- [ ] Empty states teach the feature.
- [ ] A findable support path for the 1% who are stuck.

## Severity scale (rate every finding)

| Rating | Meaning | Action |
|---|---|---|
| 0 | Not a problem | ignore |
| 1 | Cosmetic | fix if time allows |
| 2 | Minor — annoyance, workaround exists | backlog |
| 3 | Major — users fail or take a long detour | fix before release |
| 4 | Catastrophic — task cannot be completed, data loss, or legal/accessibility failure | block release |

Score = frequency × impact × persistence. Fix all 3s and 4s.

## Additional mobile-specific heuristics
- **One-handed reachability**: primary actions in the bottom third.
- **Interruption tolerance**: state survives a phone call, app switch, and process death.
- **Connectivity tolerance**: everything works offline or degrades explicitly.
- **Battery/data awareness**: no autoplay video on cellular by default; heavy downloads ask first.
- **Notification hygiene**: every notification is actionable, categorised into channels the user can control, and never used for marketing without opt-in.
- **Permission timing**: request at the moment of need with a rationale; handle "denied forever".
- **Input economy**: right keyboard type, autofill hints, no forced re-entry of what the system knows.

## Running an evaluation
1. Pick 3–5 core tasks.
2. Walk each task screen by screen, alone, listing violations with heuristic number + severity + screenshot.
3. Repeat as a second pass focused on error paths and edge data (empty, huge, long names, RTL).
4. Consolidate duplicates, sort by severity, assign owners.
5. Re-evaluate after fixes; track the count over releases.

5 evaluators find ~75% of issues; 1 evaluator finds ~35%. If you are alone, do two passes on
different days and complement with 5 real users — usability testing with 5 users surfaces the
majority of major problems.

## Quick usability test script (unmoderated, 20 minutes)
```
1. "Without tapping, tell me what this app does and who it's for." (5s first impression)
2. "Complete <core task>." — observe, do not help. Note every hesitation > 3s.
3. "You made a mistake — undo it."
4. "You lost connection. Try again." (airplane mode)
5. "Find <secondary feature>." — measure time and wrong turns.
6. Post: "What was confusing? What would you tell a friend this app does?"
```
Metrics: task completion rate, time on task, error count, SUS score (target > 68, good > 80).
