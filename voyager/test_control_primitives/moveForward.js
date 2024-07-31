async function moveForward(bot, ticks) {
    if (typeof ticks !== "number") {
        throw new Error("tick must be a number");
    }
    if (bot.getControlState('forward') !== true){
        try{
            bot.setControlState('forward', true);
            // bot.chat('I press the key W');
        }catch(err){
        }

    }
    await bot.waitForTicks(ticks);
    bot.setControlState('forward', false);
}
