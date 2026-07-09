frappe.query_reports["Import Batch Row Errors"] = {
  filters: [
    {
      fieldname: "import_batch",
      label: __("Import Batch"),
      fieldtype: "Link",
      options: "SEI Import Batch"
    },
    {
      fieldname: "row_status",
      label: __("Row Status"),
      fieldtype: "Select",
      options: "\nFailed\nDuplicate Warning\nSkipped"
    },
  ],
};
