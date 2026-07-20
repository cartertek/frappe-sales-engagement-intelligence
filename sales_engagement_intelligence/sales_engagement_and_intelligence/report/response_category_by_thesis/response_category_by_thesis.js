frappe.query_reports["Response Category by Playbook"] = {
  filters: [
    {
      fieldname: "sei_playbook",
      label: __("Playbook"),
      fieldtype: "Link",
      options: "SEI Playbook"
    },
    {
      fieldname: "channel",
      label: __("Channel"),
      fieldtype: "Select",
      options: "\nEmail\nLinkedIn\nPhone\nContact Form\nCommunity DM\nIn-Person\nReferral Intro\nOther"
    },
  ],
};
