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
      fieldname: "research_arena",
      label: __("Research Arena"),
      fieldtype: "Link",
      options: "SEI Research Arena"
    },
    {
      fieldname: "sei_playbook",
      label: __("Playbook"),
      fieldtype: "Link",
      options: "SEI Playbook"
    },
  ],
};
