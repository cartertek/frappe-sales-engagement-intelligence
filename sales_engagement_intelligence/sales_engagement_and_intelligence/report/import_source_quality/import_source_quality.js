frappe.query_reports["Import Source Quality"] = {
  filters: [
    {
      fieldname: "source_type",
      label: __("Source Type"),
      fieldtype: "Select",
      options: "\nManual CSV\nDirectory Research\nJob Board Research\nLaunch Source Research\nGitHub / Technical Distress Research\nCommunity Research\nAgency / Partner List\nProcurement Research\nOther"
    },
    {
      fieldname: "source_arena",
      label: __("Source Arena"),
      fieldtype: "Data"
    },
  ],
};
