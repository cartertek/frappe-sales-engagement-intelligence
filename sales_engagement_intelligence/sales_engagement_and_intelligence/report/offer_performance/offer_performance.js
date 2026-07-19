frappe.query_reports["Offer Performance"] = {
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
