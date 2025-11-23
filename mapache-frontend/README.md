# Mapache Frontend

Modern Next.js frontend for the Mapache AI Agent Platform - providing a beautiful conversational UI and agent marketplace for interacting with 511 specialized AI agents.

## Features

### 🎯 Core Features
- **Conversational UI** - Modern chat interface with streaming responses
- **Agent Marketplace** - Discover and search 511 AI agents
- **Real-time Streaming** - See agent responses as they're generated
- **Tool Visualization** - Watch tools execute in real-time
- **Session Management** - Track conversations and costs
- **File Upload** - Share files with agents
- **Mobile Responsive** - Works seamlessly on all devices

### 🛠️ Technical Stack
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **State Management**: React Hooks
- **Testing**: Jest, React Testing Library, Playwright

## Quick Start

### Prerequisites
- Node.js 18+ (LTS recommended)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

## Project Structure

```
mapache-frontend/
├── src/
│   ├── app/                      # Next.js app router pages
│   │   ├── page.tsx              # Homepage
│   │   ├── marketplace/          # Agent marketplace
│   │   ├── chat/[agentId]/       # Chat interface
│   │   └── api/                  # API routes
│   ├── components/               # React components
│   │   ├── chat/                 # Chat UI components
│   │   ├── marketplace/          # Marketplace components
│   │   ├── session/              # Session management
│   │   ├── tools/                # Tool visualization
│   │   └── ui/                   # Base UI components
│   ├── hooks/                    # Custom React hooks
│   ├── lib/                      # Utilities and types
│   │   ├── api/                  # API clients
│   │   ├── types/                # TypeScript types
│   │   └── utils/                # Helper functions
│   └── config/                   # Configuration files
├── tests/                        # Test files
│   ├── integration/              # Integration tests
│   ├── e2e/                      # End-to-end tests
│   └── fixtures/                 # Test data
└── public/                       # Static assets
```

## Available Scripts

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Testing
```bash
npm test             # Run unit tests
npm run test:watch   # Run tests in watch mode
npm run test:e2e     # Run E2E tests with Playwright
```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_WS_URL=ws://localhost:8080/ws

# Optional: Authentication
NEXT_PUBLIC_AUTH_ENABLED=false

# Optional: Analytics
NEXT_PUBLIC_ANALYTICS_ENABLED=false
```

## Key Components

### Chat Components
- **ChatContainer** - Main chat interface wrapper
- **MessageList** - Scrollable message history
- **Message** - Individual message display with markdown support
- **StreamingMessage** - Real-time streaming response
- **MessageInput** - User input with file upload
- **ToolCallDisplay** - Visualize tool executions

### Marketplace Components
- **AgentCard** - Agent preview card with stats
- **AgentSearch** - Search and filter agents
- **CategoryFilter** - Filter by agent category

### Session Components
- **SessionHeader** - Display active session info
- **SessionControls** - Start/end session controls

## API Routes

### Agent APIs
- `GET /api/agents/list` - List all available agents
- `GET /api/agents/[agentId]` - Get specific agent details
- `POST /api/agents/[agentId]/chat` - Send message to agent (streaming)

### Session APIs
- `POST /api/sessions` - Create new session
- `DELETE /api/sessions/[sessionId]` - End session

## Custom Hooks

### useAgentChat
Manages chat communication with an agent:
```typescript
const { sendMessage, isStreaming, streamingContent } = useAgentChat(agentId);
```

### useSessionManager
Manages session lifecycle:
```typescript
const { session, startSession, endSession } = useSessionManager();
```

### useAgentList
Fetches and manages agent list:
```typescript
const { agents, isLoading, error } = useAgentList();
```

## Connecting to Backend

Currently, the frontend uses mock data for demonstration. To connect to the real Mapache backend:

1. **Update API Routes** (`src/app/api/`)
   - Replace mock responses with actual backend calls
   - Point to your agent backend URL

2. **Update Environment Variables**
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

3. **Implement Authentication** (if required)
   - Add auth provider
   - Update API clients to include auth tokens

4. **WebSocket Support** (for real-time features)
   - Implement WebSocket connection for streaming
   - Update `useAgentChat` hook

## Deployment

### Google Cloud Platform (Recommended)

Deploy the Mapache frontend to Google Cloud Run for seamless integration with your existing backend infrastructure.

#### Prerequisites

```bash
# Install Google Cloud SDK (if not already installed)
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

#### Option 1: Cloud Run (Recommended)

**Step 1: Build and deploy using Cloud Build**

```bash
# From the mapache-frontend directory
cd mapache-frontend

# Build and deploy in one command
gcloud run deploy mapache-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="NEXT_PUBLIC_API_URL=https://your-backend-url.run.app" \
  --set-env-vars="NEXT_PUBLIC_WS_URL=wss://your-backend-url.run.app/ws"
```

**Step 2: Configure additional environment variables (optional)**

```bash
gcloud run services update mapache-frontend \
  --region us-central1 \
  --set-env-vars="NEXT_PUBLIC_AUTH_ENABLED=true" \
  --set-env-vars="NEXT_PUBLIC_ANALYTICS_ENABLED=true"
```

**Step 3: Get your deployed URL**

```bash
gcloud run services describe mapache-frontend \
  --region us-central1 \
  --format="value(status.url)"
```

#### Option 2: Manual Docker Deployment

**Step 1: Build Docker image**

```bash
# Build the image
docker build -t gcr.io/YOUR_PROJECT_ID/mapache-frontend:latest .

# Test locally
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8080 \
  gcr.io/YOUR_PROJECT_ID/mapache-frontend:latest
```

**Step 2: Push to Google Container Registry**

```bash
# Configure Docker for GCR
gcloud auth configure-docker

# Push image
docker push gcr.io/YOUR_PROJECT_ID/mapache-frontend:latest
```

**Step 3: Deploy to Cloud Run**

```bash
gcloud run deploy mapache-frontend \
  --image gcr.io/YOUR_PROJECT_ID/mapache-frontend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 3000 \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

#### Option 3: CI/CD with Cloud Build

**Step 1: Create `cloudbuild.yaml`** (already included in the project)

**Step 2: Set up Cloud Build trigger**

```bash
# Create trigger from GitHub repository
gcloud builds triggers create github \
  --repo-name=mapachev1 \
  --repo-owner=mapachekurt \
  --branch-pattern="^main$" \
  --build-config=mapache-frontend/cloudbuild.yaml \
  --included-files="mapache-frontend/**"
```

**Step 3: Push to trigger deployment**

```bash
git push origin main
# Cloud Build will automatically build and deploy
```

#### Environment Variables Configuration

Set environment variables using Secret Manager for sensitive data:

```bash
# Create secrets
echo -n "https://your-backend-url.run.app" | \
  gcloud secrets create api-url --data-file=-

echo -n "wss://your-backend-url.run.app/ws" | \
  gcloud secrets create ws-url --data-file=-

# Update Cloud Run service to use secrets
gcloud run services update mapache-frontend \
  --region us-central1 \
  --update-secrets=NEXT_PUBLIC_API_URL=api-url:latest \
  --update-secrets=NEXT_PUBLIC_WS_URL=ws-url:latest
```

#### Custom Domain Setup

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service mapache-frontend \
  --domain mapache.app \
  --region us-central1

# Add DNS records (follow the instructions provided)
```

#### Monitoring and Logging

```bash
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mapache-frontend" \
  --limit 50 \
  --format json

# Monitor metrics in Cloud Console
# https://console.cloud.google.com/run/detail/REGION/mapache-frontend/metrics
```

### Local Production Build

```bash
# Build the application
npm run build

# Start production server
npm start

# Or test with Docker locally
docker build -t mapache-frontend .
docker run -p 3000:3000 mapache-frontend
```

## Testing

### Unit Tests
```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm run test:watch
```

### E2E Tests
```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run with UI
npx playwright test --ui
```

## Performance Optimization

### Current Optimizations
- ✅ React Server Components for static content
- ✅ Dynamic imports for heavy components
- ✅ Image optimization with Next.js Image
- ✅ Tailwind CSS purging for minimal bundle size
- ✅ Streaming responses for better perceived performance

### Future Optimizations
- [ ] Implement Redis caching for agent list
- [ ] Add service worker for offline support
- [ ] Implement virtual scrolling for large message lists
- [ ] Add WebSocket for real-time updates
- [ ] Optimize bundle with code splitting

## Accessibility

This application follows WCAG 2.1 AA standards:
- ✅ Keyboard navigation support
- ✅ Screen reader friendly
- ✅ ARIA labels on interactive elements
- ✅ High contrast mode support
- ✅ Focus indicators

## Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

When contributing to the frontend:

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Ensure all tests pass
5. Submit PR with clear description

### Code Style
- Use TypeScript for all new files
- Follow existing naming conventions
- Add JSDoc comments for complex functions
- Use functional components with hooks

## Troubleshooting

### Common Issues

**Build fails with TypeScript errors**
```bash
# Clean and rebuild
rm -rf .next
npm run build
```

**Tests failing**
```bash
# Clear Jest cache
npx jest --clearCache
npm test
```

**Streaming not working**
- Check CORS settings on backend
- Verify API URL in .env
- Check browser console for errors

## Roadmap

### Phase 1: Current (Complete)
- ✅ Basic chat interface
- ✅ Agent marketplace
- ✅ Mock data integration
- ✅ Core UI components

### Phase 2: Backend Integration (Next)
- [ ] Connect to real agent backend
- [ ] Implement authentication
- [ ] WebSocket streaming
- [ ] Session persistence

### Phase 3: Enhanced Features
- [ ] Voice input/output
- [ ] Multi-agent workflows
- [ ] Agent comparison tool
- [ ] Usage analytics dashboard
- [ ] Advanced search with filters

### Phase 4: Production Hardening
- [ ] Rate limiting
- [ ] CDN integration
- [ ] Database for sessions
- [ ] Redis caching
- [ ] Monitoring and alerts

## Support

For issues or questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

## License

[Add your license here]

---

Built with ❤️ for the Mapache Agent Platform
