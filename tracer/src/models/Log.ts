import mongoose, { Document, Schema } from 'mongoose';

export interface ILog extends Document {
  level: string;
  message: string;
  timestamp: Date;
  service: string;
  userId?: string;
  metadata?: Record<string, any>;
}

const LogSchema: Schema = new Schema({
  level: { type: String, required: true },
  message: { type: String, required: true },
  timestamp: { type: Date, default: Date.now },
  service: { type: String, required: true },
  userId: { type: String },
  metadata: { type: Schema.Types.Mixed },
});

export const Log = mongoose.model<ILog>('Log', LogSchema);
