# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

While testing the game, I noticed several bugs that affected the way the game displayed results and responded to player actions.

### Bugs Noticed

1. **Score display did not match the final score**
   - **Expected:** The game should display the player's actual final score.
   - **Actual:** The game displayed a score-related message that seemed incorrect or exaggerated, even though the final score was 85.

2. **New Game button did not work on desktop**
   - **Expected:** Clicking the **New Game** button should reset the game and start a new round.
   - **Actual:** On my desktop, clicking the **New Game** button did not appear to restart or reset the game.

3. **Guess count appeared inconsistent between testers**
   - **Expected:** The game should count guesses consistently for each player during a run.
   - **Actual:** While discussing the game with other testers in the breakout room, one tester appeared to receive one fewer guess during their run than expected.

### Bug Reproduction Log

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output |
| ---------- | ----------------- | --------------- | ---------------------- |
| Completed a game with a final score of 85 | The final score display should show 85 or feedback that matches that score | The game displayed score-related feedback that did not seem to match the final score | None observed |
| Clicked the **New Game** button after finishing a round on desktop | The game should reset and allow a new round to begin | The button did not appear to do anything and the game did not restart | None observed |
| Compared gameplay results with another tester in the breakout room | Each player should receive the correct number of guesses during a run | One tester appeared to receive one fewer guess than expected | None observed |

During the class demo, pytest was introduced as a way to automate testing of the game's logic. After refactoring the game functions into a separate module, I created and ran a pytest test suite containing 23 tests. The first run failed because the functions had not yet been implemented in the testing module. After moving the logic into the module, 17 tests passed and 6 tests failed, revealing several reproducible defects.

The pytest results identified the following issues:

- Hard difficulty used a smaller number range than Normal difficulty, making it easier rather than harder.
- A guess that was too high displayed the hint "Go HIGHER" instead of "Go LOWER."
- A guess that was too low displayed the hint "Go LOWER" instead of "Go HIGHER."
- Comparing integer guesses against string-based secret values produced incorrect comparison results.
- On certain attempts, incorrect guesses could increase the player's score instead of decreasing it.

Using pytest made it possible to verify game behavior quickly and consistently without manually repeating every gameplay scenario.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used AI as a coding assistant throughout the debugging and refactoring process. I asked it questions about the code, requested explanations of how specific functions worked, and used it to help identify potential causes of bugs. AI also helped generate pytest test cases, explain test failures, and suggest refactoring opportunities to separate the game logic from the Streamlit user interface.

### Example of a Correct AI Suggestion

The AI suggested that the hint messages inside the check_guess() function were reversed. When a player's guess was too high, the game instructed the player to "Go HIGHER," and when a guess was too low, the game instructed the player to "Go LOWER."

This suggestion was correct.

I verified the issue by:

1. Reviewing the code in the check_guess() function.
2. Running the pytest suite and observing the failing tests related to hint directions.
3. Running the game and confirming the incorrect hints appeared during gameplay.

After correcting the messages, the tests passed and the game behaved as expected.

### Example of an Incorrect or Misleading AI Suggestion

The AI initially identified the Hard difficulty range as a bug because Hard mode used a range of 1–50 while Normal mode used 1–100. While the test suite flagged this behavior, determining whether it was truly a bug required human judgment because difficulty settings are a design decision rather than a coding error.

I verified this by reviewing the game requirements and considering the intended gameplay. Rather than blindly accepting the AI's recommendation, I evaluated whether the change aligned with the game's design goals before making the modification.

This demonstrated that AI suggestions should be reviewed and validated rather than accepted automatically.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I verified my repairs using both automated and manual testing.

First, I created and executed pytest test cases to identify defects in the game's logic. The initial test suite revealed several issues involving hint messages, score calculations, difficulty settings, input validation, and type comparisons.

After refactoring the game logic into logic_utils.py and applying fixes, I reran the pytest suite to verify the changes. The tests confirmed that the repaired functions behaved as expected.

I also manually tested the game by launching the application with:

```bash
streamlit run app.py
```

During manual testing, I entered various valid and invalid guesses, verified score behavior, confirmed that hints pointed players in the correct direction, and ensured the game remained functional after the refactoring process.

Using both automated testing and manual gameplay helped confirm that the repairs worked correctly and did not introduce new issues.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit is what lets players play the game inside a web browser instead of from a terminal, which enhances the user experience. Every time a player submits a guess, the script is rerun behind the scenes — but on screen nothing feels interrupted, so the player stays in the experience. Session state is what makes this work: it holds onto important values like the secret number and the score across those reruns so they don't reset every time the page refreshes.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to carry forward is using AI to help write pytest test cases that cover different scenarios and edge cases. That way automated testing handles the heavy lifting, and manual testing can be reserved for quality control and the overall user experience.

Next time I work with AI on a coding task, I would review the changes it makes to the code more carefully before accepting them, rather than moving forward too quickly.

This project made me feel a lot more confident having AI as a co-pilot in coding. I have a much better sense of what it can do well and where my own judgment still needs to be in the loop.
