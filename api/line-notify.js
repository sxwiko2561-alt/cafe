// Vercel Serverless Function สำหรับส่ง LINE Notification
export default async function handler(req, res) {
  // เช็ค CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // เช็ค method
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // LINE Messaging API credentials
    const LINE_CHANNEL_ACCESS_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN;

    if (!LINE_CHANNEL_ACCESS_TOKEN) {
      return res.status(500).json({ error: 'LINE token not configured' });
    }

    // ส่งข้อความผ่าน LINE Broadcast API
    const response = await fetch('https://api.line.me/v2/bot/message/broadcast', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${LINE_CHANNEL_ACCESS_TOKEN}`
      },
      body: JSON.stringify({
        messages: [{
          type: 'text',
          text: message
        }]
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('LINE API Error:', response.status, errorText);
      return res.status(response.status).json({ 
        error: 'LINE API error', 
        details: errorText,
        status: response.status 
      });
    }

    return res.status(200).json({ 
      success: true, 
      message: 'LINE notification sent successfully' 
    });

  } catch (error) {
    console.error('Function error:', error);
    return res.status(500).json({ 
      error: 'Internal server error', 
      details: error.message 
    });
  }
}
