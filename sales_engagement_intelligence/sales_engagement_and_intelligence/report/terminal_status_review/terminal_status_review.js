frappe.query_reports["Terminal Status Review"] = {
  filters: [
    {
      fieldname: "lifecycle_status",
      label: __("Lifecycle Status"),
      fieldtype: "Select",
      options: "\nRejected\nDo Not Contact"
    },
    {
      fieldname: "qualification_status",
      label: __("Qualification Status"),
      fieldtype: "Select",
      options: "\nRejected\nDo Not Contact"
    },
    {
      fieldname: "source_arena",
      label: __("Source Arena"),
      fieldtype: "Data"
    },
    {
      fieldname: "sei_playbook",
      label: __("Playbook"),
      fieldtype: "Link",
      options: "SEI Playbook"
    },
  ],
};
