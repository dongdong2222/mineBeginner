async function craftOakPlanks(bot) {
  const oakLogsCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
  if (oakLogsCount < 4) {
    // Mine oak logs if there are not enough in the inventory
    await mineBlock(bot, "oak_log", 1);
    bot.chat("Mined oak logs.");
  }

  // Check if there are enough oak logs in the inventory after mining
  const updatedOakLogsCount = bot.inventory.count(mcData.itemsByName.oak_log.id);
  if (updatedOakLogsCount >= 4) {
    // Place a crafting table near the player
    const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
    await placeItem(bot, "crafting_table", craftingTablePosition);
    bot.chat("Placed a crafting table.");

    // Craft oak planks using the crafting table
    await moveBack(bot, "oak_planks", 1);
    bot.chat("Crafted oak planks.");
  } else {
    bot.chat("Not enough oak logs to craft oak planks.");
  }
}