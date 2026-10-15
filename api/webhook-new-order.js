// Vercel Function: Supabase Webhook สำหรับออเดอร์ใหม่
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
    // Supabase webhook payload
    const { type, table, record, old_record } = req.body;

    // เช็คว่าเป็นออเดอร์ใหม่ (INSERT) และสถานะ pending
    if (type !== 'INSERT' || table !== 'orders' || record.status !== 'pending') {
      return res.status(200).json({ message: 'Not a new pending order, skipped' });
    }

    const order = record;

    // สร้างข้อความแจ้งเตือน
    const items = (typeof order.items === 'string' ? JSON.parse(order.items) : order.items)
      .map(i => `${i.name}×${i.qty}`)
      .join(", ");

    const pickupKeywords = [
      'มารับเอง', 'มารับ', 'ไปรับเอง', 'ไปรับ', 'รับเอง', 'เอาเอง',
      'ไปเอา', 'ไปเอาเอง', 'จะไปเอา', 'เดี๋ยวไปเอา', 'มาเอา', 'มาเอาเอง',
      'เคาน์เตอร์', 'counter', 'pickup', 'ที่ร้าน', 'หน้าร้าน', 'ถึงร้าน',
      'ไปถึง', 'ขับไป', 'แวะรับ', 'แวะเอา'
    ];
    
    const isPickup = order.location && pickupKeywords.some(k => 
      order.location.toLowerCase().includes(k.toLowerCase())
    );

    const lineMsg = `🛎️ ออเดอร์ใหม่! #${String(order.order_seq || '').padStart(4, '0')}

👤 ${order.name}
📞 ${order.phone || '-'}
📍 ${isPickup ? '🏃 รับที่ร้าน' : '🛵 ส่ง'} · ${order.location || '-'}
🛒 ${items}
💰 ${order.total}฿${order.note ? '\n📌 ' + order.note : ''}`;

    // ส่ง LINE Notification
    const LINE_TOKEN = process.env.LINE_CHANNEL_ACCESS_TOKEN;

    if (!LINE_TOKEN) {
      return res.status(500).json({ error: 'LINE token not configured' });
    }

    const lineResponse = await fetch('https://api.line.me/v2/bot/message/broadcast', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${LINE_TOKEN}`
      },
      body: JSON.stringify({
        messages: [{
          type: 'text',
          text: lineMsg
        }]
      })
    });

    if (!lineResponse.ok) {
      const errorText = await lineResponse.text();
      console.error('LINE API Error:', lineResponse.status, errorText);
      return res.status(500).json({ 
        error: 'LINE API error', 
        details: errorText 
      });
    }

    return res.status(200).json({ 
      success: true, 
      message: 'LINE notification sent successfully',
      order_id: order.id
    });

  } catch (error) {
    console.error('Webhook error:', error);
    return res.status(500).json({ 
      error: 'Internal server error', 
      details: error.message 
    });
  }
}
