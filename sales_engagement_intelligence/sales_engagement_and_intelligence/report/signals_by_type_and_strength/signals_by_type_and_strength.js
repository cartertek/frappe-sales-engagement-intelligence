frappe.query_reports["Signals by Type and Strength"] = {
  filters: [
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Select",
      options: "\nFailed Recruitment\nTechnical Distress\nLaunch Aftermath\nAgency Overflow\nEcosystem Adjacency\nVendor/Directory Presence\nCommunity Request\nProcurement Visibility\nCredibility/Referral Signal\nReactivation Signal\nOther"
    },
    {
      fieldname: "signal_strength",
      label: __("Signal Strength"),
      fieldtype: "Select",
      options: "\nWeak\nModerate\nStrong"
    },
    {
      fieldname: "evidence_basis",
      label: __("Evidence Basis"),
      fieldtype: "Select",
      options: "\nObserved\nInferred"
    },
    {
      fieldname: "exclude_from_qualification",
      label: __("Exclude from Qualification"),
      fieldtype: "Check",
      default: 0
    },
  ],
};
