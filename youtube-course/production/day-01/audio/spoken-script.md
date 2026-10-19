# Day 1 — Run Your First Python File

**Language:** English, confirmed. **Draft voice:** clear and encouraging; creator voice samples pending. This script focuses on setup and first execution. The complete Day 1 reference remains in the HTML lab.

**Title:** Run Your First Python File | Day 1  
**Thumbnail:** IT RUNS  
**Packaging score:** 100/100 from the installed title linter; not a performance prediction.

The two scored opening options and their five-property panels are in [the Day 1 brief](episodes/day-01.md). This draft uses the more specific question hook, even though it scores below the generic warning: matching the actual demo matters more than maximizing the heuristic.

Read only the blockquoted paragraphs as narration. Code and bracketed directions are production instructions. The measured word count and 150-words-per-minute estimate are in [pilot-metrics.json](scores/pilot-metrics.json). Allow additional time for installation, typing, and learner pauses; aim for an 8–12 minute edited pilot, then measure the recorded runtime.

## 1. Hook — show the puzzle

[ON SCREEN: split view. Python shell shows `10 + 20` and `30`; a saved file containing only `10 + 20` runs without printing anything.]

> Why does your Python file show nothing when the shell shows 30? Both contain the same calculation. By the end of this lesson, you will understand the difference and run your own saved Python program.

[ON SCREEN: add `print(10 + 20)` to the file; run it and show `30` immediately. Reveal the result early; explain the mechanism later.]

## 2. Turn — one concrete destination

[ON SCREEN: `hello.py` prints a greeting and a calculation. Briefly show the course mind-map branch: setup → shell → file.]

> This is what we are building: a small file that prints a greeting and an answer. We need Python, somewhere to write our code, and a way to run it. We will check each one, then deliberately break a line so you can see how to fix it.

## 3. What Python does

[ON SCREEN: three labels—automation, data, web—then return to the working file.]

> Python is a programming language. You write instructions, and a Python interpreter executes them. People use Python for automation, data analysis, web applications, and AI tools. Those are different destinations, but they share the same starting point: writing a small instruction and understanding its result.

> You do not need to choose a career path today. Our goal is smaller and testable: can you run a file, change it, and explain what changed? That is the first step this course asks you to take.

## 4. Verify your interpreter

[ON SCREEN: terminal, clearly labeled TERMINAL. Record the current official Python installation flow on the actual recording machine; installer screens can differ.]

> Open a terminal and check whether Python is already installed. On this machine, I am using the command shown here. Look for a Python 3 version in the result. On another computer, the command may be python3 or py instead. Use the command that actually works on your machine throughout the lesson.

```text
python --version
```

> If none of those commands starts Python, open python.org and follow the installation instructions for your operating system. After installation, open a new terminal and check the version again. Do not copy an old version number from a screenshot. The important thing is that your interpreter is installed and you know how to start it.

[ON SCREEN: successful version check. Edit out download waits. Provide platform-specific setup details in the lab rather than reading three complete installation flows aloud.]

## 5. Know which prompt you are using

[ON SCREEN: type `python`; highlight the `>>>` prompt.]

> Now start Python. See these three greater-than signs? They tell you that you are inside the Python interactive shell. This is different from the terminal prompt we used a moment ago. The terminal starts programs. The Python shell accepts Python code.

> Here is a useful check when something seems wrong: look at the prompt before changing your code. If you see three greater-than signs, you are inside Python. To run a terminal command such as python hello.py, first leave this shell with exit(). Then run the command at the terminal prompt.

[ON SCREEN: show shell → `exit()` → terminal → shell again. Keep both prompt labels visible.]

## 6. First expressions and quoted text

[ON SCREEN: enter one expression at a time and wait for the result.]

```python
10 + 20
10 - 3
4 * 5
print("Hello, Python!")
```

> Type ten plus twenty and press Enter. The shell displays thirty. Try subtraction and multiplication too. Before pressing Enter, predict the answer. That habit will help you notice when your code does something different from what you intended.

> Now try a greeting. The words are inside quotation marks because they are text. The parentheses contain the value we give to print. Run the line, change the greeting, and run it again. You are already changing a program and checking the result.

## 7. Break one line and recover

[ON SCREEN: deliberately enter `print("Hello, Python!"` without its final parenthesis. Label this BROKEN EXAMPLE.]

> This time I have left out the closing parenthesis. Depending on how you entered the line, the interactive shell may wait for more input, or Python may report a syntax error when the incomplete statement is submitted. In a saved file, the missing parenthesis prevents the file from running normally.

> A syntax error does not mean you cannot program. It means Python could not read the instruction in its current form. Compare the opening and closing punctuation, add the missing parenthesis, and run the corrected line. Change one thing, then check again.

[ON SCREEN: correct the example; show successful output. Cancel an unfinished interactive input if necessary before continuing.]

## 8. Save and run a file

[ON SCREEN: official code.visualstudio.com download page, then VS Code Extensions showing Python by Microsoft. Capture installation on the recording machine; cut download waits.]

> We will use Visual Studio Code as our editor. If you do not have it yet, download it from code.visualstudio.com and install the version for your operating system. Open its Extensions panel, search for Python, and install the Python extension published by Microsoft. The editor helps us write code; the Python interpreter we installed earlier is what runs it.

[ON SCREEN: VS Code, opened folder `python-30-days`, new file `hello.py`. Show the Python extension and selected interpreter briefly.]

> The shell is useful for quick experiments. A file lets us keep several instructions and run them again. Open a folder in your editor, create a file called hello.py, and save these lines. In VS Code, select the Python interpreter you verified earlier so the editor uses the same installation.

```python
print("Hello, Python!")
print(10 + 20)
```

> Open a terminal in the folder containing the file. Leave the Python shell first if you are still inside it. Now run python hello.py, using your working Python command. You should see the greeting and then thirty. Change the greeting, save the file, and run the same command again.

```text
python hello.py
```

> If Python says it cannot open the file, check the filename and your terminal's current folder. If you still see the old greeting, check whether you saved the change and whether you are running the same file you edited. These checks are often more useful than immediately reinstalling anything.

## 9. Resolve the opening puzzle

[ON SCREEN: compare shell evaluation with a file containing `10 + 20`, then add `print(...)`.]

> Here is why our first two examples looked different. In the interactive shell, Python normally displays the result of an expression for you. In a saved script, writing an expression by itself does not ask Python to display it. The calculation still happens, but there is no printed output. Use print when your script needs to show the result.

> We have now delivered the opening promise: you can run a saved Python file and explain why it prints something, or why it stays quiet. The shell helps you experiment; the file keeps the instructions you want to repeat.

## 10. Preview types and comments

[ON SCREEN: inspect a number, decimal, text, and Boolean. Show the larger type map as a preview, not a requirement to memorize.]

```python
# Inspect the kinds of values Python is working with.
print(type(30))
print(type(3.5))
print(type("Python"))
print(type(True))
```

> Python works with different kinds of values. These examples are an integer, a floating-point number, a string, and a Boolean. The type function tells us which kind we have. You do not need every detail yet. Just notice that a number and text containing digits are not the same kind of value.

> The line beginning with a hash is a comment. It explains the code to a reader without becoming an instruction to execute. The lab also previews lists, tuples, sets, and dictionaries. We will work with each of those in its own lesson. Later, indentation will matter when we group instructions into blocks.

## 11. Challenge — one request

[ON SCREEN: challenge card beside the HTML Day 1 exercises; keep the complete solution hidden.]

> Your challenge is to make a new file that prints your name, prints the result of ten plus twenty, and displays the types of thirty, three point five, and the word Python. Run it from the terminal and change one line successfully. Pause here and try it yourself before opening the lab solution.

## Recording notes

- Keep the selected interpreter, folder, filename, and prompt visible whenever they explain a problem.
- Record the working output first; it becomes the opening proof shot.
- Keep the deliberate error and its repair in the same visual context.
- Use the current install flow. The source HTML includes historical version screenshots and older installation wording.
- The script makes no certificate, job, or mastery promise. The HTML's certificate and group references need owner confirmation before being used in promotional copy.
- Final chapter timestamps and Shorts boundaries must come from the actual edited recording.

```text
Record: working result → shell/file contrast → setup → first code → repair → saved file → challenge.
```

ship it, or change it?
