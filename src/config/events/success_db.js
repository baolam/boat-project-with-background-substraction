const events = require("events");

const EventEmitter = new events.EventEmitter();
EventEmitter.setMaxListeners(1);

module.exports = EventEmitter;