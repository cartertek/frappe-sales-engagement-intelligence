frappe.query_reports["Active Prospect Queue"] = {
  filters: [
    {
      fieldname: "lifecycle_status",
      label: __("Lifecycle Status"),
      fieldtype: "Select",
      options: "\nNew\nNeeds Research\nResearch Complete\nQualified\nFind Contact\nReady for CRM Conversion\nConverted to CRM Lead\nConverted to CRM Deal\nRejected\nDo Not Contact"
    },
    {
      fieldname: "qualification_status",
      label: __("Qualification Status"),
      fieldtype: "Select",
      options: "\nUnqualified\nNeeds Review\nQualified\nManually Approved\nRejected\nDo Not Contact"
    },
    {
      fieldname: "assigned_to",
      label: __("Assigned To"),
      fieldtype: "Link",
      options: "User"
    },
    {
      fieldname: "source_arena",
      label: __("Source Arena"),
      fieldtype: "Data"
    },
    {
      fieldname: "sei_thesis",
      label: __("Thesis"),
      fieldtype: "Link",
      options: "SEI Thesis"
    },
    {
      fieldname: "next_action_date",
      label: __("Next Action Due On Or Before"),
      fieldtype: "Date"
    },
  ],
};
