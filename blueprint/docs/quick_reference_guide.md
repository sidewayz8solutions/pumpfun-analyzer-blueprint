
# SMART BUY ANALYSIS ENGINE - QUICK REFERENCE

## Core Scoring Formula

```
Smart Buy Score = Base Score + Opportunity Boost - Risk Penalty

Where:
Base Score = Σ(Component Score × Weight)
Opportunity Boost = Early Opportunity Score × 0.15
Risk Penalty = Overall Risk Score × 0.5
```

## Factor Weights

| Factor | Weight | Target Value |
|--------|--------|--------------|
| Liquidity Health | 20% | >5% of market cap |
| Holder Distribution | 15% | Top 10 < 40% |
| Volume Quality | 20% | Natural growth |
| Price Action | 15% | Healthy momentum |
| Bonding Curve | 10% | Early stage (20-60%) |
| Developer Activity | 10% | No selling, locked |
| Social Signals | 10% | Positive sentiment |

## Key Formulas

### 1. Liquidity Depth Score
```
LDS = min(100, (liquidity_SOL / market_cap) × 1000)
Target: LDS ≥ 50 (5% ratio)
```

### 2. Concentration Risk Index
```
CRI = max(0, 100 - top_10_percent × 1.5)
Excellent: CRI > 70 (top 10 < 20%)
Good: CRI 40-70 (top 10 20-40%)
Risky: CRI < 40 (top 10 > 40%)
```

### 3. Natural Volume Indicator
```
NVI = 100 - (artificial_volume_score × 100)

artificial_volume_score considers:
- Trade size uniformity (power law deviation)
- Temporal clustering (regular intervals)
- Wallet reuse ratio
- Round number bias
- Buy-sell alternation
```

### 4. Pump & Dump Detection
```
Early Pump: price_1h > +50%, volume_spike > 3×, volatility < 30%
Mature Pump: price_24h > +300%, volume_spike > 5×
Distribution: price_1h flat, price_24h > +200%, volatility > 40%
Dump: price_1h < -30%, volume_spike > 2×
Accumulation: price flat, volume up, low volatility
Organic Growth: price +50-300%, volume 1-5×, low volatility
```

### 5. Wash Trading Detection
```
wash_score = 0.35×cycle_score + 0.25×cluster_score + 0.25×zero_sum + 0.15×fee_tolerance

Red flags:
- Circular transactions (A→B→A)
- Zero-sum wallet groups
- Fee loss tolerance
- Synchronized patterns
```

### 6. Risk Score Calculation
```
Risk Score = 0.25×concentration + 0.20×liquidity + 0.20×manipulation +
             0.15×contract + 0.10×time + 0.10×social

Risk Levels:
LOW: 0-30
MODERATE: 31-50
ELEVATED: 51-70
HIGH: 71-100
```

### 7. Early Opportunity Score
```
opportunity = 0.5×recency + 0.3×acceleration + 0.2×pattern

recency = max(0, 1 - age_hours / 24)
acceleration = holder_growth_1h / (holder_growth_4h / 4)
```

## Recommendation Thresholds

| Score | Risk | Recommendation |
|-------|------|----------------|
| ≥75 | <40 | STRONG_BUY |
| ≥60 | <50 | BUY |
| ≥45 | <60 | MODERATE_BUY |
| ≥35 | <70 | WATCH |
| Any | ≥70 | HIGH_RISK |
| <35 | Any | AVOID |

## Critical Red Flags (Auto-AVOID)

1. **Dev Rugged**: Dev sold >90% of allocation
2. **Liquidity Removed**: >50% liquidity drop in 1 hour
3. **Honeypot Contract**: Cannot sell tokens
4. **Massive Whale Dump**: Top 3 sold >30% in 1 hour
5. **Pump Complete**: Mature pump pattern + extreme price rise

## Data Update Frequency

| Data Type | Frequency |
|-----------|-----------|
| Price/Trades | Real-time |
| Liquidity | 30 seconds |
| Holders | 2 minutes |
| Risk Flags | 5 minutes |
| Social | 15 minutes |

## Normalization Functions

```python
# Min-Max Normalization
def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val) * 100

# Z-Score
def z_score(value, mean, std):
    return (value - mean) / std

# Sigmoid
def sigmoid(x, k=1):
    return 100 / (1 + math.exp(-k * x))
```

## Statistical Indicators

```
Coefficient of Variation = σ / μ
(Use for consistency scoring - lower is better)

Sharpe Ratio = (return - risk_free) / σ
(Use for risk-adjusted returns)

Volume Spike = current_volume / average_volume
(>3× = significant, >5× = extreme)
```

## Confidence Calculation

```
confidence = data_quality × (1 - risk_score / 200)

data_quality = sample_size×30 + freshness×25 + reliability×25 + completeness×20
```

## Time Decay

```
decay_factor = exp(-0.1 × hours_since_last_trade)

Score after 1 hour of inactivity: 90% of original
Score after 6 hours: 55% of original
Score after 24 hours: 9% of original
```

## Example Calculation

For a token with:
- Liquidity: 5% of market cap → LDS = 50
- Top 10 holders: 35% → CRI = 47.5
- Volume: Natural, 2× average → VTS = 75
- Price: +20% in 1h, +80% in 24h → PMS = 60
- Bonding: 40% progress → PS = 40
- Dev: No selling, 30-day wallet → DCS = 100, DWA = 100
- Risk: Moderate concentration, no manipulation → Risk = 45

Calculation:
```
Base Score = 50×0.20 + 47.5×0.15 + 75×0.20 + 60×0.15 + 40×0.10 + 95×0.10 + 50×0.10
           = 10 + 7.125 + 15 + 9 + 4 + 9.5 + 5
           = 59.625

Opportunity Boost = 0.6 × 15 = 9
Risk Penalty = 45 × 0.5 = 22.5

Final Score = 59.625 + 9 - 22.5 = 46.125

Recommendation: MODERATE_BUY (score 45-60, risk <60)
```
