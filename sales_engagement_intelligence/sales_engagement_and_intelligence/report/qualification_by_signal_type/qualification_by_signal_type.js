frappe.query_reports["Qualification by Signal Type"] = {
  filters: [
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Select",
      options: "\nFailed Recruitment\nTechnical Distress\nLaunch Aftermath\nAgency Overflow\nEcosystem Adjacency\nVendor/Directory Presence\nCommunity Request\nProcurement Visibility\nCredibility/Referral Signal\nReactivation Signal\nOther"
    },
    {
      fieldname: "evidence_basis",
      label: __("Evidence Basis"),
      fieldtype: "Select",
      options: "\nObserved\nInferred"
    },
    {
      fieldname: "counts_toward_qualification",
      label: __("Counts Toward Qualification"),
      fieldtype: "Check",
      default: 0
    },
  ],
};
