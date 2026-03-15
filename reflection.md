# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

---

When I first ran the game, the hints were backward — guessing too high told you to go higher, and guessing too low told you to go lower. The score never reset when starting a new game, so it carried over between rounds. The submit button had to be clicked twice after changing a guess, which turned out to be the state bug — the text input wasn't persisting its value across reruns.



## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---
I used Claude Code. I asked it in natural language if the sections or behavior I was seeing were valid, were the state bug, etc. I let it do the refactor to logic_utils.py without checking it much since I thought that would be straightforward, and it did well — I verified it by running pytest and all tests passed. The most obvious one was when we fixed a bug (hint display) but it didn't solve all of the behavior I expected (was still disappearing because there was also a state bug). It wasn't wrong per se, but I hadn't been complete in my description of the problem and it didn't assume what it should have looked like. 

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---
To determine if something was fixed, I first ran the app to see if what I expected was happening.  Once I had technically fixed the bug I was after (higher/lower) but I then noticed a second state bug we hadn't fixed yet.  I had Claude create a test for the fix we did, pushed that to main, and then created a new fix branch for the next bug. Some of the tests were hard to understand because it was using Streamlit to simulate user interaction, but you can't see it. Creating one test found yet another state bug because the test failed, which was also good. 

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

I never actually saw the secret number change bug — it had been fixed by the instructor before I forked it. Looking at the original code in git history, the bug was caused by generating the secret with a plain variable (`secret = random.randint(1, 100)`) instead of session state, so it got a new random number on every rerun. The fix was wrapping it in `if "secret" not in st.session_state`, so it only generates once per session. I did find other state bugs though. I think I would describe it as Streamlit reruns the entire script on every interaction, so regular Python variables reset each time. st.session_state is how you tell Streamlit to remember a value between reruns — like a notepad that survives each rerun for the duration of the browser session. The state bugs (broken reset, score not resetting, double-submit, hint disappearing after rerun) were all fixed using st.session_state. The backward hints were a separate issue — just wrong strings in the code, not a state problem.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

---
This is the first time I've consistently used AI for testing.  It was nice, although it took me into tests that I don't fully understand if it just passes or if it passes the intent of the test. I think Claude knows a lot more about coding than I do, but it's set to help me understand.  While this slows the project down, I can definitely do more and more quickly because I have AI tutoring me. 