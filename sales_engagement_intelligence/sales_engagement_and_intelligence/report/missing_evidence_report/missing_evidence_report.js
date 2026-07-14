frappe.query_reports["Missing Evidence Report"] = {
  filters: [
    {
      fieldname: "source_arena",
      label: __("Source Arena"),
      fieldtype: "Data"
    },
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Select",
      options: "\nFailed Recruitment\nTechnical Distress\nLaunch Aftermath\nAgency Overflow\nEcosystem Adjacency\nVendor/Directory Presence\nCommunity Request\nProcurement Visibility\nCredibility/Referral Signal\nReactivation Signal"
    },
  ],
};
