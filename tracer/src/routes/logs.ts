import { Request, Response, Router } from 'express';
import { logger } from '../infra/logger/pino';
import { Log } from '../models/Log';

const router = Router();

// POST /logs - Save a new log
router.post('/', async (req: Request, res: Response) => {
  try {
    const { level, message, service, userId, metadata } = req.body;

    if (!level || !message || !service) {
      return res.status(400).json({ error: 'level, message, and service are required' });
    }

    const log = new Log({
      level,
      message,
      service,
      userId,
      metadata,
    });

    await log.save();

    logger.info('Log saved successfully', { logId: log._id });

    res.status(201).json({ message: 'Log saved', logId: log._id });
  } catch (error) {
    logger.error('Error saving log', { error });
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /logs - Retrieve logs with optional filters
router.get('/', async (req: Request, res: Response) => {
  try {
    const { level, service, userId, limit = 50, skip = 0 } = req.query;

    const filter: any = {};
    if (level) filter.level = level;
    if (service) filter.service = service;
    if (userId) filter.userId = userId;

    const logs = await Log.find(filter)
      .sort({ timestamp: -1 })
      .limit(parseInt(limit as string))
      .skip(parseInt(skip as string));

    res.json({ logs });
  } catch (error) {
    logger.error('Error retrieving logs', { error });
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;
