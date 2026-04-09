
# PUMP.FUN MEME COIN SMART BUY ANALYSIS ENGINE
## Complete Algorithm Specification v1.0

---

## 1. SCORING FRAMEWORK

### 1.1 Overall Scoring Methodology

**Primary Score: Smart Buy Score (SBS)**
- Scale: 0-100 (higher = better opportunity)
- Updated: Real-time with every new transaction
- Components:
  - Opportunity Score (40%): Growth potential indicators
  - Health Score (35%): Market structure quality
  - Risk Score (25%): Danger indicators (inverted)

**Secondary Metrics:**
- Confidence Level: 0-100% based on data quality and sample size
- Risk Level: LOW (0-30), MEDIUM (31-60), HIGH (61-100)
- Time Decay Factor: Score reduction for stale data

### 1.2 Score Calculation Pipeline

```
Raw Data → Factor Calculations → Normalization → Weighted Aggregation → Final Score
```

**Normalization Method:** Min-Max with Outlier Clipping
```python
def normalize(value, min_val, max_val, clip_outliers=True):
    if clip_outliers:
        value = max(min_val, min(value, max_val))
    return (value - min_val) / (max_val - min_val) * 100
```

### 1.3 Time Decay Function

Scores decay based on time since last significant event:
```
decay_factor = exp(-λ × hours_since_last_trade)
where λ = 0.1 (configurable)
```

---

## 2. KEY FACTORS & WEIGHTS

### 2.1 Factor Categories

| Category | Weight | Factors Included |
|----------|--------|------------------|
| **Liquidity Health** | 20% | Depth, Spread, Growth Rate |
| **Holder Distribution** | 15% | Concentration, Growth, Retention |
| **Volume Quality** | 20% | Natural vs Artificial, Trend |
| **Price Action** | 15% | Momentum, Volatility, Support |
| **Bonding Curve** | 10% | Progress, Velocity, Milestones |
| **Developer Activity** | 10% | Wallet Behavior, Commitment |
| **Social Signals** | 10% | Engagement, Sentiment (if available) |

### 2.2 Detailed Factor Breakdown

#### A. LIQUIDITY HEALTH (Weight: 20%)

**A1. Liquidity Depth Score (LDS)**
```
LDS = min(100, (liquidity_SOL / market_cap) × 100 × 10)
Target: >5% liquidity ratio = 100 points
```

**A2. Bid-Ask Spread Score (BAS)**
```
BAS = max(0, 100 - (spread_percent × 20))
where spread_percent = (ask - bid) / mid_price × 100
Perfect spread <0.5% = 100 points
```

**A3. Liquidity Growth Rate (LGR)**
```
LGR = (liquidity_now - liquidity_1h_ago) / liquidity_1h_ago × 100
Normalized: -50% to +100% mapped to 0-100
```

**Liquidity Health Composite:**
```
Liquidity_Score = 0.5×LDS + 0.3×BAS + 0.2×LGR
```

#### B. HOLDER DISTRIBUTION (Weight: 15%)

**B1. Concentration Risk Index (CRI)**
```
CRI = 100 - (top_10_holder_percent × 1.5)
where top_10_holder_percent = sum of top 10 wallets / total_supply × 100

Scoring:
- Top 10 < 20%: 100 points (excellent)
- Top 10 20-40%: 70-100 points (good)
- Top 10 40-60%: 40-70 points (moderate risk)
- Top 10 > 60%: 0-40 points (high risk)
```

**B2. Holder Growth Rate (HGR)**
```
HGR = normalize((holders_now - holders_1h_ago) / holders_1h_ago × 100, 0, 50)
Target: 10-30% hourly growth = optimal
```

**B3. Holder Retention Rate (HRR)**
```
HRR = (holders_who_bought_1h_ago AND still_hold) / holders_who_bought_1h_ago × 100
Normalized: 0-100 mapped directly
```

**B4. Whale Activity Score (WAS)**
```
WAS = 100 - (whale_net_buy_pressure × 2)
where whale_net_buy_pressure = (whale_buys - whale_sells) / total_volume × 100
Negative = whales selling (bad), Positive = whales accumulating (good)
```

**Holder Distribution Composite:**
```
Holder_Score = 0.4×CRI + 0.25×HGR + 0.2×HRR + 0.15×WAS
```

#### C. VOLUME QUALITY (Weight: 20%)

**C1. Volume Trend Score (VTS)**
```
VTS = normalize(volume_24h / average_volume_7d × 100, 50, 300)
Target: 100-200% of average = healthy growth
```

**C2. Volume Consistency Score (VCS)**
```
cv = standard_deviation(hourly_volumes_24h) / mean(hourly_volumes_24h)
VCS = max(0, 100 - cv × 50)
Lower coefficient of variation = more consistent = better
```

**C3. Buy/Sell Ratio Score (BSR)**
```
BSR = min(100, buy_volume / (buy_volume + sell_volume) × 200)
Target: 55-65% buy ratio = bullish but not extreme
```

**C4. Natural Volume Indicator (NVI)**
```
NVI = 100 - (artificial_volume_score × 100)
```

**Volume Quality Composite:**
```
Volume_Score = 0.3×VTS + 0.2×VCS + 0.25×BSR + 0.25×NVI
```

#### D. PRICE ACTION (Weight: 15%)

**D1. Price Momentum Score (PMS)**
```
PMS = normalize(price_change_1h × 2 + price_change_24h, -50, 100)
Balanced view of short and medium term momentum
```

**D2. Volatility Health Score (VHS)**
```
volatility = std_dev(5min_returns_24h) × sqrt(288)
VHS = 100 - min(100, abs(volatility - 0.5) × 100)
Target: 30-70% annualized volatility = healthy
```

**D3. Support Level Strength (SLS)**
```
support_touches = count of price bouncing off support in last 24h
SLS = min(100, support_touches × 25 + (price_above_support / support_price) × 50)
```

**D4. Price Pattern Score (PPS)**
```
PPS = detect_pattern_score()
```

**Price Action Composite:**
```
Price_Score = 0.35×PMS + 0.25×VHS + 0.25×SLS + 0.15×PPS
```

#### E. BONDING CURVE (Weight: 10%)

**E1. Progress Score (PS)**
```
PS = bonding_curve_progress_percent
Early stage (<20%): Higher opportunity score
Mid stage (20-80%): Moderate score
Late stage (>80%): Lower opportunity, higher completion probability
```

**E2. Bonding Velocity (BV)**
```
BV = normalize(progress_change_24h, 0, 20)
Faster progress = more momentum
```

**E3. Milestone Proximity (MP)**
```
MP = 100 - (distance_to_next_milestone / total_curve × 100)
Closer to milestones = higher attention potential
```

**Bonding Curve Composite:**
```
Bonding_Score = 0.5×PS + 0.3×BV + 0.2×MP
```

#### F. DEVELOPER ACTIVITY (Weight: 10%)

**F1. Developer Commitment Score (DCS)**
```
DCS = 100 - (dev_sold_percent × 2)
dev_sold_percent = dev_tokens_sold / dev_initial_allocation × 100
```

**F2. Developer Wallet Age (DWA)**
```
DWA = min(100, wallet_age_days / 30 × 100)
Older wallet = more established = lower rug risk
```

**F3. Liquidity Lock Score (LLS)**
```
LLS = liquidity_locked ? 100 : 0
If partial lock: LLS = locked_percent
```

**Developer Activity Composite:**
```
Dev_Score = 0.5×DCS + 0.25×DWA + 0.25×LLS
```

#### G. SOCIAL SIGNALS (Weight: 10%)

**G1. Social Engagement Score (SES)**
```
if social_data_available:
    SES = normalize(mentions_1h, 0, 1000)
else:
    SES = 50  # Neutral if no data
```

**G2. Sentiment Score (SS)**
```
if sentiment_data_available:
    SS = (positive_mentions - negative_mentions) / total_mentions × 50 + 50
else:
    SS = 50  # Neutral
```

**Social Signals Composite:**
```
Social_Score = 0.6×SES + 0.4×SS
```

---

## 3. ADVANCED DETECTION ALGORITHMS

### 3.1 Artificial Volume Detection

**Algorithm: Multi-Factor Volume Authenticity Check**

Returns artificial_volume_score (0-1, higher = more artificial)

```python
def detect_artificial_volume(token_data):
    scores = []

    # Factor 1: Trade Size Distribution Anomaly
    trade_sizes = token_data.trade_sizes
    expected_distribution = power_law_distribution(mean(trade_sizes))
    ks_statistic = kolmogorov_smirnov_test(trade_sizes, expected_distribution)
    scores.append(min(1, ks_statistic * 2))

    # Factor 2: Temporal Clustering
    trade_times = token_data.trade_timestamps
    time_diffs = diff(trade_times)
    clustering_score = 1 - (std(time_diffs) / mean(time_diffs))
    scores.append(max(0, clustering_score))

    # Factor 3: Wallet Reuse Pattern
    unique_wallets = len(set(token_data.trader_addresses))
    total_trades = len(token_data.trades)
    reuse_ratio = 1 - (unique_wallets / total_trades)
    scores.append(reuse_ratio)

    # Factor 4: Round Number Bias
    round_number_percent = count_round_number_trades(trade_sizes) / total_trades
    scores.append(min(1, round_number_percent * 3))

    # Factor 5: Buy-Sell Alternation Pattern
    alternation_score = detect_alternating_pattern(token_data.trades)
    scores.append(alternation_score)

    # Weighted combination
    weights = [0.25, 0.20, 0.25, 0.15, 0.15]
    artificial_score = sum(s * w for s, w in zip(scores, weights))

    return artificial_score
```

**Key Indicators of Artificial Volume:**
1. **Uniform Trade Sizes**: Real trades follow power law, bot trades often uniform
2. **Regular Timing**: Human trades are irregular, bot trades often evenly spaced
3. **Wallet Recycling**: Same wallets trading repeatedly
4. **Round Numbers**: Excessive trades at round numbers (1, 5, 10 SOL)
5. **Perfect Alternation**: Buy-sell-buy-sell patterns

### 3.2 Wash Trading Detection

**Algorithm: Circular Trading Detection**

Returns wash_trading_score (0-1, higher = more wash trading)

```python
def detect_wash_trading(token_data, time_window_minutes=60):
    scores = []

    # Build transaction graph
    G = build_transaction_graph(token_data.trades, time_window_minutes)

    # Factor 1: Circular Transaction Chains
    cycles = find_cycles(G, max_length=4)
    cycle_volume = sum(cycle['volume'] for cycle in cycles)
    total_volume = token_data.volume_24h
    cycle_score = min(1, cycle_volume / total_volume * 5)
    scores.append(cycle_score)

    # Factor 2: Same-Entity Clustering
    clusters = cluster_by_behavior(token_data.trader_addresses)
    cluster_score = max_cluster_size / total_unique_wallets
    scores.append(cluster_score)

    # Factor 3: Zero-Sum Wallet Groups
    wallet_pnl = calculate_wallet_pnl(token_data.trades)
    zero_sum_groups = find_zero_sum_groups(wallet_pnl, threshold=0.01)
    zero_sum_score = len(zero_sum_groups) / len(token_data.trader_addresses)
    scores.append(min(1, zero_sum_score * 10))

    # Factor 4: Fee Loss Tolerance
    total_fees = sum(trade['fee'] for trade in token_data.trades)
    suspicious_wallets = find_wallets_accepting_losses(token_data.trades, threshold=0.1)
    fee_tolerance_score = len(suspicious_wallets) / len(token_data.trader_addresses)
    scores.append(min(1, fee_tolerance_score * 5))

    # Weighted combination
    weights = [0.35, 0.25, 0.25, 0.15]
    wash_score = sum(s * w for s, w in zip(scores, weights))

    return wash_score
```

**Wash Trading Red Flags:**
- Wallet A → Wallet B → Wallet A (circular)
- Groups of wallets with near-zero net P&L
- Wallets accepting consistent losses (paying fees for no profit)
- Synchronized trading patterns across multiple wallets

### 3.3 Coordinated Buying Detection

**Algorithm: Synchronized Purchase Detection**

Returns coordination_score (0-1, higher = more coordinated)

```python
def detect_coordinated_buying(token_data, time_window_seconds=30):
    scores = []

    # Group trades by time windows
    time_windows = group_trades_by_time(token_data.buys, time_window_seconds)

    # Factor 1: Simultaneous Buy Spike
    buy_counts = [len(window) for window in time_windows]
    spike_score = (max(buy_counts) - mean(buy_counts)) / std(buy_counts)
    scores.append(min(1, spike_score / 5))

    # Factor 2: New Wallet Concentration
    new_wallet_ratio = count_new_wallets(token_data.buys) / len(token_data.buys)
    scores.append(min(1, new_wallet_ratio * 2))

    # Factor 3: Similar Trade Sizes
    trade_size_variance = coefficient_of_variation(token_data.buy_amounts)
    size_uniformity_score = 1 - min(1, trade_size_variance)
    scores.append(size_uniformity_score)

    # Factor 4: Source Funding Correlation
    funding_sources = trace_funding_sources(token_data.buyer_addresses)
    common_source_ratio = count_common_funding_sources(funding_sources) / len(funding_sources)
    scores.append(common_source_ratio)

    # Weighted combination
    weights = [0.30, 0.25, 0.25, 0.20]
    coordination_score = sum(s * w for s, w in zip(scores, weights))

    return coordination_score
```

### 3.4 Pump & Dump Pattern Recognition

**Algorithm: Pattern Detection System**

```python
def detect_pump_dump_pattern(token_data):
    price_history = token_data.price_5min_ohlc
    volume_history = token_data.volume_5min

    patterns = {
        'early_pump': 0,
        'mature_pump': 0,
        'distribution': 0,
        'dump': 0,
        'accumulation': 0,
        'organic_growth': 0
    }

    # Calculate key metrics
    price_change_1h = (price_history[-12] - price_history[-1]) / price_history[-1]
    price_change_24h = (price_history[0] - price_history[-1]) / price_history[-1]
    volume_spike = max(volume_history[-12:]) / mean(volume_history[-288:-12])
    volatility = std_dev(price_history[-12:]) / mean(price_history[-12:])

    # Pattern: Early Pump
    if price_change_1h > 0.5 and volume_spike > 3 and volatility < 0.3:
        patterns['early_pump'] = min(1, price_change_1h) * 0.8

    # Pattern: Mature Pump (high risk)
    if price_change_24h > 3 and volume_spike > 5:
        patterns['mature_pump'] = min(1, price_change_24h / 10) * 0.9

    # Pattern: Distribution
    if (price_change_1h < 0.1 and price_change_24h > 2 and 
        volume_spike > 2 and volatility > 0.4):
        patterns['distribution'] = 0.85

    # Pattern: Dump
    if price_change_1h < -0.3 and volume_spike > 2:
        patterns['dump'] = min(1, abs(price_change_1h)) * 0.9

    # Pattern: Accumulation
    if (abs(price_change_24h) < 0.5 and volume_spike > 1.5 and 
        volatility < 0.2 and detect_whale_accumulation(token_data)):
        patterns['accumulation'] = 0.75

    # Pattern: Organic Growth
    if (price_change_24h > 0.5 and price_change_24h < 3 and 
        volume_spike > 1 and volume_spike < 5 and 
        volatility < 0.3 and detect_holder_growth(token_data)):
        patterns['organic_growth'] = 0.80

    return patterns
```

### 3.5 Early Opportunity Detection

**Algorithm: Early Signal Detection**

```python
def detect_early_opportunity(token_data):
    scores = []

    # Factor 1: Launch Recency
    hours_since_launch = token_data.age_hours
    recency_score = max(0, 1 - hours_since_launch / 24)
    scores.append(recency_score * 0.5)

    # Factor 2: Holder Growth Acceleration
    holder_growth_1h = token_data.holder_growth_1h
    holder_growth_4h = token_data.holder_growth_4h
    acceleration = holder_growth_1h / (holder_growth_4h / 4 + 0.001)
    acceleration_score = min(1, acceleration / 3)
    scores.append(acceleration_score * 0.3)

    # Factor 3: Volume Precedes Price
    volume_lead = detect_volume_price_lead(token_data, lag_periods=3)
    scores.append(volume_lead * 0.2)

    # Factor 4: Smart Money Entry
    smart_money_score = detect_smart_money_entry(token_data)
    scores.append(smart_money_score * 0.5)

    # Factor 5: Social Momentum (if available)
    if token_data.social_data_available:
        social_momentum = token_data.mention_growth_1h / token_data.mention_growth_4h
        scores.append(min(1, social_momentum / 2) * 0.3)

    opportunity_score = sum(scores)
    return min(1, opportunity_score)

def detect_smart_money_entry(token_data):
    smart_indicators = 0

    # Check for profitable wallet history
    profitable_buyers = count_profitable_wallet_buyers(token_data.buys)
    if profitable_buyers / len(token_data.buys) > 0.3:
        smart_indicators += 1

    # Check for whale accumulation
    if detect_whale_accumulation(token_data):
        smart_indicators += 1

    # Check for multiple small buys (retail FOMO not started)
    if count_large_buys(token_data.buys) / len(token_data.buys) < 0.2:
        smart_indicators += 1

    return smart_indicators / 3
```

---

## 4. RISK ASSESSMENT FRAMEWORK

### 4.1 Risk Scoring Methodology

**Overall Risk Score (0-100, higher = more risky)**

```
Risk_Score = max(0, min(100, 
    0.25×Concentration_Risk + 
    0.20×Liquidity_Risk + 
    0.20×Manipulation_Risk + 
    0.15×Contract_Risk + 
    0.10×Time_Risk + 
    0.10×Social_Risk
))
```

### 4.2 Risk Components

**Concentration Risk (0-100)**
```
if top_1_holder > 30%: concentration_risk = 100
elif top_5_holders > 50%: concentration_risk = 80
elif top_10_holders > 70%: concentration_risk = 70
else: concentration_risk = max(0, (top_10_holders - 20) × 1.5)
```

**Liquidity Risk (0-100)**
```
liquidity_ratio = liquidity_SOL / market_cap
if liquidity_ratio < 0.01: liquidity_risk = 100
elif liquidity_ratio < 0.03: liquidity_risk = 80
elif liquidity_ratio < 0.05: liquidity_risk = 60
else: liquidity_risk = max(0, (0.1 - liquidity_ratio) × 1000)
```

**Manipulation Risk (0-100)**
```
manipulation_risk = (
    artificial_volume_score × 30 +
    wash_trading_score × 30 +
    coordination_score × 25 +
    pump_dump_pattern_score × 15
)
```

**Contract Risk (0-100)**
```
contract_risk = 0
if not_contract_verified: contract_risk += 40
if mint_authority_enabled: contract_risk += 30
if freeze_authority_enabled: contract_risk += 20
if dev_can_mint_more: contract_risk += 10
```

**Time Risk (0-100)**
```
if age_hours < 1: time_risk = 80
elif age_hours < 6: time_risk = 60
elif age_hours < 24: time_risk = 40
else: time_risk = max(0, 40 - (age_hours - 24) / 10)
```

**Social Risk (0-100)**
```
if social_data_available:
    negative_sentiment_ratio = negative_mentions / total_mentions
    social_risk = negative_sentiment_ratio × 100
else:
    social_risk = 50
```

### 4.3 Red Flag Detection System

**Critical Red Flags (Immediate disqualification)**
```python
CRITICAL_FLAGS = {
    'dev_rugged': dev_sold > 90% of allocation,
    'liquidity_removed': liquidity_decreased > 50% in 1h,
    'contract_honeypot': detect_honeypot(token_data),
    'massive_whale_dump': top_3_sold > 30% in 1h,
    'coordinated_pump_complete': pump_dump_score > 0.9 and price_change_1h > 10
}
```

**High Risk Flags (Score reduction)**
```python
HIGH_RISK_FLAGS = {
    'high_concentration': top_10_holders > 80%,
    'artificial_volume': artificial_volume_score > 0.7,
    'wash_trading': wash_trading_score > 0.6,
    'low_liquidity': liquidity_ratio < 0.02,
    'fresh_wallets': new_wallet_ratio > 0.7,
    'dev_selling': dev_net_sell > 20% in 24h
}
```

**Medium Risk Flags (Minor score reduction)**
```python
MEDIUM_RISK_FLAGS = {
    'moderate_concentration': top_10_holders > 60%,
    'declining_volume': volume_trend < -30%,
    'high_volatility': volatility > 100%,
    'contract_not_verified': True,
    'limited_holder_growth': holder_growth_24h < 10%
}
```

### 4.4 Confidence Intervals

**Data Quality Score (0-100)**
```
data_quality = min(100, 
    sample_size_factor × 30 +
    data_freshness × 25 +
    source_reliability × 25 +
    completeness × 20
)

where:
- sample_size_factor = min(1, trade_count / 100)
- data_freshness = max(0, 1 - minutes_since_update / 5)
- source_reliability = 1.0 for on-chain, 0.8 for APIs
- completeness = fields_with_data / total_fields
```

**Confidence Level Calculation**
```
confidence_level = data_quality × (1 - risk_score / 200)
```

---

## 5. FINAL SCORING & RECOMMENDATIONS

### 5.1 Smart Buy Score Calculation

```python
def calculate_smart_buy_score(token_data):
    # Check critical red flags first
    if has_critical_red_flag(token_data):
        return {
            'score': 0,
            'recommendation': 'AVOID',
            'reason': get_critical_flag_reason(token_data),
            'confidence': 100
        }

    # Calculate component scores
    liquidity_score = calculate_liquidity_score(token_data)
    holder_score = calculate_holder_score(token_data)
    volume_score = calculate_volume_score(token_data)
    price_score = calculate_price_score(token_data)
    bonding_score = calculate_bonding_score(token_data)
    dev_score = calculate_dev_score(token_data)
    social_score = calculate_social_score(token_data)

    # Calculate risk score
    risk_score = calculate_risk_score(token_data)

    # Calculate opportunity score (early detection)
    opportunity_score = detect_early_opportunity(token_data) * 100

    # Weighted combination
    weights = {
        'liquidity': 0.20,
        'holder': 0.15,
        'volume': 0.20,
        'price': 0.15,
        'bonding': 0.10,
        'dev': 0.10,
        'social': 0.10
    }

    base_score = (
        liquidity_score * weights['liquidity'] +
        holder_score * weights['holder'] +
        volume_score * weights['volume'] +
        price_score * weights['price'] +
        bonding_score * weights['bonding'] +
        dev_score * weights['dev'] +
        social_score * weights['social']
    )

    # Apply opportunity boost for early coins
    opportunity_boost = opportunity_score * 0.15

    # Apply risk penalty
    risk_penalty = risk_score * 0.5

    # Final score
    final_score = max(0, min(100, base_score + opportunity_boost - risk_penalty))

    # Calculate confidence
    confidence = calculate_confidence(token_data, risk_score)

    # Generate recommendation
    recommendation = generate_recommendation(final_score, risk_score, confidence)

    return {
        'score': round(final_score, 1),
        'confidence': round(confidence, 1),
        'risk_level': get_risk_level(risk_score),
        'recommendation': recommendation,
        'components': {
            'liquidity': round(liquidity_score, 1),
            'holder': round(holder_score, 1),
            'volume': round(volume_score, 1),
            'price': round(price_score, 1),
            'bonding': round(bonding_score, 1),
            'dev': round(dev_score, 1),
            'social': round(social_score, 1)
        },
        'risk_breakdown': get_risk_breakdown(token_data),
        'flags': get_all_flags(token_data)
    }
```

### 5.2 Recommendation Logic

```python
def generate_recommendation(score, risk_score, confidence):
    if confidence < 30:
        return 'INSUFFICIENT_DATA'

    if score >= 75 and risk_score < 40:
        return 'STRONG_BUY'
    elif score >= 60 and risk_score < 50:
        return 'BUY'
    elif score >= 45 and risk_score < 60:
        return 'MODERATE_BUY'
    elif score >= 35 and risk_score < 70:
        return 'WATCH'
    elif risk_score >= 70:
        return 'HIGH_RISK'
    else:
        return 'AVOID'
```

### 5.3 Risk Level Classification

```python
def get_risk_level(risk_score):
    if risk_score < 30:
        return 'LOW'
    elif risk_score < 50:
        return 'MODERATE'
    elif risk_score < 70:
        return 'ELEVATED'
    else:
        return 'HIGH'
```

---

## 6. OUTPUT FORMAT SPECIFICATION

### 6.1 Smart Buy Recommendation Output

```json
{
  "token_address": "string",
  "token_symbol": "string",
  "analysis_timestamp": "ISO8601",

  "smart_buy_score": {
    "overall": 72.5,
    "confidence": 85.0,
    "recommendation": "BUY",
    "risk_level": "MODERATE"
  },

  "component_scores": {
    "liquidity": 78.0,
    "holder_distribution": 65.0,
    "volume_quality": 82.0,
    "price_action": 71.0,
    "bonding_curve": 45.0,
    "developer_activity": 88.0,
    "social_signals": 55.0
  },

  "risk_assessment": {
    "overall_risk_score": 42.0,
    "breakdown": {
      "concentration_risk": 35.0,
      "liquidity_risk": 25.0,
      "manipulation_risk": 55.0,
      "contract_risk": 40.0,
      "time_risk": 60.0,
      "social_risk": 45.0
    }
  },

  "detection_flags": {
    "critical": [],
    "high_risk": ["moderate_concentration"],
    "medium_risk": ["limited_holder_growth"],
    "positive": ["strong_liquidity", "dev_committed"]
  },

  "pattern_analysis": {
    "detected_pattern": "organic_growth",
    "pattern_confidence": 0.75,
    "early_opportunity_score": 0.65,
    "artificial_volume_detected": false,
    "wash_trading_detected": false,
    "coordinated_buying_detected": false
  },

  "key_metrics": {
    "price_change_1h": 12.5,
    "price_change_24h": 45.0,
    "volume_24h_SOL": 1250.5,
    "liquidity_SOL": 85.2,
    "holders": 1250,
    "holder_growth_1h": 15.2,
    "market_cap_SOL": 1500.0,
    "bonding_curve_progress": 35.0,
    "top_10_holder_percent": 45.0
  },

  "recommendation_details": {
    "action": "BUY",
    "entry_strategy": "Consider entry on any dip below current price",
    "position_size": "MODERATE",
    "stop_loss": "-20% from entry",
    "take_profit": "+100% from entry",
    "time_horizon": "24-72 hours",
    "rationale": [
      "Strong liquidity with healthy depth",
      "Developer has not sold any tokens",
      "Natural volume growth with no artificial patterns",
      "Early stage bonding curve (35%) with room to grow",
      "Moderate concentration risk - monitor top holders"
    ]
  },

  "alerts": [
    {
      "type": "INFO",
      "message": "Token is in early growth phase with strong fundamentals"
    },
    {
      "type": "WARNING", 
      "message": "Top 10 holders control 45% - watch for large sells"
    }
  ],

  "comparative_ranking": {
    "percentile_all_meme_coins": 78.0,
    "percentile_same_age": 85.0,
    "percentile_same_market_cap": 72.0
  }
}
```

### 6.2 Simplified Display Format

```
╔══════════════════════════════════════════════════════════╗
║  $TOKEN    SMART BUY SCORE: 72.5/100    [BUY]            ║
║  Confidence: 85%    Risk: MODERATE    Age: 6h            ║
╠══════════════════════════════════════════════════════════╣
║  Liquidity:     78/100  Strong depth                     ║
║  Holders:       65/100  Moderate concentration           ║
║  Volume:        82/100  Natural growth                   ║
║  Price:         71/100  Healthy momentum                 ║
║  Bonding:       45/100  Early stage (35%)                ║
║  Developer:     88/100  Committed, no sells              ║
║  Social:        55/100  Limited data                     ║
╠══════════════════════════════════════════════════════════╣
║  Warnings: Top 10 holders = 45% (monitor)                ║
║  Positives: Strong liquidity, Dev committed              ║
╚══════════════════════════════════════════════════════════╝
```

---

## 7. IMPLEMENTATION NOTES

### 7.1 Data Requirements

**Required Data Points:**
- Token metadata (address, symbol, decimals)
- Price history (5-min OHLC minimum)
- Trade history (all transactions)
- Liquidity pool data
- Holder balances and count
- Developer wallet address
- Bonding curve progress
- Contract verification status

**Optional Data Points:**
- Social media mentions
- Sentiment analysis
- Wallet age/history
- Cross-exchange data

### 7.2 Update Frequency

| Data Type | Update Frequency | Priority |
|-----------|-----------------|----------|
| Price/Volume | Real-time (WebSocket) | Critical |
| Trades | Real-time | Critical |
| Liquidity | Every 30 seconds | High |
| Holders | Every 2 minutes | High |
| Risk flags | Every 5 minutes | Medium |
| Social data | Every 15 minutes | Low |

### 7.3 Performance Considerations

- Cache intermediate calculations for 30 seconds
- Use incremental updates rather than full recalculation
- Pre-compute common metrics (moving averages, etc.)
- Implement score change thresholds to reduce noise
- Batch database queries for multiple tokens

---

## 8. CALIBRATION & VALIDATION

### 8.1 Score Calibration

**Backtesting Framework:**
```python
def backtest_scoring_model(historical_data, holding_period_days=7):
    results = []

    for token in historical_data:
        score = calculate_smart_buy_score(token.at_launch)
        actual_return = token.price_after_7d / token.price_at_launch - 1

        results.append({
            'score': score,
            'actual_return': actual_return,
            'predicted_success': score > 60
        })

    # Calculate metrics
    precision = calculate_precision(results)
    recall = calculate_recall(results)
    roi_by_score_bucket = calculate_roi_by_bucket(results)

    return {
        'precision': precision,
        'recall': recall,
        'roi_by_bucket': roi_by_score_bucket
    }
```

**Calibration Targets:**
- Score 80-100: >70% positive return rate
- Score 60-79: >50% positive return rate
- Score 40-59: ~40% positive return rate
- Score 0-39: <30% positive return rate

### 8.2 Continuous Improvement

**Metrics to Track:**
- Prediction accuracy by score range
- False positive rate (high score, negative return)
- False negative rate (low score, positive return)
- Average return by recommendation type
- Risk flag accuracy

**Feedback Loop:**
1. Track actual outcomes for all scored tokens
2. Analyze prediction errors monthly
3. Adjust factor weights based on performance
4. Add new detection algorithms as patterns evolve
5. Update thresholds based on market conditions

---

## APPENDIX A: FORMULA QUICK REFERENCE

### Normalization Functions
```
z_score_normalize(x, μ, σ) = (x - μ) / σ
min_max_normalize(x, min, max) = (x - min) / (max - min) × 100
sigmoid_normalize(x, k=1) = 100 / (1 + exp(-k × x))
```

### Statistical Measures
```
coefficient_of_variation = σ / μ
sharpe_ratio = (return - risk_free_rate) / σ
skewness = E[(X - μ)^3] / σ^3
kurtosis = E[(X - μ)^4] / σ^4 - 3
```

### Time Series Indicators
```
EMA_t = α × price_t + (1-α) × EMA_{t-1}
where α = 2 / (N + 1)

RSI = 100 - 100 / (1 + RS)
where RS = average_gain / average_loss

Bollinger Bands:
Upper = SMA + 2σ
Lower = SMA - 2σ
```

---

*End of Specification*
