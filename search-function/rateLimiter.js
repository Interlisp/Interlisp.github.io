'use strict';

const { Firestore } = require('@google-cloud/firestore');

const db = new Firestore({ projectId: process.env.PROJECT_ID });

// Rate limit configuration
// Adjust these values based on your traffic patterns
const LIMITS = {
  perIp: {
    requests: 20,    // max 20 requests per IP
    windowSec: 60,   // per 60 second window
  },
  global: {
    requests: 500,   // max 500 total requests
    windowSec: 60,   // per 60 second window
  }
};

/**
 * Atomically check and increment a rate limit counter in Firestore.
 * Returns { allowed: true/false, count: current count }
 */
async function checkLimit(key, limit) {
  const ref      = db.collection('rate_limits').doc(key);
  const now      = Date.now();
  const windowMs = limit.windowSec * 1000;

  try {
    const result = await db.runTransaction(async t => {
      const doc  = await t.get(ref);
      const data = doc.exists ? doc.data() : null;

      // Start a new window if first request or window has expired
      if (!data || (now - data.windowStart) > windowMs) {
        t.set(ref, {
          count:       1,
          windowStart: now,
          updatedAt:   now
        });
        return { allowed: true, count: 1 };
      }

      // Window is active — check if over limit
      if (data.count >= limit.requests) {
        return { allowed: false, count: data.count };
      }

      // Increment counter
      t.update(ref, {
        count:     Firestore.FieldValue.increment(1),
        updatedAt: now
      });
      return { allowed: true, count: data.count + 1 };
    });

    return result;

  } catch (err) {
    // Fail open — if Firestore is unavailable don't block searches
    console.error('Rate limiter error:', err.message);
    return { allowed: true, count: 0 };
  }
}

/**
 * Main rate limit check — runs IP and global checks in parallel.
 * Returns { limited: false } or { limited: true, reason, retryAfter }
 */
async function isRateLimited(req) {
  // Get client IP — Cloud Functions passes real IP in x-forwarded-for
  const ip = req.headers['x-forwarded-for']
    ?.split(',')[0]
    ?.trim() || 'unknown';

  // Run both checks in parallel
  const [ipCheck, globalCheck] = await Promise.all([
    checkLimit(`ip:${ip}`, LIMITS.perIp),
    checkLimit('global',   LIMITS.global),
  ]);

  if (!ipCheck.allowed) {
    return {
      limited:    true,
      reason:     'Too many requests. Please wait a moment before searching again.',
      retryAfter: LIMITS.perIp.windowSec
    };
  }

  if (!globalCheck.allowed) {
    return {
      limited:    true,
      reason:     'Search service is temporarily busy. Please try again shortly.',
      retryAfter: LIMITS.global.windowSec
    };
  }

  return { limited: false };
}

module.exports = { isRateLimited };
