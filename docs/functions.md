# Functions

| Name | Args | Returns |
|---|---|---|
| `await get_stats` | `username: str` | `dict[str, str]` |
| `await get_broken_blocks` | `username: str` | `int` |
| `await get_deaths` | `username: str` | `int` |
| `await get_kills` | `username: str` | `int` |
| `await get_mobs_killed` | `username: str` | `int` |
| `await get_balance` | `username: str` | `int` — `money` |
| `await get_money_made_from_sell` | `username: str` | `int` |
| `await get_money_spent_on_shop` | `username: str` | `int` |
| `await get_placed_blocks` | `username: str` | `int` |
| `await get_playtime` | `username: str` | `int` |
| `await get_shards` | `username: str` | `int` |
| `await get_stats_embed` | `username: str, color: discord.Color \| Default` | `discord.Embed` — requires `donutstats[discord]` |
| `await close` | `None` | closes the session

### `get_stats` keys

`broken_blocks`, `deaths`, `kills`, `mobs_killed`, `money`, `money_made_from_sell`, `money_spent_on_shop`, `placed_blocks`, `playtime`, `shards`