//Go right 10 ticks: right(10)
async function moveRight(bot, ticks){
    bot.setControlState('right', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('right', false);
}