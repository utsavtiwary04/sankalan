import { io } from 'socket.io-client';

const URL = process.env.SOCKET_SERVER_URL || "http://localhost:8001"

export const socket = io(URL, {
	autoConnect: false
});