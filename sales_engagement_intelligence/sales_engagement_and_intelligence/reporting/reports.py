# ruff: noqa: E501
from __future__ import annotations

import frappe

from sales_engagement_intelligence.sales_engagement_and_intelligence.reporting import utils


def _link(label, fieldname, options, width=180):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Link", "options": options, "width": width}


def _data(label, fieldname, width=180):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Data", "width": width}


def _int(label, fieldname, width=120):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Int", "width": width}


def _percent(label, fieldname, width=130):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Percent", "width": width}


def _date(label, fieldname, width=140):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Date", "width": width}


def _datetime(label, fieldname, width=170):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Datetime", "width": width}


def _check(label, fieldname, width=110):
    return {"label": label, "fieldname": fieldname, "fieldtype": "Check", "width": width}


def _sql(query: str, params: dict | None = None):
    return frappe.db.sql(query, params or {}, as_dict=True)


def _has_crm_doctype(doctype):
    return utils.has_doctype(doctype)


def _row_value(row, fieldname):
    if isinstance(row, dict):
        return row.get(fieldname)
    return getattr(row, fieldname, None)


def _bar_chart(data, label_field, value_field, dataset_name):
    return {
        "data": {
            "labels": [str(_row_value(row, label_field) or "(Blank)") for row in data],
            "datasets": [
                {
                    "name": dataset_name,
                    "values": [int(_row_value(row, value_field) or 0) for row in data],
                }
            ],
        },
        "type": "bar",
    }


def _single_row_chart(row, fields, dataset_name):
    return {
        "data": {
            "labels": [label for label, _fieldname in fields],
            "datasets": [
                {
                    "name": dataset_name,
                    "values": [int(_row_value(row, fieldname) or 0) for _label, fieldname in fields],
                }
            ],
        },
        "type": "bar",
    }


def _execute_prospect_lifecycle_summary(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    columns = [_data("Lifecycle Status", "lifecycle_status"), _data("Qualification Status", "qualification_status"), _int("Prospect Count", "prospect_count"), _datetime("Oldest Modified", "oldest_modified"), _datetime("Newest Modified", "newest_modified")]
    data = _sql(f"""
        SELECT lifecycle_status, qualification_status, COUNT(*) prospect_count, MIN(modified) oldest_modified, MAX(modified) newest_modified
        FROM {utils.table('SEI Prospect')}
        GROUP BY lifecycle_status, qualification_status
        ORDER BY lifecycle_status, qualification_status
    """)
    return columns, data, None, _bar_chart(data, "lifecycle_status", "prospect_count", "Prospects")


def _execute_active_prospect_queue(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    where, params = utils.make_conditions(filters, "SEI Prospect", {"lifecycle_status": "lifecycle_status", "qualification_status": "qualification_status", "assigned_to": "assigned_to", "source_arena": "source_arena", "sei_thesis": "thesis"})
    columns = [_link("Prospect", "prospect", "SEI Prospect"), _data("Prospect Type", "prospect_type"), _data("Source Arena", "source_arena"), _link("Thesis", "thesis", "SEI Thesis"), _data("Qualification Status", "qualification_status"), _data("Lifecycle Status", "lifecycle_status"), _data("Next Action", "next_action"), _date("Next Action Date", "next_action_date"), _link("Assigned To", "assigned_to", "User"), _link("CRM Lead", "crm_lead", "CRM Lead"), _link("CRM Deal", "crm_deal", "CRM Deal"), _datetime("Modified", "modified")]
    data = _sql(f"""
        SELECT name prospect, prospect_type, source_arena, thesis, qualification_status, lifecycle_status, next_action, next_action_date, assigned_to, crm_lead, crm_deal, modified
        FROM {utils.table('SEI Prospect')}{where}
        ORDER BY COALESCE(next_action_date, '2999-12-31'), modified DESC
    """, params)
    return columns, data


def _execute_ready_for_crm_conversion(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {"source_arena": "source_arena", "sei_thesis": "thesis"},
    )
    filter_sql = where.replace(" WHERE ", " AND ", 1)
    columns = [_link("Prospect", "prospect", "SEI Prospect"), _data("Website", "website"), _data("Source Arena", "source_arena"), _link("Thesis", "thesis", "SEI Thesis"), _data("Qualification Explanation", "qualification_explanation", 260), _data("Primary Contact Email", "primary_contact_email", 220), _link("CRM Lead", "crm_lead", "CRM Lead"), _link("CRM Organization", "crm_organization", "CRM Organization"), _link("Contact", "contact", "Contact"), _link("CRM Deal", "crm_deal", "CRM Deal"), _date("Next Action Date", "next_action_date")]
    data = _sql(f"""
        SELECT name prospect, website, source_arena, thesis, qualification_explanation, primary_contact_email, crm_lead, crm_organization, crm_contact contact, crm_deal, next_action_date
        FROM {utils.table('SEI Prospect')}
        WHERE qualification_status IN ('Qualified', 'Manually Approved')
          AND ready_for_crm_conversion = 1
          AND COALESCE(do_not_contact, 0) = 0
          AND COALESCE(lifecycle_status, '') NOT IN ('Rejected', 'Do Not Contact')
          {filter_sql}
        ORDER BY COALESCE(next_action_date, '2999-12-31'), modified DESC
    """, params)
    return columns, data


def _execute_terminal_status_review(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {
            "lifecycle_status": "lifecycle_status",
            "qualification_status": "qualification_status",
            "source_arena": "source_arena",
            "sei_thesis": "thesis",
        },
    )
    filter_sql = where.replace(" WHERE ", " AND ", 1)
    columns = [_link("Prospect", "prospect", "SEI Prospect"), _data("Lifecycle Status", "lifecycle_status"), _data("Qualification Status", "qualification_status"), _data("Rejected Reason", "rejected_reason", 240), _check("Do Not Contact", "do_not_contact"), _data("Source Arena", "source_arena"), _link("Thesis", "thesis", "SEI Thesis"), _link("Modified By", "modified_by", "User"), _datetime("Modified", "modified")]
    data = _sql(f"""
        SELECT name prospect, lifecycle_status, qualification_status, rejected_reason, do_not_contact, source_arena, thesis, modified_by, modified
        FROM {utils.table('SEI Prospect')}
        WHERE (lifecycle_status IN ('Rejected', 'Do Not Contact') OR qualification_status IN ('Rejected', 'Do Not Contact') OR COALESCE(do_not_contact, 0) = 1)
          {filter_sql}
        ORDER BY modified DESC
    """, params)
    return columns, data


def _execute_signals_by_type_and_strength(filters):
    if not utils.has_doctype("SEI Signal"):
        return utils.empty_result("SEI Signal is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Signal",
        {
            "signal_type": "signal_type",
            "signal_strength": "signal_strength",
            "evidence_basis": "evidence_basis",
            "counts_toward_qualification": "counts_toward_qualification",
        },
    )
    columns = [_data("Signal Type", "signal_type"), _data("Signal Strength", "signal_strength"), _data("Evidence Basis", "evidence_basis"), _check("Counts Toward Qualification", "counts_toward_qualification"), _int("Signal Count", "signal_count"), _int("Prospect Count", "prospect_count")]
    data = _sql(f"""
        SELECT signal_type, signal_strength, evidence_basis, counts_toward_qualification, COUNT(*) signal_count, COUNT(DISTINCT prospect) prospect_count
        FROM {utils.table('SEI Signal')}{where}
        GROUP BY signal_type, signal_strength, evidence_basis, counts_toward_qualification
        ORDER BY signal_type, signal_strength, evidence_basis
    """, params)
    return columns, data, None, _bar_chart(data, "signal_type", "signal_count", "Signals")


def _execute_qualification_by_signal_type(filters):
    if not utils.doctypes_available("SEI Signal", "SEI Prospect"):
        return utils.empty_result("SEI Signal and SEI Prospect are required.")
    where, params = utils.make_conditions(
        filters,
        "SEI Signal",
        {
            "signal_type": "signal_type",
            "evidence_basis": "evidence_basis",
            "counts_toward_qualification": "counts_toward_qualification",
        },
    )
    columns = [_data("Signal Type", "signal_type"), _int("Total Prospects", "total_prospects"), _int("Qualified Prospects", "qualified_prospects"), _int("Manually Approved Prospects", "manually_approved_prospects"), _int("Needs Review Prospects", "needs_review_prospects"), _int("Rejected Prospects", "rejected_prospects"), _int("Do Not Contact Prospects", "do_not_contact_prospects"), _percent("Qualification Rate", "qualification_rate")]
    data = _sql(f"""
        SELECT s.signal_type,
               COUNT(DISTINCT p.name) total_prospects,
               COUNT(DISTINCT CASE WHEN p.qualification_status = 'Qualified' THEN p.name END) qualified_prospects,
               COUNT(DISTINCT CASE WHEN p.qualification_status = 'Manually Approved' THEN p.name END) manually_approved_prospects,
               COUNT(DISTINCT CASE WHEN p.qualification_status = 'Needs Review' THEN p.name END) needs_review_prospects,
               COUNT(DISTINCT CASE WHEN p.qualification_status = 'Rejected' THEN p.name END) rejected_prospects,
               COUNT(DISTINCT CASE WHEN p.qualification_status = 'Do Not Contact' OR COALESCE(p.do_not_contact, 0) = 1 THEN p.name END) do_not_contact_prospects,
               {utils.pct_expr("COUNT(DISTINCT CASE WHEN p.qualification_status IN ('Qualified','Manually Approved') THEN p.name END)", "COUNT(DISTINCT p.name)")} qualification_rate
        FROM {utils.table('SEI Signal')} s
        LEFT JOIN {utils.table('SEI Prospect')} p ON p.name = s.prospect
        {where.replace(utils.table('SEI Signal'), 's')}
        GROUP BY s.signal_type
        ORDER BY qualification_rate DESC, total_prospects DESC
    """, params)
    return columns, data, None, _bar_chart(data, "signal_type", "total_prospects", "Prospects")


def _execute_inferred_signal_review(filters):
    if not utils.has_doctype("SEI Signal"):
        return utils.empty_result("SEI Signal is not installed.")
    columns = [_link("Signal", "signal", "SEI Signal"), _link("Prospect", "prospect", "SEI Prospect"), _data("Signal Type", "signal_type"), _data("Signal Strength", "signal_strength"), _data("Evidence Basis", "evidence_basis"), _check("Counts Toward Qualification", "counts_toward_qualification"), _data("Source URL", "source_url", 240), _data("Evidence Notes", "evidence_notes", 300), _date("Review Date", "review_date")]
    data = _sql(f"""
        SELECT name `signal`, prospect, signal_type, signal_strength, evidence_basis, counts_toward_qualification, source_url, evidence_notes, review_date
        FROM {utils.table('SEI Signal')}
        WHERE evidence_basis = 'Inferred' AND COALESCE(counts_toward_qualification, 0) = 1
        ORDER BY modified DESC
    """)
    return columns, data


def _execute_missing_evidence_report(filters):
    if not utils.doctypes_available("SEI Prospect", "SEI Signal"):
        return utils.empty_result("SEI Prospect and SEI Signal are required.")
    columns = [_data("Issue Type", "issue_type"), _link("Prospect", "prospect", "SEI Prospect"), _link("Signal", "signal", "SEI Signal"), _data("Source Arena", "source_arena"), _data("Signal Type", "signal_type"), _data("Details", "details", 360), _datetime("Modified", "modified")]
    data = _sql(f"""
        SELECT 'Prospect has no linked SEI Signal' issue_type, p.name prospect, NULL `signal`, p.source_arena, NULL signal_type, 'No SEI Signal rows reference this prospect.' details, p.modified
        FROM {utils.table('SEI Prospect')} p LEFT JOIN {utils.table('SEI Signal')} s ON s.prospect = p.name
        WHERE s.name IS NULL
        UNION ALL
        SELECT 'Signal missing source URL', prospect, name `signal`, NULL source_arena, signal_type, 'source_url is blank.' details, modified FROM {utils.table('SEI Signal')} WHERE COALESCE(source_url, '') = ''
        UNION ALL
        SELECT 'Signal missing source date', prospect, name `signal`, NULL source_arena, signal_type, 'source_date is blank.' details, modified FROM {utils.table('SEI Signal')} WHERE source_date IS NULL
        UNION ALL
        SELECT 'Signal missing evidence notes', prospect, name `signal`, NULL source_arena, signal_type, 'evidence_notes is blank.' details, modified FROM {utils.table('SEI Signal')} WHERE COALESCE(evidence_notes, '') = ''
        UNION ALL
        SELECT 'Prospect missing source arena', name prospect, NULL `signal`, source_arena, NULL signal_type, 'source_arena is blank.' details, modified FROM {utils.table('SEI Prospect')} WHERE COALESCE(source_arena, '') = ''
        ORDER BY modified DESC
    """)
    return columns, data


def _source_or_thesis(group_field: str, label: str, fieldname: str, filters=None):
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {
            "source_arena": "source_arena",
            "qualification_status": "qualification_status",
            "lifecycle_status": "lifecycle_status",
        },
    )
    columns = [_data(label, fieldname), _int("Total Prospects", "total_prospects"), _int("Qualified Prospects", "qualified_prospects"), _int("Manually Approved Prospects", "manually_approved_prospects"), _int("Ready for CRM Conversion", "ready_for_crm_conversion"), _int("Converted to CRM Lead", "converted_to_crm_lead"), _int("Converted to CRM Deal", "converted_to_crm_deal"), _int("Rejected", "rejected"), _int("Do Not Contact", "do_not_contact"), _percent("Qualification Rate", "qualification_rate"), _percent("CRM Lead Conversion Rate", "crm_lead_conversion_rate"), _percent("CRM Deal Conversion Rate", "crm_deal_conversion_rate")]
    data = _sql(f"""
        SELECT COALESCE({group_field}, '(Blank)') {fieldname}, COUNT(*) total_prospects,
               SUM(CASE WHEN qualification_status = 'Qualified' THEN 1 ELSE 0 END) qualified_prospects,
               SUM(CASE WHEN qualification_status = 'Manually Approved' THEN 1 ELSE 0 END) manually_approved_prospects,
               SUM(CASE WHEN COALESCE(ready_for_crm_conversion,0)=1 THEN 1 ELSE 0 END) ready_for_crm_conversion,
               SUM(CASE WHEN COALESCE(crm_lead,'')!='' OR lifecycle_status='Converted to CRM Lead' THEN 1 ELSE 0 END) converted_to_crm_lead,
               SUM(CASE WHEN COALESCE(crm_deal,'')!='' OR lifecycle_status='Converted to CRM Deal' THEN 1 ELSE 0 END) converted_to_crm_deal,
               SUM(CASE WHEN qualification_status='Rejected' OR lifecycle_status='Rejected' THEN 1 ELSE 0 END) rejected,
               SUM(CASE WHEN qualification_status='Do Not Contact' OR lifecycle_status='Do Not Contact' OR COALESCE(do_not_contact,0)=1 THEN 1 ELSE 0 END) do_not_contact,
               {utils.pct_expr("SUM(CASE WHEN qualification_status IN ('Qualified','Manually Approved') THEN 1 ELSE 0 END)", "COUNT(*)")} qualification_rate,
               {utils.pct_expr("SUM(CASE WHEN COALESCE(crm_lead,'')!='' OR lifecycle_status='Converted to CRM Lead' THEN 1 ELSE 0 END)", "COUNT(*)")} crm_lead_conversion_rate,
               {utils.pct_expr("SUM(CASE WHEN COALESCE(crm_deal,'')!='' OR lifecycle_status='Converted to CRM Deal' THEN 1 ELSE 0 END)", "COUNT(*)")} crm_deal_conversion_rate
        FROM {utils.table('SEI Prospect')}{where}
        GROUP BY COALESCE({group_field}, '(Blank)')
        ORDER BY total_prospects DESC
    """, params)
    return columns, data, None, _bar_chart(data, fieldname, "total_prospects", "Prospects")


def _execute_prospects_by_source_arena(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    return _source_or_thesis("source_arena", "Source Arena", "source_arena", filters)


def _execute_outcomes_by_thesis(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    return _source_or_thesis("thesis", "Thesis", "thesis", filters)


def _execute_asset_usage_and_outcomes(filters):
    if not utils.doctypes_available("SEI Asset", "SEI Interaction Attribution"):
        return utils.empty_result("SEI Asset and SEI Interaction Attribution are required.")
    where, params = utils.make_conditions(
        filters,
        "SEI Asset",
        {"sei_thesis": "related_thesis", "asset_type": "asset_type"},
    )
    columns = [_link("Asset", "asset", "SEI Asset"), _data("Asset Type", "asset_type"), _link("Related Thesis", "related_thesis", "SEI Thesis"), _int("Interaction Count", "interaction_count"), _int("Positive Responses", "positive_responses"), _int("Interested Responses", "interested_responses"), _int("Meeting Booked", "meeting_booked"), _int("Converted to CRM Lead", "converted_to_crm_lead"), _int("Converted to CRM Deal", "converted_to_crm_deal")]
    data = _sql(f"""
        SELECT a.name asset, a.asset_type, a.related_thesis,
               COUNT(ia.name) interaction_count,
               SUM(CASE WHEN ia.response_category = 'Positive' THEN 1 ELSE 0 END) positive_responses,
               SUM(CASE WHEN ia.response_category = 'Interested' THEN 1 ELSE 0 END) interested_responses,
               SUM(CASE WHEN ia.response_category = 'Meeting Booked' THEN 1 ELSE 0 END) meeting_booked,
               COUNT(DISTINCT CASE WHEN COALESCE(ia.crm_lead, '') != '' THEN ia.crm_lead END) converted_to_crm_lead,
               COUNT(DISTINCT CASE WHEN COALESCE(ia.crm_deal, '') != '' THEN ia.crm_deal END) converted_to_crm_deal
        FROM {utils.table('SEI Asset')} a
        LEFT JOIN {utils.table('SEI Interaction Attribution')} ia ON ia.marketing_asset = a.name
        {where.replace(utils.table('SEI Asset'), 'a')}
        GROUP BY a.name, a.asset_type, a.related_thesis
        ORDER BY interaction_count DESC, a.name
    """, params)
    return columns, data, None, _bar_chart(data, "asset", "interaction_count", "Interactions")


def _execute_offer_performance(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    has_attribution = utils.has_doctype("SEI Interaction Attribution")
    ia_join = f"LEFT JOIN {utils.table('SEI Interaction Attribution')} ia ON ia.prospect = p.name" if has_attribution else ""
    interaction_count = "COUNT(DISTINCT ia.name)" if has_attribution else "0"
    positive_responses = "SUM(CASE WHEN ia.response_category = 'Positive' THEN 1 ELSE 0 END)" if has_attribution else "0"
    meeting_booked = "SUM(CASE WHEN ia.response_category = 'Meeting Booked' THEN 1 ELSE 0 END)" if has_attribution else "0"
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {"source_arena": "source_arena", "sei_thesis": "thesis"},
    )
    columns = [_data("Offer", "offer"), _int("Prospect Count", "prospect_count"), _int("Interaction Count", "interaction_count"), _int("Qualified Prospects", "qualified_prospects"), _int("Positive Responses", "positive_responses"), _int("Meeting Booked", "meeting_booked"), _int("CRM Leads", "crm_leads"), _int("CRM Deals", "crm_deals")]
    data = _sql(f"""
        SELECT COALESCE(p.offer, '(Blank)') offer, COUNT(DISTINCT p.name) prospect_count,
               {interaction_count} interaction_count,
               COUNT(DISTINCT CASE WHEN p.qualification_status IN ('Qualified','Manually Approved') THEN p.name END) qualified_prospects,
               {positive_responses} positive_responses,
               {meeting_booked} meeting_booked,
               COUNT(DISTINCT CASE WHEN COALESCE(p.crm_lead,'') != '' THEN p.crm_lead END) crm_leads,
               COUNT(DISTINCT CASE WHEN COALESCE(p.crm_deal,'') != '' THEN p.crm_deal END) crm_deals
        FROM {utils.table('SEI Prospect')} p {ia_join}
        {where.replace(utils.table('SEI Prospect'), 'p')}
        GROUP BY COALESCE(p.offer, '(Blank)')
        ORDER BY prospect_count DESC
    """, params)
    return columns, data, None, _bar_chart(data, "offer", "prospect_count", "Prospects")


def _execute_crm_conversion_summary(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    columns = [_int("Total SEI Prospects", "total_sei_prospects"), _int("With CRM Lead", "with_crm_lead"), _int("With CRM Organization", "with_crm_organization"), _int("With Contact", "with_contact"), _int("With CRM Deal", "with_crm_deal"), _int("Converted to CRM Lead Lifecycle", "converted_to_crm_lead_lifecycle"), _int("Converted to CRM Deal Lifecycle", "converted_to_crm_deal_lifecycle")]
    data = _sql(f"""
        SELECT COUNT(*) total_sei_prospects,
               SUM(CASE WHEN COALESCE(crm_lead,'') != '' THEN 1 ELSE 0 END) with_crm_lead,
               SUM(CASE WHEN COALESCE(crm_organization,'') != '' THEN 1 ELSE 0 END) with_crm_organization,
               SUM(CASE WHEN COALESCE(crm_contact,'') != '' THEN 1 ELSE 0 END) with_contact,
               SUM(CASE WHEN COALESCE(crm_deal,'') != '' THEN 1 ELSE 0 END) with_crm_deal,
               SUM(CASE WHEN lifecycle_status = 'Converted to CRM Lead' THEN 1 ELSE 0 END) converted_to_crm_lead_lifecycle,
               SUM(CASE WHEN lifecycle_status = 'Converted to CRM Deal' THEN 1 ELSE 0 END) converted_to_crm_deal_lifecycle
        FROM {utils.table('SEI Prospect')}
    """)
    chart = _single_row_chart(
        data[0] if data else {},
        (
            ("Total", "total_sei_prospects"),
            ("CRM Leads", "with_crm_lead"),
            ("CRM Organizations", "with_crm_organization"),
            ("Contacts", "with_contact"),
            ("CRM Deals", "with_crm_deal"),
        ),
        "Prospects",
    )
    return columns, data, None, chart


def _execute_crm_lead_conversion_detail(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {
            "source_arena": "source_arena",
            "sei_thesis": "thesis",
            "qualification_status": "qualification_status",
        },
    )
    filter_sql = where.replace(" WHERE ", " AND ", 1)
    columns = [_link("SEI Prospect", "sei_prospect", "SEI Prospect"), _data("Source Arena", "source_arena"), _link("Thesis", "thesis", "SEI Thesis"), _data("Qualification Status", "qualification_status"), _data("Lifecycle Status", "lifecycle_status"), _link("CRM Lead", "crm_lead", "CRM Lead"), _link("CRM Organization", "crm_organization", "CRM Organization"), _link("Contact", "contact", "Contact"), _data("Primary Contact Email", "primary_contact_email", 220), _datetime("Converted / Linked Date", "converted_linked_date"), _datetime("Modified", "modified")]
    data = _sql(f"""
        SELECT name sei_prospect, source_arena, thesis, qualification_status, lifecycle_status, crm_lead, crm_organization, crm_contact contact, primary_contact_email, modified converted_linked_date, modified
        FROM {utils.table('SEI Prospect')}
        WHERE COALESCE(crm_lead, '') != ''
          {filter_sql}
        ORDER BY modified DESC
    """, params)
    return columns, data


def _execute_crm_deal_conversion_detail(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    deal_status = utils.column("CRM Deal", "status", "NULL") if _has_crm_doctype("CRM Deal") else "NULL"
    join = f"LEFT JOIN {utils.table('CRM Deal')} d ON d.name = p.crm_deal" if _has_crm_doctype("CRM Deal") else ""
    where, params = utils.make_conditions(
        filters,
        "SEI Prospect",
        {"source_arena": "source_arena", "sei_thesis": "thesis"},
    )
    filter_sql = where.replace(" WHERE ", " AND ", 1)
    if utils.has_doctype("SEI Interaction Attribution"):
        commercial_basis = f"""CASE WHEN EXISTS (SELECT 1 FROM {utils.table('SEI Interaction Attribution')} ia WHERE ia.prospect = p.name AND ia.response_category IN ('Positive','Interested','Meeting Booked','Converted to Deal')) THEN 'Attributed commercial response' ELSE NULL END"""
    else:
        commercial_basis = "NULL"
    columns = [_link("SEI Prospect", "sei_prospect", "SEI Prospect"), _data("Source Arena", "source_arena"), _link("Thesis", "thesis", "SEI Thesis"), _link("Primary Signal", "primary_signal", "SEI Signal"), _link("CRM Deal", "crm_deal", "CRM Deal"), _link("CRM Lead", "crm_lead", "CRM Lead"), _link("CRM Organization", "crm_organization", "CRM Organization"), _link("Contact", "contact", "Contact"), _data("Deal Status", "deal_status"), _data("Lifecycle Status", "lifecycle_status"), _data("Commercial Basis", "commercial_basis", 200), _datetime("Modified", "modified")]
    data = _sql(f"""
        SELECT p.name sei_prospect, p.source_arena, p.thesis, (SELECT s.name FROM {utils.table('SEI Signal')} s WHERE s.prospect = p.name ORDER BY s.source_date DESC, s.creation DESC LIMIT 1) primary_signal,
               p.crm_deal, p.crm_lead, p.crm_organization, p.crm_contact contact, {deal_status} deal_status, p.lifecycle_status,
               {commercial_basis} commercial_basis,
               p.modified
        FROM {utils.table('SEI Prospect')} p {join}
        WHERE COALESCE(p.crm_deal, '') != ''
          {filter_sql}
        ORDER BY p.modified DESC
    """, params)
    return columns, data


def _missing_context_rows_for_doctype(doctype: str, fields: list[str], record_label: str):
    if not utils.has_doctype(doctype):
        return []
    existing = [field for field in fields if utils.has_field(doctype, field)]
    if not existing:
        return []
    checks = " OR ".join([f"COALESCE(`{field}`, '') = ''" for field in existing])
    select_missing = "CONCAT_WS(', ', " + ", ".join([f"CASE WHEN COALESCE(`{field}`, '') = '' THEN '{field}' END" for field in existing]) + ")"
    return _sql(f"SELECT '{record_label}' record_type, name record, {select_missing} missing_context, modified FROM {utils.table(doctype)} WHERE {checks}")


def _execute_crm_context_missing(filters):
    columns = [_data("Record Type", "record_type"), _data("Record", "record", 220), _data("Missing Context", "missing_context", 360), _datetime("Modified", "modified")]
    rows = []
    rows.extend(_missing_context_rows_for_doctype("CRM Lead", ["sei_prospect", "sei_source_arena", "sei_thesis", "sei_qualification_summary"], "CRM Lead"))
    rows.extend(_missing_context_rows_for_doctype("CRM Deal", ["sei_prospect", "sei_source_arena", "sei_thesis", "sei_primary_signal"], "CRM Deal"))
    if utils.has_doctype("SEI Prospect"):
        rows.extend(_sql(f"""
            SELECT 'SEI Prospect' record_type, name record,
                   CONCAT_WS(', ', CASE WHEN COALESCE(crm_lead,'') != '' AND COALESCE(source_arena,'') = '' THEN 'source_arena' END, CASE WHEN COALESCE(crm_deal,'') != '' AND COALESCE(thesis,'') = '' THEN 'thesis' END) missing_context,
                   modified
            FROM {utils.table('SEI Prospect')}
            WHERE (COALESCE(crm_lead,'') != '' OR COALESCE(crm_deal,'') != '') AND (COALESCE(source_arena,'') = '' OR COALESCE(thesis,'') = '')
        """))
    return columns, rows


def _execute_possible_duplicate_crm_conversion_review(filters):
    if not utils.has_doctype("SEI Prospect"):
        return utils.empty_result("SEI Prospect is not installed.")
    columns = [_link("Prospect", "prospect", "SEI Prospect"), _data("Possible Duplicate Type", "possible_duplicate_type"), _data("Possible Duplicate Record", "possible_duplicate_record", 220), _data("Match Reason", "match_reason", 280), _data("Recommended Action", "recommended_action", 260)]
    rows = []
    # Read-only lightweight duplicate review: SEI duplicates by normalized domain or primary email.
    rows.extend(_sql(f"""
        SELECT p1.name prospect, 'SEI Prospect' possible_duplicate_type, p2.name possible_duplicate_record,
               'Same normalized domain' match_reason, 'Review and merge/link manually if appropriate.' recommended_action
        FROM {utils.table('SEI Prospect')} p1 JOIN {utils.table('SEI Prospect')} p2 ON p1.name < p2.name AND COALESCE(p1.normalized_domain,'') != '' AND p1.normalized_domain = p2.normalized_domain
        LIMIT 200
    """))
    rows.extend(_sql(f"""
        SELECT p1.name prospect, 'SEI Prospect' possible_duplicate_type, p2.name possible_duplicate_record,
               'Same primary contact email' match_reason, 'Review and merge/link manually if appropriate.' recommended_action
        FROM {utils.table('SEI Prospect')} p1 JOIN {utils.table('SEI Prospect')} p2 ON p1.name < p2.name AND COALESCE(p1.primary_contact_email,'') != '' AND p1.primary_contact_email = p2.primary_contact_email
        LIMIT 200
    """))
    return columns, rows


def _execute_import_batch_summary(filters):
    if not utils.has_doctype("SEI Import Batch"):
        return utils.empty_result("SEI Import Batch is not installed in this source tree/site.")
    where, params = utils.make_conditions(
        filters,
        "SEI Import Batch",
        {
            "source_type": "source_type",
            "source_arena": "source_arena",
            "import_kind": "import_kind",
            "import_mode": "import_mode",
            "status": "status",
        },
    )
    cols = ["source_type", "source_arena", "import_kind", "import_mode", "status", "rows_total", "rows_created", "rows_updated", "rows_skipped", "rows_failed", "started_at", "completed_at", "imported_by"]
    columns = [_link("Import Batch", "import_batch", "SEI Import Batch")] + [_data(c.replace('_',' ').title(), c) for c in cols]
    select = ", ".join([f"{utils.column('SEI Import Batch', c)} {c}" for c in cols])
    data = _sql(
        f"SELECT name import_batch, {select} FROM {utils.table('SEI Import Batch')}{where} ORDER BY modified DESC",
        params,
    )
    return columns, data, None, _bar_chart(data, "status", "rows_total", "Rows")


def _execute_import_batch_row_errors(filters):
    if not utils.has_doctype("SEI Import Batch Row"):
        return utils.empty_result("SEI Import Batch Row is not installed in this source tree/site.")
    where, params = utils.make_conditions(
        filters,
        "SEI Import Batch Row",
        {"import_batch": "parent", "row_status": "row_status"},
    )
    filter_sql = where.replace(" WHERE ", " AND ", 1)
    columns = [
        _link("Import Batch", "import_batch", "SEI Import Batch"),
        _int("Row Number", "row_number"),
        _data("Row Status", "row_status"),
        _data("Action Taken", "action_taken"),
        _link("Matched Existing Prospect", "matched_existing_prospect", "SEI Prospect"),
        _link("Prospect", "prospect", "SEI Prospect"),
        _link("Signal", "signal", "SEI Signal"),
        _data("Error Message", "error_message", 220),
        _data("Raw Row JSON", "raw_row_json", 220),
    ]
    status_col = "row_status" if utils.has_field("SEI Import Batch Row", "row_status") else "status"
    return columns, _sql(
        f"""
        SELECT parent import_batch, `row_number`, `row_status`, `action_taken`,
               `matched_existing_prospect`, `prospect`, `signal`, `error_message`, `raw_row_json`
        FROM {utils.table('SEI Import Batch Row')}
        WHERE `{status_col}` IN ('Failed','Duplicate Warning','Skipped')
          {filter_sql}
        ORDER BY modified DESC
        """,
        params,
    )


def _execute_import_source_quality(filters):
    if not utils.has_doctype("SEI Import Batch"):
        return utils.empty_result("SEI Import Batch is not installed in this source tree/site.")
    where, params = utils.make_conditions(
        filters,
        "SEI Import Batch",
        {"source_type": "source_type", "source_arena": "source_arena"},
    )
    columns = [_data("Source Type", "source_type"), _data("Source Arena", "source_arena"), _int("Import Batch Count", "import_batch_count"), _int("Rows Total", "rows_total"), _int("Rows Created", "rows_created"), _int("Rows Updated", "rows_updated"), _int("Rows Skipped", "rows_skipped"), _int("Rows Failed", "rows_failed"), _percent("Failure Rate", "failure_rate"), _percent("Duplicate Warning Rate", "duplicate_warning_rate"), _int("Qualified Prospects Created", "qualified_prospects_created")]
    data = _sql(f"""
        SELECT {utils.column('SEI Import Batch','source_type')} source_type, {utils.column('SEI Import Batch','source_arena')} source_arena,
               COUNT(*) import_batch_count,
               SUM(COALESCE({utils.column('SEI Import Batch','rows_total','0')},0)) rows_total,
               SUM(COALESCE({utils.column('SEI Import Batch','rows_created','0')},0)) rows_created,
               SUM(COALESCE({utils.column('SEI Import Batch','rows_updated','0')},0)) rows_updated,
               SUM(COALESCE({utils.column('SEI Import Batch','rows_skipped','0')},0)) rows_skipped,
               SUM(COALESCE({utils.column('SEI Import Batch','rows_failed','0')},0)) rows_failed,
               {utils.pct_expr("SUM(COALESCE(" + utils.column('SEI Import Batch','rows_failed','0') + ",0))", "SUM(COALESCE(" + utils.column('SEI Import Batch','rows_total','0') + ",0))")} failure_rate,
               0 duplicate_warning_rate,
               0 qualified_prospects_created
        FROM {utils.table('SEI Import Batch')}{where}
        GROUP BY source_type, source_arena
        ORDER BY rows_total DESC
    """, params)
    return columns, data, None, _bar_chart(data, "source_arena", "rows_total", "Rows")


def _execute_data_hygiene_dashboard(filters):
    if not utils.doctypes_available("SEI Prospect", "SEI Signal"):
        return utils.empty_result("SEI Prospect and SEI Signal are required.")
    columns = [_data("Issue", "issue", 320), _int("Count", "count"), _data("Recommended Action", "recommended_action", 360)]
    rows = []
    checks = [
        ("Prospects missing source arena", f"SELECT COUNT(*) c FROM {utils.table('SEI Prospect')} WHERE COALESCE(source_arena,'')=''", "Review prospect source attribution."),
        ("Signals missing source URL", f"SELECT COUNT(*) c FROM {utils.table('SEI Signal')} WHERE COALESCE(source_url,'')=''", "Add original evidence URL where available."),
        ("Inferred signals marked as qualifying", f"SELECT COUNT(*) c FROM {utils.table('SEI Signal')} WHERE evidence_basis='Inferred' AND COALESCE(counts_toward_qualification,0)=1", "Review whether inferred evidence should qualify prospects."),
        ("Prospects missing normalized domain where website exists", f"SELECT COUNT(*) c FROM {utils.table('SEI Prospect')} WHERE COALESCE(website,'')!='' AND COALESCE(normalized_domain,'')=''", "Run/repair domain normalization via existing hygiene utilities."),
        ("Duplicate SEI Prospects by normalized domain", f"SELECT COUNT(*) c FROM (SELECT normalized_domain FROM {utils.table('SEI Prospect')} WHERE COALESCE(normalized_domain,'')!='' GROUP BY normalized_domain HAVING COUNT(*) > 1) x", "Review potential duplicate prospects."),
        ("Duplicate SEI Signals by prospect/type/url", f"SELECT COUNT(*) c FROM (SELECT prospect, signal_type, source_url FROM {utils.table('SEI Signal')} GROUP BY prospect, signal_type, source_url HAVING COUNT(*) > 1) x", "Review potential duplicate signals."),
    ]
    for issue, sql, action in checks:
        rows.append({"issue": issue, "count": _sql(sql)[0].c, "recommended_action": action})
    return columns, rows, None, _bar_chart(rows, "issue", "count", "Issues")


def _execute_interaction_attribution_summary(filters):
    if not utils.has_doctype("SEI Interaction Attribution"):
        return utils.empty_result("SEI Interaction Attribution is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Interaction Attribution",
        {
            "interaction_type": "interaction_type",
            "channel": "channel",
            "response_category": "response_category",
            "sei_thesis": "thesis",
            "sei_asset": "marketing_asset",
        },
    )
    columns = [_data("Interaction Type", "interaction_type"), _data("Channel", "channel"), _data("Response Category", "response_category"), _link("Thesis", "thesis", "SEI Thesis"), _link("Asset", "asset", "SEI Asset"), _int("Interaction Count", "interaction_count"), _int("Prospect Count", "prospect_count"), _int("CRM Lead Count", "crm_lead_count"), _int("CRM Deal Count", "crm_deal_count")]
    data = _sql(f"""
        SELECT interaction_type, channel, response_category, thesis, marketing_asset asset, COUNT(*) interaction_count,
               COUNT(DISTINCT prospect) prospect_count, COUNT(DISTINCT crm_lead) crm_lead_count, COUNT(DISTINCT crm_deal) crm_deal_count
        FROM {utils.table('SEI Interaction Attribution')}{where}
        GROUP BY interaction_type, channel, response_category, thesis, marketing_asset
        ORDER BY interaction_count DESC
    """, params)
    return columns, data, None, _bar_chart(data, "channel", "interaction_count", "Interactions")


def _execute_response_category_by_thesis(filters):
    if not utils.has_doctype("SEI Interaction Attribution"):
        return utils.empty_result("SEI Interaction Attribution is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Interaction Attribution",
        {"sei_thesis": "thesis", "channel": "channel"},
    )
    cats = ["No Response", "Positive", "Interested", "Wrong Person", "Not Now", "Already Solved", "No Budget", "Bad Fit", "Unsubscribe / Do Not Contact", "Meeting Booked", "Converted to Deal", "Other"]
    columns = [_link("Thesis", "thesis", "SEI Thesis")] + [_int(cat, cat.lower().replace(' / ','_').replace(' ','_').replace('-','_')) for cat in cats]
    select = ", ".join([f"SUM(CASE WHEN response_category = '{cat}' THEN 1 ELSE 0 END) `{cat.lower().replace(' / ','_').replace(' ','_').replace('-','_')}`" for cat in cats])
    data = _sql(
        f"SELECT thesis, {select} FROM {utils.table('SEI Interaction Attribution')}{where} GROUP BY thesis ORDER BY thesis",
        params,
    )
    return columns, data, None, _bar_chart(data, "thesis", "positive", "Positive")


def _execute_channel_outcome_report(filters):
    if not utils.has_doctype("SEI Interaction Attribution"):
        return utils.empty_result("SEI Interaction Attribution is not installed.")
    where, params = utils.make_conditions(
        filters,
        "SEI Interaction Attribution",
        {"channel": "channel", "sei_thesis": "thesis"},
    )
    columns = [_data("Channel", "channel"), _int("Interaction Count", "interaction_count"), _int("Positive", "positive"), _int("Interested", "interested"), _int("Meeting Booked", "meeting_booked"), _int("Converted to Deal", "converted_to_deal"), _int("Bad Fit", "bad_fit"), _int("Unsubscribe / Do Not Contact", "unsubscribe_do_not_contact")]
    data = _sql(f"""
        SELECT channel, COUNT(*) interaction_count,
               SUM(CASE WHEN response_category='Positive' THEN 1 ELSE 0 END) positive,
               SUM(CASE WHEN response_category='Interested' THEN 1 ELSE 0 END) interested,
               SUM(CASE WHEN response_category='Meeting Booked' THEN 1 ELSE 0 END) meeting_booked,
               SUM(CASE WHEN response_category='Converted to Deal' THEN 1 ELSE 0 END) converted_to_deal,
               SUM(CASE WHEN response_category='Bad Fit' THEN 1 ELSE 0 END) bad_fit,
               SUM(CASE WHEN response_category='Unsubscribe / Do Not Contact' THEN 1 ELSE 0 END) unsubscribe_do_not_contact
        FROM {utils.table('SEI Interaction Attribution')}{where}
        GROUP BY channel
        ORDER BY interaction_count DESC
    """, params)
    return columns, data, None, _bar_chart(data, "channel", "interaction_count", "Interactions")


REPORT_EXECUTORS = {
    "Prospect Lifecycle Summary": _execute_prospect_lifecycle_summary,
    "Active Prospect Queue": _execute_active_prospect_queue,
    "Ready for CRM Conversion": _execute_ready_for_crm_conversion,
    "Terminal Status Review": _execute_terminal_status_review,
    "Signals by Type and Strength": _execute_signals_by_type_and_strength,
    "Qualification by Signal Type": _execute_qualification_by_signal_type,
    "Inferred Signal Review": _execute_inferred_signal_review,
    "Missing Evidence Report": _execute_missing_evidence_report,
    "Prospects by Source Arena": _execute_prospects_by_source_arena,
    "Outcomes by Thesis": _execute_outcomes_by_thesis,
    "Asset Usage and Outcomes": _execute_asset_usage_and_outcomes,
    "Offer Performance": _execute_offer_performance,
    "CRM Conversion Summary": _execute_crm_conversion_summary,
    "CRM Lead Conversion Detail": _execute_crm_lead_conversion_detail,
    "CRM Deal Conversion Detail": _execute_crm_deal_conversion_detail,
    "CRM Context Missing": _execute_crm_context_missing,
    "Possible Duplicate CRM Conversion Review": _execute_possible_duplicate_crm_conversion_review,
    "Import Batch Summary": _execute_import_batch_summary,
    "Import Batch Row Errors": _execute_import_batch_row_errors,
    "Import Source Quality": _execute_import_source_quality,
    "Data Hygiene Dashboard": _execute_data_hygiene_dashboard,
    "Interaction Attribution Summary": _execute_interaction_attribution_summary,
    "Response Category by Thesis": _execute_response_category_by_thesis,
    "Channel Outcome Report": _execute_channel_outcome_report,
}


def execute_report(report_name: str, filters=None):
    executor = REPORT_EXECUTORS.get(report_name)
    if not executor:
        return utils.empty_result(f"Unknown SEI report: {report_name}")
    return executor(filters or {})
