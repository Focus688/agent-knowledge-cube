# Z: Product Metrics Definitions

## 核心指标 / Core Metrics

### DAU / MAU
- **DAU** = Daily Active Users. 日活跃用户数.
- **MAU** = Monthly Active Users. 月活跃用户数.
- **Stickiness** = DAU/MAU. >50% 为优秀 / excellent engagement. Formula: stickiness = (DAU₁+...+DAU₂₈)/MAU.

### Retention
- **Day 1/7/30 Retention** = Users returning on day N after signup
- **Week-over-Week** = % of weekly cohort still active
- Formula: `retention_N = users_active_on_day_N / users_in_cohort`
- Benchmark: Day 1 >40%, Day 7 >20%, Day 30 >10%

### Conversion Funnel
- **Activation** → Engagement → **Purchase** → Retention → Referral
- Drop-off rate per step = `(previous_step - current_step) / previous_step × 100%`
- Identify bottleneck steps for optimization

### NPS (Net Promoter Score)
- Survey: "How likely to recommend? (0-10)"
- Promoters (9-10) - Passives (7-8) - Detractors (0-6)
- NPS = %Promoters − %Detractors. Range: -100 to +100.

### Churn / 流失率
- **Monthly Churn** = users_lost_in_month / users_at_start
- **Revenue Churn** = MRR_lost / MRR_at_start
- **Logo Churn** = customers_lost / total_customers

### LTV (Lifetime Value) / CAC (Customer Acquisition Cost)
- **LTV** = ARPU × Gross Margin × (1/Churn Rate)
- **CAC** = Total Sales & Marketing / New Customers Acquired
- **LTV:CAC Ratio** — >3:1 is healthy, <1:1 is unsustainable

### Activation Rate
- % of new users who reach the "aha moment" (key value event)
- Typically within first session or Day 1
