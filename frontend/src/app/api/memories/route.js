import fs from 'fs';
import path from 'path';

const MEMORIES_DIR = path.join(process.cwd(), 'public', 'memories');
const IMAGE_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png', '.gif', '.webp']);

export async function GET() {
  try {
    const files = fs.readdirSync(MEMORIES_DIR);
    const images = files
      .filter((file) => IMAGE_EXTENSIONS.has(path.extname(file).toLowerCase()))
      .map((file) => `/memories/${file}`);

    return new Response(JSON.stringify({ images }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    console.error('Error in memories API:', err);
    return new Response(JSON.stringify({ error: 'Internal Server Error', details: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
}
