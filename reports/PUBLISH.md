# Publish playbook (for the author)

This is your step-by-step. Read once, then execute.

The audit is built. The narrative is written. All you do from here is **push the repo public**, **submit to four channels in a specific order**, and **be at the keyboard for two windows**.

Total active time required from you: ~3 hours, spread over a week.

## Day 0 — push the repo public (15 minutes)

Already done locally as a single commit on the `main` branch. You only need to publish it.

Open a terminal in the project folder. Run these commands one at a time:

```bash
gh repo create omskykhal/agent-discoverability-audit-2026 --public --source=. --remote=origin --description="Audit of 100 AI agent projects' machine-readability to other AI agents. Average score: 6.3/100."
git push -u origin main
```

That's it. The repo is now live at:
**https://github.com/omskykhal/agent-discoverability-audit-2026**

Visit the URL once. Confirm:
- README renders correctly (badges, headings, links)
- `reports/findings.md` is browsable
- `data/results.csv` opens as a table preview
- The license shows MIT in the sidebar

If anything looks wrong, **fix it before posting anywhere**. After this point, every fix is visible in the commit history.

## Day 1 (Tuesday or Wednesday, 8–10 AM Pacific Time) — Show HN

This is the highest-stakes 60 minutes of the entire campaign.

1. Open `reports/SHOW_HN.md`. Use the title and URL from there.
2. Go to https://news.ycombinator.com/submit
3. Title: paste the chosen title (under 80 chars)
4. URL: paste the GitHub repo URL
5. Text: leave **empty** (HN policy: don't duplicate URL/text)
6. Submit.

For the **next 60 minutes**, do nothing else. Watch the post. When the first comment arrives:

- **Read `reports/SHOW_HN.md` "Comment-response tone guide"** before replying.
- Reply within 5 minutes.
- Use the templates in the tone guide as starting points; adjust the wording but keep the structure.

### What "good" looks like at the 60-minute mark

| Score | Status |
|---|---|
| 5+ points, on front page | Excellent. Stay engaged for 4 more hours. |
| 2–4 points, page 2 | Normal. Keep responding to comments. May drift up. |
| 0–1 points or flagged | Move on. Don't agonize. Reddit is the next swing. |

### Single rule

**Do not edit the post after submission.** HN labels edits as "edited" and some moderators downvote those. If you see a typo, post a self-reply correcting it.

## Day 2 (Wednesday or Thursday) — r/LocalLLaMA

24+ hours after the HN submission. Use `reports/REDDIT_POST.md` r/LocalLLaMA section.

- Title from the file
- Flair: "Discussion" or "Resources"
- Body: paste from the file

For the next **2 hours**, watch and reply. Reddit's algorithm rewards early engagement more than HN's does.

## Day 3 — X (Twitter) thread

Early afternoon US East Coast. Use `reports/X_THREAD.md`.

- Post tweet 1.
- Wait for it to publish.
- Reply to your own tweet 1 with tweet 2.
- Continue through tweet 7.
- Pin tweet 1 to your profile.

If a single tweet in the thread breaks (typo, autocorrect), **do not delete and repost**. Post a correction reply. Threads with deletions in the middle look unprofessional.

## Day 4 — r/MachineLearning

Use `reports/REDDIT_POST.md` r/MachineLearning section. Use the **stripped** body (no calls to action). Be ready for stricter moderators.

## Day 7 — r/AI_Agents and r/programming (optional)

Only post here if Day 1–4 generated meaningful traction. If everything died, skip these — they have lower signal and posting feels like begging.

## Day 14 — Go/No-Go gate

Open `hypothesis.md`. Re-read the gate. Count:

| Signal | Your number | Threshold |
|---|---|---|
| GitHub stars | _____ | ≥ 30 |
| Email/comment expressions of intent ("I'd use this") | _____ | ≥ 1 strong |
| Inbound DM (founder, investor, journalist) | _____ | ≥ 1 |

≥ 2 of 3 → **proceed to product MVP**. Open a new project folder, copy the audit's repo as a sub-directory (it's the seed data), start building.

≤ 1 of 3 → **archive**. Add a `STATUS.md` to the repo: "This research project is not being developed into a product. The dataset and scanner remain available under MIT/CC BY 4.0." Move on.

Both outcomes are fine. The point of the test is to make the decision data-driven.

## What you absolutely do NOT do

- Edit the GitHub repo's history after publishing (no `git push --force`)
- Apologize for the audit's tone if comments are critical — you measured, you reported, the data stands
- Rerun the scanner with a tweaked checklist to "improve" any specific project's score
- DM journalists / founders before the post is up — looks like manufactured launch
- Post the same thread on multiple platforms simultaneously — algorithms penalize this

## Mistakes you will make and how to recover

| Mistake | Recovery |
|---|---|
| Typo in the HN title | Self-reply: "minor: misspelled X. Repo title is correct." |
| A scored project's owner DMs angrily | Open issue, rescan with extra care, post correction with their handle. Conflict converted to credibility. |
| You forgot to add a project that someone asks about | Reply: "good catch — adding to v0.2." Open issue, add to targets.csv, rescan, comment back. |
| Some site rate-limited your scanner during initial run | Reply: "fair, will re-fetch with backoff. Updating the dataset by EOD." Then actually do it. |

## After it's all over

Whether you proceed to a product or archive, **close the loop publicly**:

```
Update on the audit: 14 days post-launch.
- GitHub: X stars
- Top question in comments was [X]
- Decision: [proceed | archive | extend by 30 days]
- Data is unchanged and CC BY 4.0; please cite as: omskykhal/agent-discoverability-audit-2026 (April 2026).
```

Post this on X and as a comment on the original HN/Reddit threads. It signals you're not the kind of person who launches and disappears, which is the most important signal you can send if you ever want to launch a real product later.
