import { google } from 'googleapis';
import fs from 'fs';
import path from 'path';

const CLIENT_ID = process.env.GOOGLE_CLIENT_ID;
const CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET;
const REDIRECT_URI = process.env.GOOGLE_REDIRECT_URI || 'urn:ietf:wg:oauth:2.0:oob';
const SCOPES = ['https://www.googleapis.com/auth/tasks.readonly'];

const TOKEN_PATH = path.join(process.cwd(), 'refresh_token.json');

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  const oAuth2Client = new google.auth.OAuth2(
    CLIENT_ID, 
    CLIENT_SECRET, 
    REDIRECT_URI
  );

  // 1. Load existing token
  if (fs.existsSync(TOKEN_PATH)) {
    const tokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf-8'));
    oAuth2Client.setCredentials(tokenData);
  }

  // 2. Handle Auth Code exchange
  if (code) {
    try {
      const { tokens } = await oAuth2Client.getToken(code);
      oAuth2Client.setCredentials(tokens);
      fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens));
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Auth failed' }), { status: 500 });
    }
  }

  // 3. Auth Check
  if (!oAuth2Client.credentials || !oAuth2Client.credentials.access_token) {
    const authUrl = oAuth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: SCOPES,
      prompt: 'consent'
    });
    return new Response(JSON.stringify({ authUrl }), { status: 200 });
  }

  // 4. Fetch Tasks from ALL lists
  try {
    const service = google.tasks({ version: 'v1', auth: oAuth2Client });

    // Step A: Get all task lists (folders)
    const taskListsRes = await service.tasklists.list({ maxResults: 50 });
    const lists = taskListsRes.data.items || [];

    // Step B: Fetch tasks for every list in parallel
    const allTasksPromises = lists.map(async (list) => {
      try {
        const response = await service.tasks.list({
          tasklist: list.id,
          maxResults: 50,
          showCompleted: true,
          showHidden: true
        });
        
        // Tag each task with its list title so you know where it came from
        return (response.data.items || []).map(task => ({
          ...task,
          listTitle: list.title 
        }));
      } catch (err) {
        console.error(`Error fetching tasks for list ${list.title}:`, err.message);
        return [];
      }
    });

    // Step C: Wait for all lists to return and flatten the array
    const results = await Promise.all(allTasksPromises);
    const combinedTasks = results.flat(); // Merges [[list1], [list2]] into one [list1, list2]

    return new Response(JSON.stringify({ tasks: combinedTasks }), { 
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    console.error('API error:', error.message);
    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }
}