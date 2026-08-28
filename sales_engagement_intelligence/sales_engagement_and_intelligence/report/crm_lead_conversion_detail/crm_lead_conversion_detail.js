frappe.query_reports["CRM Lead Conversion Detail"] = {
  filters: [
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
    {
      fieldname: "qualification_status",
      label: __("Qualification Status"),
      fieldtype: "Select",
      options: "\nUnqualified\nNeeds Review\nQualified\nManually Approved\nRejected\nDo Not Contact"
    },
  ],
};
