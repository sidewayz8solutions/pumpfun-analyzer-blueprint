"""
Pump.fun Data Collection - Implementation Examples
===================================================
Practical code examples for implementing the data collection strategy.
"""

import asyncio
import json
import base58
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import aiohttp
import websockets
from solders.pubkey import Pubkey
from solders.rpc.responses import GetTransactionResp

# ============================================================================
# CONSTANTS
# ============================================================================

PUMP_FUN_PROGRAM_ID = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
SYSTEM_PROGRAM_ID = "11111111111111111111111111111111"

# Instruction discriminators (first 8 bytes of instruction data)
CREATE_DISCRIMINATOR = bytes([24, 30, 200, 40, 5, 28, 7, 119])
CREATE_V2_DISCRIMINATOR = bytes([103, 224, 16, 83, 96, 78, 240, 33])
BUY_DISCRIMINATOR = bytes([102, 6, 61, 18, 1, 218, 235, 234])
SELL_DISCRIMINATOR = bytes([51, 230, 133, 164, 1, 127, 131, 173])


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class TokenData:
    """Token metadata and metrics."""
    mint_address: str
    symbol: str
    name: str
    decimals: int
    creator_wallet: str
    created_at: datetime
    creation_slot: int
    creation_signature: str
    description: Optional[str] = None
    image_uri: Optional[str] = None
    metadata_uri: Optional[str] = None
    bonding_curve_address: Optional[str] = None
    is_migrated: bool = False
    migrated_at: Optional[datetime] = None
    raydium_pool_address: Optional[str] = None


@dataclass
class TradeData:
    """Trade transaction data."""
    signature: str
    mint_address: str
    slot: int
    block_time: datetime
    trader_wallet: str
    trade_type: str  # 'buy' | 'sell'
    token_amount: float
    sol_amount: float
    price_sol: float
    fee_sol: float
    success: bool


@dataclass
class HolderData:
    """Token holder information."""
    wallet_address: str
    mint_address: str
    balance: float
    balance_percentage: float
    first_buy_at: Optional[datetime] = None
    last_trade_at: Optional[datetime] = None


# ============================================================================
# API CLIENTS
# ============================================================================

class HeliusRPCClient:
    """Helius RPC API client."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = f"https://mainnet.helius-rpc.com/?api-key={api_key}"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, method: str, params: Any = None) -> Any:
        """Make RPC request."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or []
        }
        
        async with self.session.post(self.base_url, json=payload) as resp:
            data = await resp.json()
            if "error" in data:
                raise Exception(f"RPC Error: {data['error']}")
            return data.get("result")
    
    async def get_account_info(self, address: str) -> Optional[Dict]:
        """Get account information."""
        result = await self._request("getAccountInfo", [address, {"encoding": "jsonParsed"}])
        return result.get("value") if result else None
    
    async def get_token_supply(self, mint: str) -> Optional[Dict]:
        """Get token supply."""
        return await self._request("getTokenSupply", [mint])
    
    async def get_token_largest_accounts(self, mint: str) -> List[Dict]:
        """Get largest token holders."""
        result = await self._request("getTokenLargestAccounts", [mint])
        return result.get("value", []) if result else []
    
    async def get_signatures_for_address(
        self,
        address: str,
        before: Optional[str] = None,
        until: Optional[str] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """Get transaction signatures for address."""
        params = [address, {"limit": limit}]
        if before:
            params[1]["before"] = before
        if until:
            params[1]["until"] = until
        return await self._request("getSignaturesForAddress", params) or []
    
    async def get_transaction(self, signature: str) -> Optional[Dict]:
        """Get full transaction details."""
        params = [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}]
        return await self._request("getTransaction", params)
    
    async def get_token_accounts_by_owner(
        self,
        owner: str,
        mint: Optional[str] = None
    ) -> List[Dict]:
        """Get token accounts owned by address."""
        if mint:
            params = [owner, {"mint": mint}, {"encoding": "jsonParsed"}]
        else:
            params = [owner, {"programId": TOKEN_PROGRAM_ID}, {"encoding": "jsonParsed"}]
        result = await self._request("getTokenAccountsByOwner", params)
        return result.get("value", []) if result else []


class PumpFunAPIClient:
    """Pump.fun Frontend API client."""
    
    def __init__(self, jwt_token: Optional[str] = None):
        self.jwt_token = jwt_token
        self.base_url = "https://frontend-api-v3.pump.fun"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        self.session = aiohttp.ClientSession(headers=headers)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def _request(self, endpoint: str, params: Dict = None) -> Any:
        """Make API request."""
        url = f"{self.base_url}{endpoint}"
        async with self.session.get(url, params=params) as resp:
            if resp.status == 429:
                raise Exception("Rate limited")
            resp.raise_for_status()
            return await resp.json()
    
    async def get_coins(
        self,
        sort_by: str = "marketCap",
        limit: int = 50,
        offset: int = 0,
        market_cap_from: Optional[float] = None,
        market_cap_to: Optional[float] = None
    ) -> List[Dict]:
        """Get list of coins with filtering."""
        params = {
            "sort_by": sort_by,
            "limit": limit,
            "offset": offset
        }
        if market_cap_from is not None:
            params["market_cap_from"] = market_cap_from
        if market_cap_to is not None:
            params["market_cap_to"] = market_cap_to
        return await self._request("/coins", params)
    
    async def get_coin(self, mint: str) -> Dict:
        """Get specific coin details."""
        return await self._request(f"/coins/{mint}")
    
    async def get_coin_trades(self, mint: str, limit: int = 100) -> List[Dict]:
        """Get trades for a coin."""
        return await self._request(f"/coins/{mint}/trades", {"limit": limit})
    
    async def get_candlesticks(
        self,
        mint: str,
        timeframe: int = 5,
        limit: int = 1000,
        offset: int = 0
    ) -> List[Dict]:
        """Get OHLCV candlestick data."""
        params = {
            "timeframe": timeframe,
            "limit": limit,
            "offset": offset
        }
        return await self._request(f"/coins/{mint}/candlesticks", params)
    
    async def get_latest_token(self) -> Dict:
        """Get most recently created token."""
        return await self._request("/coins/latest")
    
    async def get_graduates(self, limit: int = 50) -> List[Dict]:
        """Get graduated tokens (migrated to Raydium)."""
        return await self._request("/coins/graduates", {"limit": limit})
    
    async def search_tokens(self, term: str) -> List[Dict]:
        """Search tokens by term."""
        return await self._request("/search", {"term": term})


class JupiterPriceClient:
    """Jupiter Price API client."""
    
    def __init__(self):
        self.base_url = "https://api.jup.ag/price/v2"
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def get_prices(
        self,
        mints: List[str],
        vs_token: str = "USDC"
    ) -> Dict[str, float]:
        """Get token prices."""
        ids_param = ",".join(mints)
        url = f"{self.base_url}?ids={ids_param}&vsToken={vs_token}"
        
        async with self.session.get(url) as resp:
            data = await resp.json()
            prices = {}
            for mint, info in data.get("data", {}).items():
                if info and "price" in info:
                    prices[mint] = float(info["price"])
            return prices


# ============================================================================
# TRANSACTION PARSERS
# ============================================================================

class PumpFunTransactionParser:
    """Parse pump.fun transactions."""
    
    @staticmethod
    def parse_transaction(tx_data: Dict) -> Optional[Dict]:
        """Parse a pump.fun transaction."""
        meta = tx_data.get("meta", {})
        transaction = tx_data.get("transaction", {})
        message = transaction.get("message", {})
        
        # Get account keys
        account_keys = message.get("accountKeys", [])
        if not account_keys:
            return None
        
        # Get instructions
        instructions = message.get("instructions", [])
        
        for ix in instructions:
            program_id_idx = ix.get("programIdIndex", 0)
            if program_id_idx >= len(account_keys):
                continue
            
            program_id = account_keys[program_id_idx]
            if program_id != PUMP_FUN_PROGRAM_ID:
                continue
            
            # Parse instruction data
            data = ix.get("data", "")
            accounts = ix.get("accounts", [])
            
            # Decode base58 data
            try:
                decoded = base58.b58decode(data)
                discriminator = decoded[:8]
            except:
                continue
            
            # Determine instruction type
            if discriminator == CREATE_DISCRIMINATOR or discriminator == CREATE_V2_DISCRIMINATOR:
                return PumpFunTransactionParser._parse_create(tx_data, ix, account_keys)
            elif discriminator == BUY_DISCRIMINATOR:
                return PumpFunTransactionParser._parse_buy(tx_data, ix, account_keys, meta)
            elif discriminator == SELL_DISCRIMINATOR:
                return PumpFunTransactionParser._parse_sell(tx_data, ix, account_keys, meta)
        
        return None
    
    @staticmethod
    def _parse_create(tx_data: Dict, ix: Dict, account_keys: List[str]) -> Dict:
        """Parse token creation instruction."""
        accounts = ix.get("accounts", [])
        
        return {
            "type": "create",
            "signature": tx_data.get("transaction", {}).get("signatures", [""])[0],
            "slot": tx_data.get("slot"),
            "block_time": datetime.fromtimestamp(tx_data.get("blockTime", 0)),
            "mint": account_keys[accounts[0]] if len(accounts) > 0 else None,
            "bonding_curve": account_keys[accounts[2]] if len(accounts) > 2 else None,
            "creator": account_keys[0],  # Fee payer is creator
        }
    
    @staticmethod
    def _parse_buy(tx_data: Dict, ix: Dict, account_keys: List[str], meta: Dict) -> Dict:
        """Parse buy instruction."""
        accounts = ix.get("accounts", [])
        
        # Extract amounts from inner instructions or token balances
        pre_balances = meta.get("preTokenBalances", [])
        post_balances = meta.get("postTokenBalances", [])
        
        token_amount = 0
        sol_amount = 0
        
        # Calculate token amount from balance changes
        for pre in pre_balances:
            for post in post_balances:
                if pre.get("accountIndex") == post.get("accountIndex"):
                    pre_amount = float(pre.get("uiTokenAmount", {}).get("uiAmount", 0))
                    post_amount = float(post.get("uiTokenAmount", {}).get("uiAmount", 0))
                    token_amount = abs(post_amount - pre_amount)
        
        # Calculate SOL amount from native balance changes
        pre_sol = meta.get("preBalances", [0])[0] / 1e9
        post_sol = meta.get("postBalances", [0]) / 1e9
        sol_amount = abs(pre_sol - post_sol)
        
        return {
            "type": "buy",
            "signature": tx_data.get("transaction", {}).get("signatures", [""])[0],
            "slot": tx_data.get("slot"),
            "block_time": datetime.fromtimestamp(tx_data.get("blockTime", 0)),
            "mint": account_keys[accounts[2]] if len(accounts) > 2 else None,
            "trader": account_keys[accounts[6]] if len(accounts) > 6 else None,
            "token_amount": token_amount,
            "sol_amount": sol_amount,
            "price_sol": sol_amount / token_amount if token_amount > 0 else 0,
        }
    
    @staticmethod
    def _parse_sell(tx_data: Dict, ix: Dict, account_keys: List[str], meta: Dict) -> Dict:
        """Parse sell instruction."""
        accounts = ix.get("accounts", [])
        
        # Similar to buy but with reversed amounts
        pre_balances = meta.get("preTokenBalances", [])
        post_balances = meta.get("postTokenBalances", [])
        
        token_amount = 0
        sol_amount = 0
        
        for pre in pre_balances:
            for post in post_balances:
                if pre.get("accountIndex") == post.get("accountIndex"):
                    pre_amount = float(pre.get("uiTokenAmount", {}).get("uiAmount", 0))
                    post_amount = float(post.get("uiTokenAmount", {}).get("uiAmount", 0))
                    token_amount = abs(pre_amount - post_amount)
        
        pre_sol = meta.get("preBalances", [0])[0] / 1e9
        post_sol = meta.get("postBalances", [0]) / 1e9
        sol_amount = abs(pre_sol - post_sol)
        
        return {
            "type": "sell",
            "signature": tx_data.get("transaction", {}).get("signatures", [""])[0],
            "slot": tx_data.get("slot"),
            "block_time": datetime.fromtimestamp(tx_data.get("blockTime", 0)),
            "mint": account_keys[accounts[2]] if len(accounts) > 2 else None,
            "trader": account_keys[accounts[6]] if len(accounts) > 6 else None,
            "token_amount": token_amount,
            "sol_amount": sol_amount,
            "price_sol": sol_amount / token_amount if token_amount > 0 else 0,
        }


# ============================================================================
# REAL-TIME STREAMS
# ============================================================================

class PumpFunWebSocketStream:
    """WebSocket stream for real-time pump.fun data."""
    
    def __init__(self, jwt_token: Optional[str] = None):
        self.jwt_token = jwt_token
        self.ws_url = "wss://frontend-api-v3.pump.fun/ws"
        self.ws = None
        self.running = False
    
    async def connect(self):
        """Connect to WebSocket."""
        headers = {}
        if self.jwt_token:
            headers["Authorization"] = f"Bearer {self.jwt_token}"
        
        self.ws = await websockets.connect(self.ws_url, extra_headers=headers)
        self.running = True
    
    async def subscribe_trades(self, mint: Optional[str] = None):
        """Subscribe to trade events."""
        message = {
            "method": "subscribe",
            "params": {
                "channel": "trades",
                "mint": mint  # Subscribe to specific token or all
            }
        }
        await self.ws.send(json.dumps(message))
    
    async def subscribe_new_tokens(self):
        """Subscribe to new token creation events."""
        message = {
            "method": "subscribe",
            "params": {
                "channel": "new_tokens"
            }
        }
        await self.ws.send(json.dumps(message))
    
    async def listen(self, callback):
        """Listen for messages."""
        while self.running:
            try:
                message = await self.ws.recv()
                data = json.loads(message)
                await callback(data)
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed, reconnecting...")
                await self.connect()
            except Exception as e:
                print(f"Error: {e}")
    
    async def close(self):
        """Close connection."""
        self.running = False
        if self.ws:
            await self.ws.close()


class HeliusWebhookHandler:
    """Handle Helius webhook events."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.helius.xyz/v0"
    
    async def create_webhook(
        self,
        webhook_url: str,
        account_addresses: List[str],
        transaction_types: List[str] = None
    ) -> str:
        """Create a new webhook."""
        url = f"{self.base_url}/webhooks?api-key={self.api_key}"
        
        payload = {
            "webhookURL": webhook_url,
            "accountAddresses": account_addresses,
            "webhookType": "enhanced",
            "transactionTypes": transaction_types or ["Any"]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()
                return data.get("webhookID")
    
    async def delete_webhook(self, webhook_id: str):
        """Delete a webhook."""
        url = f"{self.base_url}/webhooks/{webhook_id}?api-key={self.api_key}"
        
        async with aiohttp.ClientSession() as session:
            await session.delete(url)


# ============================================================================
# RUG PULL DETECTION
# ============================================================================

class RugPullDetector:
    """Detect potential rug pulls."""
    
    def __init__(self, rpc_client: HeliusRPCClient, db: Any):
        self.rpc = rpc_client
        self.db = db
    
    async def analyze_token(self, mint: str) -> Dict[str, Any]:
        """Analyze token for rug pull indicators."""
        indicators = {
            "mint": mint,
            "calculated_at": datetime.utcnow(),
            "risk_score": 0,
            "indicators": []
        }
        
        # 1. Check creator sell-off
        creator_risk = await self._check_creator_sell_off(mint)
        indicators["creator_sold_percentage"] = creator_risk["percentage"]
        if creator_risk["is_risky"]:
            indicators["indicators"].append("creator_sell_off")
            indicators["risk_score"] += 25
        
        # 2. Check holder concentration
        concentration = await self._check_holder_concentration(mint)
        indicators["top_10_percentage"] = concentration["top_10"]
        if concentration["is_concentrated"]:
            indicators["indicators"].append("high_concentration")
            indicators["risk_score"] += 20
        
        # 3. Check liquidity
        liquidity = await self._check_liquidity(mint)
        indicators["liquidity_sol"] = liquidity["amount"]
        if liquidity["is_low"]:
            indicators["indicators"].append("low_liquidity")
            indicators["risk_score"] += 20
        
        # 4. Check trading patterns
        patterns = await self._check_trading_patterns(mint)
        if patterns["has_wash_trading"]:
            indicators["indicators"].append("wash_trading")
            indicators["risk_score"] += 15
        
        # 5. Check if creator has history of rugs
        creator_history = await self._check_creator_history(mint)
        if creator_history["has_rug_history"]:
            indicators["indicators"].append("creator_rug_history")
            indicators["risk_score"] += 20
        
        # Determine risk level
        if indicators["risk_score"] >= 70:
            indicators["risk_level"] = "HIGH"
        elif indicators["risk_score"] >= 40:
            indicators["risk_level"] = "MEDIUM"
        else:
            indicators["risk_level"] = "LOW"
        
        return indicators
    
    async def _check_creator_sell_off(self, mint: str) -> Dict:
        """Check if creator has sold significant portion."""
        # Get token info
        token = await self.db.get_token(mint)
        creator = token["creator_wallet"]
        
        # Get creator's current balance
        token_accounts = await self.rpc.get_token_accounts_by_owner(creator, mint)
        current_balance = sum(
            float(acc["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"] or 0)
            for acc in token_accounts
        )
        
        # Get total supply
        supply_info = await self.rpc.get_token_supply(mint)
        total_supply = float(supply_info.get("uiAmount", 0))
        
        if total_supply == 0:
            return {"percentage": 0, "is_risky": False}
        
        # Calculate percentage creator still holds
        creator_percentage = (current_balance / total_supply) * 100
        sold_percentage = 100 - creator_percentage
        
        return {
            "percentage": sold_percentage,
            "is_risky": sold_percentage > 80  # Risky if creator sold >80%
        }
    
    async def _check_holder_concentration(self, mint: str) -> Dict:
        """Check if supply is concentrated among few holders."""
        largest = await self.rpc.get_token_largest_accounts(mint)
        
        supply_info = await self.rpc.get_token_supply(mint)
        total_supply = float(supply_info.get("uiAmount", 0))
        
        if total_supply == 0 or not largest:
            return {"top_10": 0, "is_concentrated": False}
        
        # Calculate top 10 holder percentage
        top_10_amount = sum(
            float(holder.get("uiAmount", 0))
            for holder in largest[:10]
        )
        top_10_percentage = (top_10_amount / total_supply) * 100
        
        return {
            "top_10": top_10_percentage,
            "is_concentrated": top_10_percentage > 50  # Risky if >50% held by top 10
        }
    
    async def _check_liquidity(self, mint: str) -> Dict:
        """Check liquidity status."""
        token = await self.db.get_token(mint)
        
        # For non-migrated tokens, check bonding curve
        if not token.get("is_migrated"):
            # Get bonding curve balance
            bonding_curve = token.get("bonding_curve_address")
            if bonding_curve:
                account = await self.rpc.get_account_info(bonding_curve)
                if account:
                    # Parse bonding curve data for SOL amount
                    # This is simplified - actual parsing would be more complex
                    return {
                        "amount": 0,  # Parse from account data
                        "is_low": True
                    }
        
        return {
            "amount": 0,
            "is_low": False
        }
    
    async def _check_trading_patterns(self, mint: str) -> Dict:
        """Check for suspicious trading patterns."""
        # Get recent trades
        trades = await self.db.get_recent_trades(mint, hours=24)
        
        # Check for wash trading (same wallet buying and selling)
        wallet_activity = {}
        for trade in trades:
            wallet = trade["trader_wallet"]
            if wallet not in wallet_activity:
                wallet_activity[wallet] = {"buys": 0, "sells": 0}
            
            if trade["trade_type"] == "buy":
                wallet_activity[wallet]["buys"] += 1
            else:
                wallet_activity[wallet]["sells"] += 1
        
        # Flag wallets with both buys and sells
        wash_trading_wallets = [
            w for w, activity in wallet_activity.items()
            if activity["buys"] > 0 and activity["sells"] > 0
        ]
        
        return {
            "has_wash_trading": len(wash_trading_wallets) > 5,
            "suspicious_wallets": wash_trading_wallets
        }
    
    async def _check_creator_history(self, mint: str) -> Dict:
        """Check if creator has history of rug pulls."""
        token = await self.db.get_token(mint)
        creator = token["creator_wallet"]
        
        # Get all tokens created by this wallet
        creator_tokens = await self.db.get_tokens_by_creator(creator)
        
        # Count how many were flagged as rugs
        rug_count = sum(1 for t in creator_tokens if t.get("is_rugged"))
        total_tokens = len(creator_tokens)
        
        rug_percentage = (rug_count / total_tokens * 100) if total_tokens > 0 else 0
        
        return {
            "has_rug_history": rug_percentage > 50,  # Risky if >50% of tokens rugged
            "rug_percentage": rug_percentage,
            "total_tokens": total_tokens,
            "rug_count": rug_count
        }


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

async def example_token_discovery():
    """Example: Discover new tokens via RPC polling."""
    api_key = "your_helius_api_key"
    
    async with HeliusRPCClient(api_key) as rpc:
        # Get recent signatures for pump.fun program
        signatures = await rpc.get_signatures_for_address(
            PUMP_FUN_PROGRAM_ID,
            limit=100
        )
        
        for sig_info in signatures:
            sig = sig_info["signature"]
            tx = await rpc.get_transaction(sig)
            
            if tx:
                parsed = PumpFunTransactionParser.parse_transaction(tx)
                if parsed and parsed["type"] == "create":
                    print(f"New token created: {parsed['mint']}")
                    print(f"Creator: {parsed['creator']}")
                    print(f"Slot: {parsed['slot']}")


async def example_trade_monitoring():
    """Example: Monitor trades via WebSocket."""
    jwt_token = "your_pump_fun_jwt"
    
    stream = PumpFunWebSocketStream(jwt_token)
    await stream.connect()
    await stream.subscribe_trades()
    
    async def handle_trade(data):
        """Process incoming trade."""
        if data.get("type") == "trade":
            trade = data.get("data", {})
            print(f"Trade: {trade.get('type')} {trade.get('tokenAmount')} tokens")
            print(f"Price: {trade.get('price')} SOL")
            print(f"Trader: {trade.get('user')}")
    
    await stream.listen(handle_trade)


async def example_price_tracking():
    """Example: Track token prices."""
    token_mints = [
        "2q7jMwWYFxUdxBqWbi8ohztyG1agjQMrasUXwqGCpump",
        # Add more token mints
    ]
    
    async with JupiterPriceClient() as jupiter:
        prices = await jupiter.get_prices(token_mints)
        
        for mint, price in prices.items():
            print(f"Token {mint}: ${price:.6f}")


async def example_historical_backfill():
    """Example: Backfill historical data."""
    api_key = "your_helius_api_key"
    mint = "2q7jMwWYFxUdxBqWbi8ohztyG1agjQMrasUXwqGCpump"
    
    async with HeliusRPCClient(api_key) as rpc:
        # Get all signatures for token
        all_signatures = []
        before = None
        
        while True:
            signatures = await rpc.get_signatures_for_address(
                mint,
                before=before,
                limit=1000
            )
            
            if not signatures:
                break
            
            all_signatures.extend(signatures)
            before = signatures[-1]["signature"]
            
            print(f"Fetched {len(all_signatures)} signatures so far...")
            await asyncio.sleep(0.1)  # Rate limiting
        
        print(f"Total signatures: {len(all_signatures)}")
        
        # Fetch and parse transactions
        for sig_info in all_signatures:
            tx = await rpc.get_transaction(sig_info["signature"])
            if tx:
                parsed = PumpFunTransactionParser.parse_transaction(tx)
                if parsed:
                    print(f"{parsed['type']}: {parsed.get('token_amount', 'N/A')} tokens")


async def example_rug_pull_detection():
    """Example: Detect rug pull indicators."""
    api_key = "your_helius_api_key"
    mint = "suspicious_token_mint"
    
    # Mock database
    class MockDB:
        async def get_token(self, mint):
            return {
                "mint_address": mint,
                "creator_wallet": "creator_wallet_address",
                "is_migrated": False
            }
        
        async def get_recent_trades(self, mint, hours=24):
            return []  # Mock trades
        
        async def get_tokens_by_creator(self, creator):
            return []  # Mock tokens
    
    async with HeliusRPCClient(api_key) as rpc:
        detector = RugPullDetector(rpc, MockDB())
        analysis = await detector.analyze_token(mint)
        
        print(f"Risk Score: {analysis['risk_score']}/100")
        print(f"Risk Level: {analysis['risk_level']}")
        print(f"Indicators: {', '.join(analysis['indicators'])}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Run examples
    print("=" * 60)
    print("Pump.fun Data Collection - Implementation Examples")
    print("=" * 60)
    
    # Uncomment to run specific examples:
    # asyncio.run(example_token_discovery())
    # asyncio.run(example_trade_monitoring())
    # asyncio.run(example_price_tracking())
    # asyncio.run(example_historical_backfill())
    # asyncio.run(example_rug_pull_detection())
