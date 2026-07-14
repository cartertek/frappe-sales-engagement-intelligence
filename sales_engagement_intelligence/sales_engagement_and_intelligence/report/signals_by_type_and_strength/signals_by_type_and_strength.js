frappe.query_reports["Signals by Type and Strength"] = {
  filters: [
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Link",
      options: "SEI Signal Type"
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
