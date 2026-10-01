const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..", "..", "app", "assets");
exports.Engine = require(path.join(ROOT, "js/engine/engine.js"));
exports.X = require(path.join(ROOT, "js/engine/expr.js"));
exports.Inputs = require(path.join(ROOT, "js/engine/inputs.js"));
exports.load = (id) => JSON.parse(fs.readFileSync(path.join(ROOT, "content/scores", id + ".json")));
exports.demo = () => JSON.parse(fs.readFileSync(path.join(ROOT, "content/dev/demo-inputs.json")));
exports.scoreIds = () => fs.readdirSync(path.join(ROOT, "content/scores")).map((f) => f.replace(".json", ""));
exports.ROOT = ROOT;
