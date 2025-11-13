#!/usr/bin/env python3
"""
COMPLETE AUTONOMOUS AGENT GENERATION SYSTEM
Generates all 50 industry-specific AI agents with full specifications
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class IndustryAgentGenerator:
    """Complete agent generation system for all 50 industry agents"""

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path(__file__).parent.parent / "outputs"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.agents = []
        self.validation_report = {
            "total_generated": 0,
            "validation_passed": 0,
            "validation_failed": 0,
            "errors": []
        }

    def get_tier_2_template(self, number: int, id_suffix: str, name: str, naics: str,
                            category: str, market_data: Dict) -> Dict:
        """Generate Tier 2 agent from template"""
        return {
            "id": f"agent_{number:03d}_{id_suffix}",
            "number": number,
            "tier": 2,
            "name": name,
            "naics": naics,
            "category": category,
            "system_prompt": f"""You are a {name.lower()} operations specialist.

Your expertise includes optimizing business operations, technology systems, compliance requirements,
and growth strategies for {category.lower()} businesses.

When analyzing operations, focus on:
1. Operational efficiency and productivity
2. Technology adoption and integration
3. Customer/client satisfaction and retention
4. Regulatory compliance
5. Revenue optimization and cost control

Provide specific, actionable recommendations tailored to the industry's unique challenges.""",
            "expertise_areas": [
                "Operations management",
                "Technology systems",
                "Compliance & regulations",
                "Customer management",
                "Financial optimization",
                "Staff management",
                "Industry-specific workflows",
                "Performance analytics"
            ],
            "smb_profile": {
                "employee_range": "5-100",
                "revenue_range": "$500K-$10M+",
                "types": ["Independent", "Small chains", "Franchises"],
                "locations": "1-5",
                "staff_mix": "Mixed operational and administrative"
            },
            "control_points": {
                "primary": "Industry-specific management system",
                "secondary": "CRM/Customer management",
                "tertiary": "Accounting/Finance"
            },
            "expansion_products": [
                "Customer communication platform",
                "Staff scheduling & management",
                "Analytics & reporting",
                "Mobile apps",
                "Payment processing",
                "Marketing automation"
            ],
            "regulatory_compliance": [
                "Industry-specific regulations",
                "Employment law",
                "Data privacy",
                "Safety requirements",
                "Licensing requirements"
            ],
            "pain_points": [
                "Manual process inefficiencies",
                "Customer retention challenges",
                "Staff productivity gaps",
                "Technology fragmentation",
                "Compliance tracking difficulties"
            ],
            "success_metrics": [
                "Improve operational efficiency 20-30%",
                "Increase customer retention 15-25%",
                "Reduce manual work 40-50%",
                "Improve compliance adherence to 100%",
                "Increase revenue per customer 15-30%"
            ],
            "market_data": market_data
        }

    def get_tier_3_template(self, number: int, id_suffix: str, name: str, naics: str,
                            category: str, market_data: Dict) -> Dict:
        """Generate Tier 3 agent from template"""
        return {
            "id": f"agent_{number:03d}_{id_suffix}",
            "number": number,
            "tier": 3,
            "name": name,
            "naics": naics,
            "category": category,
            "system_prompt": f"""You are a {name.lower()} operations specialist for emerging and specialized industries.

Your expertise focuses on:
- Modern technology adoption and digital transformation
- Industry-specific operational challenges
- Regulatory compliance and risk management
- Growth strategies and market positioning
- Customer/client acquisition and retention

Provide forward-thinking, innovation-focused recommendations while maintaining
operational excellence and compliance.""",
            "expertise_areas": [
                "Digital transformation",
                "Operations optimization",
                "Compliance management",
                "Growth strategies",
                "Technology integration",
                "Risk management",
                "Industry best practices",
                "Performance metrics"
            ],
            "smb_profile": {
                "employee_range": "5-50",
                "revenue_range": "$500K-$5M+",
                "types": ["Specialized providers", "Emerging businesses"],
                "locations": "1-3",
                "staff_mix": "Specialized and administrative"
            },
            "control_points": {
                "primary": "Specialized management platform",
                "secondary": "Customer/project management",
                "tertiary": "Financial systems"
            },
            "expansion_products": [
                "Industry-specific tools",
                "Analytics platforms",
                "Communication systems",
                "Automation tools",
                "Compliance tracking",
                "Customer portals"
            ],
            "regulatory_compliance": [
                "Industry regulations",
                "Data protection",
                "Safety standards",
                "Professional licensing",
                "Insurance requirements"
            ],
            "pain_points": [
                "Technology adoption challenges",
                "Market differentiation",
                "Operational scalability",
                "Compliance complexity",
                "Resource constraints"
            ],
            "success_metrics": [
                "Accelerate digital adoption 30-50%",
                "Improve operational efficiency 25-40%",
                "Increase market share 20-30%",
                "Enhance compliance 100%",
                "Reduce operational costs 15-25%"
            ],
            "market_data": market_data
        }

    def generate_tier_2_agents(self) -> List[Dict]:
        """Generate all 22 Tier 2 agents"""
        tier_2_specs = [
            (13, "home_services", "Home Services & Contracting", "238", "Construction/Services",
             {"total_us_companies": 300000, "addressable": 250000, "current_saas_adoption": 0.25, "growth_cagr": 0.09, "market_size_b": 12, "growth_descriptor": "HVAC, plumbing, electrical"}),

            (14, "veterinary", "Veterinary Practice Management", "541940", "Professional Services",
             {"total_us_companies": 30000, "addressable": 28000, "current_saas_adoption": 0.40, "growth_cagr": 0.10, "market_size_b": 5, "growth_descriptor": "Pet care SaaS growing"}),

            (15, "landscaping", "Lawn & Landscape Services", "561730", "Services",
             {"total_us_companies": 80000, "addressable": 70000, "current_saas_adoption": 0.20, "growth_cagr": 0.08, "market_size_b": 8, "growth_descriptor": "Field service opportunities"}),

            (16, "beauty_spa", "Beauty & Personal Care (Salons/Spas)", "812112", "Personal Services",
             {"total_us_companies": 70000, "addressable": 65000, "current_saas_adoption": 0.35, "growth_cagr": 0.09, "market_size_b": 6, "growth_descriptor": "Appointment-based services"}),

            (17, "fitness", "Fitness & Recreation (Gyms/Wellness)", "713940", "Recreation",
             {"total_us_companies": 35000, "addressable": 32000, "current_saas_adoption": 0.40, "growth_cagr": 0.11, "market_size_b": 7, "growth_descriptor": "Membership & class mgmt"}),

            (18, "event_planning", "Event Planning & Catering", "561920", "Services",
             {"total_us_companies": 25000, "addressable": 22000, "current_saas_adoption": 0.30, "growth_cagr": 0.10, "market_size_b": 4, "growth_descriptor": "Project-based services"}),

            (19, "nonprofit", "Nonprofit Organization Management", "813", "Nonprofit",
             {"total_us_companies": 1200000, "addressable": 100000, "current_saas_adoption": 0.25, "growth_cagr": 0.12, "market_size_b": 15, "growth_descriptor": "Donor & program mgmt"}),

            (20, "accounting", "Accounting & Bookkeeping Services", "541211", "Professional Services",
             {"total_us_companies": 50000, "addressable": 45000, "current_saas_adoption": 0.55, "growth_cagr": 0.09, "market_size_b": 10, "growth_descriptor": "High SaaS adoption"}),

            (21, "insurance_agency", "Insurance Agency Operations", "524210", "Insurance",
             {"total_us_companies": 40000, "addressable": 35000, "current_saas_adoption": 0.40, "growth_cagr": 0.08, "market_size_b": 8, "growth_descriptor": "Independent agencies"}),

            (22, "property_leasing", "Residential/Commercial Leasing", "531110", "Real Estate",
             {"total_us_companies": 60000, "addressable": 55000, "current_saas_adoption": 0.50, "growth_cagr": 0.10, "market_size_b": 12, "growth_descriptor": "Property management"}),

            (23, "pest_control", "Pest Control Operations", "561710", "Services",
             {"total_us_companies": 20000, "addressable": 18000, "current_saas_adoption": 0.35, "growth_cagr": 0.09, "market_size_b": 3, "growth_descriptor": "Route-based services"}),

            (24, "medical_supplies", "Medical & Dental Supplies Distribution", "423450", "Distribution",
             {"total_us_companies": 15000, "addressable": 13000, "current_saas_adoption": 0.45, "growth_cagr": 0.10, "market_size_b": 5, "growth_descriptor": "B2B distribution"}),

            (25, "cleaning_services", "Commercial & Residential Cleaning", "561720", "Services",
             {"total_us_companies": 90000, "addressable": 80000, "current_saas_adoption": 0.30, "growth_cagr": 0.09, "market_size_b": 9, "growth_descriptor": "Field service mgmt"}),

            (26, "childcare", "Childcare & Daycare Centers", "624410", "Social Services",
             {"total_us_companies": 50000, "addressable": 45000, "current_saas_adoption": 0.35, "growth_cagr": 0.08, "market_size_b": 6, "growth_descriptor": "Parent communication"}),

            (27, "security_services", "Security & Guard Services", "561612", "Services",
             {"total_us_companies": 12000, "addressable": 10000, "current_saas_adoption": 0.40, "growth_cagr": 0.09, "market_size_b": 4, "growth_descriptor": "Scheduling & dispatch"}),

            (28, "printing", "Printing & Publishing Services", "323", "Manufacturing/Services",
             {"total_us_companies": 25000, "addressable": 20000, "current_saas_adoption": 0.35, "growth_cagr": 0.06, "market_size_b": 3, "growth_descriptor": "Order & production mgmt"}),

            (29, "moving_storage", "Moving & Storage Services", "484210", "Transportation",
             {"total_us_companies": 18000, "addressable": 15000, "current_saas_adoption": 0.30, "growth_cagr": 0.08, "market_size_b": 4, "growth_descriptor": "Logistics operations"}),

            (30, "wholesale", "Wholesale & Distribution", "42", "Wholesale",
             {"total_us_companies": 400000, "addressable": 80000, "current_saas_adoption": 0.30, "growth_cagr": 0.08, "market_size_b": 18, "growth_descriptor": "B2B operations"}),

            (31, "hotels_lodging", "Hotels & Lodging Operations", "721", "Hospitality",
             {"total_us_companies": 55000, "addressable": 50000, "current_saas_adoption": 0.50, "growth_cagr": 0.10, "market_size_b": 14, "growth_descriptor": "Property management"}),

            (32, "auto_sales", "Automotive Sales & Dealerships", "441", "Retail",
             {"total_us_companies": 18000, "addressable": 16000, "current_saas_adoption": 0.60, "growth_cagr": 0.07, "market_size_b": 9, "growth_descriptor": "DMS systems"}),

            (33, "marketing_agency", "Marketing & Advertising Agencies", "541810", "Professional Services",
             {"total_us_companies": 35000, "addressable": 30000, "current_saas_adoption": 0.50, "growth_cagr": 0.11, "market_size_b": 8, "growth_descriptor": "Project & client mgmt"}),

            (34, "architecture", "Architecture & Engineering Services", "541310", "Professional Services",
             {"total_us_companies": 25000, "addressable": 22000, "current_saas_adoption": 0.45, "growth_cagr": 0.09, "market_size_b": 6, "growth_descriptor": "Project management"})
        ]

        return [self.get_tier_2_template(*spec) for spec in tier_2_specs]

    def generate_tier_3_agents(self) -> List[Dict]:
        """Generate all 16 Tier 3 agents"""
        tier_3_specs = [
            (35, "renewable_energy", "Renewable Energy Services", "221114", "Utilities",
             {"total_us_companies": 10000, "addressable": 8000, "current_saas_adoption": 0.20, "growth_cagr": 0.15, "market_size_b": 8, "growth_descriptor": "Emerging market"}),

            (36, "telecom", "Telecommunications Operations", "517", "Telecom",
             {"total_us_companies": 5000, "addressable": 4000, "current_saas_adoption": 0.50, "growth_cagr": 0.07, "market_size_b": 12, "growth_descriptor": "Service providers"}),

            (37, "cannabis", "Cannabis Retail & Distribution", "453", "Retail",
             {"total_us_companies": 8000, "addressable": 7000, "current_saas_adoption": 0.35, "growth_cagr": 0.25, "market_size_b": 3, "growth_descriptor": "Regulated emerging"}),

            (38, "funeral_services", "Funeral & Mortuary Services", "812210", "Personal Services",
             {"total_us_companies": 20000, "addressable": 18000, "current_saas_adoption": 0.25, "growth_cagr": 0.05, "market_size_b": 2, "growth_descriptor": "Traditional industry"}),

            (39, "equipment_rental", "Equipment Rental & Leasing", "532", "Rental Services",
             {"total_us_companies": 15000, "addressable": 12000, "current_saas_adoption": 0.40, "growth_cagr": 0.09, "market_size_b": 5, "growth_descriptor": "Asset management"}),

            (40, "environmental", "Environmental Services & Waste Mgmt", "562", "Services",
             {"total_us_companies": 18000, "addressable": 15000, "current_saas_adoption": 0.30, "growth_cagr": 0.08, "market_size_b": 6, "growth_descriptor": "Route & compliance"}),

            (41, "testing_labs", "Testing & Laboratory Services", "541380", "Professional Services",
             {"total_us_companies": 8000, "addressable": 7000, "current_saas_adoption": 0.45, "growth_cagr": 0.10, "market_size_b": 4, "growth_descriptor": "Sample tracking"}),

            (42, "locksmith", "Locksmith & Security Installation", "561622", "Services",
             {"total_us_companies": 12000, "addressable": 10000, "current_saas_adoption": 0.20, "growth_cagr": 0.07, "market_size_b": 2, "growth_descriptor": "Field service"}),

            (43, "pool_service", "Pool Service & Maintenance", "561790", "Services",
             {"total_us_companies": 15000, "addressable": 13000, "current_saas_adoption": 0.25, "growth_cagr": 0.08, "market_size_b": 3, "growth_descriptor": "Route services"}),

            (44, "electrical_contracting", "Electrical Contracting", "238210", "Construction",
             {"total_us_companies": 80000, "addressable": 60000, "current_saas_adoption": 0.25, "growth_cagr": 0.09, "market_size_b": 7, "growth_descriptor": "Project-based"}),

            (45, "plumbing", "Plumbing Services", "238220", "Construction",
             {"total_us_companies": 120000, "addressable": 90000, "current_saas_adoption": 0.20, "growth_cagr": 0.08, "market_size_b": 9, "growth_descriptor": "Service & installation"}),

            (46, "hvac", "HVAC Services", "238220", "Construction",
             {"total_us_companies": 100000, "addressable": 80000, "current_saas_adoption": 0.30, "growth_cagr": 0.09, "market_size_b": 10, "growth_descriptor": "Maintenance contracts"}),

            (47, "appliance_repair", "Appliance Repair Services", "811412", "Repair Services",
             {"total_us_companies": 25000, "addressable": 20000, "current_saas_adoption": 0.25, "growth_cagr": 0.06, "market_size_b": 3, "growth_descriptor": "Service calls"}),

            (48, "tree_services", "Tree Service & Arborist", "561730", "Services",
             {"total_us_companies": 28000, "addressable": 24000, "current_saas_adoption": 0.20, "growth_cagr": 0.08, "market_size_b": 4, "growth_descriptor": "Project & route"}),

            (49, "flooring", "Flooring Installation & Sales", "238330", "Construction",
             {"total_us_companies": 30000, "addressable": 25000, "current_saas_adoption": 0.25, "growth_cagr": 0.08, "market_size_b": 4, "growth_descriptor": "Project management"}),

            (50, "roofing", "Roofing Services", "238160", "Construction",
             {"total_us_companies": 80000, "addressable": 65000, "current_saas_adoption": 0.25, "growth_cagr": 0.09, "market_size_b": 8, "growth_descriptor": "Project-based"})
        ]

        return [self.get_tier_3_template(*spec) for spec in tier_3_specs]

    def validate_agent(self, agent: Dict) -> Tuple[bool, str]:
        """Validate agent has all required fields"""
        required_fields = [
            "id", "number", "tier", "name", "naics", "system_prompt",
            "expertise_areas", "smb_profile", "control_points",
            "expansion_products", "regulatory_compliance", "pain_points",
            "success_metrics", "market_data"
        ]

        for field in required_fields:
            if field not in agent:
                return False, f"Missing field: {field}"
            if agent[field] is None or agent[field] == "":
                return False, f"Empty field: {field}"

        return True, "Valid"

    def generate_all_agents(self):
        """Generate all 50 agents"""
        print("\n" + "="*80)
        print("GENERATING ALL 50 INDUSTRY AGENTS")
        print("="*80 + "\n")

        # Load Tier 1 agents from the main file
        from generate_agents import TIER_1_AGENTS

        print("[TIER 1] Generating 12 core control-point agents...")
        for agent in TIER_1_AGENTS:
            is_valid, msg = self.validate_agent(agent)
            if is_valid:
                self.agents.append(agent)
                self.validation_report["validation_passed"] += 1
                print(f"  ✓ Agent #{agent['number']:02d}: {agent['name']}")
            else:
                self.validation_report["validation_failed"] += 1
                self.validation_report["errors"].append({
                    "agent": agent.get("name", "Unknown"),
                    "error": msg
                })
                print(f"  ✗ Agent #{agent['number']:02d}: {msg}")

        print(f"\n[TIER 2] Generating 22 expansion agents...")
        tier_2_agents = self.generate_tier_2_agents()
        for agent in tier_2_agents:
            is_valid, msg = self.validate_agent(agent)
            if is_valid:
                self.agents.append(agent)
                self.validation_report["validation_passed"] += 1
                print(f"  ✓ Agent #{agent['number']:02d}: {agent['name']}")
            else:
                self.validation_report["validation_failed"] += 1
                self.validation_report["errors"].append({
                    "agent": agent.get("name", "Unknown"),
                    "error": msg
                })
                print(f"  ✗ Agent #{agent['number']:02d}: {msg}")

        print(f"\n[TIER 3] Generating 16 specialized agents...")
        tier_3_agents = self.generate_tier_3_agents()
        for agent in tier_3_agents:
            is_valid, msg = self.validate_agent(agent)
            if is_valid:
                self.agents.append(agent)
                self.validation_report["validation_passed"] += 1
                print(f"  ✓ Agent #{agent['number']:02d}: {agent['name']}")
            else:
                self.validation_report["validation_failed"] += 1
                self.validation_report["errors"].append({
                    "agent": agent.get("name", "Unknown"),
                    "error": msg
                })
                print(f"  ✗ Agent #{agent['number']:02d}: {msg}")

        self.validation_report["total_generated"] = len(self.agents)

        print("\n" + "="*80)
        print(f"GENERATION COMPLETE: {len(self.agents)} agents generated")
        print("="*80 + "\n")

        return self.agents

    def export_agents(self):
        """Export agents to JSON files"""
        print("\n[EXPORT] Creating output files...\n")

        # Create master registry
        master_registry = {
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "total_agents": len(self.agents),
            "agents_by_tier": {
                "tier_1": len([a for a in self.agents if a["tier"] == 1]),
                "tier_2": len([a for a in self.agents if a["tier"] == 2]),
                "tier_3": len([a for a in self.agents if a["tier"] == 3])
            },
            "agents": self.agents
        }

        registry_path = self.output_dir / "agent_registry_complete.json"
        with open(registry_path, 'w') as f:
            json.dump(master_registry, f, indent=2)
        print(f"✓ Master registry: {registry_path}")

        # Create NAICS lookup
        naics_lookup = {}
        for agent in self.agents:
            naics_code = agent['naics']
            naics_lookup[naics_code] = {
                "agent_id": agent['id'],
                "agent_name": agent['name'],
                "agent_number": agent['number'],
                "tier": agent['tier'],
                "category": agent['category']
            }

        naics_path = self.output_dir / "naics_lookup_table.json"
        with open(naics_path, 'w') as f:
            json.dump(naics_lookup, f, indent=2)
        print(f"✓ NAICS lookup table: {naics_path}")

        # Create agent by tier
        for tier in [1, 2, 3]:
            tier_agents = [a for a in self.agents if a["tier"] == tier]
            tier_path = self.output_dir / f"tier_{tier}_agents.json"
            with open(tier_path, 'w') as f:
                json.dump({"tier": tier, "count": len(tier_agents), "agents": tier_agents}, f, indent=2)
            print(f"✓ Tier {tier} agents: {tier_path} ({len(tier_agents)} agents)")

        # Create summary report
        report = {
            "execution_status": "SUCCESS",
            "timestamp": datetime.now().isoformat(),
            "summary": self.validation_report,
            "agents_by_tier": master_registry["agents_by_tier"],
            "total_naics_codes": len(naics_lookup),
            "output_files": {
                "master_registry": str(registry_path),
                "naics_lookup": str(naics_path),
                "tier_files": [
                    str(self.output_dir / f"tier_{tier}_agents.json")
                    for tier in [1, 2, 3]
                ]
            }
        }

        report_path = self.output_dir / "generation_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✓ Generation report: {report_path}")

        return report

def main():
    """Main execution function"""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         AUTONOMOUS INDUSTRY AGENT GENERATION SYSTEM                        ║
║         Complete 50-Agent System                                           ║
║                                                                            ║
║         Start Time: {}                                           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Initialize generator
    generator = IndustryAgentGenerator()

    # Generate all agents
    agents = generator.generate_all_agents()

    # Export results
    report = generator.export_agents()

    # Print final summary
    print("\n" + "="*80)
    print("EXECUTION SUMMARY")
    print("="*80)
    print(f"\n✓ Total agents generated: {report['summary']['total_generated']}")
    print(f"  - Tier 1 (Core): {report['agents_by_tier']['tier_1']}")
    print(f"  - Tier 2 (Expansion): {report['agents_by_tier']['tier_2']}")
    print(f"  - Tier 3 (Specialized): {report['agents_by_tier']['tier_3']}")
    print(f"\n✓ Validation passed: {report['summary']['validation_passed']}")
    print(f"✓ Validation failed: {report['summary']['validation_failed']}")
    print(f"✓ NAICS codes mapped: {report['total_naics_codes']}")
    print(f"\n✓ All files exported to: {generator.output_dir}")

    if report['summary']['validation_failed'] > 0:
        print("\n⚠ Errors encountered:")
        for error in report['summary']['errors']:
            print(f"  - {error['agent']}: {error['error']}")

    print("\n" + "="*80)
    print("SYSTEM READY FOR DEPLOYMENT")
    print("="*80 + "\n")

    return report

if __name__ == "__main__":
    main()
