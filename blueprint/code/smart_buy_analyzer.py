"""
Pump.fun Meme Coin Smart Buy Analysis Engine
Core Implementation

This module provides the core scoring algorithms and detection systems
for evaluating meme coins and generating smart buy recommendations.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import math


@dataclass
class TokenData:
    """Data structure for token analysis input"""
    address: str
    symbol: str
    price: float
    market_cap: float
    liquidity_sol: float
    holders: int
    volume_24h: float
    bonding_curve_progress: float

    # Historical data
    price_history: List[float]  # 5-min OHLC or similar
    volume_history: List[float]
    trade_history: List[Dict]

    # Holder data
    holder_balances: Dict[str, float]
    holder_history: List[int]

    # Developer data
    dev_wallet: str
    dev_initial_allocation: float
    dev_current_balance: float
    dev_wallet_age_days: int

    # Contract data
    contract_verified: bool
    mint_authority_enabled: bool
    freeze_authority_enabled: bool
    liquidity_locked: bool
    locked_percent: float

    # Timing
    launch_timestamp: datetime

    # Optional social data
    social_data_available: bool = False
    mentions_1h: int = 0
    mentions_24h: int = 0
    positive_mentions: int = 0
    negative_mentions: int = 0


class SmartBuyAnalyzer:
    """
    Main analysis engine for generating smart buy recommendations.
    """

    # Factor weights
    WEIGHTS = {
        'liquidity': 0.20,
        'holder': 0.15,
        'volume': 0.20,
        'price': 0.15,
        'bonding': 0.10,
        'dev': 0.10,
        'social': 0.10
    }

    # Risk weights
    RISK_WEIGHTS = {
        'concentration': 0.25,
        'liquidity': 0.20,
        'manipulation': 0.20,
        'contract': 0.15,
        'time': 0.10,
        'social': 0.10
    }

    def __init__(self):
        self.cache = {}
        self.cache_ttl = 30  # seconds

    def normalize(self, value: float, min_val: float, max_val: float, 
                  clip_outliers: bool = True) -> float:
        """Min-max normalization with optional outlier clipping"""
        if clip_outliers:
            value = max(min_val, min(value, max_val))
        if max_val == min_val:
            return 50.0
        return (value - min_val) / (max_val - min_val) * 100

    def calculate_liquidity_score(self, data: TokenData) -> float:
        """Calculate liquidity health score (0-100)"""
        # Liquidity Depth Score
        liquidity_ratio = data.liquidity_sol / max(data.market_cap, 1)
        lds = min(100, liquidity_ratio * 100 * 10)

        # Liquidity Growth Rate (if history available)
        if len(data.volume_history) >= 12:
            lgr = self.normalize(
                (data.volume_history[-1] - data.volume_history[-12]) / max(data.volume_history[-12], 1) * 100,
                -50, 100
            )
        else:
            lgr = 50

        # Composite score
        return 0.6 * lds + 0.4 * lgr

    def calculate_holder_score(self, data: TokenData) -> float:
        """Calculate holder distribution score (0-100)"""
        # Concentration Risk Index
        if data.holder_balances:
            sorted_balances = sorted(data.holder_balances.values(), reverse=True)
            total_supply = sum(sorted_balances)
            top_10_percent = sum(sorted_balances[:10]) / max(total_supply, 1) * 100
            cri = max(0, 100 - top_10_percent * 1.5)
        else:
            cri = 50

        # Holder Growth Rate
        if len(data.holder_history) >= 2:
            hgr = self.normalize(
                (data.holder_history[-1] - data.holder_history[0]) / max(data.holder_history[0], 1) * 100,
                0, 200
            )
        else:
            hgr = 50

        return 0.6 * cri + 0.4 * hgr

    def detect_artificial_volume(self, data: TokenData) -> float:
        """
        Detect artificial volume patterns.
        Returns score 0-1 (higher = more artificial)
        """
        if not data.trade_history or len(data.trade_history) < 10:
            return 0.0

        scores = []

        # Factor 1: Trade size uniformity
        trade_sizes = [t.get('amount', 0) for t in data.trade_history]
        if trade_sizes:
            cv = np.std(trade_sizes) / (np.mean(trade_sizes) + 0.001)
            uniformity_score = max(0, 1 - cv)
            scores.append(uniformity_score)

        # Factor 2: Temporal clustering
        trade_times = [t.get('timestamp', 0) for t in data.trade_history]
        if len(trade_times) > 1:
            time_diffs = np.diff(trade_times)
            if len(time_diffs) > 0 and np.mean(time_diffs) > 0:
                clustering = 1 - (np.std(time_diffs) / (np.mean(time_diffs) + 0.001))
                scores.append(max(0, clustering))

        # Factor 3: Wallet reuse
        unique_wallets = len(set(t.get('trader', '') for t in data.trade_history))
        total_trades = len(data.trade_history)
        reuse_ratio = 1 - (unique_wallets / max(total_trades, 1))
        scores.append(reuse_ratio)

        # Factor 4: Round number bias
        round_count = sum(1 for s in trade_sizes if s > 0 and s % 1 == 0)
        round_bias = round_count / max(len(trade_sizes), 1)
        scores.append(min(1, round_bias * 3))

        weights = [0.25, 0.20, 0.30, 0.25]
        return sum(s * w for s, w in zip(scores, weights))

    def detect_wash_trading(self, data: TokenData) -> float:
        """
        Detect wash trading patterns.
        Returns score 0-1 (higher = more wash trading)
        """
        if not data.trade_history or len(data.trade_history) < 20:
            return 0.0

        scores = []

        # Build simple transaction graph
        wallet_flows = {}
        for trade in data.trade_history:
            buyer = trade.get('buyer', '')
            seller = trade.get('seller', '')
            amount = trade.get('amount', 0)

            if buyer and seller:
                key = (buyer, seller)
                wallet_flows[key] = wallet_flows.get(key, 0) + amount

        # Check for reciprocal flows (A->B and B->A)
        reciprocal_count = 0
        for (a, b), amount_ab in wallet_flows.items():
            if (b, a) in wallet_flows:
                reciprocal_count += 1

        reciprocal_score = reciprocal_count / max(len(wallet_flows), 1)
        scores.append(min(1, reciprocal_score * 5))

        # Check for zero-sum groups (simplified)
        wallet_pnl = {}
        for trade in data.trade_history:
            buyer = trade.get('buyer', '')
            seller = trade.get('seller', '')
            amount = trade.get('amount', 0)
            wallet_pnl[buyer] = wallet_pnl.get(buyer, 0) - amount
            wallet_pnl[seller] = wallet_pnl.get(seller, 0) + amount

        near_zero = sum(1 for pnl in wallet_pnl.values() if abs(pnl) < 0.01)
        zero_sum_score = near_zero / max(len(wallet_pnl), 1)
        scores.append(min(1, zero_sum_score * 3))

        weights = [0.6, 0.4]
        return sum(s * w for s, w in zip(scores, weights))

    def detect_coordinated_buying(self, data: TokenData) -> float:
        """
        Detect coordinated buying patterns.
        Returns score 0-1 (higher = more coordinated)
        """
        if not data.trade_history or len(data.trade_history) < 10:
            return 0.0

        scores = []

        # Group buys by time windows (30 seconds)
        buys = [t for t in data.trade_history if t.get('type') == 'buy']
        if len(buys) < 5:
            return 0.0

        time_windows = {}
        for buy in buys:
            ts = buy.get('timestamp', 0)
            window = int(ts / 30)  # 30-second windows
            time_windows[window] = time_windows.get(window, 0) + 1

        # Spike detection
        if time_windows:
            counts = list(time_windows.values())
            if len(counts) > 1 and np.std(counts) > 0:
                spike_score = (max(counts) - np.mean(counts)) / (np.std(counts) + 0.001)
                scores.append(min(1, spike_score / 5))

        # Trade size similarity
        buy_amounts = [b.get('amount', 0) for b in buys]
        if buy_amounts and np.mean(buy_amounts) > 0:
            cv = np.std(buy_amounts) / np.mean(buy_amounts)
            similarity_score = max(0, 1 - cv)
            scores.append(similarity_score)

        weights = [0.6, 0.4]
        return sum(s * w for s, w in zip(scores, weights))

    def calculate_volume_score(self, data: TokenData) -> float:
        """Calculate volume quality score (0-100)"""
        # Volume trend
        if len(data.volume_history) >= 2:
            vts = self.normalize(
                data.volume_history[-1] / max(np.mean(data.volume_history[:-1]), 1) * 100,
                50, 300
            )
        else:
            vts = 50

        # Volume consistency
        if len(data.volume_history) >= 12:
            cv = np.std(data.volume_history) / (np.mean(data.volume_history) + 0.001)
            vcs = max(0, 100 - cv * 50)
        else:
            vcs = 50

        # Natural volume indicator
        artificial_score = self.detect_artificial_volume(data)
        nvi = 100 - artificial_score * 100

        return 0.35 * vts + 0.25 * vcs + 0.40 * nvi

    def detect_pump_dump_pattern(self, data: TokenData) -> Dict[str, float]:
        """
        Detect pump and dump patterns.
        Returns dictionary of pattern scores.
        """
        patterns = {
            'early_pump': 0.0,
            'mature_pump': 0.0,
            'distribution': 0.0,
            'dump': 0.0,
            'accumulation': 0.0,
            'organic_growth': 0.0
        }

        if len(data.price_history) < 12:
            return patterns

        # Calculate metrics
        price_change_1h = (data.price_history[-1] - data.price_history[-12]) / max(data.price_history[-12], 0.001)
        price_change_24h = (data.price_history[-1] - data.price_history[0]) / max(data.price_history[0], 0.001)

        if len(data.volume_history) >= 12:
            volume_spike = max(data.volume_history[-12:]) / max(np.mean(data.volume_history[:-12]), 1)
        else:
            volume_spike = 1.0

        volatility = np.std(data.price_history[-12:]) / (np.mean(data.price_history[-12:]) + 0.001)

        # Pattern detection
        if price_change_1h > 0.5 and volume_spike > 3 and volatility < 0.3:
            patterns['early_pump'] = min(1, price_change_1h) * 0.8

        if price_change_24h > 3 and volume_spike > 5:
            patterns['mature_pump'] = min(1, price_change_24h / 10) * 0.9

        if price_change_1h < 0.1 and price_change_24h > 2 and volume_spike > 2 and volatility > 0.4:
            patterns['distribution'] = 0.85

        if price_change_1h < -0.3 and volume_spike > 2:
            patterns['dump'] = min(1, abs(price_change_1h)) * 0.9

        if abs(price_change_24h) < 0.5 and volume_spike > 1.5 and volatility < 0.2:
            patterns['accumulation'] = 0.75

        if 0.5 < price_change_24h < 3 and 1 < volume_spike < 5 and volatility < 0.3:
            patterns['organic_growth'] = 0.80

        return patterns

    def calculate_price_score(self, data: TokenData) -> float:
        """Calculate price action score (0-100)"""
        if len(data.price_history) < 12:
            return 50.0

        # Price momentum
        price_change_1h = (data.price_history[-1] - data.price_history[-12]) / max(data.price_history[-12], 0.001) * 100
        price_change_24h = (data.price_history[-1] - data.price_history[0]) / max(data.price_history[0], 0.001) * 100
        pms = self.normalize(price_change_1h * 2 + price_change_24h, -50, 100)

        # Volatility health
        price_array = np.array(data.price_history)
        returns = np.diff(price_array) / (price_array[:-1] + 0.001)
        volatility = np.std(returns) * np.sqrt(288)  # Annualized
        vhs = 100 - min(100, abs(volatility - 0.5) * 100)

        # Pattern score
        patterns = self.detect_pump_dump_pattern(data)
        if patterns['organic_growth'] > 0.5:
            pps = 80
        elif patterns['early_pump'] > 0.5:
            pps = 70
        elif patterns['accumulation'] > 0.5:
            pps = 75
        elif patterns['mature_pump'] > 0.5 or patterns['dump'] > 0.5:
            pps = 20
        else:
            pps = 50

        return 0.40 * pms + 0.30 * vhs + 0.30 * pps

    def calculate_bonding_score(self, data: TokenData) -> float:
        """Calculate bonding curve score (0-100)"""
        # Progress score
        ps = data.bonding_curve_progress

        # Early stage bonus
        if ps < 20:
            ps = 80 + ps  # Higher score for early opportunities
        elif ps > 80:
            ps = ps * 0.7  # Lower score for late stage

        return min(100, ps)

    def calculate_dev_score(self, data: TokenData) -> float:
        """Calculate developer activity score (0-100)"""
        # Developer commitment
        if data.dev_initial_allocation > 0:
            dev_sold_percent = (data.dev_initial_allocation - data.dev_current_balance) / data.dev_initial_allocation * 100
            dcs = max(0, 100 - dev_sold_percent * 2)
        else:
            dcs = 50

        # Wallet age
        dwa = min(100, data.dev_wallet_age_days / 30 * 100)

        # Liquidity lock
        lls = data.locked_percent if data.liquidity_locked else 0

        return 0.5 * dcs + 0.25 * dwa + 0.25 * lls

    def calculate_social_score(self, data: TokenData) -> float:
        """Calculate social signals score (0-100)"""
        if not data.social_data_available:
            return 50.0

        # Engagement
        ses = self.normalize(data.mentions_1h, 0, 1000)

        # Sentiment
        total = data.positive_mentions + data.negative_mentions
        if total > 0:
            ss = (data.positive_mentions - data.negative_mentions) / total * 50 + 50
        else:
            ss = 50

        return 0.6 * ses + 0.4 * ss

    def detect_early_opportunity(self, data: TokenData) -> float:
        """
        Detect early opportunity signals.
        Returns score 0-1 (higher = better opportunity)
        """
        scores = []

        # Launch recency
        age_hours = (datetime.now() - data.launch_timestamp).total_seconds() / 3600
        recency = max(0, 1 - age_hours / 24)
        scores.append(recency * 0.5)

        # Holder growth acceleration
        if len(data.holder_history) >= 5:
            recent_growth = (data.holder_history[-1] - data.holder_history[-2]) / max(data.holder_history[-2], 1)
            older_growth = (data.holder_history[-1] - data.holder_history[0]) / max(data.holder_history[0], 1)
            if older_growth > 0:
                acceleration = recent_growth / older_growth
                scores.append(min(1, acceleration) * 0.3)

        # Pattern-based opportunity
        patterns = self.detect_pump_dump_pattern(data)
        if patterns['accumulation'] > 0.5:
            scores.append(0.4)
        elif patterns['organic_growth'] > 0.5:
            scores.append(0.3)

        return min(1, sum(scores))

    def calculate_risk_score(self, data: TokenData) -> Dict:
        """
        Calculate comprehensive risk score.
        Returns risk breakdown and overall score.
        """
        risks = {}

        # Concentration risk
        if data.holder_balances:
            sorted_balances = sorted(data.holder_balances.values(), reverse=True)
            total = sum(sorted_balances)
            top_10 = sum(sorted_balances[:10]) / max(total, 1) * 100

            if sorted_balances[0] / max(total, 1) > 0.3:
                risks['concentration'] = 100
            elif top_10 > 70:
                risks['concentration'] = 80
            else:
                risks['concentration'] = max(0, (top_10 - 20) * 1.5)
        else:
            risks['concentration'] = 50

        # Liquidity risk
        liquidity_ratio = data.liquidity_sol / max(data.market_cap, 1)
        if liquidity_ratio < 0.01:
            risks['liquidity'] = 100
        elif liquidity_ratio < 0.03:
            risks['liquidity'] = 80
        elif liquidity_ratio < 0.05:
            risks['liquidity'] = 60
        else:
            risks['liquidity'] = max(0, (0.1 - liquidity_ratio) * 1000)

        # Manipulation risk
        artificial = self.detect_artificial_volume(data)
        wash = self.detect_wash_trading(data)
        coord = self.detect_coordinated_buying(data)
        patterns = self.detect_pump_dump_pattern(data)
        pump_dump = max(patterns['mature_pump'], patterns['dump'])

        risks['manipulation'] = min(100, (
            artificial * 30 + wash * 30 + coord * 25 + pump_dump * 15
        ))

        # Contract risk
        contract_risk = 0
        if not data.contract_verified:
            contract_risk += 40
        if data.mint_authority_enabled:
            contract_risk += 30
        if data.freeze_authority_enabled:
            contract_risk += 20
        risks['contract'] = contract_risk

        # Time risk
        age_hours = (datetime.now() - data.launch_timestamp).total_seconds() / 3600
        if age_hours < 1:
            risks['time'] = 80
        elif age_hours < 6:
            risks['time'] = 60
        elif age_hours < 24:
            risks['time'] = 40
        else:
            risks['time'] = max(0, 40 - (age_hours - 24) / 10)

        # Social risk
        if data.social_data_available:
            total = data.positive_mentions + data.negative_mentions
            if total > 0:
                risks['social'] = data.negative_mentions / total * 100
            else:
                risks['social'] = 50
        else:
            risks['social'] = 50

        # Overall risk score
        overall = sum(risks[k] * self.RISK_WEIGHTS[k] for k in risks.keys())

        return {
            'breakdown': risks,
            'overall': min(100, overall)
        }

    def check_critical_flags(self, data: TokenData) -> List[str]:
        """Check for critical red flags"""
        flags = []

        # Dev rugged check
        if data.dev_initial_allocation > 0:
            dev_sold = (data.dev_initial_allocation - data.dev_current_balance) / data.dev_initial_allocation
            if dev_sold > 0.9:
                flags.append('dev_rugged')

        # Liquidity removed
        if len(data.volume_history) >= 12:
            recent_liquidity = data.volume_history[-1]
            older_liquidity = data.volume_history[-12]
            if older_liquidity > 0 and (recent_liquidity - older_liquidity) / older_liquidity < -0.5:
                flags.append('liquidity_removed')

        # Massive whale dump
        if data.holder_balances:
            # This would need historical data to detect
            pass

        return flags

    def calculate_confidence(self, data: TokenData, risk_score: float) -> float:
        """Calculate confidence level based on data quality"""
        # Sample size factor
        sample_factor = min(1, len(data.trade_history) / 100)

        # Data freshness (assume recent)
        freshness = 1.0

        # Completeness
        required_fields = [
            data.price, data.market_cap, data.liquidity_sol,
            data.holders, data.volume_24h
        ]
        completeness = sum(1 for f in required_fields if f > 0) / len(required_fields)

        data_quality = min(100, (
            sample_factor * 30 +
            freshness * 25 +
            1.0 * 25 +  # Source reliability
            completeness * 20
        ))

        return data_quality * (1 - risk_score / 200)

    def generate_recommendation(self, score: float, risk_score: float, 
                                confidence: float) -> str:
        """Generate final recommendation"""
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

    def analyze(self, data: TokenData) -> Dict:
        """
        Main analysis function.
        Returns complete analysis results.
        """
        # Check critical flags first
        critical_flags = self.check_critical_flags(data)
        if critical_flags:
            return {
                'score': 0,
                'confidence': 100,
                'recommendation': 'AVOID',
                'risk_level': 'CRITICAL',
                'critical_flags': critical_flags,
                'reason': f'Critical flags detected: {", ".join(critical_flags)}'
            }

        # Calculate component scores
        liquidity_score = self.calculate_liquidity_score(data)
        holder_score = self.calculate_holder_score(data)
        volume_score = self.calculate_volume_score(data)
        price_score = self.calculate_price_score(data)
        bonding_score = self.calculate_bonding_score(data)
        dev_score = self.calculate_dev_score(data)
        social_score = self.calculate_social_score(data)

        # Calculate risk
        risk = self.calculate_risk_score(data)

        # Calculate opportunity boost
        opportunity = self.detect_early_opportunity(data) * 100

        # Base score calculation
        base_score = (
            liquidity_score * self.WEIGHTS['liquidity'] +
            holder_score * self.WEIGHTS['holder'] +
            volume_score * self.WEIGHTS['volume'] +
            price_score * self.WEIGHTS['price'] +
            bonding_score * self.WEIGHTS['bonding'] +
            dev_score * self.WEIGHTS['dev'] +
            social_score * self.WEIGHTS['social']
        )

        # Apply adjustments
        final_score = max(0, min(100, 
            base_score + opportunity * 0.15 - risk['overall'] * 0.5
        ))

        # Confidence
        confidence = self.calculate_confidence(data, risk['overall'])

        # Recommendation
        recommendation = self.generate_recommendation(
            final_score, risk['overall'], confidence
        )

        # Risk level
        if risk['overall'] < 30:
            risk_level = 'LOW'
        elif risk['overall'] < 50:
            risk_level = 'MODERATE'
        elif risk['overall'] < 70:
            risk_level = 'ELEVATED'
        else:
            risk_level = 'HIGH'

        return {
            'token_address': data.address,
            'token_symbol': data.symbol,
            'analysis_timestamp': datetime.now().isoformat(),
            'smart_buy_score': {
                'overall': round(final_score, 1),
                'confidence': round(confidence, 1),
                'recommendation': recommendation,
                'risk_level': risk_level
            },
            'component_scores': {
                'liquidity': round(liquidity_score, 1),
                'holder_distribution': round(holder_score, 1),
                'volume_quality': round(volume_score, 1),
                'price_action': round(price_score, 1),
                'bonding_curve': round(bonding_score, 1),
                'developer_activity': round(dev_score, 1),
                'social_signals': round(social_score, 1)
            },
            'risk_assessment': {
                'overall_risk_score': round(risk['overall'], 1),
                'breakdown': {k: round(v, 1) for k, v in risk['breakdown'].items()}
            },
            'detection_results': {
                'artificial_volume_score': round(self.detect_artificial_volume(data), 2),
                'wash_trading_score': round(self.detect_wash_trading(data), 2),
                'coordinated_buying_score': round(self.detect_coordinated_buying(data), 2),
                'early_opportunity_score': round(opportunity / 100, 2),
                'pump_dump_patterns': self.detect_pump_dump_pattern(data)
            },
            'key_metrics': {
                'price': data.price,
                'market_cap': data.market_cap,
                'liquidity_sol': data.liquidity_sol,
                'holders': data.holders,
                'volume_24h': data.volume_24h,
                'bonding_curve_progress': data.bonding_curve_progress,
                'age_hours': round((datetime.now() - data.launch_timestamp).total_seconds() / 3600, 1)
            }
        }


# Example usage
if __name__ == '__main__':
    # Create sample token data
    sample_data = TokenData(
        address='SampleTokenAddress123',
        symbol='SAMPLE',
        price=0.001,
        market_cap=10000,
        liquidity_sol=500,
        holders=250,
        volume_24h=2000,
        bonding_curve_progress=35.0,
        price_history=[0.0005] * 200 + [0.001] * 100,
        volume_history=[100] * 280 + [200] * 20,
        trade_history=[
            {'type': 'buy', 'amount': 1.0, 'timestamp': i, 'trader': f'wallet_{i%50}', 'buyer': f'buyer_{i}', 'seller': f'seller_{i}'}
            for i in range(100)
        ],
        holder_balances={f'wallet_{i}': 1000 for i in range(100)},
        holder_history=[100, 150, 200, 250],
        dev_wallet='dev_wallet_1',
        dev_initial_allocation=10000,
        dev_current_balance=10000,
        dev_wallet_age_days=60,
        contract_verified=True,
        mint_authority_enabled=False,
        freeze_authority_enabled=False,
        liquidity_locked=True,
        locked_percent=100.0,
        launch_timestamp=datetime.now() - timedelta(hours=6)
    )

    # Run analysis
    analyzer = SmartBuyAnalyzer()
    result = analyzer.analyze(sample_data)

    # Print results
    import json
    print(json.dumps(result, indent=2))
