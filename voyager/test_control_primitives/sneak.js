async function sneak(bot, ticks) {
    if (typeof ticks !== "number") {
        throw new Error("tick must be a number");
    }
    if (bot.getControlState('sneak') !== true){
        try{
            bot.setControlState('sneak', true);
            // bot.chat('I press the key W');
        }catch(err){
        }

    }
    await bot.waitForTicks(ticks);
    bot.setControlState('sneak', false);
}