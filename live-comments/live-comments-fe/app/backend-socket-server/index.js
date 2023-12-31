const http = require("http");
const { Server } = require("socket.io");
const cors = require("cors");

const httpServer = http.createServer();

// // --- SETUP SERVER --- //
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FE_WHITELIST || "http://localhost:3000",
    methods: ["GET", "POST"],
    allowedHeaders: ["my-custom-header"],
    credentials: true,
  },
});

io.on("connection", (socket) => {
  console.log("A user connected:", socket.id);

  socket.on("join_room", (roomId) => {
    socket.join(roomId);
    console.log(`user with id-${socket.id} joined room - ${roomId}. Total : ${io.engine.clientsCount}`);
  });

  socket.on("send_msg", (data) => {
    console.log(data, "DATA");
    socket.to(data.roomId).emit("receive_msg", data);
  });

  socket.on("disconnect", () => {
    console.log("A user disconnected:", socket.id);
  });

  socket.on("message", ({ messages, channel_id, channel_name }) => {
    console.log(`${messages.length} messages received on channel ${channel_name}(CHANNEL ID: ${channel_id})`)
    socket.broadcast.emit(`message`, { messages, channel_id, channel_name })
    console.log("message sent")
  })
});

io.engine.on("connection_error", (err) => {
  console.log(err.req); 
  console.log(err.code);
  console.log(err.message);
  console.log(err.context);
});

const PORT = process.env.PORT || 8001;
httpServer.listen(PORT, () => {
  console.log(`Socket.io server is running on port ${PORT}`);
});

