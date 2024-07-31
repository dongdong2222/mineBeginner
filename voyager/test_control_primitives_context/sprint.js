//Go sprint 10 ticks: sprint(10)
async function sprint(bot, ticks){
    bot.setControlState('sprint', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('sprint', false);
}
