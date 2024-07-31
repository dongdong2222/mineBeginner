//Go forward 10 ticks: forward(10)
async function moveForward(bot, ticks) {
    bot.setControlState('forward', true);
    await bot.waitForTicks(ticks);
    bot.setControlState('forward', false);
}

