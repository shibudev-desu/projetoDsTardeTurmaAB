import mongoose from "mongoose";

const LogSchema = new mongoose.Schema({
  message: String,
  level: String,
  createdAt: {
    type: Date,
    default: Date.now
  }
});

export default mongoose.model("Log", LogSchema);
