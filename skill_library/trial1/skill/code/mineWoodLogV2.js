async function mineWoodLog(bot) {
  const axeName = "wooden_axe";
  const woodLogNames = ["oak_log", "birch_log", "spruce_log", "jungle_log", "acacia_log", "dark_oak_log", "mangrove_log"];
  const hasAxe = bot.inventory.findInventoryItem(mcData.itemsByName[axeName].id);
  if (!hasAxe) {
    await mineThreeMoreOakLogs(bot);
  }
  let woodLogBlock = null;
  while (!woodLogBlock) {
    woodLogBlock = await exploreUntil(bot, new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1), 60, () => {
      return bot.findBlock({
        matching: block => woodLogNames.includes(block.name),
        maxDistance: 32
      });
    });
  }
  await mineBlock(bot, woodLogBlock.name, 1);
  bot.chat("Wood log mined.");
}