const Observation = require("./base.js").Observation;

class onDetection extends Observation {
    constructor(bot) {
        super(bot);
        this.name = "onDetection";
        this.obs = {};
        bot.on("detect", (factor, value) => {
            this.obs[factor] = value;
            this.bot.event(this.name);
        });
    }

    observe() {
        const result = this.obs;
        this.obs = {};
        return result;
    }
}

module.exports = onDetection;
