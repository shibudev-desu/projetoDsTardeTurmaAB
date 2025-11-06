import mongoose from 'mongoose';

export class MongodbDatabase {
  connectionString: string;
  instance: typeof mongoose | null = null;

  constructor(connectionString: string) {
    this.connectionString = connectionString;
  }

  async connect(): Promise<void> {
    try {
      this.instance = await mongoose.connect(this.connectionString);
      console.log('Connected to MongoDB');
    } catch (error) {
      console.error('Error connecting to MongoDB:', error);
      throw error;
    }
  }

  async disconnect(): Promise<void> {
    if (this.instance) {
      await mongoose.disconnect();
      console.log('Disconnected from MongoDB');
    }
  }
}
