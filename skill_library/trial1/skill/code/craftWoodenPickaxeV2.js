async function craftWoodenPickaxe(bot) {
  // Check if there are enough oak logs in the inventory
  const oakLogsCount = bot.inventory.count(mcData.itemsByName.oak_log.id);

  // If not enough oak logs, explore until oak logs are found
  if (oakLogsCount < 3) {
    bot.chat("No oak logs in inventory, exploring to find oak logs.");
    const oakLogsFound = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const oakLog = bot.findBlock({
        matching: mcData.blocksByName["oak_log"].id,
        maxDistance: 32
      });
      return oakLog;
    });
    if (!oakLogsFound) {
      bot.chat("Could not find oak logs in time.");
      return;
    }
  }

  // Check if there is a crafting table in the inventory
  const craftingTableCount = bot.inventory.count(mcData.itemsByName.crafting_table.id);

  // If no crafting table, explore until a crafting table is found
  if (craftingTableCount === 0) {
    bot.chat("No crafting table in inventory, exploring to find a crafting table.");
    const craftingTableFound = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
      const craftingTable = bot.findBlock({
        matching: mcData.blocksByName["crafting_table"].id,
        maxDistance: 32
      });
      return craftingTable;
    });
    if (!craftingTableFound) {
      bot.chat("Could not find a crafting table in time.");
      return;
    }
  }

  // Check if there are enough oak planks and sticks in the inventory
  const oakPlanksCount = bot.inventory.count(mcData.itemsByName.oak_planks.id);
  const sticksCount = bot.inventory.count(mcData.itemsByName.stick.id);

  // If not enough oak planks, craft oak planks
  if (oakPlanksCount < 3) {
    await craftItem(bot, "oak_planks", 3 - oakPlanksCount);
    bot.chat("Crafted oak planks.");
  }

  // If not enough sticks, craft sticks
  if (sticksCount < 2) {
    await craftItem(bot, "stick", 2 - sticksCount);
    bot.chat("Crafted sticks.");
  }

  // Place the crafting table near the bot
  const craftingTablePosition = bot.entity.position.offset(1, 0, 0);
  await placeItem(bot, "crafting_table", craftingTablePosition);

  // Craft a wooden pickaxe using the crafting table
  await craftItem(bot, "wooden_pickaxe", 1);
  bot.chat("Crafted a wooden pickaxe.");
}