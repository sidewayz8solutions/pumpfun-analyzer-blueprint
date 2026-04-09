# Pump.Fun Reputation System - Architecture Diagrams

## 1. High-Level System Architecture

```
                                    ┌─────────────────────────────────────┐
                                    │           USER INTERFACE            │
                                    │  (Wallet Lookup, Alerts, Reports)   │
                                    └─────────────────┬───────────────────┘
                                                      │
                                                      ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              API GATEWAY LAYER                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   /wallet    │  │   /token     │  │   /cluster   │  │   /alerts    │         │
│  │  /reputation │  │    /risk     │  │  /analyze    │  │   /stream    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────────────────────────────────────────────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│   REPUTATION ENGINE   │  │   PATTERN DETECTOR    │  │   ENTITY RESOLVER     │
│                       │  │                       │  │                       │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │
│  │  Score          │  │  │  │  Rug Pull       │  │  │  │  Wallet         │  │
│  │  Calculator     │  │  │  │  Detection      │  │  │  │  Clustering     │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  └─────────────────┘  │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │
│  │  Factor         │  │  │  │  Snipe          │  │  │  │  Social         │  │
│  │  Weights        │  │  │  │  Detection      │  │  │  │  Graph          │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  │  Analysis       │  │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  └─────────────────┘  │
│  │  Time Decay     │  │  │  │  Insider        │  │  │  ┌─────────────────┐  │
│  │  Model          │  │  │  │  Detection      │  │  │  │  Cross-Wallet   │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  │  Matching       │  │
└───────────────────────┘  └───────────────────────┘  │  └─────────────────┘  │
                                                        └───────────────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
┌───────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐
│   REAL-TIME           │  │   DATA STORAGE        │  │   ANALYTICS           │
│   PROCESSOR           │  │   LAYER               │  │   ENGINE              │
│                       │  │                       │  │                       │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │
│  │  Transaction    │  │  │  │  PostgreSQL     │  │  │  │  Trend          │  │
│  │  Stream         │  │  │  │  (Primary)      │  │  │  │  Analysis       │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  └─────────────────┘  │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │
│  │  Event          │  │  │  │  Redis          │  │  │  │  Reporting      │  │
│  │  Handler        │  │  │  │  (Cache)        │  │  │  │  Dashboard      │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  └─────────────────┘  │
│  ┌─────────────────┐  │  │  ┌─────────────────┐  │  │  ┌─────────────────┐  │
│  │  Alert          │  │  │  │  ClickHouse     │  │  │  │  Model          │  │
│  │  Generator      │  │  │  │  (Analytics)    │  │  │  │  Training       │  │
│  └─────────────────┘  │  │  └─────────────────┘  │  │  └─────────────────┘  │
└───────────────────────┘  └───────────────────────┘  └───────────────────────┘
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              DATA SOURCES                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Solana RPC  │  │  Pump.Fun    │  │  DEX APIs    │  │  Price       │         │
│  │              │  │  API         │  │  (Raydium,   │  │  Oracles     │         │
│  │              │  │              │  │  Jupiter)    │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘         │
└──────────────────────────────────────────────────────────────────────────────────┘
```

## 2. Reputation Score Calculation Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        REPUTATION CALCULATION PIPELINE                       │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │ Wallet Input │
    │   Address    │
    └──────┬───────┘
           │
           ▼
┌──────────────────────────┐
│  1. FETCH TRANSACTIONS   │
│     • Last 90 days       │
│     • All token swaps    │
│     • LP interactions    │
│     • Token creations    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  2. PATTERN DETECTION    │
│     • Rug pull patterns  │
│     • Sniping behavior   │
│     • Insider signals    │
│     • Dump patterns      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  3. FACTOR CALCULATION   │
│                          │
│  Positive Factors:       │
│  ✓ Long-term holding     │
│  ✓ Profitability         │
│  ✓ LP provision          │
│  ✓ Community building    │
│                          │
│  Negative Factors:       │
│  ✗ Confirmed rugs        │
│  ✗ Suspicious patterns   │
│  ✗ Coordinated activity  │
│  ✗ Honeypot creation     │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  4. TIME DECAY APPLY     │
│                          │
│  Recent events:  2.0x    │
│  7-30 days:      1.2x    │
│  30-90 days:     1.0x    │
│  90+ days:       0.5x    │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  5. CLUSTER ADJUSTMENT   │
│                          │
│  If in suspicious        │
│  cluster: -10 to -30     │
│                          │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│  6. FINAL SCORE          │
│                          │
│  Base: 50                │
│  + Positive (weighted)   │
│  - Negative              │
│  + Cluster adjustment    │
│  = Final (0-100)         │
│                          │
│  Category Assignment:    │
│  0-15:  CRITICAL         │
│  16-35: HIGH RISK        │
│  36-55: NEUTRAL          │
│  56-75: TRUSTWORTHY      │
│  76-100: REPUTABLE       │
└──────────┬───────────────┘
           │
           ▼
    ┌──────────────┐
    │ Store Result │
    │ Update Cache │
│
```

## 3. Real-Time Detection Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME THREAT DETECTION PIPELINE                     │
└─────────────────────────────────────────────────────────────────────────────┘

  New Transaction
  Detected on-chain
         │
         ▼
┌─────────────────────────┐
│ 1. PARSE TRANSACTION    │
│    • Extract wallets    │
│    • Identify program   │
│    • Classify type      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. IMMEDIATE CHECKS     │
│                         │
│ Is this a:              │
│ • LP removal? ──────┐   │
│ • Large token dump?─┼───┼──┐
│ • Token creation?   │   │  │
│ • First buy?        │   │  │
└──────────┬──────────┘   │  │
           │              │  │
           ▼              │  │
┌────────────────────────┐│  │
│ 3. PATTERN MATCHING    ││  │
│                        ││  │
│ Check for:             ││  │
│ • Instant rug pattern  ││  │
│ • Coordination signals ││  │
│ • Insider indicators   ││  │
│ • Bot behavior         ││  │
└──────────┬─────────────┘│  │
           │              │  │
     Pattern Found?      │  │
           │              │  │
      ┌────┴────┐         │  │
      │         │         │  │
     YES       NO         │  │
      │         │         │  │
      ▼         ▼         │  │
┌─────────┐ ┌─────────────┐│  │
│ CRITICAL│ │  Continue   ││  │
│  ALERT  │ │  Monitoring ││  │
└────┬────┘ └─────────────┘│  │
     │                     │  │
     ▼                     │  │
┌────────────────────────┐ │  │
│ 4. ALERT GENERATION    │ │  │
│                        │ │  │
│ • Create alert record  │ │  │
│ • Notify subscribers   │ │  │
│ • Update UI            │ │  │
│ • Log for analysis     │ │  │
└──────────┬─────────────┘ │  │
           │               │  │
           ▼               │  │
┌────────────────────────┐ │  │
│ 5. ASYNC PROCESSING    │ │  │
│    (Background)        │ │  │
│                        │ │  │
│ • Update reputation    │◄┘  │
│ • Recalculate cluster  │◄───┘
│ • Store metrics        │
│ • Trigger ML inference │
└────────────────────────┘
```

## 4. Wallet Clustering Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENTITY RESOLUTION (CLUSTERING)                        │
└─────────────────────────────────────────────────────────────────────────────┘

    Seed Wallet
    Provided
        │
        ▼
┌─────────────────────────┐
│ 1. GATHER CANDIDATES    │
│                         │
│ Find wallets that:      │
│ • Received funds from   │
│   seed wallet           │
│ • Sent profits to seed  │
│ • Interacted with same  │
│   contracts             │
│ • Had synchronized txs  │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. SIGNAL ANALYSIS      │
│                         │
│ For each candidate:     │
│                         │
│ Funding Signal:         │
│ ┌─────────────────┐     │
│ │ Same funder?    │─────┼──► +0.90 confidence
│ └─────────────────┘     │
│                         │
│ Profit Signal:          │
│ ┌─────────────────┐     │
│ │ Same recipient? │─────┼──► +0.85 confidence
│ └─────────────────┘     │
│                         │
│ Behavior Signal:        │
│ ┌─────────────────┐     │
│ │ Same patterns?  │─────┼──► +0.75 confidence
│ └─────────────────┘     │
│                         │
│ Timing Signal:          │
│ ┌─────────────────┐     │
│ │ Synced trades?  │─────┼──► +0.70 confidence
│ └─────────────────┘     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 3. CONFIDENCE MERGE     │
│                         │
│ Combined = weighted     │
│ average with boost for  │
│ multiple signals        │
│                         │
│ If confidence > 0.70:   │
│   Add to cluster        │
│                         │
│ If confidence > 0.50:   │
│   Flag for review       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 4. EXPAND SEARCH        │
│                         │
│ For each new cluster    │
│ member, repeat analysis │
│ (BFS up to depth 3)     │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 5. CLUSTER FINALIZATION │
│                         │
│ • Assign cluster ID     │
│ • Identify primary      │
│   (control) wallet      │
│ • Calculate aggregate   │
│   reputation            │
│ • Store relationships   │
└──────────┬──────────────┘
           │
           ▼
    ┌──────────────┐
    │ Return       │
    │ Cluster Info │
    └──────────────┘
```

## 5. Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW DIAGRAM                               │
└─────────────────────────────────────────────────────────────────────────────┘

  Solana Blockchain
         │
         │ New blocks, transactions
         ▼
┌────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION SERVICE                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ RPC Client  │  │ WebSocket   │  │ Historical Backfill     │ │
│  │ (Helius,    │  │ Listener    │  │ (On-demand)             │ │
│  │  QuickNode) │  │             │  │                         │ │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘ │
└─────────┼────────────────┼─────────────────────┼───────────────┘
          │                │                     │
          └────────────────┴─────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                     MESSAGE QUEUE (Redis/RabbitMQ)              │
│                                                                 │
│  Topics:                                                        │
│  • transactions.new                                             │
│  • transactions.token_swap                                      │
│  • transactions.lp_event                                        │
│  • tokens.new                                                   │
│  • alerts.critical                                              │
└────────────────────────────────────────────────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  REAL-TIME    │  │   PATTERN     │  │   ANALYTICS   │
│  PROCESSOR    │  │   DETECTION   │  │   WORKER      │
│               │  │   ENGINE      │  │               │
│ • Quick checks│  │               │  │ • Aggregation │
│ • Alert gen   │  │ • Deep        │  │ • Reporting   │
│ • Cache upd   │  │   analysis    │  │ • ML training │
└───────┬───────┘  └───────┬───────┘  └───────┬───────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PostgreSQL (Primary)                                    │   │
│  │  • Wallets, transactions, patterns, clusters            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Redis (Cache)                                           │   │
│  │  • Hot reputation scores, session data                  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ClickHouse (Analytics)                                  │   │
│  │  • Time-series metrics, aggregated statistics           │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                        API LAYER                                │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ REST API    │  │ WebSocket   │  │ GraphQL                 │ │
│  │ (Primary)   │  │ (Real-time  │  │ (Flexible queries)      │ │
│  │             │  │  alerts)    │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                      CLIENT APPLICATIONS                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ Web App     │  │ Mobile App  │  │ Third-party             │ │
│  │ (React)     │  │ (React      │  │ Integrations            │ │
│  │             │  │  Native)    │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## 6. Alert System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ALERT SYSTEM FLOW                                  │
└─────────────────────────────────────────────────────────────────────────────┘

  Pattern Detection
  System
        │
        │ Alert Trigger
        ▼
┌─────────────────────────┐
│ 1. ALERT CLASSIFICATION │
│                         │
│ Severity:               │
│ • CRITICAL (Score 0-15) │
│ • HIGH (Score 16-35)    │
│ • MEDIUM (Score 36-55)  │
│ • LOW (Score 56+)       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 2. ALERT ENRICHMENT     │
│                         │
│ Add context:            │
│ • Wallet reputation     │
│ • Token info            │
│ • Related wallets       │
│ • Historical patterns   │
│ • Price impact          │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 3. ALERT ROUTING        │
│                         │
│ Based on:               │
│ • User preferences      │
│ • Subscription level    │
│ • Alert type            │
└──────────┬──────────────┘
           │
     ┌─────┴─────┬─────────┬─────────┐
     │           │         │         │
     ▼           ▼         ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│In-App  │ │Push    │ │Discord │ │Webhook │
│Notif   │ │Notif   │ │Bot     │ │API     │
│        │ │        │ │        │ │        │
│Immediate│ │Immediate│ │Immediate│ │Immediate│
│for CRIT│ │for HIGH+│ │for ALL │ │for ALL │
└────────┘ └────────┘ └────────┘ └────────┘
           │
           ▼
┌─────────────────────────┐
│ 4. ALERT STORAGE        │
│                         │
│ Store for:              │
│ • Audit trail           │
│ • Analytics             │
│ • User history          │
│ • Model training        │
└─────────────────────────┘
```

---

## Component Interaction Summary

| Component | Input | Output | Frequency |
|-----------|-------|--------|-----------|
| Data Ingestion | Blockchain RPC | Message Queue | Real-time |
| Pattern Detection | Transaction Stream | Alerts, Flags | Real-time |
| Reputation Engine | Transaction History | Score Updates | Every 15 min |
| Entity Resolver | Wallet Addresses | Clusters | Daily |
| Analytics Engine | All Data | Reports, Metrics | Hourly |
| API Layer | User Requests | JSON Responses | On-demand |
