import socketIOClient from 'socket.io-client';

const client = socketIOClient("/user");

export default client;