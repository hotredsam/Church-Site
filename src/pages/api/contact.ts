import fs from 'fs';
import path from 'path';

export async function POST({ request }) {
  try {
    const data = await request.json();
    // basic honeypot check
    if(data.hp) return new Response('Spam detected', { status: 400 });
    const name = (data.name || '').toString().trim();
    const email = (data.email || '').toString().trim();
    const message = (data.message || '').toString().trim();
    if(!name || !email || !message) return new Response('Missing required fields', { status: 400 });

    const record = {
      id: new Date().toISOString(),
      name, email, phone: (data.phone||'').toString().trim(), message,
      source: data.source || '/get-connected/contact-fallback',
      timestamp: new Date().toISOString()
    };

    // write to data/contacts.json
    const dataDir = path.resolve('./data');
    if(!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
    const file = path.join(dataDir, 'contacts.json');
    let arr = [];
    if(fs.existsSync(file)) {
      try { arr = JSON.parse(fs.readFileSync(file, 'utf-8') || '[]'); } catch(e) { arr = []; }
    }
    arr.push(record);
    fs.writeFileSync(file, JSON.stringify(arr, null, 2), 'utf-8');

    // forward to webhook if configured
    const webhook = process.env.EMAIL_WEBHOOK_URL;
    if(webhook) {
      try {
        await fetch(webhook, { method: 'POST', headers: { 'content-type':'application/json' }, body: JSON.stringify(record) });
      } catch(e) {
        // Non-fatal: log to console for server logs
        console.error('Webhook forwarding failed', e);
      }
    }

    return new Response(JSON.stringify({ ok: true }), { status: 200, headers: { 'content-type':'application/json' } });
  } catch(err) {
    console.error(err);
    return new Response('Server error', { status: 500 });
  }
}
