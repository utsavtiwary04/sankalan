import { io } from 'socket.io-client';

// "undefined" means the URL will be computed from the `window.location` object
const URL = process.env.SOCKET_SERVER_URL || "http://localhost:8001"

export const socket = io(URL, {
	autoConnect: false
});