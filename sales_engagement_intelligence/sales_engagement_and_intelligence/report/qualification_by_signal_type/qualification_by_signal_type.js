frappe.query_reports["Qualification by Signal Type"] = {
  filters: [
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Link",
      options: "SEI Signal Type"
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
