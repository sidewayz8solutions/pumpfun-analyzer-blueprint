# Pump.Fun Meme Coin Reputation & Rugger Detection System
## Comprehensive Technical Specification

---

## Executive Summary

This document outlines a comprehensive reputation and risk detection system designed specifically for analyzing wallet behavior on Pump.Fun and related Solana meme coin ecosystems. The system combines on-chain transaction analysis, behavioral pattern recognition, and machine learning to identify high-risk actors, detect rug pulls in progress, and provide actionable intelligence for traders.

---

## 1. WALLET ANALYSIS FRAMEWORK

### 1.1 Historical Data Analysis

#### Core Transaction Data Points
```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSACTION DATA LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  • Token Transfers (SPL tokens)                                 │
│  • SOL transfers                                                │
│  • DEX Swaps (Raydium, Orca, Jupiter)                           │
│  • Liquidity Pool Interactions                                  │
│  • Token Account Creation/Closure                               │
│  • Program Interactions (Pump.Fun, Raydium, etc.)               │
│  • Account Creation Patterns                                    │
│  • Staking/Vesting Activities                                   │
└─────────────────────────────────────────────────────────────────┘
```

#### Temporal Analysis Windows
| Window | Purpose | Weight |
|--------|---------|--------|
| 24 hours | Immediate behavior, active scams | 1.5x |
| 7 days | Short-term patterns | 1.2x |
| 30 days | Medium-term behavior | 1.0x |
| 90 days | Historical context | 0.8x |
| All-time | Lifetime reputation | 0.6x |

#### Key Metrics to Track

**Volume Metrics**
- Total SOL transacted (in/out)
- Total token volume traded
- Number of unique tokens interacted with
- Average transaction size
- Transaction frequency

**Timing Metrics**
- Time of first interaction with token
- Time between token creation and first buy
- Hold duration distribution
- Sell timing relative to milestones

**Relationship Metrics**
- Number of unique counterparties
- Clustering coefficient
- Interaction with known addresses
- Cross-wallet fund flows

### 1.2 Transaction Pattern Analysis

#### Pattern Recognition Framework

```python
class TransactionPattern:
    """
    Core pattern detection for wallet behavior analysis
    """
    
    PATTERN_TYPES = {
        # Buying Patterns
        'EARLY_BUYER': 'Purchase within first 5 minutes of token launch',
        'SNIPER': 'Purchase within first 30 seconds with high gas',
        'ACCUMULATOR': 'Multiple small buys over time',
        'WHALE_BUY': 'Single purchase >5% of supply',
        
        # Selling Patterns  
        'QUICK_FLIP': 'Sell within 1 hour of purchase',
        'GRADUAL_EXIT': 'Multiple sells over extended period',
        'DUMP': 'Sell >50% of holdings in single transaction',
        'RUG_PULL': 'Remove liquidity + dump tokens simultaneously',
        
        # Liquidity Patterns
        'LP_CREATOR': 'Created liquidity pool for token',
        'LP_REMOVER': 'Removed liquidity from pool',
        'LP_ADDER': 'Added liquidity to existing pool',
        
        # Token Creation
        'TOKEN_CREATOR': 'Deployed token contract',
        'MINT_AUTHORITY': 'Holds mint authority',
        'FREEZE_AUTHORITY': 'Holds freeze authority',
    }
```

#### Behavioral Signature Extraction

```python
class BehavioralSignature:
    """
    Extract unique behavioral fingerprints from wallet history
    """
    
    def extract_signature(self, wallet_address: str) -> dict:
        return {
            # Temporal Patterns
            'preferred_trading_hours': self.get_active_hours(),
            'avg_hold_time': self.calculate_avg_hold(),
            'reaction_time_to_new_tokens': self.measure_reaction_time(),
            
            # Size Patterns
            'typical_position_size': self.get_position_distribution(),
            'risk_tolerance_score': self.calculate_risk_score(),
            
            # Strategy Patterns
            'profit_taking_behavior': self.analyze_exit_patterns(),
            'loss_cutting_behavior': self.analyze_stop_loss(),
            'rebuy_patterns': self.detect_dca_behavior(),
            
            # Social Patterns
            'copy_trading_score': self.detect_copy_trading(),
            'herd_behavior_score': self.detect_herd_behavior(),
            'contrarian_score': self.detect_contrarian_behavior(),
        }
```

### 1.3 Cross-Contract Behavior Tracking

#### Multi-Contract Analysis

```python
class CrossContractAnalyzer:
    """
    Track behavior across multiple token contracts and DEXs
    """
    
    def analyze_cross_contract_behavior(self, wallet: str) -> dict:
        analysis = {
            'token_diversity': self.count_unique_tokens(),
            'repeat_token_creator': self.detect_creator_patterns(),
            'serial_launcher': self.detect_serial_launching(),
            'cross_token_funding': self.trace_funding_chains(),
            'coordinated_activity': self.detect_coordination(),
        }
        return analysis
    
    def detect_serial_launching(self) -> dict:
        """
        Detect wallets that repeatedly create tokens
        """
        indicators = {
            'tokens_created_count': 0,
            'avg_time_between_launches': 0,
            'success_rate': 0,  # % of tokens that didn't rug
            'common_patterns': [],  # Similar names, similar supply, etc.
            'cross_promotion': [],  # Same socials across tokens
        }
        return indicators
```

---

## 2. RUGGER DETECTION PATTERNS

### 2.1 Rug Pull Pattern Library

#### Classic Rug Pull Signatures

```python
RUG_PULL_PATTERNS = {
    
    'LIQUIDITY_RUG': {
        'description': 'Remove liquidity and dump tokens',
        'sequence': [
            'CREATE_LP',
            'ACCUMULATE_TOKENS',  # Optional - may already hold
            'REMOVE_LIQUIDITY',
            'DUMP_TOKENS',
            'TRANSFER_REMAINING',
        ],
        'timeframe': 'hours_to_days',
        'confidence_threshold': 0.85,
        'indicators': {
            'lp_removal_percentage': '>90%',
            'token_dump_percentage': '>50%',
            'time_lp_to_dump': '<1 hour',
        }
    },
    
    'HONEYPOT_RUG': {
        'description': 'Create token that can only be bought, not sold',
        'sequence': [
            'CREATE_TOKEN_WITH_SELL_RESTRICTION',
            'PROMOTE_TOKEN',
            'ACCUMULATE_BUYS',
            'DISABLE_SELLING',
            'DUMP_VIA_EXCLUDED_ADDRESS',
        ],
        'indicators': {
            'sell_transactions': 0,
            'buy_to_sell_ratio': 'infinite',
            'special_wallets_allowed_sell': True,
        }
    },
    
    'PUMP_AND_DUMP': {
        'description': 'Artificially inflate price then dump',
        'sequence': [
            'CREATE_TOKEN',
            'WASH_TRADING',  # Buy from self to create volume
            'MARKETING_PUSH',
            'RETAIL_FOMO',
            'COORDINATED_DUMP',
        ],
        'indicators': {
            'wash_trading_volume': '>30% of total',
            'price_increase': '>500% in <1 hour',
            'dump_coordination': 'Multiple wallets selling simultaneously',
        }
    },
    
    'SLOW_RUG': {
        'description': 'Gradual draining over extended period',
        'sequence': [
            'CREATE_TOKEN',
            'BUILD_COMMUNITY',
            'GRADUAL_LP_REMOVAL',
            'DEVELOPER_SELLS',
            'ABANDON_PROJECT',
        ],
        'indicators': {
            'lp_removal_pattern': 'Small amounts over weeks',
            'dev_wallet_selling': 'Consistent selling pressure',
            'community_engagement_drop': '>80%',
        }
    },
    
    'MIGRATION_RUG': {
        'description': 'Rug during/after Raydium migration',
        'sequence': [
            'LAUNCH_ON_PUMPFUN',
            'REACH_BONDING_CURVE',
            'MIGRATE_TO_RAYDIUM',
            'REMOVE_LP_OR_DUMP',
        ],
        'indicators': {
            'post_migration_dump': '>50% within 1 hour',
            'lp_removal_after_migration': True,
            'pre_migration_accumulation': True,
        }
    }
}
```

### 2.2 Developer Wallet Red Flags

#### Developer Risk Indicators

```python
DEV_WALLET_RED_FLAGS = {
    
    'CRITICAL': {  # Immediate high-risk classification
        'mint_authority_retained': {
            'weight': 100,
            'description': 'Can mint unlimited tokens',
            'detection': 'check_mint_authority()',
        },
        'freeze_authority_retained': {
            'weight': 80,
            'description': 'Can freeze token accounts',
            'detection': 'check_freeze_authority()',
        },
        'hidden_mint_function': {
            'weight': 100,
            'description': 'Custom program allows minting',
            'detection': 'analyze_token_program()',
        },
        'honeypot_mechanism': {
            'weight': 100,
            'description': 'Contract prevents selling',
            'detection': 'simulate_sell_transaction()',
        },
    },
    
    'HIGH': {  # Strong suspicion indicators
        'lp_tokens_not_burned': {
            'weight': 60,
            'description': 'Can remove liquidity at any time',
            'detection': 'check_lp_token_holder()',
        },
        'large_dev_allocation': {
            'weight': 50,
            'description': 'Dev holds >20% of supply',
            'detection': 'calculate_dev_allocation()',
        },
        'no_lock_period': {
            'weight': 40,
            'description': 'Liquidity not locked',
            'detection': 'check_lp_lock_status()',
        },
        'anonymous_deployer': {
            'weight': 30,
            'description': 'No social presence/history',
            'detection': 'analyze_deployer_history()',
        },
    },
    
    'MEDIUM': {  # Concerning but not definitive
        'recent_wallet_creation': {
            'weight': 25,
            'description': 'Wallet created <7 days before token',
            'detection': 'check_wallet_age()',
        },
        'funded_via_mixer': {
            'weight': 35,
            'description': 'Initial funds from privacy service',
            'detection': 'trace_funding_source()',
        },
        'multiple_token_deployments': {
            'weight': 30,
            'description': 'Deployed >3 tokens in 30 days',
            'detection': 'count_token_deployments()',
        },
        'copycat_token': {
            'weight': 20,
            'description': 'Similar to existing popular token',
            'detection': 'compare_token_metadata()',
        },
    }
}
```

### 2.3 Sniping and Insider Trading Patterns

#### Snipe Detection Algorithm

```python
class SnipeDetector:
    """
    Detect wallets that consistently buy tokens at optimal early moments
    """
    
    SNIPE_INDICATORS = {
        'time_to_first_buy': {
            'ultra_snipe': '<10 seconds',      # Score: 100
            'fast_snipe': '<30 seconds',       # Score: 80
            'early_snipe': '<2 minutes',       # Score: 60
            'early_buyer': '<5 minutes',       # Score: 40
        },
        
        'consistency_score': {
            'bot_like': '>90% first 100 buyers',  # Score: 100
            'highly_consistent': '>70%',          # Score: 80
            'often_early': '>50%',                # Score: 60
        },
        
        'gas_premium_paid': {
            'extreme': '>10x average',    # Score: 80
            'high': '>5x average',        # Score: 60
            'elevated': '>2x average',    # Score: 40
        },
        
        'success_rate': {
            'uncanny': '>80% profitable',    # Score: 100
            'suspicious': '>65% profitable', # Score: 70
            'skilled': '>50% profitable',    # Score: 40
        }
    }
    
    def calculate_snipe_score(self, wallet: str) -> dict:
        """
        Calculate comprehensive sniping behavior score
        """
        return {
            'snipe_score': 0,  # 0-100
            'snipe_tier': 'none',  # none, suspected, confirmed_bot, insider
            'evidence': [],
            'related_wallets': [],  # Clustered sniper wallets
        }
```

#### Insider Trading Detection

```python
class InsiderDetector:
    """
    Detect wallets with suspicious pre-launch knowledge
    """
    
    INSIDER_INDICATORS = [
        {
            'name': 'dev_wallet_funding',
            'description': 'Received funds from token creator before launch',
            'detection_method': 'trace_funding_24h_before_launch',
            'confidence': 0.9,
        },
        {
            'name': 'social_connection',
            'description': 'Connected to dev via previous transactions',
            'detection_method': 'analyze_social_graph',
            'confidence': 0.7,
        },
        {
            'name': 'perfect_timing',
            'description': 'Consistently buys at absolute bottom',
            'detection_method': 'analyze_entry_timing_distribution',
            'confidence': 0.8,
        },
        {
            'name': 'information_edge',
            'description': 'Buys before major announcements',
            'detection_method': 'correlate_buys_with_events',
            'confidence': 0.85,
        },
    ]
```

### 2.4 Liquidity Removal Patterns

```python
class LiquidityPatternAnalyzer:
    """
    Analyze liquidity pool interactions for rug pull detection
    """
    
    LP_RUG_PATTERNS = {
        
        'INSTANT_RUG': {
            'pattern': 'Remove >90% LP within 1 hour of creation',
            'severity': 'CRITICAL',
            'detection': self.detect_instant_rug,
        },
        
        'GRADUAL_DRAIN': {
            'pattern': 'Remove 5-20% LP daily over multiple days',
            'severity': 'HIGH',
            'detection': self.detect_gradual_drain,
        },
        
        'MIGRATION_RUG': {
            'pattern': 'Remove LP immediately after Raydium migration',
            'severity': 'CRITICAL',
            'detection': self.detect_migration_rug,
        },
        
        'EMERGENCY_REMOVE': {
            'pattern': 'Remove LP during high volatility',
            'severity': 'MEDIUM',
            'detection': self.detect_emergency_remove,
        },
        
        'PARTIAL_REMOVE_DUMP': {
            'pattern': 'Remove LP, dump tokens, repeat',
            'severity': 'HIGH',
            'detection': self.detect_cyclic_dump,
        },
    }
    
    def analyze_lp_behavior(self, token_address: str) -> dict:
        """
        Comprehensive LP analysis for a token
        """
        return {
            'lp_creation_time': None,
            'lp_creator_wallet': None,
            'lp_tokens_burned': False,
            'lp_lock_info': {
                'locked': False,
                'unlock_time': None,
                'lock_provider': None,
            },
            'removal_history': [],
            'current_lp_depth': 0,
            'rug_risk_score': 0,
        }
```

### 2.5 Token Dumping Patterns

```python
class DumpingPatternDetector:
    """
    Detect coordinated or suspicious token dumping
    """
    
    DUMP_PATTERNS = {
        
        'SINGLE_MASSIVE_DUMP': {
            'criteria': 'Sell >30% of supply in one transaction',
            'impact': 'CRITICAL',
            'typical_actor': 'Dev wallet, whale',
        },
        
        'COORDINATED_DUMP': {
            'criteria': 'Multiple wallets dump within 5 minutes',
            'impact': 'CRITICAL',
            'typical_actor': 'Organized group, insider circle',
            'detection_method': 'correlate_sell_timing',
        },
        
        'GRADUAL_DUMP': {
            'criteria': 'Consistent selling over days/weeks',
            'impact': 'HIGH',
            'typical_actor': 'Patient rugger, slow exit',
        },
        
        'FOMO_DUMP': {
            'criteria': 'Dump immediately after price spike',
            'impact': 'MEDIUM',
            'typical_actor': 'Experienced trader, bot',
        },
        
        'STOP_LOSS_CASCADE': {
            'criteria': 'Multiple stop losses triggered',
            'impact': 'MEDIUM',
            'typical_actor': 'Market mechanism, not malicious',
        },
    }
    
    def detect_dump_coordination(self, sells: list) -> dict:
        """
        Detect if multiple sells are coordinated
        """
        analysis = {
            'is_coordinated': False,
            'coordination_score': 0,
            'wallet_cluster': [],
            'time_window': 0,
            'total_impact_percentage': 0,
        }
        
        # Check timing correlation
        timestamps = [s['timestamp'] for s in sells]
        time_variance = self.calculate_variance(timestamps)
        
        if time_variance < 300:  # Within 5 minutes
            analysis['is_coordinated'] = True
            analysis['coordination_score'] += 50
            
        # Check wallet relationships
        wallets = [s['wallet'] for s in sells]
        relationships = self.analyze_wallet_relationships(wallets)
        
        if relationships['has_connections']:
            analysis['coordination_score'] += 30
            analysis['wallet_cluster'] = relationships['clusters']
            
        return analysis
```

### 2.6 Bot Coordination Indicators

```python
class BotCoordinationDetector:
    """
    Detect coordinated bot activity
    """
    
    BOT_INDICATORS = {
        
        'TIMING_SYNCHRONIZATION': {
            'description': 'Multiple transactions in same block/slot',
            'threshold': '>5 related txs in same slot',
            'confidence': 0.85,
        },
        
        'BEHAVIORAL_CLONE': {
            'description': 'Identical transaction patterns',
            'threshold': '>90% pattern similarity',
            'confidence': 0.9,
        },
        
        'FUNDING_COMMONALITY': {
            'description': 'Same funding source',
            'threshold': 'Same wallet funded all within 24h',
            'confidence': 0.95,
        },
        
        'PROFIT_SHARING': {
            'description': 'Profits flow to common wallet',
            'threshold': '>50% of profits to same address',
            'confidence': 0.9,
        },
        
        'GAS_PATTERN': {
            'description': 'Similar gas/priority fee patterns',
            'threshold': 'Standard deviation <10%',
            'confidence': 0.75,
        },
    }
    
    def detect_bot_cluster(self, wallets: list) -> dict:
        """
        Identify if wallets are part of a bot network
        """
        return {
            'is_bot_cluster': False,
            'cluster_confidence': 0,
            'cluster_size': 0,
            'control_wallet': None,  # Master wallet
            'behavioral_fingerprint': {},
            'estimated_profits': 0,
        }
```

---

## 3. REPUTATION SCORING SYSTEM

### 3.1 Scoring Methodology

#### Base Reputation Formula

```python
class ReputationScorer:
    """
    Calculate comprehensive reputation score for wallets
    """
    
    def calculate_reputation(self, wallet: str) -> dict:
        """
        Main reputation calculation
        """
        # Base score starts at 50 (neutral)
        base_score = 50
        
        # Calculate all components
        positive_score = self.calculate_positive_factors(wallet)
        negative_score = self.calculate_negative_factors(wallet)
        
        # Apply time decay
        time_decay_factor = self.calculate_time_decay(wallet)
        
        # Calculate final score
        final_score = base_score + (positive_score * time_decay_factor) - negative_score
        
        # Clamp to 0-100 range
        final_score = max(0, min(100, final_score))
        
        return {
            'overall_score': final_score,
            'category': self.get_category(final_score),
            'positive_factors': positive_score,
            'negative_factors': negative_score,
            'time_decay': time_decay_factor,
            'confidence': self.calculate_confidence(wallet),
            'last_updated': datetime.now(),
        }
```

#### Positive Factors (Reputation Builders)

```python
POSITIVE_FACTORS = {
    
    'LONG_TERM_HOLDER': {
        'description': 'Holds tokens for extended periods',
        'calculation': 'avg_hold_time > 30 days',
        'base_points': 15,
        'tiers': {
            '>90_days': 25,
            '>60_days': 20,
            '>30_days': 15,
            '>14_days': 10,
            '>7_days': 5,
        }
    },
    
    'CONSISTENT_PROFITABILITY': {
        'description': 'Profitable trading record',
        'calculation': 'win_rate > 50% over 20+ trades',
        'base_points': 20,
        'tiers': {
            '>80%': 30,
            '>65%': 25,
            '>50%': 20,
        }
    },
    
    'LIQUIDITY_PROVIDER': {
        'description': 'Provides liquidity to pools',
        'calculation': 'LP positions created/maintained',
        'base_points': 15,
        'multiplier': 'based_on_lp_duration',
    },
    
    'COMMUNITY_BUILDER': {
        'description': 'Creates tokens with lasting communities',
        'calculation': 'tokens_created with active_community > 30 days',
        'base_points': 25,
    },
    
    'TRANSPARENT_DEVELOPER': {
        'description': 'Public identity, doxxed team',
        'calculation': 'verified_identity + active_communication',
        'base_points': 20,
    },
    
    'TOKEN_BURNER': {
        'description': 'Burns tokens/lp tokens',
        'calculation': 'percentage_of_supply_burned',
        'base_points': 10,
        'multiplier': 'burn_percentage',
    },
    
    'HELPER_WALLET': {
        'description': 'Helps other users, educational content',
        'calculation': 'manual_review + community_reports',
        'base_points': 15,
    },
    
    'VETERAN_TRADER': {
        'description': 'Long history, survived multiple cycles',
        'calculation': 'wallet_age > 1 year + active_trading',
        'base_points': 10,
    },
}
```

#### Negative Factors (Reputation Destroyers)

```python
NEGATIVE_FACTORS = {
    
    'CONFIRMED_RUGGER': {
        'description': 'Executed confirmed rug pull',
        'calculation': 'pattern_match == RUG_PULL',
        'base_points': -100,
        'permanent': True,
        'appealable': False,
    },
    
    'RUG_PULL_ATTEMPT': {
        'description': 'Attempted rug but failed',
        'calculation': 'detected_preparation_patterns',
        'base_points': -80,
        'permanent': True,
        'appealable': True,
    },
    
    'SERIAL_TOKEN_CREATOR': {
        'description': 'Creates multiple tokens that fail',
        'calculation': 'tokens_created > 3 with <50% success',
        'base_points': -40,
        'escalation': '-10 per additional failed token',
    },
    
    'COORDINATED_DUMPER': {
        'description': 'Part of coordinated dump group',
        'calculation': 'detected_coordination_pattern',
        'base_points': -60,
    },
    
    'SNIPER_BOT': {
        'description': 'Automated sniping behavior',
        'calculation': 'snipe_score > 80',
        'base_points': -30,
        'note': 'Not necessarily malicious, but flagged',
    },
    
    'INSIDER_TRADER': {
        'description': 'Suspected insider trading',
        'calculation': 'insider_score > 70',
        'base_points': -50,
    },
    
    'WASH_TRADER': {
        'description': 'Artificial volume creation',
        'calculation': 'wash_trading_detected',
        'base_points': -45,
    },
    
    'HONEYPOT_CREATOR': {
        'description': 'Created honeypot token',
        'calculation': 'honeypot_pattern_confirmed',
        'base_points': -100,
        'permanent': True,
    },
    
    'LP_ABUSER': {
        'description': 'Repeatedly removes LP maliciously',
        'calculation': 'multiple_lp_removals_with_dump',
        'base_points': -50,
    },
    
    'COPYCAT_SCAMMER': {
        'description': 'Creates tokens mimicking legitimate projects',
        'calculation': 'copycat_detection_score > 80',
        'base_points': -35,
    },
    
    'SYBIL_ATTACKER': {
        'description': 'Multiple fake accounts for manipulation',
        'calculation': 'sybil_cluster_confirmed',
        'base_points': -60,
    },
    
    'FUNDED_VIA_MIXER': {
        'description': 'Uses privacy services to hide origin',
        'calculation': 'funding_from_privacy_service',
        'base_points': -20,
        'note': 'Not always malicious, but suspicious',
    },
}
```

### 3.2 Weight System

```python
class WeightCalculator:
    """
    Calculate dynamic weights based on context
    """
    
    WEIGHT_FACTORS = {
        
        'RECENCY_MULTIPLIER': {
            'description': 'Recent behavior weighted more heavily',
            'formula': 'weight * (2 ^ (-days_ago / 30))',
            'example': {
                'today': 2.0,
                '7_days': 1.6,
                '30_days': 1.0,
                '90_days': 0.5,
                '1_year': 0.25,
            }
        },
        
        'FREQUENCY_MULTIPLIER': {
            'description': 'Repeated behavior increases weight',
            'formula': 'base_weight * log10(count + 1)',
            'example': {
                '1_occurrence': 1.0,
                '5_occurrences': 1.7,
                '10_occurrences': 2.0,
                '50_occurrences': 2.7,
            }
        },
        
        'SEVERITY_MULTIPLIER': {
            'description': 'Impact magnitude affects weight',
            'formula': 'weight * (impact_usd / 10000) ^ 0.5',
        },
        
        'CONTEXT_MULTIPLIER': {
            'description': 'Market conditions affect severity',
            'bull_market': 1.2,  # More opportunities, less excuse
            'bear_market': 0.9,  # Survival mode
            'high_volatility': 1.1,
        },
    }
```

### 3.3 Time Decay System

```python
class TimeDecayCalculator:
    """
    Apply time-based decay to historical behaviors
    """
    
    DECAY_MODELS = {
        
        'EXPONENTIAL_DECAY': {
            'description': 'Standard exponential decay',
            'formula': 'value * e^(-lambda * t)',
            'lambda': 0.023,  # ~50% decay in 30 days
            'use_for': ['minor_infractions', 'positive_behavior'],
        },
        
        'STEP_DECAY': {
            'description': 'Decay in discrete steps',
            'schedule': {
                '0_days': 1.0,
                '30_days': 0.75,
                '90_days': 0.5,
                '180_days': 0.25,
                '365_days': 0.1,
            },
            'use_for': ['moderate_infractions'],
        },
        
        'NO_DECAY': {
            'description': 'Permanent record',
            'formula': 'value * 1.0',
            'use_for': ['confirmed_rugs', 'honeypots', 'major_scams'],
        },
        
        'RECOVERY_DECAY': {
            'description': 'Can recover with good behavior',
            'formula': 'max(0, value - recovery_rate * t)',
            'recovery_rate': 5,  # Points per month
            'use_for': ['suspicious_behavior', 'minor_risk_flags'],
        },
    }
```

### 3.4 Wallet Clustering Impact

```python
class ClusterReputationCalculator:
    """
    Calculate reputation for wallet clusters
    """
    
    def calculate_cluster_reputation(self, cluster_id: str) -> dict:
        """
        Aggregate reputation across wallet cluster
        """
        wallets = self.get_cluster_wallets(cluster_id)
        
        # Calculate individual scores
        individual_scores = [self.get_reputation(w) for w in wallets]
        
        # Weight by activity level
        weighted_scores = []
        for wallet, score in zip(wallets, individual_scores):
            activity_weight = self.calculate_activity_weight(wallet)
            weighted_scores.append(score * activity_weight)
        
        # Cluster-level penalties
        cluster_penalties = self.calculate_cluster_penalties(cluster_id)
        
        # Final cluster score
        cluster_score = sum(weighted_scores) / len(weighted_scores) + cluster_penalties
        
        return {
            'cluster_score': cluster_score,
            'individual_scores': dict(zip(wallets, individual_scores)),
            'cluster_penalties': cluster_penalties,
            'cluster_size': len(wallets),
            'primary_wallet': self.identify_primary_wallet(wallets),
        }
    
    def calculate_cluster_penalties(self, cluster_id: str) -> float:
        """
        Additional penalties for coordinated behavior
        """
        penalties = 0
        
        # Coordination penalty
        if self.detected_coordination(cluster_id):
            penalties -= 20
            
        # Size penalty (larger clusters more suspicious)
        size = self.get_cluster_size(cluster_id)
        if size > 10:
            penalties -= 10
        if size > 50:
            penalties -= 20
            
        # Activity concentration penalty
        if self.high_activity_concentration(cluster_id):
            penalties -= 15
            
        return penalties
```

---

## 4. ENTITY RESOLUTION SYSTEM

### 4.1 Wallet Clustering Methodology

```python
class WalletClusterer:
    """
    Identify wallets controlled by the same entity
    """
    
    CLUSTERING_SIGNALS = {
        
        'FUNDING_RELATIONSHIP': {
            'weight': 0.90,
            'description': 'Same wallet funded multiple wallets',
            'detection': self.trace_funding_sources,
            'confidence_boost': 0.15,
        },
        
        'PROFIT_CONVERGENCE': {
            'weight': 0.85,
            'description': 'Profits flow to common wallet',
            'detection': self.trace_profit_flows,
            'confidence_boost': 0.12,
        },
        
        'TEMPORAL_CORRELATION': {
            'weight': 0.70,
            'description': 'Transactions occur in synchronized patterns',
            'detection': self.analyze_timing_patterns,
            'confidence_boost': 0.10,
        },
        
        'BEHAVIORAL_FINGERPRINT': {
            'weight': 0.75,
            'description': 'Identical trading patterns and preferences',
            'detection': self.compare_behavioral_signatures,
            'confidence_boost': 0.10,
        },
        
        'GAS_PATTERN': {
            'weight': 0.60,
            'description': 'Similar gas/fee settings',
            'detection': self.analyze_gas_patterns,
            'confidence_boost': 0.05,
        },
        
        'CONTRACT_INTERACTION': {
            'weight': 0.65,
            'description': 'Interact with same set of contracts',
            'detection': self.compare_contract_interactions,
            'confidence_boost': 0.08,
        },
        
        'IP_METADATA': {
            'weight': 0.80,
            'description': 'Same IP/origin (if available)',
            'detection': self.analyze_connection_metadata,
            'confidence_boost': 0.15,
        },
    }
```

### 4.2 Cross-Wallet Pattern Matching

```python
class CrossWalletAnalyzer:
    """
    Match patterns across multiple wallets
    """
    
    def find_pattern_matches(self, wallets: list) -> dict:
        """
        Find common patterns across wallet set
        """
        patterns = {
            'common_funding_source': self.find_common_funder(wallets),
            'common_profit_destination': self.find_common_destination(wallets),
            'synchronized_trading': self.detect_synchronization(wallets),
            'identical_strategies': self.compare_strategies(wallets),
            'shared_counterparties': self.find_common_counterparties(wallets),
        }
        return patterns
    
    def calculate_similarity_score(self, wallet1: str, wallet2: str) -> float:
        """
        Calculate similarity score between two wallets (0-1)
        """
        features = {
            'trading_hours': self.compare_trading_hours(wallet1, wallet2),
            'position_sizes': self.compare_position_sizes(wallet1, wallet2),
            'hold_times': self.compare_hold_times(wallet1, wallet2),
            'token_preferences': self.compare_token_preferences(wallet1, wallet2),
            'exit_strategies': self.compare_exit_strategies(wallet1, wallet2),
            'contract_interactions': self.compare_contracts(wallet1, wallet2),
        }
        
        # Weighted average
        weights = {
            'trading_hours': 0.15,
            'position_sizes': 0.15,
            'hold_times': 0.20,
            'token_preferences': 0.20,
            'exit_strategies': 0.20,
            'contract_interactions': 0.10,
        }
        
        similarity = sum(features[k] * weights[k] for k in features)
        return similarity
```

### 4.3 Social Graph Analysis

```python
class SocialGraphAnalyzer:
    """
    Build and analyze social graph of wallet interactions
    """
    
    def build_interaction_graph(self, center_wallet: str, depth: int = 2) -> dict:
        """
        Build interaction graph around a wallet
        """
        graph = {
            'nodes': [],  # Wallets
            'edges': [],  # Transactions between wallets
            'clusters': [],  # Detected clusters
            'centrality_scores': {},  # Importance of each wallet
        }
        
        # BFS to build graph
        visited = set()
        queue = [(center_wallet, 0)]
        
        while queue:
            wallet, current_depth = queue.pop(0)
            
            if wallet in visited or current_depth > depth:
                continue
                
            visited.add(wallet)
            graph['nodes'].append(wallet)
            
            # Find interactions
            interactions = self.get_wallet_interactions(wallet)
            
            for interaction in interactions:
                counterparty = interaction['counterparty']
                graph['edges'].append({
                    'from': wallet,
                    'to': counterparty,
                    'value': interaction['value'],
                    'count': interaction['count'],
                })
                
                if counterparty not in visited:
                    queue.append((counterparty, current_depth + 1))
        
        # Calculate centrality
        graph['centrality_scores'] = self.calculate_centrality(graph)
        
        # Detect clusters
        graph['clusters'] = self.detect_communities(graph)
        
        return graph
    
    def identify_key_influencers(self, graph: dict) -> list:
        """
        Identify influential wallets in the graph
        """
        influencers = []
        
        for wallet in graph['nodes']:
            score = (
                graph['centrality_scores'].get(wallet, 0) * 0.4 +
                self.calculate_outreach(wallet, graph) * 0.3 +
                self.calculate_funding_role(wallet, graph) * 0.3
            )
            
            influencers.append({
                'wallet': wallet,
                'influence_score': score,
                'role': self.classify_role(wallet, graph),
            })
        
        return sorted(influencers, key=lambda x: x['influence_score'], reverse=True)
```

---

## 5. RISK CATEGORIES

### 5.1 Actor Classification System

```python
RISK_CATEGORIES = {
    
    'CONFIRMED_RUGGER': {
        'risk_level': 'CRITICAL',
        'reputation_range': (0, 10),
        'description': 'Confirmed to have executed rug pulls',
        'indicators': [
            'Executed confirmed rug pull pattern',
            'Multiple scam tokens created',
            'Pattern confirmed by community',
        ],
        'action': 'PERMANENT_BLACKLIST',
        'alert_level': 'RED',
    },
    
    'SUSPECTED_RUGGER': {
        'risk_level': 'HIGH',
        'reputation_range': (10, 30),
        'description': 'Strong indicators of malicious intent',
        'indicators': [
            'Multiple failed tokens',
            'Suspicious LP behavior',
            'Coordinated dumping detected',
        ],
        'action': 'HIGH_ALERT_MONITORING',
        'alert_level': 'ORANGE',
    },
    
    'PROFESSIONAL_SNIPER': {
        'risk_level': 'MEDIUM-HIGH',
        'reputation_range': (20, 50),
        'description': 'Automated or highly skilled early buyer',
        'indicators': [
            'Consistently first 100 buyers',
            'Bot-like behavior patterns',
            'Extreme timing precision',
        ],
        'action': 'MONITOR_AND_FLAG',
        'alert_level': 'YELLOW',
    },
    
    'INSIDER_TRADER': {
        'risk_level': 'HIGH',
        'reputation_range': (15, 35),
        'description': 'Suspected of having insider information',
        'indicators': [
            'Pre-launch funding from dev wallets',
            'Perfect timing on announcements',
            'Social connections to developers',
        ],
        'action': 'INVESTIGATE_AND_MONITOR',
        'alert_level': 'ORANGE',
    },
    
    'WASH_TRADER': {
        'risk_level': 'MEDIUM',
        'reputation_range': (25, 45),
        'description': 'Creates artificial volume',
        'indicators': [
            'Circular trading patterns',
            'Volume without price movement',
            'Self-trading detected',
        ],
        'action': 'FLAG_TRANSACTIONS',
        'alert_level': 'YELLOW',
    },
    
    'SERIAL_LAUNCHER': {
        'risk_level': 'MEDIUM-HIGH',
        'reputation_range': (20, 40),
        'description': 'Repeatedly creates tokens',
        'indicators': [
            '>5 tokens created in 90 days',
            'Low success rate',
            'Similar token characteristics',
        ],
        'action': 'REQUIRE_ADDITIONAL_VERIFICATION',
        'alert_level': 'YELLOW',
    },
    
    'COORDINATED_GROUP_MEMBER': {
        'risk_level': 'HIGH',
        'reputation_range': (15, 35),
        'description': 'Part of coordinated manipulation group',
        'indicators': [
            'Detected in wallet cluster',
            'Synchronized trading patterns',
            'Common funding/profit destination',
        ],
        'action': 'CLUSTER_MONITORING',
        'alert_level': 'ORANGE',
    },
    
    'COPYCAT_SCAMMER': {
        'risk_level': 'MEDIUM-HIGH',
        'reputation_range': (20, 40),
        'description': 'Creates tokens mimicking legitimate projects',
        'indicators': [
            'Token names similar to popular projects',
            'Copied metadata/images',
            'Attempting to confuse buyers',
        ],
        'action': 'FLAG_AND_WARN',
        'alert_level': 'YELLOW',
    },
    
    'SYBIL_ATTACKER': {
        'risk_level': 'HIGH',
        'reputation_range': (10, 30),
        'description': 'Uses multiple fake identities',
        'indicators': [
            'Part of large wallet cluster',
            'Artificial community appearance',
            'Fake engagement patterns',
        ],
        'action': 'CLUSTER_BLACKLIST',
        'alert_level': 'ORANGE',
    },
    
    'HONEYPOT_CREATOR': {
        'risk_level': 'CRITICAL',
        'reputation_range': (0, 5),
        'description': 'Creates tokens that trap buyers',
        'indicators': [
            'Sell-restricting code',
            'Only dev can sell',
            'Confirmed honeypot pattern',
        ],
        'action': 'PERMANENT_BLACKLIST',
        'alert_level': 'RED',
    },
    
    'PUMP_AND_DUMP_OPERATOR': {
        'risk_level': 'HIGH',
        'reputation_range': (15, 35),
        'description': 'Coordinates artificial pumps for dumping',
        'indicators': [
            'Wash trading patterns',
            'Coordinated buying then selling',
            'Marketing manipulation',
        ],
        'action': 'MONITOR_AND_ALERT',
        'alert_level': 'ORANGE',
    },
    
    'LEGITIMATE_TRADER': {
        'risk_level': 'LOW',
        'reputation_range': (60, 100),
        'description': 'Normal trading behavior',
        'indicators': [
            'Consistent profitability',
            'Reasonable hold times',
            'No suspicious patterns',
        ],
        'action': 'NONE',
        'alert_level': 'GREEN',
    },
    
    'REPUTABLE_DEVELOPER': {
        'risk_level': 'VERY_LOW',
        'reputation_range': (80, 100),
        'description': 'Established trustworthy developer',
        'indicators': [
            'Successful project history',
            'Transparent identity',
            'Active community engagement',
            'No rug history',
        ],
        'action': 'VERIFIED_BADGE',
        'alert_level': 'GREEN',
    },
}
```

### 5.2 Alert Level System

```python
ALERT_LEVELS = {
    
    'RED': {
        'severity': 'CRITICAL',
        'description': 'Confirmed malicious actor',
        'actions': [
            'Immediate user warning',
            'Transaction blocking (optional)',
            'Public blacklist',
            'Community notification',
        ],
        'response_time': 'immediate',
    },
    
    'ORANGE': {
        'severity': 'HIGH',
        'description': 'Strong suspicion of malicious activity',
        'actions': [
            'Prominent warning on profile',
            'Enhanced monitoring',
            'User notification',
            'Manual review queue',
        ],
        'response_time': '<1 hour',
    },
    
    'YELLOW': {
        'severity': 'MEDIUM',
        'description': 'Suspicious patterns detected',
        'actions': [
            'Subtle warning indicator',
            'Pattern monitoring',
            'Data collection enhancement',
        ],
        'response_time': '<24 hours',
    },
    
    'GREEN': {
        'severity': 'LOW',
        'description': 'No significant risk detected',
        'actions': [
            'Standard monitoring',
            'Regular reputation updates',
        ],
        'response_time': 'routine',
    },
}
```

---

## 6. DATA REQUIREMENTS

### 6.1 Historical Data Specifications

#### Required Data Sources

```yaml
Data_Sources:
  
  Solana_RPC:
    description: "Primary blockchain data source"
    endpoints:
      - getTransaction
      - getBlock
      - getAccountInfo
      - getTokenAccountsByOwner
      - getSignaturesForAddress
    priority: CRITICAL
    
  PumpFun_API:
    description: "Pump.Fun specific data"
    endpoints:
      - token_creation_events
      - bonding_curve_data
      - migration_events
    priority: CRITICAL
    
  DEX_Data:
    description: "Decentralized exchange data"
    sources:
      - Raydium API
      - Orca API
      - Jupiter API
    data_points:
      - swap_events
      - liquidity_events
      - price_data
    priority: HIGH
    
  Price_Oracles:
    description: "Historical price data"
    sources:
      - CoinGecko
      - CoinMarketCap
      - Birdeye
    priority: HIGH
    
  Social_Data:
    description: "Social sentiment and connections"
    sources:
      - Twitter API
      - Discord (if available)
      - Telegram (if available)
    priority: MEDIUM
```

#### Data Retention Policy

```python
DATA_RETENTION = {
    
    'RAW_TRANSACTIONS': {
        'retention_period': '2 years',
        'storage_tier': 'hot',
        'compression': 'gzip',
        'access_pattern': 'frequent',
    },
    
    'AGGREGATED_METRICS': {
        'retention_period': '5 years',
        'storage_tier': 'warm',
        'compression': 'none',
        'access_pattern': 'moderate',
    },
    
    'REPUTATION_SCORES': {
        'retention_period': 'indefinite',
        'storage_tier': 'hot',
        'compression': 'none',
        'access_pattern': 'very_frequent',
    },
    
    'PATTERN_DETECTIONS': {
        'retention_period': 'indefinite',
        'storage_tier': 'warm',
        'compression': 'gzip',
        'access_pattern': 'moderate',
    },
    
    'WALLET_CLUSTERS': {
        'retention_period': 'indefinite',
        'storage_tier': 'hot',
        'compression': 'none',
        'access_pattern': 'frequent',
    },
    
    'ALERT_HISTORY': {
        'retention_period': '3 years',
        'storage_tier': 'cold',
        'compression': 'gzip',
        'access_pattern': 'rare',
    },
}
```

### 6.2 Analysis Time Windows

```python
ANALYSIS_WINDOWS = {
    
    'REAL_TIME': {
        'window': '0-1 hour',
        'purpose': 'Immediate threat detection',
        'update_frequency': 'continuous',
        'data_points': [
            'new_transactions',
            'price_movements',
            'liquidity_changes',
        ],
    },
    
    'SHORT_TERM': {
        'window': '1-24 hours',
        'purpose': 'Active pattern detection',
        'update_frequency': '15 minutes',
        'data_points': [
            'trading_patterns',
            'coordination_signals',
            'suspicious_activity',
        ],
    },
    
    'MEDIUM_TERM': {
        'window': '1-30 days',
        'purpose': 'Behavioral analysis',
        'update_frequency': '1 hour',
        'data_points': [
            'profitability_metrics',
            'holding_patterns',
            'reputation_trends',
        ],
    },
    
    'LONG_TERM': {
        'window': '30-365 days',
        'purpose': 'Historical reputation',
        'update_frequency': '24 hours',
        'data_points': [
            'lifetime_performance',
            'rug_history',
            'pattern_consistency',
        ],
    },
    
    'FULL_HISTORY': {
        'window': 'all time',
        'purpose': 'Comprehensive background',
        'update_frequency': 'weekly',
        'data_points': [
            'complete_transaction_history',
            'all_token_interactions',
            'cross_chain_activity',
        ],
    },
}
```

### 6.3 Storage Requirements

```python
STORAGE_ESTIMATES = {
    
    'per_wallet_metadata': {
        'size_kb': 10,
        'description': 'Basic wallet info, creation date, etc.',
    },
    
    'per_transaction': {
        'size_kb': 2,
        'description': 'Compressed transaction data',
    },
    
    'per_token_interaction': {
        'size_kb': 1,
        'description': 'Token transfer/swap record',
    },
    
    'reputation_score': {
        'size_kb': 5,
        'description': 'Score + metadata + history',
    },
    
    'pattern_detection': {
        'size_kb': 20,
        'description': 'Pattern matches + evidence',
    },
    
    'cluster_data': {
        'size_kb': 50,
        'description': 'Cluster membership + relationships',
    },
}

# Example calculation for 1 million active wallets
ESTIMATED_STORAGE = {
    'wallets': 1_000_000,
    'avg_transactions_per_wallet': 500,
    'avg_tokens_per_wallet': 50,
    
    'total_storage_tb': {
        'wallet_metadata': '10 GB',
        'transactions': '1 TB',
        'token_interactions': '50 GB',
        'reputation_scores': '5 GB',
        'pattern_detections': '20 GB',
        'cluster_data': '50 GB',
        'indexes_and_overhead': '200 GB',
        'TOTAL': '~1.3 TB',
    },
    
    'growth_rate': {
        'monthly_increase': '~100 GB',
        'annual_projection': '~1.5 TB',
    },
}
```

---

## 7. IMPLEMENTATION ARCHITECTURE

### 7.1 System Components

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    REPUTATION SYSTEM ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   Data       │───▶│   Pattern    │───▶│  Reputation  │               │
│  │   Ingestion  │    │   Detection  │    │   Engine     │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                   │                        │
│         ▼                   ▼                   ▼                        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │   Entity     │    │   Risk       │    │   Alert      │               │
│  │   Resolution │    │   Scoring    │    │   System     │               │
│  └──────────────┘    └──────────────┘    └──────────────┘               │
│         │                   │                   │                        │
│         └───────────────────┴───────────────────┘                        │
│                             │                                            │
│                             ▼                                            │
│                    ┌──────────────────┐                                  │
│                    │   API / UI Layer │                                  │
│                    └──────────────────┘                                  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Real-Time Processing Pipeline

```python
class RealTimeProcessor:
    """
    Process transactions in real-time for immediate detection
    """
    
    async def process_transaction(self, tx_data: dict):
        """
        Real-time transaction processing pipeline
        """
        # Step 1: Extract entities
        wallets = self.extract_wallets(tx_data)
        tokens = self.extract_tokens(tx_data)
        
        # Step 2: Update metrics
        for wallet in wallets:
            await self.update_wallet_metrics(wallet, tx_data)
        
        # Step 3: Pattern detection
        patterns = self.detect_patterns(tx_data)
        
        # Step 4: Risk assessment
        for pattern in patterns:
            if pattern['severity'] == 'CRITICAL':
                await self.trigger_immediate_alert(pattern)
        
        # Step 5: Reputation update (async)
        asyncio.create_task(self.update_reputation_scores(wallets))
        
        # Step 6: Cluster analysis (async, batched)
        self.queue_for_cluster_analysis(wallets)
```

### 7.3 API Endpoints

```python
API_SPECIFICATION = {
    
    'GET /api/v1/wallet/{address}/reputation': {
        'description': 'Get wallet reputation score and details',
        'response': {
            'score': 75,
            'category': 'LEGITIMATE_TRADER',
            'risk_level': 'LOW',
            'factors': {
                'positive': [...],
                'negative': [...],
            },
            'cluster_info': {...},
            'last_updated': '2024-01-15T10:30:00Z',
        }
    },
    
    'GET /api/v1/wallet/{address}/history': {
        'description': 'Get wallet transaction history with risk flags',
        'response': {
            'transactions': [...],
            'patterns_detected': [...],
            'risk_events': [...],
        }
    },
    
    'GET /api/v1/token/{address}/risk': {
        'description': 'Get token-specific risk assessment',
        'response': {
            'overall_risk': 'MEDIUM',
            'dev_wallet_risk': {...},
            'holder_concentration': {...},
            'liquidity_risk': {...},
            'pattern_risks': [...],
        }
    },
    
    'POST /api/v1/analyze/cluster': {
        'description': 'Analyze wallet cluster',
        'request': {
            'wallets': [...],
        },
        'response': {
            'cluster_id': 'abc123',
            'confidence': 0.92,
            'relationships': [...],
            'risk_assessment': {...},
        }
    },
    
    'GET /api/v1/alerts': {
        'description': 'Get active alerts',
        'query_params': {
            'level': 'RED|ORANGE|YELLOW',
            'type': 'RUG_PULL|INSIDER|...',
        },
        'response': {
            'alerts': [...],
        }
    },
}
```

---

## 8. CONTINUOUS IMPROVEMENT

### 8.1 Model Updates

```python
MODEL_UPDATE_STRATEGY = {
    
    'PATTERN_LIBRARY_UPDATES': {
        'frequency': 'weekly',
        'source': [
            'New rug pull analysis',
            'Community reports',
            'Manual review findings',
            'Academic research',
        ],
    },
    
    'SCORING_WEIGHT_ADJUSTMENTS': {
        'frequency': 'monthly',
        'methodology': [
            'Backtest against historical rugs',
            'Measure false positive rate',
            'Community feedback integration',
            'A/B testing',
        ],
    },
    
    'MACHINE_LEARNING_RETRAINING': {
        'frequency': 'quarterly',
        'process': [
            'Collect new labeled data',
            'Retrain classification models',
            'Validate performance metrics',
            'Gradual rollout',
        ],
    },
}
```

### 8.2 Feedback Loops

```python
FEEDBACK_MECHANISMS = {
    
    'COMMUNITY_REPORTS': {
        'channels': [
            'In-app report button',
            'Discord/Telegram bots',
            'Email submissions',
        ],
        'processing': 'Manual review queue',
        'impact': 'Direct pattern/weight updates',
    },
    
    'FALSE_POSITIVE_TRACKING': {
        'collection': 'User appeals and disputes',
        'analysis': 'Weekly review of contested flags',
        'adjustment': 'Weight tuning and threshold updates',
    },
    
    'SUCCESS_METRICS': {
        'detection_rate': '% of rugs detected before completion',
        'false_positive_rate': '% of legitimate users flagged',
        'time_to_detection': 'Average time to identify new threat',
        'user_trust_score': 'Survey-based confidence metric',
    },
}
```

---

## Appendix A: Pattern Detection Algorithms

### A.1 Rug Pull Detection Algorithm

```python
def detect_rug_pull(wallet: str, token: str, lookback_hours: int = 24) -> dict:
    """
    Detect if a rug pull is in progress or completed
    """
    result = {
        'is_rug_pull': False,
        'confidence': 0,
        'stage': None,
        'evidence': [],
    }
    
    # Get relevant transactions
    lp_interactions = get_lp_interactions(wallet, token, lookback_hours)
    token_sales = get_token_sales(wallet, token, lookback_hours)
    
    # Check for LP removal
    lp_removed = sum(tx['amount'] for tx in lp_interactions if tx['type'] == 'REMOVE')
    lp_total = get_total_lp(token)
    
    if lp_removed > lp_total * 0.5:
        result['evidence'].append({
            'type': 'MASSIVE_LP_REMOVAL',
            'details': f'Removed {lp_removed/lp_total*100:.1f}% of LP',
        })
        result['confidence'] += 40
    
    # Check for token dumping
    tokens_sold = sum(tx['amount'] for tx in token_sales)
    tokens_held = get_wallet_token_balance(wallet, token, before=lookback_hours)
    
    if tokens_sold > tokens_held * 0.5:
        result['evidence'].append({
            'type': 'MASSIVE_TOKEN_DUMP',
            'details': f'Dumped {tokens_sold/tokens_held*100:.1f}% of holdings',
        })
        result['confidence'] += 40
    
    # Check timing correlation
    if lp_interactions and token_sales:
        lp_time = max(tx['timestamp'] for tx in lp_interactions)
        sell_time = min(tx['timestamp'] for tx in token_sales)
        time_diff = abs(lp_time - sell_time)
        
        if time_diff < 3600:  # Within 1 hour
            result['evidence'].append({
                'type': 'TIMING_CORRELATION',
                'details': f'LP removal and dump within {time_diff/60:.0f} minutes',
            })
            result['confidence'] += 20
    
    # Determine if rug pull
    if result['confidence'] >= 80:
        result['is_rug_pull'] = True
        result['stage'] = 'COMPLETED' if not has_remaining_tokens(wallet, token) else 'IN_PROGRESS'
    
    return result
```

### A.2 Wallet Clustering Algorithm

```python
def cluster_wallets(seed_wallet: str, min_confidence: float = 0.7) -> list:
    """
    Find wallets likely controlled by same entity
    """
    clusters = []
    visited = set()
    queue = [seed_wallet]
    
    while queue:
        wallet = queue.pop(0)
        if wallet in visited:
            continue
        visited.add(wallet)
        
        # Find related wallets
        candidates = find_candidate_wallets(wallet)
        
        for candidate in candidates:
            if candidate in visited:
                continue
                
            # Calculate relationship confidence
            confidence = calculate_relationship_confidence(wallet, candidate)
            
            if confidence >= min_confidence:
                clusters.append({
                    'wallet': candidate,
                    'confidence': confidence,
                    'connection_type': get_connection_type(wallet, candidate),
                })
                queue.append(candidate)
    
    return clusters

def calculate_relationship_confidence(w1: str, w2: str) -> float:
    """
    Calculate confidence that two wallets are related
    """
    signals = []
    
    # Funding relationship
    if has_funding_relationship(w1, w2):
        signals.append(0.90)
    
    # Profit convergence
    if has_common_profit_destination(w1, w2):
        signals.append(0.85)
    
    # Behavioral similarity
    similarity = calculate_behavioral_similarity(w1, w2)
    if similarity > 0.8:
        signals.append(similarity * 0.75)
    
    # Temporal correlation
    correlation = calculate_temporal_correlation(w1, w2)
    if correlation > 0.9:
        signals.append(correlation * 0.70)
    
    # Combine signals
    if not signals:
        return 0
    
    # Weighted combination
    return min(1.0, sum(signals) / len(signals) * (1 + 0.1 * len(signals)))
```

---

## Appendix B: Quick Reference

### B.1 Risk Score Interpretation

| Score | Category | Action |
|-------|----------|--------|
| 0-10 | Confirmed Rugger | Avoid completely |
| 11-25 | High Risk | Extreme caution |
| 26-40 | Suspicious | Verify before interacting |
| 41-55 | Neutral | Standard due diligence |
| 56-75 | Trustworthy | Generally safe |
| 76-90 | Reputable | Low risk |
| 91-100 | Verified | Highly trusted |

### B.2 Pattern Priority Matrix

| Pattern | Detection Speed | Confidence | Priority |
|---------|----------------|------------|----------|
| Honeypot | Immediate | 100% | P0 |
| Instant LP Rug | <5 min | 95% | P0 |
| Coordinated Dump | <15 min | 85% | P1 |
| Insider Trading | <1 hour | 70% | P1 |
| Wash Trading | <1 hour | 80% | P2 |
| Slow Rug | Days | 75% | P2 |

---

*Document Version: 1.0*
*Last Updated: 2024*
*Classification: Technical Specification*
