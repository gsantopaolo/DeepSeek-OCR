Here is your text converted to **Markdown with LaTeX rendering**, with **formulas left completely untouched** — only wrapped so they render properly.

---

# DeepSeek-OCR File Type Test Results

**Date:** 2025-11-14 13:12:31
**Total File Types Tested:** 1

---

## PNG - stanford.png - ✅ SUCCESS

**File:** `stanford.png`

**OCR Result (Markdown + LaTeX):**

```markdown
## 2 Learning from Preferences

In the previous part you trained multiple policies from scratch and compared them at the end of training. In this section, we will see how we can use human preferences on two roll-outs to learn a reward function.

We will follow the framework proposed by [2]. A reward function \( r : \mathcal{O} \times \mathcal{A} \to \mathbb{R} \) defines a preference relation \( \succ \) if for all trajectories \( \sigma^i = (o^i_t, a^i_t)_{t=0,\ldots,T} \) we have that

$$
((o^1_0, a^1_0), \ldots, (o^1_T, a^1_T)) \succ ((o^2_0, a^2_0), \ldots, (o^2_T, a^2_T))
$$

whenever

$$
r(o^1_0, a^1_0) + \cdots + r(o^1_T, a^1_T) > r(o^2_0, a^2_0) + \cdots + r(o^2_T, a^2_T).
$$

Following the Bradley-Terry preference model [1], we can calculate the probability of one trajectory \( \sigma^1 \) being preferred over \( \sigma^2 \) as follows:

$$
\hat{P}[\sigma^1 \succ \sigma^2] = \frac{\exp \sum \hat{r}(o^1_t, a^1_t)}{\exp \sum \hat{r}(o^1_t, a^1_t) + \exp \sum \hat{r}(o^2_t, a^2_t)},
$$

where \( \hat{r} \) is an estimate of the reward for a state-action pair. This is similar to a classification problem, and we can fit a function approximator to \( \hat{r} \) by minimizing the cross-entropy loss between the values predicted with the above formula and ground truth human preference labels \( \mu(1) \) and \( \mu(2) \):

$$
\text{loss}(\hat{r}) = -\sum_{(\sigma^1, \sigma^2, \mu) \in \mathcal{D}} \mu(1) \log \hat{P}[\sigma^1 \succ \sigma^2] + \mu(2) \log \hat{P}[\sigma^2 \succ \sigma^1].
$$

Once we have learned the reward function \( \hat{r} \), we can apply any policy optimization algorithm (such as PPO) to maximize the returns of a model under it.
```

---

If you'd like, I can also generate a version with inline math only, or convert it to a different style (e.g., GitHub-friendly math rendering).
