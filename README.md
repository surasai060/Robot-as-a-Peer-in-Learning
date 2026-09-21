# 🤖 Robot Quiz – Peer vs Tutor Study

A simple web-based quiz to test if a robot that acts like a **study buddy** changes how people ask for help and how comfortable they feel, compared to a robot that acts like a **teacher**.

---

##  What's This About?

We built a quiz where a robot helps you answer 10 football questions.  
The robot can either be:

| Role | What it does |
|------|--------------|
| **Peer (Study Buddy)** | Friendly, says "we'll figure this out together". Removes a wrong option when you ask for help. Gives you a second chance if you get it wrong. |
| **Tutor (Teacher)** | Formal, gives you clues when you ask for help. No second chance. |

We wanted to see:
- Do people ask for help more with a peer robot?
- Do they feel more comfortable?
- Do they score better?

---

##  What We Found

| Hypothesis | Result | p-value |
|------------|--------|---------|
| Peer asks for help more |  Not significant | p = 0.105 |
| Peer feels more comfortable |  **Significant** | p < 0.001 |
| Peer scores higher |  **Significant** | p = 0.006 |

**But there's a catch**: The peer robot was **too helpful**.  
It removed wrong options instead of just giving clues. So people could use the help button repeatedly to **eliminate all wrong answers** and get the right one without actually knowing it. This is why peer participants scored higher – not because they learned more, but because the help system made the quiz easier.

---

##  How It Works

- **Backend**: Python + Flask
- **Frontend**: HTML + CSS + JavaScript
- **Speech**: Uses your browser's built-in speech (reads questions, listens to answers)
- **Data**: Saves everything to CSV files automatically

---

##  Files

| File | What it does |
|------|--------------|
| `app.py` | Runs the quiz server |
| `templates/index.html` | The quiz page you see |
| `analysis.py` | Runs statistics on the data |
| `experiment_data.csv` | Saves participant results |
| `help_log.csv` | Saves every peer help request |

---

##  How to Run

1. **Install Python** (if you don't have it)

2. **Install the requirements**
   ```bash
   pip install flask pandas scipy matplotlib seaborn numpy
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

5. **Share with participants** (using ngrok)
   ```bash
   ngrok http 5000
   ```
   Share the `https://xxxx.ngrok-free.app` link.

---

##  Run the Analysis

After collecting data:

```bash
python analysis.py
```

This gives you:
- Summary table with means and SDs
- t-test results
- Effect sizes (Cohen's d)
- Bar charts (saved as `full_dataset_results.png`)

---

##  What We Learned (The Hard Way)

### The Big Problem

The **peer robot's help was too powerful**:
- It removed a wrong option every time you asked
- You could ask 3 times per question and eliminate all wrong answers
- This made the quiz much easier for peer participants

### The Tutor Robot

- Only gave a clue (no option removed)
- Couldn't be "gamed" the same way
- Participants had to actually know the answer

### What This Means

The comfort result (peer felt more comfortable) is **confused** –  
people felt comfortable because they were doing well, not necessarily because the robot was friendly.

---

##  Next Time

- Make both robots give the **same kind of help** (both clues, or both remove options)
- Limit help requests (max 1 or 2 per question)
- Equalise the pre-quiz explanations
- Get more participants (we had only 14)

---

##  Credits

**Author**: Likhith Kumar Shivakumar  
**Course**: User Studies in Intelligent Systems  
**University**: Bielefeld University  
**Year**: 2026

---

##  Reference

Belpaeme, T., Kennedy, J., Ramachandran, A., Scassellati, B., & Tanaka, F. (2018). Social robots for education: A review. *Science Robotics, 3*(21), eaat5954.
