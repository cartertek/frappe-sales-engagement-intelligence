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
      fieldtype: "Link",
      options: "SEI Signal Type"
    },
  ],
};
