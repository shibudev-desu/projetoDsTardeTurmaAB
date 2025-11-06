import express from 'express';
import Log from '../models/Log';

const router = express.Router();

// Example route to get all logs
router.get('/', async (req, res) => {
  try {
    const logs = await Log.find();
    res.json(logs);
  } catch (error) {
    res.status(500).json({ message: error instanceof Error ? error.message : 'An unknown error occurred' });
  }
});

// Example route to create a log
router.post('/', async (req, res) => {
  const log = new Log({
    message: req.body.message,
    level: req.body.level
  });

  try {
    const newLog = await log.save();
    res.status(201).json(newLog);
  } catch (error) {
    res.status(400).json({ message: error instanceof Error ? error.message : 'An unknown error occurred' });
  }
});

export default router;
