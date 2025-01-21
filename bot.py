import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta  # 用於日期計算

# 初始化 Bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# 統測日期設定
統測日期 = datetime(2025, 4, 26)

@bot.event
async def on_ready():
    print(f"已登入為 {bot.user}")
    try:
        synced = await bot.tree.sync()  # 同步全域指令
        print(f"同步 {len(synced)} 個指令成功！")
    except Exception as e:
        print(f"同步指令失敗：{e}")

# 定義一個倒數的 Slash Command
@bot.tree.command(name="countdown")
async def countdown(interaction: discord.Interaction, seconds: int):
    """倒數計時指令"""
    if seconds <= 0:
        await interaction.response.send_message("請輸入大於 0 的秒數！", ephemeral=True)
        return

    # 初次回應，用於告知倒數開始
    await interaction.response.defer()  # 延遲回應以允許後續操作
    message = await interaction.followup.send(f"倒數開始：{seconds} 秒")

    # 倒數計時
    for i in range(seconds, 0, -1):
        await asyncio.sleep(1)  # 使用 asyncio.sleep 延遲
        await message.edit(content=f"倒數：{i} 秒")

    # 倒數結束
    await message.edit(content="⏰ 時間到！")

# 定義統測倒數的 Slash Command
@bot.tree.command(name="統測倒數")
async def 統測倒數(interaction: discord.Interaction):
    """計算距離統測還有多少天"""
    # 計算剩餘天數
    today = datetime.now()
    days_left = (統測日期 - today).days

    if days_left < 0:
        message = "統測已經結束，請繼續加油努力！🎓"
    elif days_left == 0:
        message = "今天就是統測！祝你考試順利！📚✏️"
    else:
        message = f"距離統測還有 {days_left} 天，請好好準備！💪"

    # 回應使用者
    await interaction.response.send_message(message)

# 啟動 Bot（將 "YOUR_TOKEN_HERE" 替換為你的機器人 Token）
bot.run("")
