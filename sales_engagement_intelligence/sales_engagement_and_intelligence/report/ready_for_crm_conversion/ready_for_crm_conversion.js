frappe.query_reports["Ready for CRM Conversion"] = {
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
    {
      fieldname: "next_action_date",
      label: __("Next Action Due On Or Before"),
      fieldtype: "Date"
    },
  ],
};
