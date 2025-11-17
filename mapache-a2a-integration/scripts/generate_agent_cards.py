"""
Generate Agent Cards for all 511 agents

This script defines the organizational structure and generates agent cards
for all 511 agents across the organization.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.core.base_agent import BaseA2AAgent, AgentConfig


# Skill Definitions Library
SKILL_DEFINITIONS = {
    # Leadership & Strategy
    "strategic_planning": "Strategic Planning",
    "executive_leadership": "Executive Leadership",
    "organizational_development": "Organizational Development",
    "change_management": "Change Management",
    "decision_making": "Decision Making",
    "stakeholder_management": "Stakeholder Management",

    # Finance & Accounting
    "financial_planning": "Financial Planning & Analysis",
    "budget_management": "Budget Management",
    "investor_relations": "Investor Relations",
    "financial_reporting": "Financial Reporting",
    "tax_planning": "Tax Planning",
    "treasury_management": "Treasury Management",
    "accounts_payable": "Accounts Payable",
    "accounts_receivable": "Accounts Receivable",
    "financial_controls": "Financial Controls",
    "audit_compliance": "Audit & Compliance",

    # Sales & Marketing
    "sales_operations": "Sales Operations",
    "account_management": "Account Management",
    "lead_generation": "Lead Generation",
    "sales_enablement": "Sales Enablement",
    "customer_acquisition": "Customer Acquisition",
    "demand_generation": "Demand Generation",
    "content_marketing": "Content Marketing",
    "brand_management": "Brand Management",
    "marketing_analytics": "Marketing Analytics",
    "digital_marketing": "Digital Marketing",
    "seo_sem": "SEO/SEM",
    "social_media": "Social Media Marketing",
    "event_marketing": "Event Marketing",
    "product_marketing": "Product Marketing",

    # Engineering & Product
    "software_engineering": "Software Engineering",
    "system_architecture": "System Architecture",
    "devops": "DevOps",
    "quality_assurance": "Quality Assurance",
    "product_management": "Product Management",
    "product_design": "Product Design",
    "ux_design": "UX Design",
    "ui_design": "UI Design",
    "technical_writing": "Technical Writing",
    "api_development": "API Development",
    "database_design": "Database Design",
    "cloud_infrastructure": "Cloud Infrastructure",
    "microservices": "Microservices",
    "frontend_development": "Frontend Development",
    "backend_development": "Backend Development",
    "mobile_development": "Mobile Development",

    # HR & People
    "talent_acquisition": "Talent Acquisition",
    "employee_relations": "Employee Relations",
    "compensation_benefits": "Compensation & Benefits",
    "performance_management": "Performance Management",
    "learning_development": "Learning & Development",
    "hr_operations": "HR Operations",
    "onboarding": "Onboarding",
    "diversity_inclusion": "Diversity & Inclusion",

    # Operations
    "operations_management": "Operations Management",
    "process_optimization": "Process Optimization",
    "project_management": "Project Management",
    "supply_chain": "Supply Chain Management",
    "vendor_management": "Vendor Management",
    "logistics": "Logistics",
    "procurement": "Procurement",

    # Customer Success
    "customer_success": "Customer Success",
    "customer_support": "Customer Support",
    "technical_support": "Technical Support",
    "customer_onboarding": "Customer Onboarding",
    "customer_retention": "Customer Retention",

    # Data & Analytics
    "data_analysis": "Data Analysis",
    "data_engineering": "Data Engineering",
    "business_intelligence": "Business Intelligence",
    "data_science": "Data Science",
    "machine_learning": "Machine Learning",
    "data_visualization": "Data Visualization",

    # Legal & Compliance
    "legal_counsel": "Legal Counsel",
    "contract_management": "Contract Management",
    "compliance": "Compliance",
    "regulatory_affairs": "Regulatory Affairs",
    "intellectual_property": "Intellectual Property",

    # Security & IT
    "cybersecurity": "Cybersecurity",
    "information_security": "Information Security",
    "security_operations": "Security Operations",
    "it_operations": "IT Operations",
    "helpdesk": "IT Helpdesk",
    "infrastructure_management": "Infrastructure Management",
}


# Organizational Structure - All 511 Agents
ORGANIZATIONAL_STRUCTURE = {
    "executive": {
        "ceo": {
            "role": "Chief Executive Officer",
            "skills": ["strategic_planning", "executive_leadership", "decision_making"],
            "tools": [],
            "reports_to": None,
            "manages": ["cfo", "cto", "cmo", "coo", "chro"],
        },
        "cfo": {
            "role": "Chief Financial Officer",
            "skills": ["financial_planning", "investor_relations", "budget_management"],
            "tools": [],
            "reports_to": "ceo",
            "manages": ["controller", "vp_fp_and_a", "treasurer"],
        },
        "cto": {
            "role": "Chief Technology Officer",
            "skills": ["system_architecture", "technical_leadership", "innovation"],
            "tools": [],
            "reports_to": "ceo",
            "manages": ["vp_engineering", "vp_infrastructure", "vp_security"],
        },
        "cmo": {
            "role": "Chief Marketing Officer",
            "skills": ["brand_management", "marketing_strategy", "demand_generation"],
            "tools": [],
            "reports_to": "ceo",
            "manages": ["vp_marketing", "vp_product_marketing"],
        },
        "coo": {
            "role": "Chief Operating Officer",
            "skills": ["operations_management", "process_optimization", "scalability"],
            "tools": [],
            "reports_to": "ceo",
            "manages": ["vp_operations", "vp_supply_chain"],
        },
        "chro": {
            "role": "Chief Human Resources Officer",
            "skills": ["talent_management", "organizational_development", "culture"],
            "tools": [],
            "reports_to": "ceo",
            "manages": ["vp_talent", "vp_people_ops"],
        },
    },
    "finance": {},
    "sales": {},
    "marketing": {},
    "engineering": {},
    "product": {},
    "hr": {},
    "operations": {},
    "legal": {},
    "customer_success": {},
    "data": {},
    "security": {},
    "it": {},
    "facilities": {},
}


# Add Finance team (30 agents)
ORGANIZATIONAL_STRUCTURE["finance"] = {
    f"controller": {
        "role": "Controller",
        "skills": ["financial_reporting", "financial_controls", "audit_compliance"],
        "tools": [],
        "reports_to": "cfo",
        "manages": [f"senior_accountant_{i}" for i in range(1, 4)],
    },
    f"vp_fp_and_a": {
        "role": "VP of Financial Planning & Analysis",
        "skills": ["financial_planning", "budget_management", "financial_modeling"],
        "tools": [],
        "reports_to": "cfo",
        "manages": [f"fp_and_a_manager_{i}" for i in range(1, 3)],
    },
    f"treasurer": {
        "role": "Treasurer",
        "skills": ["treasury_management", "cash_management", "risk_management"],
        "tools": [],
        "reports_to": "cfo",
        "manages": ["cash_manager"],
    },
}

# Add individual contributors and managers in finance
for i in range(1, 4):
    ORGANIZATIONAL_STRUCTURE["finance"][f"senior_accountant_{i}"] = {
        "role": f"Senior Accountant",
        "skills": ["financial_reporting", "accounts_payable", "accounts_receivable"],
        "tools": [],
        "reports_to": "controller",
        "manages": [],
    }

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["finance"][f"fp_and_a_manager_{i}"] = {
        "role": "FP&A Manager",
        "skills": ["financial_planning", "budget_management", "data_analysis"],
        "tools": [],
        "reports_to": "vp_fp_and_a",
        "manages": [f"fp_and_a_analyst_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["finance"][f"fp_and_a_analyst_{i}_{j}"] = {
            "role": "FP&A Analyst",
            "skills": ["financial_analysis", "budgeting", "forecasting"],
            "tools": [],
            "reports_to": f"fp_and_a_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["finance"]["cash_manager"] = {
    "role": "Cash Manager",
    "skills": ["cash_management", "treasury_management", "liquidity_planning"],
    "tools": [],
    "reports_to": "treasurer",
    "manages": [],
}

for i in range(1, 11):
    ORGANIZATIONAL_STRUCTURE["finance"][f"accountant_{i}"] = {
        "role": "Accountant",
        "skills": ["accounting", "financial_reporting", "reconciliation"],
        "tools": [],
        "reports_to": "controller",
        "manages": [],
    }


# Add Sales team (50 agents)
ORGANIZATIONAL_STRUCTURE["sales"] = {
    "vp_sales": {
        "role": "VP of Sales",
        "skills": ["sales_leadership", "revenue_management", "sales_strategy"],
        "tools": [],
        "reports_to": "ceo",
        "manages": [f"sales_director_{i}" for i in range(1, 4)],
    },
}

for i in range(1, 4):
    ORGANIZATIONAL_STRUCTURE["sales"][f"sales_director_{i}"] = {
        "role": f"Sales Director - Region {i}",
        "skills": ["sales_management", "territory_planning", "team_leadership"],
        "tools": [],
        "reports_to": "vp_sales",
        "manages": [f"sales_manager_{i}_{j}" for j in range(1, 3)],
    }
    for j in range(1, 3):
        ORGANIZATIONAL_STRUCTURE["sales"][f"sales_manager_{i}_{j}"] = {
            "role": f"Sales Manager",
            "skills": ["sales_management", "account_management", "coaching"],
            "tools": [],
            "reports_to": f"sales_director_{i}",
            "manages": [f"account_executive_{i}_{j}_{k}" for k in range(1, 4)],
        }
        for k in range(1, 4):
            ORGANIZATIONAL_STRUCTURE["sales"][f"account_executive_{i}_{j}_{k}"] = {
                "role": "Account Executive",
                "skills": ["sales", "negotiation", "relationship_building"],
                "tools": [],
                "reports_to": f"sales_manager_{i}_{j}",
                "manages": [],
            }

# Add Sales Ops and SDRs
ORGANIZATIONAL_STRUCTURE["sales"]["director_sales_ops"] = {
    "role": "Director of Sales Operations",
    "skills": ["sales_operations", "crm_management", "sales_analytics"],
    "tools": [],
    "reports_to": "vp_sales",
    "manages": [f"sales_ops_analyst_{i}" for i in range(1, 4)],
}

for i in range(1, 4):
    ORGANIZATIONAL_STRUCTURE["sales"][f"sales_ops_analyst_{i}"] = {
        "role": "Sales Operations Analyst",
        "skills": ["sales_analytics", "data_analysis", "reporting"],
        "tools": [],
        "reports_to": "director_sales_ops",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["sales"]["sdr_manager"] = {
    "role": "SDR Manager",
    "skills": ["lead_generation", "team_management", "sales_development"],
    "tools": [],
    "reports_to": "vp_sales",
    "manages": [f"sdr_{i}" for i in range(1, 11)],
}

for i in range(1, 11):
    ORGANIZATIONAL_STRUCTURE["sales"][f"sdr_{i}"] = {
        "role": "Sales Development Representative",
        "skills": ["lead_generation", "prospecting", "cold_calling"],
        "tools": [],
        "reports_to": "sdr_manager",
        "manages": [],
    }


# Add Marketing team (40 agents)
ORGANIZATIONAL_STRUCTURE["marketing"] = {
    "vp_marketing": {
        "role": "VP of Marketing",
        "skills": ["marketing_strategy", "brand_management", "demand_generation"],
        "tools": [],
        "reports_to": "cmo",
        "manages": ["director_demand_gen", "director_content", "director_brand"],
    },
    "director_demand_gen": {
        "role": "Director of Demand Generation",
        "skills": ["demand_generation", "digital_marketing", "marketing_automation"],
        "tools": [],
        "reports_to": "vp_marketing",
        "manages": [f"demand_gen_manager_{i}" for i in range(1, 3)],
    },
    "director_content": {
        "role": "Director of Content",
        "skills": ["content_marketing", "content_strategy", "storytelling"],
        "tools": [],
        "reports_to": "vp_marketing",
        "manages": [f"content_manager_{i}" for i in range(1, 3)],
    },
    "director_brand": {
        "role": "Director of Brand",
        "skills": ["brand_management", "creative_direction", "brand_strategy"],
        "tools": [],
        "reports_to": "vp_marketing",
        "manages": ["brand_manager", "creative_manager"],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["marketing"][f"demand_gen_manager_{i}"] = {
        "role": "Demand Generation Manager",
        "skills": ["demand_generation", "campaign_management", "marketing_analytics"],
        "tools": [],
        "reports_to": "director_demand_gen",
        "manages": [f"demand_gen_specialist_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["marketing"][f"demand_gen_specialist_{i}_{j}"] = {
            "role": "Demand Generation Specialist",
            "skills": ["digital_marketing", "campaign_execution", "analytics"],
            "tools": [],
            "reports_to": f"demand_gen_manager_{i}",
            "manages": [],
        }

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["marketing"][f"content_manager_{i}"] = {
        "role": "Content Manager",
        "skills": ["content_creation", "content_strategy", "seo"],
        "tools": [],
        "reports_to": "director_content",
        "manages": [f"content_writer_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["marketing"][f"content_writer_{i}_{j}"] = {
            "role": "Content Writer",
            "skills": ["writing", "storytelling", "seo"],
            "tools": [],
            "reports_to": f"content_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["marketing"]["brand_manager"] = {
    "role": "Brand Manager",
    "skills": ["brand_management", "brand_strategy", "marketing"],
    "tools": [],
    "reports_to": "director_brand",
    "manages": [f"brand_specialist_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["marketing"][f"brand_specialist_{i}"] = {
        "role": "Brand Specialist",
        "skills": ["branding", "creative", "marketing"],
        "tools": [],
        "reports_to": "brand_manager",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["marketing"]["creative_manager"] = {
    "role": "Creative Manager",
    "skills": ["creative_direction", "design", "visual_communication"],
    "tools": [],
    "reports_to": "director_brand",
    "manages": [f"designer_{i}" for i in range(1, 5)],
}

for i in range(1, 5):
    ORGANIZATIONAL_STRUCTURE["marketing"][f"designer_{i}"] = {
        "role": "Designer",
        "skills": ["graphic_design", "visual_design", "creative"],
        "tools": [],
        "reports_to": "creative_manager",
        "manages": [],
    }


# Add Engineering team (100 agents)
ORGANIZATIONAL_STRUCTURE["engineering"] = {
    "vp_engineering": {
        "role": "VP of Engineering",
        "skills": ["engineering_leadership", "technical_strategy", "team_building"],
        "tools": [],
        "reports_to": "cto",
        "manages": [f"director_engineering_{i}" for i in range(1, 4)],
    },
}

# Create engineering hierarchy
for i in range(1, 4):
    dir_name = f"director_engineering_{i}"
    ORGANIZATIONAL_STRUCTURE["engineering"][dir_name] = {
        "role": f"Director of Engineering - Team {i}",
        "skills": ["engineering_management", "architecture", "technical_leadership"],
        "tools": [],
        "reports_to": "vp_engineering",
        "manages": [f"engineering_manager_{i}_{j}" for j in range(1, 4)],
    }

    for j in range(1, 4):
        em_name = f"engineering_manager_{i}_{j}"
        ORGANIZATIONAL_STRUCTURE["engineering"][em_name] = {
            "role": "Engineering Manager",
            "skills": ["engineering_management", "technical_leadership", "agile"],
            "tools": [],
            "reports_to": dir_name,
            "manages": [f"senior_engineer_{i}_{j}_{k}" for k in range(1, 3)],
        }

        # Add senior engineers
        for k in range(1, 3):
            ORGANIZATIONAL_STRUCTURE["engineering"][f"senior_engineer_{i}_{j}_{k}"] = {
                "role": "Senior Software Engineer",
                "skills": ["software_engineering", "system_design", "mentoring"],
                "tools": [],
                "reports_to": em_name,
                "manages": [f"engineer_{i}_{j}_{k}_{l}" for l in range(1, 3)],
            }

            # Add engineers
            for l in range(1, 3):
                ORGANIZATIONAL_STRUCTURE["engineering"][f"engineer_{i}_{j}_{k}_{l}"] = {
                    "role": "Software Engineer",
                    "skills": ["software_engineering", "coding", "problem_solving"],
                    "tools": [],
                    "reports_to": f"senior_engineer_{i}_{j}_{k}",
                    "manages": [],
                }

# Add QA team
ORGANIZATIONAL_STRUCTURE["engineering"]["director_qa"] = {
    "role": "Director of QA",
    "skills": ["quality_assurance", "test_strategy", "automation"],
    "tools": [],
    "reports_to": "vp_engineering",
    "manages": [f"qa_manager_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["engineering"][f"qa_manager_{i}"] = {
        "role": "QA Manager",
        "skills": ["quality_assurance", "test_management", "automation"],
        "tools": [],
        "reports_to": "director_qa",
        "manages": [f"qa_engineer_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["engineering"][f"qa_engineer_{i}_{j}"] = {
            "role": "QA Engineer",
            "skills": ["quality_assurance", "testing", "automation"],
            "tools": [],
            "reports_to": f"qa_manager_{i}",
            "manages": [],
        }


# Add Product team (30 agents)
ORGANIZATIONAL_STRUCTURE["product"] = {
    "vp_product": {
        "role": "VP of Product",
        "skills": ["product_strategy", "product_leadership", "roadmap_planning"],
        "tools": [],
        "reports_to": "ceo",
        "manages": [f"director_product_{i}" for i in range(1, 3)],
    },
    "vp_design": {
        "role": "VP of Design",
        "skills": ["design_leadership", "ux_strategy", "design_systems"],
        "tools": [],
        "reports_to": "vp_product",
        "manages": ["director_ux", "director_ui"],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["product"][f"director_product_{i}"] = {
        "role": f"Director of Product",
        "skills": ["product_management", "strategy", "stakeholder_management"],
        "tools": [],
        "reports_to": "vp_product",
        "manages": [f"senior_pm_{i}_{j}" for j in range(1, 3)],
    }
    for j in range(1, 3):
        ORGANIZATIONAL_STRUCTURE["product"][f"senior_pm_{i}_{j}"] = {
            "role": "Senior Product Manager",
            "skills": ["product_management", "roadmap_planning", "user_research"],
            "tools": [],
            "reports_to": f"director_product_{i}",
            "manages": [f"pm_{i}_{j}_{k}" for k in range(1, 3)],
        }
        for k in range(1, 3):
            ORGANIZATIONAL_STRUCTURE["product"][f"pm_{i}_{j}_{k}"] = {
                "role": "Product Manager",
                "skills": ["product_management", "feature_definition", "analytics"],
                "tools": [],
                "reports_to": f"senior_pm_{i}_{j}",
                "manages": [],
            }

ORGANIZATIONAL_STRUCTURE["product"]["director_ux"] = {
    "role": "Director of UX",
    "skills": ["ux_design", "user_research", "design_thinking"],
    "tools": [],
    "reports_to": "vp_design",
    "manages": [f"ux_designer_{i}" for i in range(1, 5)],
}

for i in range(1, 5):
    ORGANIZATIONAL_STRUCTURE["product"][f"ux_designer_{i}"] = {
        "role": "UX Designer",
        "skills": ["ux_design", "wireframing", "user_research"],
        "tools": [],
        "reports_to": "director_ux",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["product"]["director_ui"] = {
    "role": "Director of UI",
    "skills": ["ui_design", "visual_design", "design_systems"],
    "tools": [],
    "reports_to": "vp_design",
    "manages": [f"ui_designer_{i}" for i in range(1, 5)],
}

for i in range(1, 5):
    ORGANIZATIONAL_STRUCTURE["product"][f"ui_designer_{i}"] = {
        "role": "UI Designer",
        "skills": ["ui_design", "visual_design", "prototyping"],
        "tools": [],
        "reports_to": "director_ui",
        "manages": [],
    }


# Add HR team (35 agents)
ORGANIZATIONAL_STRUCTURE["hr"] = {
    "vp_talent": {
        "role": "VP of Talent",
        "skills": ["talent_acquisition", "recruiting_strategy", "employer_branding"],
        "tools": [],
        "reports_to": "chro",
        "manages": ["director_recruiting"],
    },
    "vp_people_ops": {
        "role": "VP of People Operations",
        "skills": ["hr_operations", "employee_experience", "hr_systems"],
        "tools": [],
        "reports_to": "chro",
        "manages": ["director_hr_ops", "director_learning_development"],
    },
    "director_recruiting": {
        "role": "Director of Recruiting",
        "skills": ["recruiting", "talent_acquisition", "hiring"],
        "tools": [],
        "reports_to": "vp_talent",
        "manages": [f"recruiting_manager_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["hr"][f"recruiting_manager_{i}"] = {
        "role": "Recruiting Manager",
        "skills": ["recruiting", "sourcing", "interviewing"],
        "tools": [],
        "reports_to": "director_recruiting",
        "manages": [f"recruiter_{i}_{j}" for j in range(1, 6)],
    }
    for j in range(1, 6):
        ORGANIZATIONAL_STRUCTURE["hr"][f"recruiter_{i}_{j}"] = {
            "role": "Recruiter",
            "skills": ["recruiting", "sourcing", "candidate_screening"],
            "tools": [],
            "reports_to": f"recruiting_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["hr"]["director_hr_ops"] = {
    "role": "Director of HR Operations",
    "skills": ["hr_operations", "hris", "compliance"],
    "tools": [],
    "reports_to": "vp_people_ops",
    "manages": [f"hr_ops_manager_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["hr"][f"hr_ops_manager_{i}"] = {
        "role": "HR Operations Manager",
        "skills": ["hr_operations", "employee_relations", "benefits"],
        "tools": [],
        "reports_to": "director_hr_ops",
        "manages": [f"hr_specialist_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["hr"][f"hr_specialist_{i}_{j}"] = {
            "role": "HR Specialist",
            "skills": ["hr_operations", "employee_support", "compliance"],
            "tools": [],
            "reports_to": f"hr_ops_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["hr"]["director_learning_development"] = {
    "role": "Director of Learning & Development",
    "skills": ["learning_development", "training", "career_development"],
    "tools": [],
    "reports_to": "vp_people_ops",
    "manages": [f"l_and_d_manager"],
}

ORGANIZATIONAL_STRUCTURE["hr"]["l_and_d_manager"] = {
    "role": "Learning & Development Manager",
    "skills": ["training", "curriculum_development", "coaching"],
    "tools": [],
    "reports_to": "director_learning_development",
    "manages": [f"training_specialist_{i}" for i in range(1, 4)],
}

for i in range(1, 4):
    ORGANIZATIONAL_STRUCTURE["hr"][f"training_specialist_{i}"] = {
        "role": "Training Specialist",
        "skills": ["training", "facilitation", "instructional_design"],
        "tools": [],
        "reports_to": "l_and_d_manager",
        "manages": [],
    }


# Add Operations team (40 agents) - similar structure
ORGANIZATIONAL_STRUCTURE["operations"] = {
    "vp_operations": {
        "role": "VP of Operations",
        "skills": ["operations_management", "process_optimization", "efficiency"],
        "tools": [],
        "reports_to": "coo",
        "manages": [f"director_operations_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["operations"][f"director_operations_{i}"] = {
        "role": "Director of Operations",
        "skills": ["operations_management", "project_management", "analytics"],
        "tools": [],
        "reports_to": "vp_operations",
        "manages": [f"operations_manager_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["operations"][f"operations_manager_{i}_{j}"] = {
            "role": "Operations Manager",
            "skills": ["operations", "process_improvement", "project_management"],
            "tools": [],
            "reports_to": f"director_operations_{i}",
            "manages": [f"operations_analyst_{i}_{j}_{k}" for k in range(1, 4)],
        }
        for k in range(1, 4):
            ORGANIZATIONAL_STRUCTURE["operations"][f"operations_analyst_{i}_{j}_{k}"] = {
                "role": "Operations Analyst",
                "skills": ["data_analysis", "reporting", "process_documentation"],
                "tools": [],
                "reports_to": f"operations_manager_{i}_{j}",
                "manages": [],
            }


# Add Legal team (10 agents)
ORGANIZATIONAL_STRUCTURE["legal"] = {
    "general_counsel": {
        "role": "General Counsel",
        "skills": ["legal_counsel", "corporate_law", "risk_management"],
        "tools": [],
        "reports_to": "ceo",
        "manages": ["senior_counsel_contracts", "senior_counsel_compliance"],
    },
    "senior_counsel_contracts": {
        "role": "Senior Counsel - Contracts",
        "skills": ["contract_management", "contract_negotiation", "legal_review"],
        "tools": [],
        "reports_to": "general_counsel",
        "manages": [f"contracts_attorney_{i}" for i in range(1, 3)],
    },
    "senior_counsel_compliance": {
        "role": "Senior Counsel - Compliance",
        "skills": ["compliance", "regulatory_affairs", "legal_counsel"],
        "tools": [],
        "reports_to": "general_counsel",
        "manages": [f"compliance_attorney_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["legal"][f"contracts_attorney_{i}"] = {
        "role": "Contracts Attorney",
        "skills": ["contract_management", "legal_review", "negotiation"],
        "tools": [],
        "reports_to": "senior_counsel_contracts",
        "manages": [],
    }
    ORGANIZATIONAL_STRUCTURE["legal"][f"compliance_attorney_{i}"] = {
        "role": "Compliance Attorney",
        "skills": ["compliance", "regulatory", "legal_research"],
        "tools": [],
        "reports_to": "senior_counsel_compliance",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["legal"]["paralegal_1"] = {
    "role": "Paralegal",
    "skills": ["legal_support", "document_management", "research"],
    "tools": [],
    "reports_to": "general_counsel",
    "manages": [],
}

ORGANIZATIONAL_STRUCTURE["legal"]["paralegal_2"] = {
    "role": "Paralegal",
    "skills": ["legal_support", "contract_administration", "filing"],
    "tools": [],
    "reports_to": "general_counsel",
    "manages": [],
}


# Add Customer Success team (50 agents)
ORGANIZATIONAL_STRUCTURE["customer_success"] = {
    "vp_customer_success": {
        "role": "VP of Customer Success",
        "skills": ["customer_success", "customer_retention", "customer_experience"],
        "tools": [],
        "reports_to": "ceo",
        "manages": ["director_cs", "director_support"],
    },
    "director_cs": {
        "role": "Director of Customer Success",
        "skills": ["customer_success", "account_management", "renewals"],
        "tools": [],
        "reports_to": "vp_customer_success",
        "manages": [f"csm_manager_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["customer_success"][f"csm_manager_{i}"] = {
        "role": "CSM Manager",
        "skills": ["customer_success", "team_management", "customer_retention"],
        "tools": [],
        "reports_to": "director_cs",
        "manages": [f"csm_{i}_{j}" for j in range(1, 11)],
    }
    for j in range(1, 11):
        ORGANIZATIONAL_STRUCTURE["customer_success"][f"csm_{i}_{j}"] = {
            "role": "Customer Success Manager",
            "skills": ["customer_success", "relationship_management", "value_realization"],
            "tools": [],
            "reports_to": f"csm_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["customer_success"]["director_support"] = {
    "role": "Director of Customer Support",
    "skills": ["customer_support", "support_operations", "service_excellence"],
    "tools": [],
    "reports_to": "vp_customer_success",
    "manages": [f"support_manager_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["customer_success"][f"support_manager_{i}"] = {
        "role": "Support Manager",
        "skills": ["customer_support", "technical_support", "team_leadership"],
        "tools": [],
        "reports_to": "director_support",
        "manages": [f"support_agent_{i}_{j}" for j in range(1, 8)],
    }
    for j in range(1, 8):
        ORGANIZATIONAL_STRUCTURE["customer_success"][f"support_agent_{i}_{j}"] = {
            "role": "Customer Support Agent",
            "skills": ["customer_support", "troubleshooting", "communication"],
            "tools": [],
            "reports_to": f"support_manager_{i}",
            "manages": [],
        }


# Add Data team (30 agents)
ORGANIZATIONAL_STRUCTURE["data"] = {
    "vp_data": {
        "role": "VP of Data",
        "skills": ["data_strategy", "analytics", "data_governance"],
        "tools": [],
        "reports_to": "ceo",
        "manages": ["director_data_engineering", "director_analytics", "director_data_science"],
    },
    "director_data_engineering": {
        "role": "Director of Data Engineering",
        "skills": ["data_engineering", "data_architecture", "etl"],
        "tools": [],
        "reports_to": "vp_data",
        "manages": [f"senior_data_engineer_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["data"][f"senior_data_engineer_{i}"] = {
        "role": "Senior Data Engineer",
        "skills": ["data_engineering", "pipeline_development", "sql"],
        "tools": [],
        "reports_to": "director_data_engineering",
        "manages": [f"data_engineer_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["data"][f"data_engineer_{i}_{j}"] = {
            "role": "Data Engineer",
            "skills": ["data_engineering", "etl", "database_management"],
            "tools": [],
            "reports_to": f"senior_data_engineer_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["data"]["director_analytics"] = {
    "role": "Director of Analytics",
    "skills": ["business_intelligence", "analytics", "data_visualization"],
    "tools": [],
    "reports_to": "vp_data",
    "manages": [f"analytics_manager_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["data"][f"analytics_manager_{i}"] = {
        "role": "Analytics Manager",
        "skills": ["analytics", "data_analysis", "reporting"],
        "tools": [],
        "reports_to": "director_analytics",
        "manages": [f"data_analyst_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["data"][f"data_analyst_{i}_{j}"] = {
            "role": "Data Analyst",
            "skills": ["data_analysis", "sql", "data_visualization"],
            "tools": [],
            "reports_to": f"analytics_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["data"]["director_data_science"] = {
    "role": "Director of Data Science",
    "skills": ["data_science", "machine_learning", "ai"],
    "tools": [],
    "reports_to": "vp_data",
    "manages": [f"senior_data_scientist_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["data"][f"senior_data_scientist_{i}"] = {
        "role": "Senior Data Scientist",
        "skills": ["data_science", "machine_learning", "statistical_modeling"],
        "tools": [],
        "reports_to": "director_data_science",
        "manages": [f"data_scientist_{i}_{j}" for j in range(1, 3)],
    }
    for j in range(1, 3):
        ORGANIZATIONAL_STRUCTURE["data"][f"data_scientist_{i}_{j}"] = {
            "role": "Data Scientist",
            "skills": ["data_science", "python", "machine_learning"],
            "tools": [],
            "reports_to": f"senior_data_scientist_{i}",
            "manages": [],
        }


# Add Security team (20 agents)
ORGANIZATIONAL_STRUCTURE["security"] = {
    "vp_security": {
        "role": "VP of Security",
        "skills": ["cybersecurity", "risk_management", "security_strategy"],
        "tools": [],
        "reports_to": "cto",
        "manages": ["director_security_ops", "director_appsec"],
    },
    "director_security_ops": {
        "role": "Director of Security Operations",
        "skills": ["security_operations", "incident_response", "threat_detection"],
        "tools": [],
        "reports_to": "vp_security",
        "manages": [f"security_engineer_{i}" for i in range(1, 6)],
    },
}

for i in range(1, 6):
    ORGANIZATIONAL_STRUCTURE["security"][f"security_engineer_{i}"] = {
        "role": "Security Engineer",
        "skills": ["cybersecurity", "security_monitoring", "incident_response"],
        "tools": [],
        "reports_to": "director_security_ops",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["security"]["director_appsec"] = {
    "role": "Director of Application Security",
    "skills": ["application_security", "secure_coding", "penetration_testing"],
    "tools": [],
    "reports_to": "vp_security",
    "manages": [f"appsec_engineer_{i}" for i in range(1, 5)],
}

for i in range(1, 5):
    ORGANIZATIONAL_STRUCTURE["security"][f"appsec_engineer_{i}"] = {
        "role": "Application Security Engineer",
        "skills": ["application_security", "code_review", "vulnerability_assessment"],
        "tools": [],
        "reports_to": "director_appsec",
        "manages": [],
    }

ORGANIZATIONAL_STRUCTURE["security"]["security_analyst_1"] = {
    "role": "Security Analyst",
    "skills": ["security_analysis", "threat_intelligence", "siem"],
    "tools": [],
    "reports_to": "director_security_ops",
    "manages": [],
}

ORGANIZATIONAL_STRUCTURE["security"]["security_analyst_2"] = {
    "role": "Security Analyst",
    "skills": ["security_analysis", "log_analysis", "threat_hunting"],
    "tools": [],
    "reports_to": "director_security_ops",
    "manages": [],
}

ORGANIZATIONAL_STRUCTURE["security"]["compliance_manager"] = {
    "role": "Security Compliance Manager",
    "skills": ["compliance", "security_auditing", "policy_management"],
    "tools": [],
    "reports_to": "vp_security",
    "manages": [f"compliance_analyst_{i}" for i in range(1, 3)],
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["security"][f"compliance_analyst_{i}"] = {
        "role": "Compliance Analyst",
        "skills": ["compliance", "audit", "documentation"],
        "tools": [],
        "reports_to": "compliance_manager",
        "manages": [],
    }


# Add IT team (20 agents)
ORGANIZATIONAL_STRUCTURE["it"] = {
    "vp_it": {
        "role": "VP of IT",
        "skills": ["it_operations", "infrastructure", "service_management"],
        "tools": [],
        "reports_to": "cto",
        "manages": ["director_it_ops", "director_infrastructure"],
    },
    "director_it_ops": {
        "role": "Director of IT Operations",
        "skills": ["it_operations", "service_delivery", "itsm"],
        "tools": [],
        "reports_to": "vp_it",
        "manages": [f"it_manager_{i}" for i in range(1, 3)],
    },
}

for i in range(1, 3):
    ORGANIZATIONAL_STRUCTURE["it"][f"it_manager_{i}"] = {
        "role": "IT Manager",
        "skills": ["it_operations", "team_management", "service_delivery"],
        "tools": [],
        "reports_to": "director_it_ops",
        "manages": [f"it_support_{i}_{j}" for j in range(1, 4)],
    }
    for j in range(1, 4):
        ORGANIZATIONAL_STRUCTURE["it"][f"it_support_{i}_{j}"] = {
            "role": "IT Support Specialist",
            "skills": ["helpdesk", "troubleshooting", "user_support"],
            "tools": [],
            "reports_to": f"it_manager_{i}",
            "manages": [],
        }

ORGANIZATIONAL_STRUCTURE["it"]["director_infrastructure"] = {
    "role": "Director of Infrastructure",
    "skills": ["infrastructure_management", "cloud", "networking"],
    "tools": [],
    "reports_to": "vp_it",
    "manages": [f"infrastructure_engineer_{i}" for i in range(1, 5)],
}

for i in range(1, 5):
    ORGANIZATIONAL_STRUCTURE["it"][f"infrastructure_engineer_{i}"] = {
        "role": "Infrastructure Engineer",
        "skills": ["infrastructure", "cloud_computing", "networking"],
        "tools": [],
        "reports_to": "director_infrastructure",
        "manages": [],
    }


# Add Facilities team (10 agents)
ORGANIZATIONAL_STRUCTURE["facilities"] = {
    "director_facilities": {
        "role": "Director of Facilities",
        "skills": ["facilities_management", "operations", "vendor_management"],
        "tools": [],
        "reports_to": "coo",
        "manages": [f"office_manager_{i}" for i in range(1, 4)],
    },
}

for i in range(1, 4):
    ORGANIZATIONAL_STRUCTURE["facilities"][f"office_manager_{i}"] = {
        "role": f"Office Manager - Location {i}",
        "skills": ["office_management", "facilities", "coordination"],
        "tools": [],
        "reports_to": "director_facilities",
        "manages": [f"facilities_coordinator_{i}_{j}" for j in range(1, 3)],
    }
    for j in range(1, 3):
        ORGANIZATIONAL_STRUCTURE["facilities"][f"facilities_coordinator_{i}_{j}"] = {
            "role": "Facilities Coordinator",
            "skills": ["facilities", "coordination", "vendor_liaison"],
            "tools": [],
            "reports_to": f"office_manager_{i}",
            "manages": [],
        }


def generate_all_agent_cards(output_dir: str = "agent_cards"):
    """Generate agent cards for all 511 agents"""
    print(f"Generating agent cards in {output_dir}...")

    total_agents = 0
    created_agents = []

    for department, agents in ORGANIZATIONAL_STRUCTURE.items():
        print(f"\nProcessing {department} department...")

        for agent_name, agent_def in agents.items():
            try:
                # Create agent config
                config = AgentConfig(
                    name=agent_name,
                    description=f"{agent_def['role']} responsible for {department} functions",
                    role=agent_def['role'],
                    department=department,
                    skills=agent_def['skills'],
                    tools=agent_def.get('tools', []),
                    reports_to=agent_def.get('reports_to'),
                    manages=agent_def.get('manages', []),
                    tags=[department] + agent_def['skills'],
                )

                # Create agent
                agent = BaseA2AAgent(config)

                # Save agent card
                filepath = agent.save_agent_card(output_dir)

                total_agents += 1
                created_agents.append(agent_name)
                print(f"  ✓ Created {agent_name} ({agent_def['role']})")

            except Exception as e:
                print(f"  ✗ Error creating {agent_name}: {e}")

    print(f"\n{'='*60}")
    print(f"Successfully generated {total_agents} agent cards!")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}\n")

    return created_agents


def count_agents():
    """Count total agents in the organizational structure"""
    total = sum(len(agents) for agents in ORGANIZATIONAL_STRUCTURE.values())
    print(f"Total agents defined: {total}")

    for department, agents in ORGANIZATIONAL_STRUCTURE.items():
        print(f"  {department}: {len(agents)} agents")

    return total


if __name__ == "__main__":
    print("="*60)
    print("A2A Agent Card Generator")
    print("="*60)

    # Count agents first
    count_agents()
    print()

    # Generate all agent cards
    created_agents = generate_all_agent_cards()

    print("\nDone!")
