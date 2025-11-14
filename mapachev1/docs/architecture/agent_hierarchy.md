# Multi-Agent System Hierarchy

## Overview

This document describes the comprehensive 4-level hierarchy for orchestrating 511 specialized AI agents across the organization. The hierarchy enables efficient routing, coordination, and execution of complex tasks through a structured delegation model.

### Hierarchy Levels

```
Level 0: Root Orchestrator (1 agent)
    └── Level 1: Division Coordinators (11 divisions)
        └── Level 2: Team Agents (56 teams)
            └── Level 3: Specialist Agents (511 specialists)
```

### Design Principles

1. **Single Responsibility**: Each coordinator/team has one clear, well-defined purpose
2. **Clear Boundaries**: No overlap between divisions or teams
3. **Balanced Distribution**: Agents distributed proportionally across divisions
4. **Logical Grouping**: Related agents grouped together for efficient routing
5. **Practical Routing**: LLM can easily determine correct division/team from natural language descriptions
6. **Scalability**: Structure supports adding new agents or reorganization

## Level 0: Root Orchestrator

**Agent**: RootOrchestrator
**Model**: gemini-2.0-flash-exp
**Purpose**: Master orchestrator that analyzes incoming requests and routes them to the appropriate division

### Capabilities
- Request classification and intent analysis
- Multi-division coordination for complex requests
- Load balancing across divisions
- High-level workflow orchestration

### Routing Logic
The Root Orchestrator analyzes request characteristics and delegates to divisions based on:
- **Functional domain** (finance, engineering, sales, etc.)
- **Request type** (operational, strategic, technical, etc.)
- **Required expertise** (data analysis, security, integration, etc.)
- **Urgency and priority**

## Level 1: Division Coordinators (11 Divisions)

Division coordinators manage major functional areas and route requests to appropriate specialized teams.

### Division Overview

| Division | Teams | Specialists | Primary Focus |
|----------|-------|-------------|---------------|
| Executive & Strategy | 3 | 76 | Leadership, strategy, communications |
| Security, Legal & Compliance | 5 | 71 | Security, legal, compliance, risk |
| Technology Infrastructure | 4 | 48 | IT infrastructure, cloud, DevOps |
| Finance & Accounting | 4 | 14 | Financial operations, accounting |
| People & Culture | 4 | 18 | HR, talent, learning, culture |
| Revenue Operations | 5 | 31 | Sales and marketing operations |
| Engineering & Product | 6 | 59 | Software development, product |
| Customer Success | 4 | 35 | Customer support and success |
| Operations & Supply Chain | 4 | 32 | Operations, logistics, manufacturing |
| Data & Analytics | 6 | 40 | Data science, BI, analytics |
| Integration & Innovation | 11 | 87 | SaaS integrations, innovation |

**Total**: 56 teams managing 511 specialists

---

## Division Details

### 1. Executive & Strategy Division
**Coordinator**: ExecutiveStrategyDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 76 agents

#### Purpose
Oversees executive leadership, corporate strategy, and communications

#### Teams (3)

##### 1.1 Executive Leadership Team
- **Specialists**: 71 agents
- **Focus**: C-suite executives and top leadership
- **Key Roles**: CEO, COO, CFO, CTO, CMO, CHRO, and other executive roles

##### 1.2 Corporate Strategy Team
- **Specialists**: 2 agents
- **Focus**: Strategic planning, business development, and corporate initiatives
- **Key Roles**: VP Corporate Strategy, VP Business Development

##### 1.3 Communications & PR Team
- **Specialists**: 3 agents
- **Focus**: Corporate communications, PR, and investor relations
- **Key Roles**: VP Corporate Communications, VP Investor Relations

---

### 2. Security, Legal & Compliance Division
**Coordinator**: SecurityLegalDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 71 agents

#### Purpose
Ensures security, legal compliance, and risk management across the organization

#### Teams (5)

##### 2.1 Legal Team
- **Specialists**: 20 agents
- **Focus**: Corporate legal, contracts, litigation, IP, and legal counsel
- **Key Roles**: General Counsel, Corporate Counsel, IP Counsel, Paralegals

##### 2.2 Cybersecurity Operations Team
- **Specialists**: 13 agents
- **Focus**: Security operations, incident response, threat intelligence, and SOC
- **Key Roles**: SOC Analysts, Incident Responders, Threat Hunters, Penetration Testers

##### 2.3 Security Engineering Team
- **Specialists**: 12 agents
- **Focus**: Application security, cloud security, network security, and DevSecOps
- **Key Roles**: Security Engineers, Security Architects, Cloud Security Engineers

##### 2.4 Regulatory Compliance Team
- **Specialists**: 13 agents
- **Focus**: Regulatory compliance, privacy, GDPR, export compliance, and ethics
- **Key Roles**: Compliance Managers, Privacy Specialists, Regulatory Analysts

##### 2.5 Security & Risk Compliance Team
- **Specialists**: 13 agents
- **Focus**: Vulnerability management, compliance, GRC, and risk analysis
- **Key Roles**: Vulnerability Analysts, GRC Analysts, Risk Analysts

---

### 3. Technology Infrastructure Division
**Coordinator**: TechnologyInfrastructureDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 48 agents

#### Purpose
Manages IT infrastructure, cloud services, networks, and IT operations

#### Teams (4)

##### 3.1 IT Service Management Team
- **Specialists**: 18 agents
- **Focus**: IT service desk, support, asset management, and project management
- **Key Roles**: IT Support, Help Desk, Asset Managers, Scrum Masters, Agile Coaches

##### 3.2 Cloud & Infrastructure Team
- **Specialists**: 8 agents
- **Focus**: Cloud architecture, infrastructure engineering, and virtualization
- **Key Roles**: Cloud Architects, Infrastructure Engineers, Kubernetes Administrators

##### 3.3 Network & Systems Team
- **Specialists**: 13 agents
- **Focus**: Network engineering, systems administration, and database management
- **Key Roles**: Network Engineers, Systems Administrators, Database Administrators

##### 3.4 DevOps & SRE Team
- **Specialists**: 9 agents
- **Focus**: DevOps, site reliability, CI/CD, and automation
- **Key Roles**: DevOps Engineers, SRE Engineers, Release Managers

---

### 4. Finance & Accounting Division
**Coordinator**: FinanceAccountingDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 14 agents

#### Purpose
Manages all financial operations, accounting, and financial planning

#### Teams (4)

##### 4.1 Financial Planning & Analysis Team
- **Specialists**: 3 agents
- **Focus**: FP&A, budgeting, forecasting, and financial analysis
- **Key Roles**: Financial Analysts, Budget Managers

##### 4.2 Tax & Treasury Team
- **Specialists**: 4 agents
- **Focus**: Tax planning, compliance, treasury management, and cash operations
- **Key Roles**: Tax Analysts, Treasury Analysts, Treasurer

##### 4.3 Internal Audit Team
- **Specialists**: 2 agents
- **Focus**: Internal audit and financial controls
- **Key Roles**: Internal Auditors

##### 4.4 Accounting Operations Team
- **Specialists**: 5 agents
- **Focus**: Accounts payable, receivable, general ledger, and financial reporting
- **Key Roles**: AP/AR Specialists, Controllers, Financial Reporting

---

### 5. People & Culture Division
**Coordinator**: PeopleCultureDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 18 agents

#### Purpose
Manages talent acquisition, development, compensation, and employee relations

#### Teams (4)

##### 5.1 Talent Acquisition Team
- **Specialists**: 2 agents
- **Focus**: Recruitment, talent sourcing, and hiring operations
- **Key Roles**: Recruiters, Talent Acquisition Specialists

##### 5.2 Compensation & Benefits Team
- **Specialists**: 3 agents
- **Focus**: Compensation planning, benefits administration
- **Key Roles**: Compensation Analysts, Benefits Administrators

##### 5.3 Learning & Development Team
- **Specialists**: 3 agents
- **Focus**: Training, development, performance management, and career growth
- **Key Roles**: Training Specialists, Performance Management Specialists

##### 5.4 HR Operations Team
- **Specialists**: 10 agents
- **Focus**: HR operations, HRIS, employee relations, and compliance
- **Key Roles**: HR Generalists, HRIS Analysts, Employee Relations Specialists

---

### 6. Revenue Operations Division
**Coordinator**: RevenueOperationsDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 31 agents

#### Purpose
Drives revenue through sales and marketing operations

#### Teams (5)

##### 6.1 Enterprise Sales Team
- **Specialists**: 3 agents
- **Focus**: Enterprise sales, account management, and revenue generation
- **Key Roles**: Account Executives, Account Managers

##### 6.2 Growth Marketing Team
- **Specialists**: 12 agents
- **Focus**: SEO/SEM, social media, email marketing, and conversion optimization
- **Key Roles**: SEO Specialists, Social Media Managers, Email Marketing Specialists

##### 6.3 Brand & Product Marketing Team
- **Specialists**: 6 agents
- **Focus**: Brand marketing, product marketing, and content creation
- **Key Roles**: Brand Designers, Product Marketing Managers, Copywriters

##### 6.4 Marketing Operations Team
- **Specialists**: 1 agents
- **Focus**: Digital marketing, demand generation, and marketing automation
- **Key Roles**: Marketing Operations Specialists

##### 6.5 Sales Operations Team
- **Specialists**: 9 agents
- **Focus**: Sales operations, enablement, CRM, and sales analytics
- **Key Roles**: Sales Operations Analysts, CRM Administrators, Sales Enablement

---

### 7. Engineering & Product Division
**Coordinator**: EngineeringProductDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 59 agents

#### Purpose
Builds and maintains software products and engineering systems

#### Teams (6)

##### 7.1 Engineering Architecture Team
- **Specialists**: 4 agents
- **Focus**: Software architects and technical architecture
- **Key Roles**: Backend Architects, Frontend Architects, Solutions Architects

##### 7.2 Product Management Team
- **Specialists**: 7 agents
- **Focus**: Product managers, product owners, and product strategy
- **Key Roles**: Product Managers, Product Owners

##### 7.3 Software Engineering Team
- **Specialists**: 13 agents
- **Focus**: Software engineers, backend, frontend, and full-stack development
- **Key Roles**: Software Engineers, Backend Engineers, Frontend Engineers, Mobile Engineers

##### 7.4 Product Design Team
- **Specialists**: 9 agents
- **Focus**: UX/UI design, product design, and design systems
- **Key Roles**: UX Designers, UI Designers, Product Designers

##### 7.5 Specialized Engineering Team
- **Specialists**: 23 agents
- **Focus**: ML/AI engineers, data engineers, security engineers, and specialized roles
- **Key Roles**: ML Engineers, AI Engineers, Technical Writers, Developer Advocates

##### 7.6 Quality Engineering Team
- **Specialists**: 3 agents
- **Focus**: QA engineers, test automation, and quality assurance
- **Key Roles**: QA Engineers, Test Automation Engineers, SDETs

---

### 8. Customer Success Division
**Coordinator**: CustomerSuccessDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 35 agents

#### Purpose
Ensures customer satisfaction, support, and success

#### Teams (4)

##### 8.1 Customer Success Team
- **Specialists**: 8 agents
- **Focus**: Customer success managers, onboarding, and training
- **Key Roles**: Customer Success Managers, Onboarding Specialists, Training Specialists

##### 8.2 Customer Support Team
- **Specialists**: 11 agents
- **Focus**: Technical support, customer support, and helpdesk operations
- **Key Roles**: Support Engineers, Support Specialists, Tier 1/2/3 Agents

##### 8.3 Customer Operations Team
- **Specialists**: 10 agents
- **Focus**: Support operations, quality, analytics, and tools
- **Key Roles**: Support Operations Managers, Quality Analysts, SLA Managers

##### 8.4 Customer Engagement Team
- **Specialists**: 6 agents
- **Focus**: Customer advocacy, community, insights, and retention
- **Key Roles**: Customer Advocates, Community Managers, Renewal Specialists

---

### 9. Operations & Supply Chain Division
**Coordinator**: OperationsSupplyChainDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 32 agents

#### Purpose
Manages operations, supply chain, logistics, and manufacturing

#### Teams (4)

##### 9.1 Supply Chain Management Team
- **Specialists**: 5 agents
- **Focus**: Supply chain planning, procurement, and vendor management
- **Key Roles**: Supply Chain Managers, Procurement Specialists, Materials Planners

##### 9.2 Logistics & Warehouse Team
- **Specialists**: 11 agents
- **Focus**: Logistics, warehouse operations, inventory, and shipping
- **Key Roles**: Warehouse Managers, Logistics Managers, Transportation Managers

##### 9.3 Process Improvement Team
- **Specialists**: 7 agents
- **Focus**: Continuous improvement, lean manufacturing, and process engineering
- **Key Roles**: Process Engineers, Industrial Engineers, Continuous Improvement Managers

##### 9.4 Manufacturing & Quality Team
- **Specialists**: 9 agents
- **Focus**: Manufacturing operations, production management, quality control, and maintenance
- **Key Roles**: Production Managers, Quality Control Managers, Maintenance Managers

---

### 10. Data & Analytics Division
**Coordinator**: DataAnalyticsDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 40 agents

#### Purpose
Manages data infrastructure, analytics, and business intelligence

#### Teams (6)

##### 10.1 Data Architecture Team
- **Specialists**: 4 agents
- **Focus**: Data architects, analytics architects, and data warehouse specialists
- **Key Roles**: Data Architects, Analytics Architects, Data Warehouse Architects

##### 10.2 Data Engineering Team
- **Specialists**: 8 agents
- **Focus**: Data engineers, analytics engineers, and ETL developers
- **Key Roles**: Data Engineers, Analytics Engineers, DataOps Engineers, MLOps Engineers

##### 10.3 Data Science Team
- **Specialists**: 6 agents
- **Focus**: Data scientists, ML scientists, and research scientists
- **Key Roles**: Data Scientists, ML Scientists, Research Scientists

##### 10.4 Business Intelligence Team
- **Specialists**: 8 agents
- **Focus**: BI developers, analysts, and reporting specialists
- **Key Roles**: BI Developers, BI Analysts, Business Analysts, Data Analysts

##### 10.5 Data Governance Team
- **Specialists**: 7 agents
- **Focus**: Data governance, quality, privacy, and stewardship
- **Key Roles**: Data Governance Managers, Data Quality Managers, Data Stewards

##### 10.6 Analytics Specialist Team
- **Specialists**: 7 agents
- **Focus**: Specialized analytics including predictive, experimentation, and forecasting
- **Key Roles**: A/B Testing Analysts, Predictive Analytics Specialists, Forecasting Analysts

---

### 11. Integration & Innovation Division
**Coordinator**: IntegrationInnovationDivision
**Model**: gemini-2.0-flash-exp
**Specialists**: 87 agents

#### Purpose
Manages SaaS integrations and drives innovation initiatives

#### Teams (11)

##### 11.1 API & Integration Engineering Team
- **Specialists**: 4 agents
- **Focus**: API development, integration architecture, and platform engineering
- **Key Roles**: Integration Engineers, API Gateway Specialists, Platform Engineers

##### 11.2 CRM & Sales Integration Team
- **Specialists**: 3 agents
- **Focus**: Salesforce, HubSpot, Marketo, and sales platform integrations
- **Key Roles**: Salesforce Specialists, HubSpot Specialists, Marketo Specialists

##### 11.3 Enterprise Integration Team
- **Specialists**: 4 agents
- **Focus**: Workday, ServiceNow, Oracle, SAP, and ERP integrations
- **Key Roles**: Workday Specialists, ServiceNow Specialists, SAP Specialists

##### 11.4 Collaboration Integration Team
- **Specialists**: 4 agents
- **Focus**: Microsoft 365, Google Workspace, Slack, Zoom, and collaboration tools
- **Key Roles**: Microsoft 365 Specialists, Slack Specialists, Zoom Specialists

##### 11.5 Support & Productivity Integration Team
- **Specialists**: 9 agents
- **Focus**: Zendesk, Jira, Confluence, Asana, and productivity tools
- **Key Roles**: Zendesk Specialists, Jira Specialists, Asana Specialists

##### 11.6 Cloud & Data Integration Team
- **Specialists**: 10 agents
- **Focus**: AWS, Azure, GCP, Snowflake, Tableau, and data platform integrations
- **Key Roles**: AWS Specialists, Azure Specialists, Tableau Specialists

##### 11.7 Commerce & Marketing Integration Team
- **Specialists**: 5 agents
- **Focus**: Stripe, PayPal, Shopify, and e-commerce integrations
- **Key Roles**: Stripe Specialists, Shopify Specialists, PayPal Specialists

##### 11.8 HR & Document Integration Team
- **Specialists**: 6 agents
- **Focus**: BambooHR, Greenhouse, DocuSign, and document management
- **Key Roles**: BambooHR Specialists, DocuSign Specialists, Greenhouse Specialists

##### 11.9 Communication & Analytics Integration Team
- **Specialists**: 10 agents
- **Focus**: Twilio, SendGrid, Intercom, Segment, and analytics platforms
- **Key Roles**: Twilio Specialists, Segment Specialists, Amplitude Specialists

##### 11.10 Monitoring & Ops Integration Team
- **Specialists**: 5 agents
- **Focus**: Datadog, New Relic, PagerDuty, and monitoring platform integrations
- **Key Roles**: Datadog Specialists, PagerDuty Specialists, Splunk Specialists

##### 11.11 Innovation & Research Team
- **Specialists**: 27 agents
- **Focus**: Innovation management, digital transformation, and emerging technology research
- **Key Roles**: Innovation Managers, Digital Transformation Specialists, AI Implementation Specialists, Blockchain Specialists

---

## Routing Guidelines

### Request Classification

The Root Orchestrator uses these guidelines to route requests:

#### Financial Requests
- **Division**: Finance & Accounting
- **Keywords**: budget, financial analysis, accounting, tax, treasury, audit
- **Example**: "Analyze Q4 budget variance"

#### Technical Infrastructure
- **Division**: Technology Infrastructure
- **Keywords**: server, network, cloud, IT support, infrastructure, DevOps
- **Example**: "Set up new cloud infrastructure for production"

#### Security & Compliance
- **Division**: Security, Legal & Compliance
- **Keywords**: security, vulnerability, legal, contract, compliance, privacy, GDPR
- **Example**: "Review contract terms" or "Assess security vulnerability"

#### Engineering & Development
- **Division**: Engineering & Product
- **Keywords**: software, code, build, test, QA, product, design, development
- **Example**: "Implement new feature" or "Fix bug in payment system"

#### Sales & Marketing
- **Division**: Revenue Operations
- **Keywords**: sales, marketing, campaign, lead generation, CRM, SEO, content
- **Example**: "Create marketing campaign" or "Analyze sales pipeline"

#### Customer Support
- **Division**: Customer Success
- **Keywords**: customer issue, support ticket, onboarding, training, churn
- **Example**: "Handle customer escalation" or "Onboard new enterprise client"

#### Data & Analytics
- **Division**: Data & Analytics
- **Keywords**: data analysis, BI report, dashboard, predictive model, data warehouse
- **Example**: "Build predictive model" or "Create BI dashboard"

#### HR & People
- **Division**: People & Culture
- **Keywords**: hiring, recruitment, training, performance review, compensation, benefits
- **Example**: "Post job opening" or "Conduct performance review"

#### Operations & Supply Chain
- **Division**: Operations & Supply Chain
- **Keywords**: supply chain, logistics, inventory, manufacturing, warehouse, quality
- **Example**: "Optimize supply chain" or "Manage warehouse inventory"

#### Integrations
- **Division**: Integration & Innovation
- **Keywords**: integration, API, Salesforce, Slack, AWS, third-party platform
- **Example**: "Integrate Salesforce with HubSpot" or "Set up Stripe payment gateway"

### Multi-Division Requests

For requests requiring coordination across multiple divisions:

1. **Root Orchestrator** analyzes and decomposes the request
2. **Delegates** to primary division
3. **Primary division** coordinates with other divisions as needed
4. **Results** are aggregated and returned through the hierarchy

**Example**: "Launch new product feature"
- Engineering (build feature)
- Marketing (create launch campaign)
- Sales (train sales team)
- Customer Success (prepare support materials)

---

## Model Selection Strategy

### Level 0 (Root Orchestrator)
- **Model**: `gemini-2.0-flash-exp`
- **Rationale**: Fast routing decisions, high throughput, cost-effective

### Level 1 (Division Coordinators)
- **Model**: `gemini-2.0-flash-exp`
- **Rationale**: Fast sub-routing within division, balance speed and intelligence

### Level 2 (Team Agents)
- **Model**: `gemini-flash`
- **Rationale**: Cost optimization for routine coordination tasks

### Level 3 (Specialist Agents)
- **Model**: `gemini-flash` or `gemini-pro`
- **Rationale**:
  - `gemini-flash` for standard tasks (most specialists)
  - `gemini-pro` for complex reasoning tasks (senior roles, architects, data scientists)

---

## Agent Distribution Statistics

### Summary
- **Total Agents**: 511
- **Divisions**: 11
- **Teams**: 56
- **Average Specialists per Division**: 46.5
- **Average Specialists per Team**: 9.1

### Distribution by Division

| Rank | Division | Specialists | Percentage | Teams |
|------|----------|-------------|------------|-------|
| 1 | Integration & Innovation | 87 | 17.0% | 11 |
| 2 | Executive & Strategy | 76 | 14.9% | 3 |
| 3 | Security, Legal & Compliance | 71 | 13.9% | 5 |
| 4 | Engineering & Product | 59 | 11.5% | 6 |
| 5 | Technology Infrastructure | 48 | 9.4% | 4 |
| 6 | Data & Analytics | 40 | 7.8% | 6 |
| 7 | Customer Success | 35 | 6.8% | 4 |
| 8 | Operations & Supply Chain | 32 | 6.3% | 4 |
| 9 | Revenue Operations | 31 | 6.1% | 5 |
| 10 | People & Culture | 18 | 3.5% | 4 |
| 11 | Finance & Accounting | 14 | 2.7% | 4 |

### Largest Teams

| Rank | Team | Specialists | Division |
|------|------|-------------|----------|
| 1 | Executive Leadership Team | 71 | Executive & Strategy |
| 2 | Innovation & Research Team | 27 | Integration & Innovation |
| 3 | Specialized Engineering Team | 23 | Engineering & Product |
| 4 | Legal Team | 20 | Security, Legal & Compliance |
| 5 | IT Service Management Team | 18 | Technology Infrastructure |

---

## Implementation Considerations

### Performance Optimization
1. **Caching**: Cache common routing decisions at Root Orchestrator
2. **Parallel Processing**: Enable parallel execution for independent sub-tasks
3. **Load Balancing**: Distribute work evenly across teams within divisions
4. **Fallback Routing**: Implement fallback logic for ambiguous requests

### Monitoring & Observability
1. **Request Tracking**: Track requests through the hierarchy
2. **Performance Metrics**: Monitor response times at each level
3. **Error Handling**: Implement graceful degradation
4. **Agent Health**: Monitor specialist agent availability and performance

### Scalability
1. **Horizontal Scaling**: Add more specialist agents to teams as needed
2. **New Teams**: Add teams to divisions as organization grows
3. **New Divisions**: Add divisions for new functional areas
4. **Dynamic Routing**: Update routing logic based on evolving organization

### Security & Compliance
1. **Access Control**: Implement role-based access for sensitive operations
2. **Audit Logging**: Log all agent interactions for compliance
3. **Data Privacy**: Ensure PII handling compliance across agents
4. **Credential Management**: Secure storage and rotation of API keys

---

## Maintenance & Updates

### Adding New Agents
1. Identify appropriate team based on role and responsibilities
2. Update team's specialist list in hierarchy JSON
3. Update documentation
4. Test routing to new agent

### Reorganizing Structure
1. Analyze current usage patterns and bottlenecks
2. Propose structural changes
3. Update hierarchy JSON
4. Update routing logic
5. Test thoroughly before deployment
6. Document changes

### Deprecating Agents
1. Mark agent as deprecated in system
2. Redirect requests to replacement agent
3. Monitor for zero usage
4. Remove from hierarchy
5. Update documentation

---

## References

- **Hierarchy JSON**: `/home/user/mapachev1/mapachev1/docs/architecture/agent_hierarchy.json`
- **Visual Diagram**: `/home/user/mapachev1/mapachev1/docs/architecture/agent_hierarchy.mermaid`
- **Agent Inventory**: `/home/user/mapachev1/mapachev1/docs/analysis/agent_inventory.csv`

---

*Last Updated: 2025-11-14*
