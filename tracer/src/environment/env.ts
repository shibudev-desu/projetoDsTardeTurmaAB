import dotenv from 'dotenv'
dotenv.config()
const ENVIRONMENT = {
    PORT: process.env.PORT || 6964,
    API_KEY: process.env.API_KEY,
    DATABASE_URI: process.env.DATABASE_URI
}

export {ENVIRONMENT};
