import frappe

THESES = [
    {
        'thesis_name': 'Agency Technical Reinforcement',
        'description': (
            'Cartertek supports agencies that need senior engineering help, '
            'implementation depth, or overflow capacity without repositioning as '
            'staff augmentation.'
        ),
        'default_offer': 'Technical reinforcement for scoped delivery work',
        'typical_prospect_types': 'Agency, Ecosystem Partner, Referral Partner',
        'typical_contact_roles': 'Agency owner, technical lead, operations lead, delivery lead',
    },
    {
        'thesis_name': 'Project Rescue',
        'description': (
            'Cartertek helps recover stalled, fragile, or half-finished software '
            'projects and moves them toward a usable delivery path.'
        ),
        'default_offer': 'Project rescue assessment and implementation plan',
        'typical_prospect_types': 'Startup, SMB, Enterprise, Directory Lead',
        'typical_contact_roles': 'Founder, owner, product lead, CTO, operations lead',
    },
    {
        'thesis_name': 'Post-Launch Stabilization',
        'description': (
            'Cartertek helps teams stabilize and improve software after a launch, '
            'migration, prototype, or public release exposes production issues.'
        ),
        'default_offer': 'Post-launch stabilization and cleanup',
        'typical_prospect_types': 'Startup, SMB, Enterprise',
        'typical_contact_roles': 'Founder, product lead, technical lead, operations lead',
    },
    {
        'thesis_name': 'Hiring-Gap Substitution',
        'description': (
            'Cartertek provides outcome-focused engineering execution when a team '
            'needs progress before a full-time hire is found.'
        ),
        'default_offer': 'Scoped engineering delivery while hiring remains open',
        'typical_prospect_types': 'Startup, SMB, Enterprise',
        'typical_contact_roles': 'Founder, CTO, hiring manager, operations lead',
    },
    {
        'thesis_name': 'Workflow Integration',
        'description': (
            'Cartertek connects disconnected tools, internal processes, and data '
            'flows so day-to-day work becomes simpler and more reliable.'
        ),
        'default_offer': 'Workflow integration build or audit',
        'typical_prospect_types': 'SMB, Enterprise, Agency, Procurement Lead',
        'typical_contact_roles': 'Owner, operations lead, department head, technical lead',
    },
    {
        'thesis_name': 'AI Workflow Implementation',
        'description': (
            'Cartertek builds practical AI capabilities into real workflows rather '
            'than isolated demos or novelty automations.'
        ),
        'default_offer': 'Practical AI workflow implementation',
        'typical_prospect_types': 'SMB, Enterprise, Startup, Agency',
        'typical_contact_roles': 'Owner, operations lead, product lead, technical lead',
    },
    {
        'thesis_name': 'Production-Readiness Cleanup',
        'description': (
            'Cartertek hardens prototypes, demo apps, and vibe-coded projects so '
            'they are maintainable, reliable, and ready for real users.'
        ),
        'default_offer': 'Production-readiness cleanup',
        'typical_prospect_types': 'Startup, SMB, Directory Lead, Community Lead',
        'typical_contact_roles': 'Founder, owner, product lead, technical lead',
    },
    {
        'thesis_name': 'Technical Diagnostic / Second Set of Eyes',
        'description': (
            'Cartertek gives buyers an expert technical review when they need '
            'clarity before deciding whether to fix, rebuild, or extend software.'
        ),
        'default_offer': 'Technical diagnostic / second set of eyes',
        'typical_prospect_types': 'SMB, Enterprise, Startup, Agency',
        'typical_contact_roles': 'Owner, founder, CTO, product lead, operations lead',
    },
]


def execute():
    for row in THESES:
        if frappe.db.exists('Thesis', row['thesis_name']):
            doc = frappe.get_doc('Thesis', row['thesis_name'])
            doc.update(row)
            doc.active = 1
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.get_doc({
                'doctype': 'Thesis',
                **row,
                'active': 1,
            })
            doc.insert(ignore_permissions=True)
