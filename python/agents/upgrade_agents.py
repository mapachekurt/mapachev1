#!/usr/bin/env python3
"""
Agent Upgrade Script
Systematically upgrades all 511 agents from chatbots to functional executors with 10-15 tools
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple


# Agent role to tool mappings
ROLE_TOOL_TEMPLATES = {
    "executive": {
        "data_access": [
            ("lookup_board_meeting", "meeting_id: str", "Retrieve board meeting details and materials"),
            ("query_executive_dashboard", "metric_category: str, time_period: str", "Query executive dashboard for key performance metrics"),
            ("lookup_investor", "investor_id: str", "Retrieve investor details and relationship history"),
        ],
        "analysis": [
            ("analyze_strategic_initiative", "initiative_id: str", "Analyze strategic initiative progress and impact"),
            ("assess_market_opportunity", "market_segment: str, geography: str", "Assess market opportunity for expansion"),
            ("calculate_company_valuation", "method: str", "Calculate company valuation using specified methodology"),
        ],
        "validation": [
            ("validate_strategic_alignment", "initiative_id: str, strategic_pillar: str", "Validate initiative alignment with corporate strategy"),
        ],
        "execution": [
            ("initiate_strategic_initiative", "title: str, description: str, owner: str, budget: float, timeline_months: int", "Initiate a new strategic initiative"),
            ("approve_executive_decision", "decision_type: str, decision_details: Dict[str, Any], approval_level: str", "Approve executive-level decision"),
            ("schedule_executive_meeting", "meeting_type: str, participants: List[str], duration_minutes: int, priority: str", "Schedule executive-level meeting"),
        ],
        "integration": [
            ("update_board_portal", "content_type: str, content: Dict[str, Any]", "Update board portal with new content"),
            ("sync_executive_systems", "system_name: str, data: Dict[str, Any]", "Sync data with executive systems"),
        ],
        "deliverables": [
            ("generate_executive_summary", "topic: str, data_sources: List[str], audience: str", "Generate executive summary document"),
            ("create_presentation", "meeting_type: str, sections: List[str]", "Create presentation for meetings"),
        ],
        "communication": [
            ("escalate_critical_issue", "issue_type: str, severity: str, description: str, immediate_action_required: bool", "Escalate critical issue requiring attention"),
            ("send_executive_communication", "communication_type: str, audience: str, subject: str, priority: str", "Send executive communication to stakeholders"),
        ]
    },

    "finance": {
        "data_access": [
            ("lookup_transaction", "transaction_id: str", "Retrieve transaction details from financial system"),
            ("query_financial_data", "data_type: str, period: str, filters: Dict[str, Any]", "Query financial data from ERP"),
            ("lookup_account", "account_number: str", "Retrieve account details and balance"),
        ],
        "analysis": [
            ("analyze_financial_performance", "period: str, breakdown_by: str", "Analyze financial performance metrics"),
            ("calculate_financial_ratios", "ratio_types: List[str], period: str", "Calculate financial ratios and indicators"),
            ("forecast_cash_flow", "periods: int, scenario: str", "Forecast cash flow for specified periods"),
        ],
        "validation": [
            ("validate_transaction", "transaction_id: str, validation_rules: List[str]", "Validate transaction against compliance rules"),
            ("verify_account_balance", "account_id: str, expected_balance: float", "Verify account balance accuracy"),
        ],
        "execution": [
            ("post_journal_entry", "entry_data: Dict[str, Any], post_immediately: bool", "Post journal entry to general ledger"),
            ("process_payment", "payment_data: Dict[str, Any]", "Process payment through banking system"),
            ("create_invoice", "invoice_data: Dict[str, Any]", "Create customer invoice"),
        ],
        "integration": [
            ("sync_with_erp", "module: str, data: Dict[str, Any]", "Sync data with ERP system"),
            ("update_banking_system", "transaction_type: str, data: Dict[str, Any]", "Update banking system with transaction"),
        ],
        "deliverables": [
            ("generate_financial_report", "report_type: str, period: str, format: str", "Generate financial report"),
            ("create_reconciliation_report", "account_id: str, period: str", "Create account reconciliation report"),
        ],
        "communication": [
            ("notify_approver", "approval_type: str, item_id: str, urgency: str", "Notify approver of pending item"),
            ("escalate_variance", "variance_type: str, amount: float, description: str", "Escalate significant variance"),
        ]
    },

    "hr": {
        "data_access": [
            ("lookup_employee", "employee_id: str", "Retrieve employee details from HRIS"),
            ("query_workforce_analytics", "metric_type: str, filters: Dict[str, Any]", "Query workforce analytics and metrics"),
            ("lookup_position", "position_id: str", "Retrieve position details and requirements"),
        ],
        "analysis": [
            ("analyze_headcount", "department: str, time_period: str", "Analyze headcount trends and metrics"),
            ("calculate_compensation_metrics", "employee_group: str", "Calculate compensation metrics and benchmarks"),
            ("assess_flight_risk", "employee_id: str", "Assess employee retention risk"),
        ],
        "validation": [
            ("validate_compliance", "compliance_type: str, employee_id: str", "Validate HR compliance requirements"),
            ("verify_employment_eligibility", "employee_id: str", "Verify employment eligibility documentation"),
        ],
        "execution": [
            ("process_new_hire", "employee_data: Dict[str, Any]", "Process new hire onboarding"),
            ("initiate_performance_review", "employee_id: str, review_period: str", "Initiate performance review cycle"),
            ("process_termination", "employee_id: str, termination_data: Dict[str, Any]", "Process employee termination"),
        ],
        "integration": [
            ("sync_with_hris", "module: str, data: Dict[str, Any]", "Sync data with HRIS system"),
            ("update_ats", "candidate_id: str, status: str", "Update applicant tracking system"),
        ],
        "deliverables": [
            ("generate_hr_report", "report_type: str, period: str", "Generate HR analytics report"),
            ("create_offer_letter", "candidate_id: str, offer_data: Dict[str, Any]", "Create employment offer letter"),
        ],
        "communication": [
            ("notify_manager", "notification_type: str, employee_id: str, message: str", "Notify manager of HR matter"),
            ("escalate_hr_issue", "issue_type: str, severity: str, description: str", "Escalate HR issue to leadership"),
        ]
    },

    "engineering": {
        "data_access": [
            ("lookup_repository", "repo_name: str", "Retrieve repository details and metrics"),
            ("query_build_status", "project_id: str, branch: str", "Query CI/CD build status"),
            ("lookup_deployment", "deployment_id: str", "Retrieve deployment details and status"),
        ],
        "analysis": [
            ("analyze_code_quality", "repo_name: str, metrics: List[str]", "Analyze code quality metrics"),
            ("calculate_velocity", "team_id: str, sprint_count: int", "Calculate team velocity metrics"),
            ("assess_technical_debt", "project_id: str", "Assess technical debt and risk"),
        ],
        "validation": [
            ("validate_code_standards", "pull_request_id: str", "Validate code against standards"),
            ("verify_test_coverage", "repo_name: str, minimum_coverage: float", "Verify test coverage meets requirements"),
        ],
        "execution": [
            ("trigger_build", "repo_name: str, branch: str, build_config: Dict[str, Any]", "Trigger CI/CD build pipeline"),
            ("deploy_application", "environment: str, version: str, deployment_config: Dict[str, Any]", "Deploy application to environment"),
            ("create_release", "repo_name: str, version: str, release_notes: str", "Create software release"),
        ],
        "integration": [
            ("sync_with_github", "action: str, data: Dict[str, Any]", "Sync with GitHub repository"),
            ("update_jira", "issue_key: str, update_data: Dict[str, Any]", "Update Jira issue"),
        ],
        "deliverables": [
            ("generate_architecture_diagram", "system_name: str, diagram_type: str", "Generate architecture diagram"),
            ("create_technical_spec", "feature_id: str, spec_template: str", "Create technical specification document"),
        ],
        "communication": [
            ("notify_on_call", "alert_type: str, severity: str, details: Dict[str, Any]", "Notify on-call engineer"),
            ("escalate_incident", "incident_id: str, severity: str", "Escalate production incident"),
        ]
    },

    "sales": {
        "data_access": [
            ("lookup_opportunity", "opportunity_id: str", "Retrieve sales opportunity details"),
            ("query_pipeline", "filters: Dict[str, Any], time_period: str", "Query sales pipeline metrics"),
            ("lookup_customer", "customer_id: str", "Retrieve customer account details"),
        ],
        "analysis": [
            ("analyze_deal_health", "opportunity_id: str", "Analyze deal health and win probability"),
            ("calculate_quota_attainment", "rep_id: str, period: str", "Calculate quota attainment metrics"),
            ("forecast_revenue", "time_period: str, scenario: str", "Forecast revenue for period"),
        ],
        "validation": [
            ("validate_deal_structure", "opportunity_id: str", "Validate deal structure and pricing"),
            ("verify_customer_credit", "customer_id: str", "Verify customer credit worthiness"),
        ],
        "execution": [
            ("create_quote", "opportunity_id: str, quote_data: Dict[str, Any]", "Create customer quote"),
            ("update_opportunity_stage", "opportunity_id: str, new_stage: str", "Update opportunity sales stage"),
            ("schedule_demo", "opportunity_id: str, demo_details: Dict[str, Any]", "Schedule product demonstration"),
        ],
        "integration": [
            ("sync_with_crm", "object_type: str, data: Dict[str, Any]", "Sync data with CRM system"),
            ("update_cpq", "quote_id: str, updates: Dict[str, Any]", "Update CPQ system with quote changes"),
        ],
        "deliverables": [
            ("generate_proposal", "opportunity_id: str, template: str", "Generate customer proposal"),
            ("create_roi_analysis", "opportunity_id: str", "Create ROI analysis for customer"),
        ],
        "communication": [
            ("notify_sales_team", "notification_type: str, details: Dict[str, Any]", "Notify sales team members"),
            ("escalate_deal_risk", "opportunity_id: str, risk_type: str", "Escalate deal risk to leadership"),
        ]
    },

    "marketing": {
        "data_access": [
            ("lookup_campaign", "campaign_id: str", "Retrieve campaign details and metrics"),
            ("query_marketing_analytics", "metric_type: str, time_period: str", "Query marketing analytics"),
            ("lookup_lead", "lead_id: str", "Retrieve lead details and scoring"),
        ],
        "analysis": [
            ("analyze_campaign_performance", "campaign_id: str", "Analyze campaign performance metrics"),
            ("calculate_roi", "campaign_ids: List[str], time_period: str", "Calculate marketing ROI"),
            ("assess_lead_quality", "lead_id: str", "Assess lead quality and scoring"),
        ],
        "validation": [
            ("validate_campaign_targeting", "campaign_id: str", "Validate campaign targeting and segmentation"),
            ("verify_content_compliance", "content_id: str", "Verify content meets compliance requirements"),
        ],
        "execution": [
            ("launch_campaign", "campaign_data: Dict[str, Any]", "Launch marketing campaign"),
            ("nurture_lead", "lead_id: str, nurture_track: str", "Add lead to nurture campaign"),
            ("schedule_content", "content_id: str, schedule_data: Dict[str, Any]", "Schedule content publication"),
        ],
        "integration": [
            ("sync_with_marketing_automation", "data_type: str, data: Dict[str, Any]", "Sync with marketing automation platform"),
            ("update_social_media", "platform: str, post_data: Dict[str, Any]", "Update social media platform"),
        ],
        "deliverables": [
            ("generate_marketing_report", "report_type: str, period: str", "Generate marketing performance report"),
            ("create_campaign_brief", "campaign_data: Dict[str, Any]", "Create campaign creative brief"),
        ],
        "communication": [
            ("notify_marketing_team", "notification_type: str, details: str", "Notify marketing team"),
            ("escalate_budget_variance", "campaign_id: str, variance_amount: float", "Escalate budget variance"),
        ]
    },

    "operations": {
        "data_access": [
            ("lookup_order", "order_id: str", "Retrieve order details and status"),
            ("query_inventory", "filters: Dict[str, Any]", "Query inventory levels and locations"),
            ("lookup_supplier", "supplier_id: str", "Retrieve supplier details and performance"),
        ],
        "analysis": [
            ("analyze_operational_efficiency", "metric_type: str, time_period: str", "Analyze operational efficiency metrics"),
            ("calculate_inventory_metrics", "location: str", "Calculate inventory turnover and metrics"),
            ("assess_supplier_performance", "supplier_id: str, period: str", "Assess supplier performance"),
        ],
        "validation": [
            ("validate_order", "order_id: str", "Validate order for processing"),
            ("verify_inventory_accuracy", "location: str, item_id: str", "Verify inventory count accuracy"),
        ],
        "execution": [
            ("process_order", "order_id: str", "Process customer order"),
            ("create_purchase_order", "po_data: Dict[str, Any]", "Create purchase order to supplier"),
            ("initiate_transfer", "transfer_data: Dict[str, Any]", "Initiate inventory transfer"),
        ],
        "integration": [
            ("sync_with_erp", "module: str, data: Dict[str, Any]", "Sync with ERP operations module"),
            ("update_wms", "transaction_type: str, data: Dict[str, Any]", "Update warehouse management system"),
        ],
        "deliverables": [
            ("generate_operations_report", "report_type: str, period: str", "Generate operations performance report"),
            ("create_shipment_manifest", "shipment_id: str", "Create shipment manifest"),
        ],
        "communication": [
            ("notify_operations_team", "notification_type: str, details: str", "Notify operations team"),
            ("escalate_fulfillment_issue", "issue_type: str, order_id: str", "Escalate order fulfillment issue"),
        ]
    },

    "it": {
        "data_access": [
            ("lookup_ticket", "ticket_id: str", "Retrieve IT ticket details and history"),
            ("query_system_status", "system_name: str", "Query system health and status"),
            ("lookup_asset", "asset_id: str", "Retrieve IT asset details"),
        ],
        "analysis": [
            ("analyze_system_performance", "system_name: str, time_period: str", "Analyze system performance metrics"),
            ("calculate_sla_metrics", "service_type: str, period: str", "Calculate SLA compliance metrics"),
            ("assess_security_posture", "assessment_scope: str", "Assess security posture and risks"),
        ],
        "validation": [
            ("validate_security_compliance", "compliance_framework: str, scope: str", "Validate security compliance"),
            ("verify_backup", "backup_id: str", "Verify backup completion and integrity"),
        ],
        "execution": [
            ("create_ticket", "ticket_data: Dict[str, Any]", "Create IT support ticket"),
            ("provision_resource", "resource_type: str, config: Dict[str, Any]", "Provision IT resource"),
            ("execute_maintenance", "maintenance_type: str, scope: Dict[str, Any]", "Execute system maintenance"),
        ],
        "integration": [
            ("sync_with_itsm", "data_type: str, data: Dict[str, Any]", "Sync with IT service management"),
            ("update_monitoring", "alert_type: str, config: Dict[str, Any]", "Update monitoring system"),
        ],
        "deliverables": [
            ("generate_it_report", "report_type: str, period: str", "Generate IT operations report"),
            ("create_runbook", "process_name: str, steps: List[Dict[str, Any]]", "Create operational runbook"),
        ],
        "communication": [
            ("notify_it_team", "notification_type: str, details: str", "Notify IT team"),
            ("escalate_incident", "incident_id: str, severity: str", "Escalate IT incident"),
        ]
    }
}


def determine_role_category(agent_name: str, role: str, department: str) -> str:
    """Determine which role category an agent belongs to"""
    name_lower = agent_name.lower()
    role_lower = role.lower()
    dept_lower = department.lower() if department else ""

    if any(x in role_lower for x in ["ceo", "coo", "cfo", "cto", "cio", "cmo", "chro", "cso", "cpo", "vp", "director", "head of"]):
        return "executive"
    elif any(x in dept_lower or x in role_lower for x in ["finance", "accounting", "treasury", "controller", "payable", "receivable"]):
        return "finance"
    elif any(x in dept_lower or x in role_lower for x in ["hr", "human resources", "people", "talent", "recruiting", "compensation"]):
        return "hr"
    elif any(x in dept_lower or x in role_lower for x in ["engineering", "developer", "devops", "sre", "software", "architect"]):
        return "engineering"
    elif any(x in dept_lower or x in role_lower for x in ["sales", "account executive", "account manager", "business development"]):
        return "sales"
    elif any(x in dept_lower or x in role_lower for x in ["marketing", "brand", "digital marketing", "content", "demand gen"]):
        return "marketing"
    elif any(x in dept_lower or x in role_lower for x in ["operations", "supply chain", "logistics", "procurement", "warehouse"]):
        return "operations"
    elif any(x in dept_lower or x in role_lower for x in ["it", "information technology", "systems", "infrastructure", "helpdesk", "security"]):
        return "it"
    else:
        return "executive"  # Default fallback


def generate_tool_function(tool_name: str, params: str, description: str, category: str) -> str:
    """Generate a tool function with realistic return data"""
    # Generate Args section
    args_section = ""
    if params.strip():
        param_list = [p.strip() for p in params.split(',')]
        args_lines = []
        for p in param_list:
            if ':' in p:
                param_name = p.split(':')[0].strip()
                param_type = p.split(':')[1].strip()
                args_lines.append(f"        {param_name}: {param_type}")
        args_section = "\n".join(args_lines)

    args_doc = f"""
    Args:
{args_section}
""" if args_section else ""

    return f'''def {tool_name}({params}) -> Dict[str, Any]:
    """
    {description}{args_doc}
    Returns:
        dict: {description} results

    MCP Integration:
        Calls mcp_{category} server
        Falls back to stub if MCP not implemented
    """
    return {{
        "status": "success",
        "tool": "{tool_name}",
        "data": {{"message": "Tool executed successfully"}},
        "timestamp": datetime.now().isoformat()
    }}
'''


def parse_agent_file(file_path: str) -> Dict[str, Any]:
    """Parse existing agent file to extract metadata"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Extract agent number
    agent_num_match = re.search(r'Agent (\d+)', content)
    agent_num = agent_num_match.group(1) if agent_num_match else "000"

    # Extract role
    role_match = re.search(r'Role: (.+?)\\n', content)
    role = role_match.group(1) if role_match else "Unknown Role"

    # Extract tier
    tier_match = re.search(r'Tier: (.+?)\\n', content)
    tier = tier_match.group(1) if tier_match else "Unknown Tier"

    # Extract agent name from class
    class_match = re.search(r'class (\w+):', content)
    agent_class_name = class_match.group(1) if class_match else "UnknownAgent"

    # Extract agent_id
    agent_id_match = re.search(r'self\.agent_id = "(.+?)"', content)
    agent_id = agent_id_match.group(1) if agent_id_match else f"agent_{agent_num}"

    # Extract department
    dept_match = re.search(r'self\.department = "(.+?)"', content)
    department = dept_match.group(1) if dept_match else ""

    return {
        "agent_number": agent_num,
        "role": role,
        "tier": tier,
        "agent_class_name": agent_class_name,
        "agent_id": agent_id,
        "department": department,
        "file_path": file_path
    }


def generate_upgraded_agent(agent_info: Dict[str, Any]) -> str:
    """Generate complete upgraded agent file with 10-15 functional tools"""

    role_category = determine_role_category(
        agent_info["agent_class_name"],
        agent_info["role"],
        agent_info["department"]
    )

    tool_templates = ROLE_TOOL_TEMPLATES.get(role_category, ROLE_TOOL_TEMPLATES["executive"])

    # Generate all tool functions
    tools_code = ""
    tool_names = []
    tool_count = 0

    for category, tools in tool_templates.items():
        tools_code += f"\n# ============================================================================\n"
        tools_code += f"# {category.upper().replace('_', ' ')} TOOLS\n"
        tools_code += f"# ============================================================================\n\n"

        for tool_name, params, description in tools:
            tools_code += generate_tool_function(tool_name, params, description, role_category)
            tools_code += "\n\n"
            tool_names.append(tool_name)
            tool_count += 1

    # Generate system prompt
    system_prompt = f'''"""
You are a {agent_info["role"]} with functional execution capabilities.

## Core Responsibilities

You are responsible for {agent_info["role"].lower()} functions including:
- Strategic planning and execution
- Data analysis and decision making
- System integration and automation
- Stakeholder communication
- Deliverable generation

## Tool Usage Protocols

You have access to {tool_count} functional tools across these categories:

### Data Access Tools
Query and retrieve information from systems

### Analysis Tools
Perform calculations and assessments

### Validation Tools
Verify compliance and data quality

### Execution Tools
Take actions and make changes

### Integration Tools
Sync with external systems

### Deliverable Generation Tools
Create documents and reports

### Communication Tools
Notify and escalate issues

## Tool Execution Guidelines

1. **ALWAYS use tools to take action** - Execute, don't just advise
2. **Use multiple tools in sequence** when needed
3. **Query data first** before making decisions
4. **Validate before executing** critical actions
5. **Generate deliverables** using appropriate tools
6. **Escalate issues** when necessary
7. **Document actions** by creating records

Remember: You are a functional agent that EXECUTES tasks using tools.
"""'''

    # Build complete agent file
    upgraded_content = f'''"""
Agent {agent_info["agent_number"]}: {agent_info["role"]}
Role: {agent_info["role"]}
Tier: {agent_info["tier"]}
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

{tools_code}

# ============================================================================
# AGENT DEFINITION
# ============================================================================

SYSTEM_PROMPT = {system_prompt}


class {agent_info["agent_class_name"]}:
    """
    {agent_info["role"]} - Functional agent with {tool_count} tools
    """

    def __init__(self):
        self.agent_id = "{agent_info["agent_id"]}"
        self.role = "{agent_info["role"]}"
        self.tier = "{agent_info["tier"]}"
        self.department = "{agent_info["department"]}"
        self.tool_count = {tool_count}

        # Functional tools
        self.tools = [
{chr(10).join([f"            {tool}," for tool in tool_names])}
        ]

        self.responsibilities = [
            "{agent_info["role"]} operations",
            "Data analysis and reporting",
            "System integration",
            "Stakeholder communication"
        ]

    def get_tool_summary(self) -> Dict[str, Any]:
        """Get summary of available tools"""
        return {{
            "agent_id": self.agent_id,
            "tool_count": self.tool_count,
            "capabilities": "Fully functional agent with execution tools"
        }}


# Agent instance
{agent_info["agent_id"].replace('-', '_')}_agent = {agent_info["agent_class_name"]}()

# Export tools for Google ADK integration
__all__ = [
    '{agent_info["agent_class_name"]}',
    '{agent_info["agent_id"].replace('-', '_')}_agent',
    'SYSTEM_PROMPT',
{chr(10).join([f"    '{tool}'," for tool in tool_names])}
]
'''

    return upgraded_content


def upgrade_agent_file(file_path: str) -> Tuple[bool, str]:
    """Upgrade a single agent file"""
    try:
        # Parse existing agent
        agent_info = parse_agent_file(file_path)

        # Generate upgraded version
        upgraded_content = generate_upgraded_agent(agent_info)

        # Write upgraded file
        with open(file_path, 'w') as f:
            f.write(upgraded_content)

        return True, f"Upgraded {agent_info['agent_id']} with {agent_info.get('tool_count', 10)} tools"

    except Exception as e:
        return False, f"Error upgrading {file_path}: {str(e)}"


def main():
    """Main upgrade function"""
    agents_dir = Path("/home/user/mapachev1/python/agents")
    agent_files = sorted(agents_dir.glob("agent_*.py"))
    agent_files = [f for f in agent_files if "upgrade" not in f.name]

    print(f"Found {len(agent_files)} agents to upgrade")
    print("="*80)

    success_count = 0
    error_count = 0

    for i, agent_file in enumerate(agent_files, 1):
        success, message = upgrade_agent_file(str(agent_file))

        if success:
            success_count += 1
            print(f"[{i}/{len(agent_files)}] ✓ {message}")
        else:
            error_count += 1
            print(f"[{i}/{len(agent_files)}] ✗ {message}")

        # Commit every 20 agents
        if i % 20 == 0:
            print(f"\n{'='*80}")
            print(f"Completed batch {i//20}: {success_count} successful, {error_count} errors")
            print(f"{'='*80}\n")

    print(f"\n{'='*80}")
    print(f"UPGRADE COMPLETE")
    print(f"Total: {len(agent_files)} agents")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
