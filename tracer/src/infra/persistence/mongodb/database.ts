export class MongodbDatabase {
  connectionString = "";
  instance
  constructor(connectionString: string) {
    this.connectionString = connectionString
  }
  
  connect(): void
}