import express from 'express'
import mongoose from 'mongoose'
import { ENVIRONMENT } from "./environment/env.js"
import logsRouter from './routes/logs.js'

const app = express()

// Middleware to parse JSON
app.use(express.json())

// Connect to MongoDB
mongoose.connect(ENVIRONMENT.DATABASE_URI as string)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err))

// Use routes
app.use('/logs', logsRouter)

app.listen(ENVIRONMENT.PORT, () => {
    console.log("SERVER LISTENING ON PORT " + ENVIRONMENT.PORT)
})
