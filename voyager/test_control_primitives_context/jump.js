//Go jump 10 ticks: jump(10)
async function jump(bot, ticks){
    bot.setControlState('jump', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('jump', false);
}
