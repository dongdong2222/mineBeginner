//Go back 10 ticks: back(10)
async function moveBack(bot, ticks){
    bot.setControlState('back', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('back', false);
}