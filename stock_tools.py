"""株式投資の基礎計算ツール。

docs/stock-basics.md で説明している計算式を、そのまま関数にしたもの。
金額は円、比率は小数（0.05 = 5%）で扱う。
"""


def position_size(total_assets, risk_ratio, entry_price, stop_price):
    """1回の取引で許容する損失額から、買える株数を求める（ポジションサイジング）。

    「何を買うか」より「いくら買うか」の方が資産曲線への影響は大きい。
    損切り幅が広い（値動きが荒い）銘柄ほど株数が自動的に小さくなるのが、この式の利点。

    total_assets: 総資産
    risk_ratio:   1トレードで許容する損失の割合（0.01 = 1%）
    entry_price:  購入価格
    stop_price:   損切り価格（entry_price より低いこと）

    総資産300万円・リスク1%・2,000円で買い1,800円で損切りするなら 150株:

    >>> position_size(3_000_000, 0.01, 2000, 1800)
    150

    損切り幅を倍（400円）にすると、株数は半分になる:

    >>> position_size(3_000_000, 0.01, 2000, 1600)
    75
    """
    if stop_price >= entry_price:
        raise ValueError("stop_price must be below entry_price")
    allowed_loss = total_assets * risk_ratio
    return int(allowed_loss // (entry_price - stop_price))


def breakeven_gain(drawdown):
    """下落率から、元本に戻すために必要な上昇率を求める。

    損失が深くなるほど、回復に必要なリターンは非線形に跳ね上がる。
    半減した資産を元に戻すには2倍にする必要がある、というのがこの式の要点。

    >>> round(breakeven_gain(0.2), 4)
    0.25
    >>> round(breakeven_gain(0.5), 4)
    1.0
    >>> round(breakeven_gain(0.8), 4)
    4.0
    """
    if not 0 <= drawdown < 1:
        raise ValueError("drawdown must be in [0, 1)")
    return 1 / (1 - drawdown) - 1


def compound(principal, annual_rate, years):
    """複利での将来価値を求める。

    利益を再投資すると、利益がさらに利益を生む。期間が延びるほど効きが大きくなる。

    100万円を年5%で30年運用すると約432万円:

    >>> round(compound(1_000_000, 0.05, 30))
    4321942
    """
    return principal * (1 + annual_rate) ** years


def per(price, eps):
    """PER（株価収益率）= 株価 ÷ EPS。

    「利益の何年分の値段か」。年100万円稼ぐ屋台を1,500万円で買えば PER 15倍。
    業種によって標準的な水準が大きく違うため、必ず同業他社と比較すること。
    EPS が 0 以下（赤字）の場合は計算できない。

    >>> per(3000, 200)
    15.0
    """
    if eps <= 0:
        raise ValueError("PER is undefined for non-positive EPS")
    return price / eps


def pbr(price, bps):
    """PBR（株価純資産倍率）= 株価 ÷ BPS。

    「1株あたりの財産の何倍の値段か」。1倍未満は帳簿上の解散価値を下回る状態だが、
    在庫やのれんが実態より過大に計上されていることもあるので資産の質の確認が要る。

    >>> pbr(3000, 2500)
    1.2
    """
    if bps <= 0:
        raise ValueError("PBR is undefined for non-positive BPS")
    return price / bps


def dividend_yield(annual_dividend, price):
    """配当利回り（小数）= 年間配当 ÷ 株価。

    高利回りは「株価が下がった結果」であることが多く、減配リスクの裏返しでもある。

    >>> round(dividend_yield(100, 2500), 4)
    0.04
    """
    return annual_dividend / price


def payout_ratio(annual_dividend, eps):
    """配当性向（小数）= 配当 ÷ 純利益。

    利益の何%を株主に配ったか。100%を超えると利益以上に配っている状態で、長続きしない。

    >>> round(payout_ratio(100, 200), 4)
    0.5
    """
    if eps <= 0:
        raise ValueError("payout ratio is undefined for non-positive EPS")
    return annual_dividend / eps


if __name__ == "__main__":
    print(f"買える株数: {position_size(3_000_000, 0.01, 2000, 1800)} 株")
    print(f"-50% からの回復に必要な上昇率: {breakeven_gain(0.5):.0%}")
    print(f"100万円を年5%で30年: {compound(1_000_000, 0.05, 30):,.0f} 円")
