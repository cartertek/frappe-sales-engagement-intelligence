frappe.query_reports["Missing Evidence Report"] = {
  filters: [
    {
      fieldname: "research_arena",
      label: __("Research Arena"),
      fieldtype: "Link",
      options: "SEI Research Arena"
    },
    {
      fieldname: "signal_type",
      label: __("Signal Type"),
      fieldtype: "Link",
      options: "SEI Signal Type"
    },
  ],
};
