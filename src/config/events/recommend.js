const events = require("events");
const EventEmitter = new events.EventEmitter();

EventEmitter.setMaxListeners(parseInt(process.env.RECOMMEND_MAX_LISTENER));
// EventEmitter.setMaxListeners(10);

module.exports = {
  recommend_events : EventEmitter,
  EVENTS : {
    UPDATE_THETA : "UPDATE_THETA"
  }
};