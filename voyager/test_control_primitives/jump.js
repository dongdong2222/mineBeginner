async function jump(bot, ticks){
    bot.setControlState('jump', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('jump', false);
}
