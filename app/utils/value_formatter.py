def getShortMoneyString(amount: int, ends= "đồng") -> str:
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

def isValidDateString(dateStr: str, dateFormat="%d/%m/%Y") -> bool:
    from datetime import datetime
    try:
        datetime.strptime(dateStr, dateFormat)
        return True
    except ValueError:
        return False
    
def convertDateStringFormat(dateStr: str, currentFormat="%d/%m/%Y", targetFormat="%Y-%m-%d") -> str | None:
    from datetime import datetime
    try:
        dateObj = datetime.strptime(dateStr, currentFormat)
        return dateObj.strftime(targetFormat)
    except ValueError:
        return None