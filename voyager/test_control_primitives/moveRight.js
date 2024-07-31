async function moveRight(bot, ticks) {
    if (typeof ticks !== "number") {
        throw new Error("tick must be a number");
    }
    if (bot.getControlState('right') !== true){
        try{
            bot.setControlState('right', true);
            // bot.chat('I press the key W');
        }catch(err){
        }

    }
    await bot.waitForTicks(ticks);
    bot.setControlState('right', false);
}