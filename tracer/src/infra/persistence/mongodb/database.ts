export class MongodbDatabase {
  connectionString = "";
  instance: any;
  constructor(connectionString: string) {
    this.connectionString = connectionString
  }

  connect(): void {
    // Implementation for connecting to MongoDB
  }
}
