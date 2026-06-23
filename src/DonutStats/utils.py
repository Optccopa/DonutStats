def fmt_amount(n: int | float) -> str:
    """Formats into a k / m / b / t string"""
    n = float(n)
    if abs(n) < 1000:
        return str(int(n)) if n == int(n) else f"{n:.2f}"
    for divisor, suffix in ((1e12, "t"), (1e9, "b"), (1e6, "m"), (1e3, "k")):
        if abs(n) >= divisor:
            v = n / divisor
            s = f"{v:.2f}".rstrip("0").rstrip(".")
            return f"{s}{suffix}"
        
def fmt_playtime(ms: int) -> str:
    """Formats donutsmp playtime"""
    seconds = ms // 1000

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")

    return " ".join(parts) or "0m"