async function collectMangroveRoots(bot) {
  const requiredMangroveRoots = 5;

  // Check if the player has enough mangrove roots
  const mangroveRootsCount = bot.inventory.count(mcData.itemsByName["mangrove_roots"].id);
  if (mangroveRootsCount < requiredMangroveRoots) {
    bot.chat("Searching for mangrove roots...");

    // Find and collect 5 mangrove roots
    const mangroveRoots = await exploreUntil(bot, new Vec3(Math.floor(Math.random() * 3) - 1, 0, Math.floor(Math.random() * 3) - 1), 32, () => {
      const roots = bot.findBlocks({
        matching: block => block.name === "mangrove_roots",
        maxDistance: 32,
        count: requiredMangroveRoots
      });
      return roots.length >= requiredMangroveRoots ? roots : null;
    });
    if (!mangroveRoots) {
      bot.chat("Could not find enough mangrove roots.");
      return;
    }

    // Mine the 5 mangrove roots
    await mineBlock(bot, "mangrove_roots", requiredMangroveRoots);
    bot.chat("Collected 5 mangrove roots.");
  } else {
    bot.chat("Already have enough mangrove roots.");
  }
}

// Call the function to collect 5 mangrove roots