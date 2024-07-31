async function mineAndCheckChest(bot) {
  // Check if you have an axe in your inventory
  const hasAxe = bot.inventory.findInventoryItem(mcData.itemsByName["wooden_axe"].id);
  if (!hasAxe) {
    // Craft an axe by mining 3 wood logs
    await mineThreeMoreOakLogs(bot);
  }

  // Find 3 oak log blocks
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

  // Mine the 3 oak log blocks
  await mineBlock(bot, "oak_log", 3);
  bot.chat("3 oak logs mined.");

  // Open and check the unknown items inside the chest
  const chest = bot.findBlock({
    matching: mcData.blocksByName["chest"].id,
    maxDistance: 32
  });
  if (chest) {
    await bot.pathfinder.goto(new GoalBlock(chest.position.x, chest.position.y, chest.position.z));
    await bot.lookAt(chest.position.offset(0.5, 0, 0.5));
    await bot.activateBlock(chest);
    bot.chat("Opened the chest.");
  } else {
    bot.chat("Could not find a chest nearby.");
  }
}