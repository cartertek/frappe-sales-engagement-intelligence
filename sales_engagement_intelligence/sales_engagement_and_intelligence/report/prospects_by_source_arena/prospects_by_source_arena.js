frappe.query_reports["Prospects by Source Arena"] = {
  filters: [
    {
      fieldname: "qualification_status",
      label: __("Qualification Status"),
      fieldtype: "Select",
      options: "\nUnqualified\nNeeds Review\nQualified\nManually Approved\nRejected\nDo Not Contact"
    },
    {
      fieldname: "lifecycle_status",
      label: __("Lifecycle Status"),
      fieldtype: "Select",
      options: "\nNew\nNeeds Research\nResearch Complete\nQualified\nFind Contact\nReady for CRM Conversion\nConverted to CRM Lead\nConverted to CRM Deal\nRejected\nDo Not Contact"
    },
  ],
};
