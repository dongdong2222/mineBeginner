async function mineWoodLog(bot) {
  const axeName = "wooden_axe";
  const woodLogNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];

  // Check if you have an axe in your inventory
  const hasAxe = bot.inventory.findInventoryItem(mcData.itemsByName[axeName].id);
  if (!hasAxe) {
    // Craft an axe by mining 3 wood logs
    await mineThreeMoreOakLogs(bot);
  }

  // Find a wood log block
  const woodLogBlock = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    return bot.findBlock({
      matching: block => woodLogNames.includes(block.name),
      maxDistance: 32
    });
  });
  if (!woodLogBlock) {
    bot.chat("Could not find a wood log.");
    return;
  }

  // Mine the wood log block
  await mineBlock(bot, woodLogBlock.name, 1);
  bot.chat("Wood log mined.");
}

async function mineThreeMoreOakLogs(bot) {
  // Check the initial inventory for oak logs
  const initialOakLogs = bot.inventory.count(mcData.itemsByName.oak_log.id);

  // Find 3 oak_log blocks
  const oakLogs = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
    const oakLogs = bot.findBlocks({
      matching: block => block.name === "oak_log",
      maxDistance: 32,
      count: 3
    });
    return oakLogs.length >= 3 ? oakLogs : null;
  });
  if (!oakLogs) {
    bot.chat("Could not find enough oak logs.");
    return;
  }

  // Mine the oak_log blocks
  await mineBlock(bot, "oak_log", 3);
  bot.chat("3 oak logs mined.");

  // Compare the final inventory with the initial inventory
  const finalOakLogs = bot.inventory.count(mcData.itemsByName.oak_log.id);
  if (finalOakLogs - initialOakLogs === 3) {
    bot.chat("Successfully mined 3 more oak logs.");
  } else {
    bot.chat("Failed to mine 3 more oak logs.");
  }
}