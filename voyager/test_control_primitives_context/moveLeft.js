//Go left 10 ticks: left(10)
async function moveLeft(bot, ticks){
    bot.setControlState('left', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('left', false);
}
