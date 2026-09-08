"""株式投資の基礎計算ツール。

docs/stock-basics.md で説明している計算式を、そのまま関数にしたもの。
金額は円、比率は小数（0.05 = 5%）で扱う。
"""


def position_size(total_assets, risk_ratio, entry_price, stop_price):
    """1回の取引で許容する損失額から、買える株数を求める。

    total_assets: 総資産
    risk_ratio:   1トレードで許容する損失の割合（0.01 = 1%）
    entry_price:  購入価格
    stop_price:   損切り価格（entry_price より低いこと）

    >>> position_size(3_000_000, 0.01, 2000, 1800)
    150
    """
    if stop_price >= entry_price:
        raise ValueError("stop_price must be below entry_price")
    allowed_loss = total_assets * risk_ratio
    return int(allowed_loss // (entry_price - stop_price))


def breakeven_gain(drawdown):
    """下落率から、元本に戻すために必要な上昇率を求める。

    >>> round(breakeven_gain(0.5), 4)
    1.0
    >>> round(breakeven_gain(0.2), 4)
    0.25
    """
    if not 0 <= drawdown < 1:
        raise ValueError("drawdown must be in [0, 1)")
    return 1 / (1 - drawdown) - 1


def compound(principal, annual_rate, years):
    """複利での将来価値を求める。

    >>> round(compound(1_000_000, 0.05, 30))
    4321942
    """
    return principal * (1 + annual_rate) ** years


def per(price, eps):
    """株価収益率。eps が 0 以下なら計算できない。"""
    if eps <= 0:
        raise ValueError("PER is undefined for non-positive EPS")
    return price / eps


def pbr(price, bps):
    """株価純資産倍率。"""
    if bps <= 0:
        raise ValueError("PBR is undefined for non-positive BPS")
    return price / bps


def dividend_yield(annual_dividend, price):
    """配当利回り（小数）。

    >>> round(dividend_yield(100, 2500), 4)
    0.04
    """
    return annual_dividend / price


def payout_ratio(annual_dividend, eps):
    """配当性向（小数）。100% を超えると持続不能のサイン。"""
    if eps <= 0:
        raise ValueError("payout ratio is undefined for non-positive EPS")
    return annual_dividend / eps


if __name__ == "__main__":
    print(f"買える株数: {position_size(3_000_000, 0.01, 2000, 1800)} 株")
    print(f"-50% からの回復に必要な上昇率: {breakeven_gain(0.5):.0%}")
    print(f"100万円を年5%で30年: {compound(1_000_000, 0.05, 30):,.0f} 円")
