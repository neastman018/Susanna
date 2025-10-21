import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const REDIRECT_URI = process.env.GOOGLE_REDIRECT_URI || 'urn:ietf:wg:oauth:2.0:oob';
const SCOPES = ['https://www.googleapis.com/auth/tasks.readonly'];

// File to store the refresh token
const TOKEN_PATH = path.join(process.cwd(), 'refresh_token.json');

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  const oAuth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI);

  // Step 1: If a refresh token is saved, use it
  if (fs.existsSync(TOKEN_PATH)) {
    const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf-8'));
    oAuth2Client.setCredentials({ refresh_token: tokenData.refresh_token });
  }

  // Step 2: If no refresh token or user submitted a new code
  if (!oAuth2Client.credentials.refresh_token && code) {
    try {
      const { tokens } = await oAuth2Client.getToken(code);
      oAuth2Client.setCredentials(tokens);

      // Save refresh token
      if (tokens.refresh_token) {
        fs.writeFileSync(TOKEN_PATH, JSON.stringify({ refresh_token: tokens.refresh_token }));
      }
    } catch (err) {
      console.error(err);
      return new Response(JSON.stringify({ error: 'Failed to get tokens.' }), { status: 500 });
    }
  }

  // Step 3: If still no refresh token, return auth URL
  if (!oAuth2Client.credentials.refresh_token) {
    const authUrl = oAuth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: SCOPES,
    });
    return new Response(JSON.stringify({ authUrl }), { status: 200 });
  }

  // Step 4: Fetch tasks
  try {
    const service = google.tasks({ version: 'v1', auth: oAuth2Client });
    const res = await service.tasks.list({ tasklist: '@default', maxResults: 50 });
    return new Response(JSON.stringify({ tasks: res.data.items || [] }), { status: 200 });
  } catch (err) {
    console.error(err);
    return new Response(JSON.stringify({ error: 'Failed to fetch tasks.' }), { status: 500 });
  }
}
