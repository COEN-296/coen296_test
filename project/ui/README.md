# UI Source Files

This directory contains the source files for the web UI.

## Files

- **index.html** - Main application interface
- **login.html** - Login page
- **USER_GUIDE.md** - User guide for the application
- **api-client.js** - API client (if applicable)

## Development Workflow

1. **Edit UI files here** in `/project/ui/`
2. **Sync to static** directory:
   ```bash
   cd /Users/suraj/Desktop/ai_goverance/coen296-main/project
   scripts/sync_ui.sh
   ```
   Or use the symlink:
   ```bash
   ./scripts/sync_ui.sh
   ```

3. **View changes**:
   - Server automatically serves from `/project/static/`
   - Refresh browser to see changes
   - Hard refresh: `Cmd + Shift + R`

## File Sync

The `sync_ui.sh` script copies files from here to `/project/static/` where they are served by the FastAPI application.

**Files synced**:
- `index.html` → `/project/static/index.html`
- `login.html` → `/project/static/login.html`
- `USER_GUIDE.md` → `/project/static/USER_GUIDE.md`

## Testing UI Changes

1. **Start server**: `./start_server.sh` (from project root)
2. **Edit UI files**: Make changes in this directory
3. **Sync files**: Run `scripts/sync_ui.sh`
4. **Refresh browser**: Hard refresh to see changes

## Related Documentation

- [UI Server Setup Guide](../../docs/UI_SERVER_SETUP.md)
- [Deployment Guide](../../docs/DEPLOYMENT.md)
