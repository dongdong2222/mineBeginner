//Go sneak 10 ticks: sneak(10)
async function sneak(bot, ticks){
    bot.setControlState('sneak', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('sneak', false);
}