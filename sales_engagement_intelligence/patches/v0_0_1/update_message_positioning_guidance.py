# ruff: noqa: E501, I001
from __future__ import annotations

import frappe

EARLY_CAPACITY_MESSAGE_GUIDANCE = """Lead with the bounded technical or operational area affected.
Address the issue in the prospect's environment using natural second-person phrasing such as “your deployment process,” “your internal tooling,” or “your evaluation workflow.”
Preserve visible consequences such as outages, delays, manual work, fragmented systems, bottlenecks, or excessive operational noise.
Translate technical shorthand into clear language without losing specificity.
When several symptoms support the same constraint, introduce them conversationally before listing them, for example: “A few things stood out.”
Do not make broad claims about the company's technical competence, staffing level, or engineering organization, and do not turn one specific constraint into a claim that the entire company lacks technical capacity.
Connect Cartertek to a bounded outcome such as automation, integration, stabilization, internal tooling, or a focused implementation sprint.
Keep the wording natural enough that it does not sound copied from the source artifact."""

FAILED_HIRING_MESSAGE_GUIDANCE = """Identify the source accurately as an open job posting or other hiring artifact.
Frame it as the reason Cartertek reached out, not as proof that recruitment has failed.
Use natural outsider-to-insider language, such as: “I came across a [company] job posting that mentioned you were having some problems with [area].”
Do not sound like a recruiter or imply that the company should abandon its permanent search.
Position Cartertek as a way to make progress while hiring continues, and connect the role to a bounded piece of work Cartertek could advance now.
Avoid celebrating or overstating hiring friction.
When the source mentions several relevant problems, move them into a second sentence and introduce them conversationally, for example: “A few things stood out.”
Do not treat the existence of an open role by itself as evidence of a capacity problem; use the specific statements or hiring pattern that qualified the signal."""


def execute():
    if frappe.db.exists("SEI Signal Type", "early-technical-capacity-gap"):
        frappe.db.set_value(
            "SEI Signal Type",
            "early-technical-capacity-gap",
            "message_guidance",
            EARLY_CAPACITY_MESSAGE_GUIDANCE,
            update_modified=False,
        )

    if frappe.db.exists("SEI Playbook", "Failed Hiring"):
        frappe.db.set_value(
            "SEI Playbook",
            "Failed Hiring",
            "message_guidance",
            FAILED_HIRING_MESSAGE_GUIDANCE,
            update_modified=False,
        )
