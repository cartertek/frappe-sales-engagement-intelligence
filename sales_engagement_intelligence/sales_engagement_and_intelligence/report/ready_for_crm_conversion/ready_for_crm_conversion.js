frappe.query_reports["Ready for CRM Conversion"] = {
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
      fieldname: "next_action_date",
      label: __("Next Action Due On Or Before"),
      fieldtype: "Date"
    },
  ],
};
