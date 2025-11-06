import { ENVIRONMENT } from "./environment/env"
import express from 'express'
const app = express()

app.listen(ENVIRONMENT.PORT, () => {
    console.log("SERVER LISTENING ON PORT " + ENVIRONMENT.PORT)
})
