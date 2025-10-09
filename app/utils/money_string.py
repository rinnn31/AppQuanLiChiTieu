def getShortMoneyStringInVND(amount: int, ends= "đồng") -> str:
    if amount  < 100_000:
        return f"{amount:,} {ends}"
    elif amount < 1_000_000:
        return f"{int(amount/1_000)}k {ends}"
    elif amount < 100_000_000:
        return f"{amount/1_000_000:.1f}tr {ends}"
    elif amount < 1_000_000_000:
        return f"{int(amount/1_000_000)}tr {ends}"
    else:
        return f"{amount/1_000_000_000:,.2f}tỷ {ends}"
