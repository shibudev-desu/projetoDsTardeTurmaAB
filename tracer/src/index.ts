import express from 'express'
import { ENVIRONMENT } from "./environment/env"
import { logger } from './infra/logger/pino'
import { MongodbDatabase } from './infra/persistence/mongodb/database'
import logsRouter from './routes/logs'

const app = express()

// Middleware
app.use(express.json())

// API Key authentication middleware
app.use((req, res, next) => {
  const apiKey = req.headers['x-api-key']
  if (!apiKey || apiKey !== ENVIRONMENT.API_KEY) {
    return res.status(401).json({ error: 'Unauthorized' })
  }
  next()
})

// Routes
app.use('/logs', logsRouter)

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok' })
})

// Connect to database and start server
const startServer = async () => {
  try {
    const db = new MongodbDatabase(ENVIRONMENT.DATABASE_URI!)
    await db.connect()
    logger.info('Connected to MongoDB')

    app.listen(ENVIRONMENT.PORT, () => {
      logger.info(`SERVER LISTENING ON PORT ${ENVIRONMENT.PORT}`)
    })
  } catch (error) {
    logger.error('Failed to start server', { error })
    process.exit(1)
  }
}

startServer()
