frappe.query_reports["CRM Deal Conversion Detail"] = {
  filters: [
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
