async function moveLeft(bot, ticks) {
    if (typeof ticks !== "number") {
        throw new Error("tick must be a number");
    }
    if (bot.getControlState('left') !== true){
        try{
            bot.setControlState('left', true);
            // bot.chat('I press the key W');
        }catch(err){
        }

    }
    await bot.waitForTicks(ticks);
    bot.setControlState('left', false);
}