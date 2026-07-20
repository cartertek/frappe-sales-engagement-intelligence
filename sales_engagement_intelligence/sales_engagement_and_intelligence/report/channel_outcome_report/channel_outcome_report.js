frappe.query_reports["Channel Outcome Report"] = {
  filters: [
    {
      fieldname: "channel",
      label: __("Channel"),
      fieldtype: "Select",
      options: "\nEmail\nLinkedIn\nPhone\nContact Form\nCommunity DM\nIn-Person\nReferral Intro\nOther"
    },
    {
      fieldname: "sei_playbook",
      label: __("Playbook"),
      fieldtype: "Link",
      options: "SEI Playbook"
    },
  ],
};
