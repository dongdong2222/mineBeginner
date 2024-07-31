async function sprint(bot, ticks) {
    if (typeof ticks !== "number") {
        throw new Error("tick must be a number");
    }
    if (bot.getControlState('sprint') !== true){
        try{
            bot.setControlState('sprint', true);
            // bot.chat('I press the key W');
        }catch(err){
        }

    }
    await bot.waitForTicks(ticks);
    bot.setControlState('sneak', false);
}