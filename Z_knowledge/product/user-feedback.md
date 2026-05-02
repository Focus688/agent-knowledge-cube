# Z: User Feedback Collection & Analysis

## 反馈渠道 / Feedback Channels

| Channel | Type | Volume | Signal Quality |
|---------|------|--------|----------------|
| In-app NPS survey | Quantitative | High | Medium |
| Customer interviews | Qualitative | Low | High |
| Support tickets | Qualitative | Medium | High |
| App Store reviews | Quantitative | Medium | Low-Medium |
| Social media | Qualitative | Low-High | Low |
| Usage analytics | Behavioral | Very High | Medium-High |
| Beta/early access | Qualitative | Low | Very High |

## 情感分析 / Sentiment Analysis
- Tag feedback: **Positive / Neutral / Negative**
- Use NLP tools (Lemonfox, Hugging Face) for automated scoring
- Track sentiment trend over time per feature area

## 优先级框架 / Prioritization Framework

### RICE for Feedback
- **R**equest frequency — how many users asked
- **I**mpact on satisfaction — would solving this increase NPS?
- **C**onfidence — is this a real pain point or a vocal minority?
- **E**ffort to implement

### Impact-Effort Matrix
```
High Impact + Low Effort → Quick wins (do now)
High Impact + High Effort → Major bets (plan)
Low Impact + Low Effort → Fill-ins (icebox)
Low Impact + High Effort → Avoid
```

## 闭环流程 / Closed-Loop Process
1. **Collect** — gather from all channels
2. **Categorize** — tag by feature, sentiment, severity
3. **Analyze** — identify themes, calculate frequency
4. **Act** — prioritize, assign, ship changes
5. **Close the loop** — notify users: "You requested this — it's live!"
